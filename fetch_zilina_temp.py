import requests
import pandas as pd
import plotly.express as px

CITY = "Zilina"
COUNTRY = "SK"
CSV_FILE = "zilina_temperature.csv"

def main():
    # 1) nájdi súradnice mesta
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": CITY,
        "countryCode": COUNTRY,
        "count": 1,
        "language": "sk",
        "format": "json",
    }

    geo_resp = requests.get(geo_url, params=geo_params, timeout=20)
    geo_resp.raise_for_status()
    geo_data = geo_resp.json()

    results = geo_data.get("results")
    if not results:
        raise RuntimeError(f"Mesto {CITY} sa nenašlo.")

    place = results[0]
    latitude = place["latitude"]
    longitude = place["longitude"]
    place_name = place["name"]

    # 2) stiahni hodinovú teplotu
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "forecast_days": 2,
        "timezone": "Europe/Bratislava",
    }

    weather_resp = requests.get(weather_url, params=weather_params, timeout=20)
    weather_resp.raise_for_status()
    weather_data = weather_resp.json()

    # 3) ulož do DataFrame
    df = pd.DataFrame({
        "timestamp": weather_data["hourly"]["time"],
        "temperature_2m": weather_data["hourly"]["temperature_2m"],
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 4) ulož do CSV
    df.to_csv(CSV_FILE, index=False, sep=";")
    print(f"Uložené do {CSV_FILE}")

    # 5) zobraz graf
    fig = px.line(
        df,
        x="timestamp",
        y="temperature_2m",
        title=f"Hodinová teplota - {place_name}",
        labels={
            "timestamp": "Čas",
            "temperature_2m": "Teplota [°C]",
        },
    )
    fig.show()

if __name__ == "__main__":
    main()