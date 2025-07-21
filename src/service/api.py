import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from joblib import load
from datetime import datetime, timedelta
from src.features.build_features import build_features
from src.utils.geocode import geocode_city
from src.utils.city_suggest import suggest_cities
from src.data_ingest.openmeteo_fetch import fetch_openmeteo_weather
from src.data_ingest.openmeteo_forecast import fetch_openmeteo_forecast
from train import train_city_model
import math

def slugify(text):
    return text.lower().replace(' ', '_')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/city-suggest")
def city_suggest(query: str = Query(..., description="City name prefix")):
    try:
        suggestions = suggest_cities(query)
        return suggestions
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/weather-stats")
def get_weather_stats(
    city: str = Query(..., description="City name, e.g. Kanpur"),
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    try:
        # Geocode city
        lat, lon, resolved_city = geocode_city(city)
        city_slug = slugify(resolved_city)
        req_date = pd.to_datetime(date)
        today = datetime.now().date()
        # If future or today, use forecast API first
        if req_date.date() >= today:
            forecast_row = fetch_openmeteo_forecast(date, lat, lon)
            if forecast_row is not None and not forecast_row.empty:
                tavg = float(forecast_row.iloc[0]['tavg'])
                avg_7d = float(forecast_row['tavg'].mean())
                if any(math.isnan(x) or math.isinf(x) for x in [tavg, avg_7d]):
                    return JSONResponse(
                        status_code=500,
                        content={"error": "Forecast data for this date is unavailable or incomplete."}
                    )
                return {
                    "city": resolved_city,
                    "date": date,
                    "predicted_tavg": round(tavg, 2),
                    "avg_tavg_7d": round(avg_7d, 2),
                    "is_forecast": True,
                    "is_ml_forecast": False
                }
            # If forecast not available, try ML model prediction
            # Load data and model
            data_path = f'data/{city_slug}_weather.csv'
            model_path = f'models/{city_slug}_tavg_model.joblib'
            if not os.path.exists(data_path):
                end = datetime.today()
                start = end - timedelta(days=3*365)
                fetch_openmeteo_weather(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), lat, lon, city_slug)
            if not os.path.exists(model_path):
                train_city_model(city_slug)
            df = pd.read_csv(data_path, parse_dates=['date'])
            model = load(model_path)
            df_feat = build_features(df)
            df_feat = df_feat.dropna()
            if df_feat.empty:
                return JSONResponse(status_code=500, content={"error": "Not enough data to predict future weather."})
            # Use the latest available row to simulate features for the future date
            latest = df_feat.iloc[-1].copy()
            # Update date and seasonality features for the requested date
            future_row = latest.copy()
            future_row['date'] = req_date
            day_of_year = req_date.dayofyear
            future_row['doy_sin'] = math.sin(2 * math.pi * day_of_year / 365)
            future_row['doy_cos'] = math.cos(2 * math.pi * day_of_year / 365)
            # Remove target column if present
            if 'tavg' in future_row:
                future_row = future_row.drop('tavg')
            # Prepare DataFrame for prediction
            X_future = pd.DataFrame([future_row]).drop(['date'], axis=1)
            pred = float(model.predict(X_future)[0])
            # For 7-day avg, use last 7 available days
            avg_7d = float(df_feat['tavg'].tail(7).mean())
            if any(math.isnan(x) or math.isinf(x) for x in [pred, avg_7d]):
                return JSONResponse(
                    status_code=500,
                    content={"error": "ML forecast for this date is unavailable or incomplete."}
                )
            return {
                "city": resolved_city,
                "date": date,
                "predicted_tavg": round(pred, 2),
                "avg_tavg_7d": round(avg_7d, 2),
                "is_forecast": True,
                "is_ml_forecast": True
            }
        # Else, use archive API/model for past dates
        data_path = f'data/{city_slug}_weather.csv'
        if not os.path.exists(data_path):
            end = datetime.today()
            start = end - timedelta(days=3*365)
            fetch_openmeteo_weather(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), lat, lon, city_slug)
        model_path = f'models/{city_slug}_tavg_model.joblib'
        if not os.path.exists(model_path):
            train_city_model(city_slug)
        df = pd.read_csv(data_path, parse_dates=['date'])
        model = load(model_path)
        if req_date.date() not in df['date'].dt.date.values:
            fetch_openmeteo_weather(date, date, lat, lon, city_slug)
            df = pd.read_csv(data_path, parse_dates=['date'])
        df_feat = build_features(df)
        df_feat = df_feat.dropna()
        row = df_feat[df_feat['date'].dt.date == req_date.date()]
        if row.empty:
            return JSONResponse(status_code=404, content={"error": "No data for requested date. Try a recent past date."})
        X = row.drop(['date', 'tavg'], axis=1)
        pred = float(model.predict(X)[0])
        idx = row.index[0]
        avg_7d = float(df_feat.iloc[max(0, idx-6):idx+1]['tavg'].mean())
        if any(math.isnan(x) or math.isinf(x) for x in [pred, avg_7d]):
            return JSONResponse(
                status_code=500,
                content={"error": "Weather data for this date is unavailable or incomplete."}
            )
        return {
            "city": resolved_city,
            "date": date,
            "predicted_tavg": round(pred, 2),
            "avg_tavg_7d": round(avg_7d, 2),
            "is_forecast": False,
            "is_ml_forecast": False
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)}) 