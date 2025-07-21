import pandas as pd
import numpy as np

def build_features(df):
    """
    Add lag features, rolling averages, and seasonality encoding to the weather DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with columns ['date', 'tmax', 'tmin', 'tavg', 'precip']
    Returns:
        pd.DataFrame: DataFrame with new features
    """
    df = df.copy()
    df = df.sort_values('date')
    # Lag features
    for lag in [1, 2, 3, 7]:
        df[f'tavg_lag{lag}'] = df['tavg'].shift(lag)
        df[f'precip_lag{lag}'] = df['precip'].shift(lag)
    # Rolling averages
    for window in [7, 30]:
        df[f'tavg_roll{window}'] = df['tavg'].rolling(window).mean()
        df[f'precip_roll{window}'] = df['precip'].rolling(window).mean()
    # Day-of-year sine/cosine encoding for seasonality
    day_of_year = df['date'].dt.dayofyear
    df['doy_sin'] = np.sin(2 * np.pi * day_of_year / 365)
    df['doy_cos'] = np.cos(2 * np.pi * day_of_year / 365)
    return df 