import threading

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog

from api import WeatherClient

open_weather_client = WeatherClient.from_environment()


class LoadingScreen(Screen):
    def on_enter(self):
        self.start_time = Clock.get_time()  # Track when the screen started
        threading.Thread(target=self.check_server).start()

    def check_server(self):
        try:
            server_available = open_weather_client.ping()
            elapsed_time = Clock.get_time() - self.start_time
            remaining_time = max(3 - elapsed_time, 0)  # Ensure minimum 3 seconds

            if server_available:
                Clock.schedule_once(self.goto_home, remaining_time)
            else:
                Clock.schedule_once(lambda dt: self.show_error("Service unavailable"), remaining_time)
        except Exception:
            elapsed_time = Clock.get_time() - self.start_time
            remaining_time = max(3 - elapsed_time, 0)
            Clock.schedule_once(lambda dt: self.show_error(f"Error during connection: {str(e)}"), remaining_time)

    def goto_home(self, dt=None):
        self.manager.current = 'home'

    def show_error(self, message):
        def close_dialog(*args):
            self.manager.current = 'home'

        dialog = MDDialog(
            title="Connection Error",
            text=message,
            buttons=[],
        )
        dialog.open()
        Clock.schedule_once(lambda dt: close_dialog(), 3)


class HomeScreen(Screen):
    def get_weather(self):
        city = self.ids.city_input.text
        if city:
            try:
                weather = open_weather_client.get_weather(city)
                temperature = weather["temperature"]
                description = weather["description"]
                self.ids.weather_label.text = f"🌡 {temperature}°C\n{description}"
            except:
                self.ids.weather_label.text = "Error during connection"


# Screen Manager
class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("weather.kv")


if __name__ == '__main__':
    WeatherApp().run()
