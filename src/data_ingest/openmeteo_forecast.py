import requests
import pandas as pd
from datetime import datetime

def fetch_openmeteo_forecast(target_date, lat, lon):
    """
    Fetch forecasted weather for a given city and date using Open-Meteo forecast API.
    Returns a DataFrame with columns: date, tmax, tmin, tavg, precip
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"
        f"&timezone=Asia%2FKolkata"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()['daily']
    df = pd.DataFrame(data)
    df.rename(columns={
        'temperature_2m_max': 'tmax',
        'temperature_2m_min': 'tmin',
        'temperature_2m_mean': 'tavg',
        'precipitation_sum': 'precip',
    }, inplace=True)
    df['date'] = pd.to_datetime(df['time'])
    df = df[['date', 'tmax', 'tmin', 'tavg', 'precip']]
    # Filter for the target date
    target_date = pd.to_datetime(target_date)
    row = df[df['date'].dt.date == target_date.date()]
    if row.empty:
        return None
    return row.reset_index(drop=True)

if __name__ == "__main__":
    print(fetch_openmeteo_forecast(datetime.today(), 28.6139, 77.2090)) 