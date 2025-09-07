# TODO
# 1. Refactor how the data is collected 
# 2. Add option to take in a location
# 3. Change how 
import os, sys
import requests 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from get_nws_data import get_nws_data, from_computer_location_get_coordinates, from_coordinates_get_info

places = {
	"Ann Arbor": (42.2808, -83.7430),
	"Nashville": (36.1627, -86.7816),
	"Berkley": (42.5031, -83.1835),
	"Farmington Hills": (42.4990, -83.3677), 
	"Argonne": (41.7183, -87.9789),
	"Detroit": (42.3314, -83.0458),
	#"FSU": (30.4419, -84.2985)
}


get_value = lambda dictionary: round(dictionary["value"])

my_coordinates = from_computer_location_get_coordinates()
points_information = from_coordinates_get_info(my_coordinates)
data = get_nws_data(points_information["hourly forecast endpoint"], my_coordinates)

timezone = points_information["timezone"]
forecast_periods = data["properties"]["periods"]

full_df = pd.DataFrame(forecast_periods)

full_df["startTime"] = pd.to_datetime(full_df["startTime"], utc=False)
full_df["endTime"] = pd.to_datetime(full_df["endTime"], utc=False)
full_df["probabilityOfPrecipitation"] = full_df["probabilityOfPrecipitation"].apply(get_value)
full_df["dewpoint"] = full_df["dewpoint"].apply(get_value)
full_df["relativeHumidity"] = full_df["relativeHumidity"].apply(get_value)


df = full_df[["startTime",
			  "temperature", 
			  'probabilityOfPrecipitation',
       		  'dewpoint', 
			  'isDaytime',
			  'relativeHumidity', 
			  'windSpeed', 
			  'windDirection',
			  'shortForecast']
			]
df.to_csv("~/Desktop/WeatherForecast.csv")

exit()
if len(sys.argv) > 1:
	hours = int(sys.argv[1])
else:
	hours = 12

df = df[0:hours+1]
y_range = range(0, 105, 5)

print(df.to_string())

fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(14,8))
plt.title(f"Weather Forecast for {points_information['name']}")

date_format = mdates.DateFormatter(fmt='%a\n%I%p', tz=timezone)
ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
ax.xaxis.grid(True, which='major', linestyle='--')
ax.yaxis.grid(True, which='major', linestyle='--')
ax.xaxis.set_major_formatter(date_format)

#plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax.set_ylim(0,100)
ax.set_yticks(y_range)
#ax.hlines(y_range, xmin=df["startTime"][0], xmax=df["startTime"].iloc[-1], color="black", linestyles="dashed", alpha=0.5)
#ax.xaxis_date(tz="ET")


ax.plot(df["startTime"], df["temperature"], label="Temperature ºF", color="r")
ax.plot(df["startTime"], df["dewpoint"], label="Dewpoint ", color="orange")
ax.plot(df["startTime"], df["probabilityOfPrecipitation"], label="Precipitation %", color="b", linestyle="dotted")
ax.plot(df["startTime"], df["relativeHumidity"], label="Relative Humidity %", color="black")

ax.legend(loc="upper right", bbox_to_anchor=(1, 1))
location_file_name = points_information["name"].replace(" ","_")
file_name = f"/Users/evan/Desktop/Forecast_{location_file_name}.png"
plt.savefig(file_name)
os.system(f"open {file_name}")
