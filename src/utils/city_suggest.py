import requests

def suggest_cities(query, count=5):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count={count}&language=en&format=json"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if not data.get('results'):
        return []
    return [
        {
            'name': r['name'],
            'country': r.get('country', ''),
            'latitude': r['latitude'],
            'longitude': r['longitude']
        }
        for r in data['results']
    ]

if __name__ == "__main__":
    print(suggest_cities("Del")) 