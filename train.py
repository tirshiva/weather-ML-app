import os
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from joblib import dump
from src.features.build_features import build_features

def train_city_model(city_slug):
    """
    Train Ridge Regression model for a given city_slug. Saves model to models/{city_slug}_tavg_model.joblib
    """
    DATA_PATH = f'data/{city_slug}_weather.csv'
    MODEL_PATH = f'models/{city_slug}_tavg_model.joblib'
    df = pd.read_csv(DATA_PATH, parse_dates=['date'])
    df_feat = build_features(df)
    df_feat = df_feat.dropna()
    if len(df_feat) < 30:
        raise ValueError("Not enough data to train model.")
    train = df_feat.iloc[:-7]
    test = df_feat.iloc[-7:]
    X_train = train.drop(['date', 'tavg'], axis=1)
    y_train = train['tavg']
    X_test = test.drop(['date', 'tavg'], axis=1)
    y_test = test['tavg']
    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Test MAE (last 7 days): {mae:.2f}°C for {city_slug}")
    os.makedirs('models', exist_ok=True)
    dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    return MODEL_PATH

if __name__ == "__main__":
    city_slug = sys.argv[1] if len(sys.argv) > 1 else 'kanpur'
    train_city_model(city_slug) 