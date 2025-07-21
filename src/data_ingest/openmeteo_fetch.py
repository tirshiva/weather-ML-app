import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_openmeteo_weather(start_date, end_date, lat=26.4499, lon=80.3319, city_slug="kanpur"):
    """
    Fetch historical weather data from Open-Meteo API and save as CSV for a given city.
    Appends new data, removes duplicates by date, and keeps only the latest for each date.
    """
    save_path = f'data/{city_slug}_weather.csv'
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"
        f"&timezone=Asia%2FKolkata"
    )
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['daily']
    df_new = pd.DataFrame(data)
    df_new.rename(columns={
        'temperature_2m_max': 'tmax',
        'temperature_2m_min': 'tmin',
        'temperature_2m_mean': 'tavg',
        'precipitation_sum': 'precip',
    }, inplace=True)
    df_new['date'] = pd.to_datetime(df_new['time'])
    df_new = df_new[['date', 'tmax', 'tmin', 'tavg', 'precip']]
    os.makedirs('data', exist_ok=True)
    # If file exists, append and deduplicate
    if os.path.exists(save_path):
        df_old = pd.read_csv(save_path, parse_dates=['date'])
        df_all = pd.concat([df_old, df_new], ignore_index=True)
        # Remove duplicates by date, keeping the last occurrence
        df_all = df_all.sort_values('date').drop_duplicates('date', keep='last')
    else:
        df_all = df_new
    df_all = df_all.sort_values('date')
    df_all.to_csv(save_path, index=False)
    print(f"Saved weather data to {save_path} (rows: {len(df_all)})")
    return save_path

if __name__ == "__main__":
    # Example: fetch last 2 years for Kanpur
    end = datetime.today()
    start = end - timedelta(days=730)
    fetch_openmeteo_weather(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')) 