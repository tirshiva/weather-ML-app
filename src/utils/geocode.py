import requests

def geocode_city(city_name):
    """
    Geocode a city name to (latitude, longitude) using Open-Meteo's geocoding API.
    Returns (lat, lon, resolved_city_name) or raises Exception if not found.
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if not data.get('results'):
        raise ValueError(f"City '{city_name}' not found.")
    result = data['results'][0]
    lat = result['latitude']
    lon = result['longitude']
    resolved_name = result['name']
    return lat, lon, resolved_name

if __name__ == "__main__":
    print(geocode_city("Kanpur")) 