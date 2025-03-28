[app]
# App name
title = WeatherApp

# Python package name
package.name = weather_app

# Package domain (reversed domain name style)
package.domain = com.example.weatherapp

# App version
version = 1.0

# Application icon (place an icon in assets/icon.png)
icon.filename = assets/icon.png

# Main Python entry point
source.include_exts = py, kv

# Include necessary files
source.include_patterns = main.py, api.py, weather.kv, assets/*

# Target platforms (for most Android devices)
android.archs = arm64-v8a, armeabi-v7a

# Screen orientation
orientation = portrait

# Minimum and target API levels
android.minapi = 21
android.api = 33

# Permissions required for API requests
android.permissions = INTERNET

# Enable cleartext for HTTP requests (necessary for UrlRequest without SSL)
android.allow_cleartext = True

# Dependencies
requirements = python3, kivy, kivymd, plyer

# Presplash screen (displayed on app startup)
android.presplash_color = "#000000"

# Python version to use
android.python_version = 3.10

# Log level (0 = no logs, 2 = verbose)
log_level = 2

[buildozer]
# Clean build files before recompiling
buildozer.clean_build = 1

# Optional: Enable for release builds
android.release = False
