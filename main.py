import threading

from kivy import platform
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from api import WeatherClient

open_weather_client = WeatherClient()

if platform == "android":
    from plyer import permissions


    def request_internet_permission():
        try:
            permissions.request_permission("android.permission.INTERNET")
        except Exception as e:
            print(f"Error: {e}")


    request_internet_permission()

Window.size = (360, 620)


class LoadingScreen(Screen):
    def on_enter(self):
        self.start_time = Clock.get_time()
        threading.Thread(target=self.check_server).start()

    def check_server(self):
        def on_success(is_available):
            elapsed_time = Clock.get_time() - self.start_time
            remaining_time = max(3 - elapsed_time, 0)
            if is_available:
                Clock.schedule_once(self.goto_home, remaining_time)
            else:
                Clock.schedule_once(lambda dt: self.show_error("Service unavailable"), remaining_time)

        def on_error(message):
            Clock.schedule_once(lambda dt: self.show_error(f"Error: {message}"))

        open_weather_client.ping(on_success, on_error)

    def goto_home(self, dt=None):
        self.manager.current = 'home'

    def show_error(self, message):
        dialog = MDDialog(
            title="Connection Error",
            text=message,
            buttons=[],
        )
        dialog.open()
        Clock.schedule_once(lambda dt: self.goto_home(), 3)


class HomeScreen(Screen):
    def get_weather(self):
        city = self.ids.city_input.text.strip()

        def on_success(weather):
            temperature = weather["temperature"]
            description = weather["description"]
            city = weather["city"]
            country = weather["country"]

            # Clear previous data
            self.ids.weather_card.clear_widgets()

            data_labels = ["City", "Country", "Temperature (°C)", "Weather"]
            data_values = [city, country, str(temperature), description]

            grid = MDGridLayout(
                cols=2,
                size_hint=(1, None),
                height=dp(150),
                spacing=dp(10)
            )

            for label, value in zip(data_labels, data_values, strict=False):
                header_label = MDLabel(
                    text=label,
                    theme_text_color="Secondary",
                    halign="right",
                    size_hint_x=None,
                    width=dp(120)
                )
                grid.add_widget(header_label)

                value_label = MDLabel(
                    text=value,
                    theme_text_color="Primary",
                    halign="left"
                )
                grid.add_widget(value_label)

            card = MDCard(
                size_hint=(1, None),
                height=dp(200),
                elevation=4,
                padding=dp(20),
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
            card.add_widget(grid)

            self.ids.weather_card.add_widget(card)
            self.ids.weather_card.opacity = 1

        def on_error(error_message):
            dialog = MDDialog(
                title="Error",
                text=error_message,
                buttons=[],
            )
            dialog.open()

        if city:
            open_weather_client.get_weather(city, on_success, on_error)
        else:
            on_error("Please enter a city name.")


# ------------------------------ APP -------------------------------- #

class WeatherApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("weather.kv")


if __name__ == '__main__':
    WeatherApp().run()
