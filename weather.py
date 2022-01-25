#Weather.py
#This program connects to the OpenWeatherMap API
#to get weather information.

#Inspired by freecodecamp's article on building a personal
#assistant using Python: https://www.freecodecamp.org/news/python-project-how-to-build-your-own-jarvis-using-python/

#This program requires an API key from both OpenWeatherMap and IpInfo, both of which are available for free.

from decouple import config
import requests
import ipinfo
import tkinter as tk
from tkinter import ttk
from tkinter import Tk

################################
##ENVIRONMENT VARIABLE GLOBALS##
################################
weatherKey = config("OPENWEATHER_API_KEY")
ipKey = config("IPINFO_API_KEY")
city = config("CITY")


class weatherApp(Tk):

    def __init__(self):
        super().__init__()
        
        #initialize variables
        self.city = tk.StringVar(value="unknown")
        self.lowTemp = tk.StringVar()
        self.currentTemp = tk.StringVar()
        self.highTemp = tk.StringVar()
        self.weatherReport = "unknown"

        #set up window
        self.overrideredirect(True)

        self.cityNameLabel = ttk.Label(self, textvariable=self.city)
        self.cityNameLabel.grid(column=1, row=0)

        self.lowTempLabel = ttk.Label(self, textvariable=self.lowTemp)
        self.currentTempLabel = ttk.Label(self, textvariable=self.currentTemp)
        self.highTempLabel = ttk.Label(self, textvariable=self.highTemp)

        self.lowTempLabel.grid(column=0, row=1, rowspan=2)
        self.currentTempLabel.grid(column=1, row=2)
        self.highTempLabel.grid(column=3, row=1, rowspan=2)

        self.weatherIcon = ttk.Label(self, text="icon")
        self.weatherIcon.grid(column=1, row=1)



    ######################
    ##LOCATION FUNCTIONS##
    ######################

    #returns the location of the device, based on ip address, from ipinfo.io
    def updateCity(self):
        print("Updating location data...")
        handler = ipinfo.getHandler(ipKey)
        details = handler.getDetails()
        self.city.set(details.city)
        print(f"Location found: {self.city.get()}")

    #########################
    ##TEMPERATURE FUNCTIONS##
    #########################

    ## fetches weather data from openweathermap, then updates the widget's variables ##
    def updateWeather(self):
        print("Fetching weather data...")
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={self.city.get()}&appid={weatherKey}&units=metric").json()
        self.weatherReport = response
        print("Weather data:")
        print(response)

        print("Updating variables...")
        self.currentTemp.set(f"{self.weatherReport['main']['temp']} C")
        self.lowTemp.set(f"{self.weatherReport['main']['temp_min']} C")
        self.currentTemp.set(f"{self.weatherReport['main']['temp']} C")
        self.highTemp.set(f"{self.weatherReport['main']['temp_max']} C")
        print("Variables updated.")
        self.after(60000, self.updateWeather)

    def updateWidget(self):
        self.updateCity()
        self.updateWeather()

#####################
##PROGRAM EXECUTION##
#####################

#initialize the window

app = weatherApp()
app.updateWidget()
app.mainloop()