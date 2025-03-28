import os

import requests
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key is required.")
        self.__api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def from_environment(cls):
        return cls(api_key=os.getenv("OPENWEATHER_API_KEY"))

    def __parse_weather_data(self, data: dict) -> dict:
        main_data = data.get("main", {})
        weather_data = data.get("weather", [{}])[0]

        return {
            "temperature": main_data.get("temp"),
            "pressure": main_data.get("pressure"),
            "humidity": main_data.get("humidity"),
            "description": weather_data.get("description").capitalize(),
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
        }

    def get_weather(self, city_name: str) -> dict:
        if not city_name:
            raise ValueError("City name cannot be empty.")

        url = f"{self.base_url}?appid={self.__api_key}&q={city_name}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("cod") != 200:
                raise ValueError(f"API Error: {data.get('message', 'Unknown error')}")

            return self.__parse_weather_data(data)

        except requests.RequestException as exc:
            raise ConnectionError(f"Network error: {exc}") from exc
        except ValueError as exc:
            raise ValueError(exc) from exc

    def ping(self) -> bool:
        url = f"{self.base_url}?appid={self.__api_key}&q=London"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False


# Example Usage
if __name__ == "__main__":
    try:
        api_key = "2454f2838b30710dfae811ee76609228"
        client = WeatherClient(api_key)

        city_name = input("Enter city name: ")
        weather_data = client.get_weather(city_name)

        print(f"\nWeather in {weather_data['city']}, {weather_data['country']}:")
        print(f" - Temperature: {weather_data['temperature']} °C")
        print(f" - Pressure: {weather_data['pressure']} hPa")
        print(f" - Humidity: {weather_data['humidity']}%")
        print(f" - Description: {weather_data['description']}")
    except (ValueError, ConnectionError) as e:
        print(f"Error: {e}")
