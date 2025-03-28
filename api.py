from kivy.network.urlrequest import UrlRequest


class WeatherClient:
    def __init__(self):
        self.__api_key = "2454f2838b30710dfae811ee76609228"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

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

    def get_weather(self, city_name: str, on_success, on_error):
        if not city_name:
            raise ValueError("City name cannot be empty.")

        url = f"{self.base_url}?appid={self.__api_key}&q={city_name}&units=metric"

        def handle_success(request, result):
            try:
                if result.get("cod") != 200:
                    raise ValueError(f"API Error: {result.get('message', 'Unknown error')}")
                weather_data = self.__parse_weather_data(result)
                on_success(weather_data)
            except Exception as e:
                on_error(str(e))

        def handle_error(request, error):
            on_error(f"Network error: {error}")

        UrlRequest(url, on_success=handle_success, on_error=handle_error)

    def ping(self, on_success, on_error):
        url = f"{self.base_url}?appid={self.__api_key}&q=London"

        def handle_success(request, result):
            if result.get("cod") == 200:
                on_success(True)
            else:
                on_success(False)

        def handle_error(request, error):
            on_error(f"Network error: {error}")

        UrlRequest(url, on_success=handle_success, on_error=handle_error)


# Exemplu de utilizare
if __name__ == "__main__":
    def print_weather(data):
        print(f"\nWeather in {data['city']}, {data['country']}:")
        print(f" - Temperature: {data['temperature']} °C")
        print(f" - Pressure: {data['pressure']} hPa")
        print(f" - Humidity: {data['humidity']}%")
        print(f" - Description: {data['description']}")


    def print_error(error_message):
        print(f"Error: {error_message}")


    try:
        api_key = "2454f2838b30710dfae811ee76609228"
        client = WeatherClient(api_key)
        city_name = input("Enter city name: ")
        client.get_weather(city_name, print_weather, print_error)
    except ValueError as e:
        print_error(str(e))
