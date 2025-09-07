from requests import get, Response

def from_computer_location_get_coordinates(verbose:bool=True) -> tuple:
	ipinfo = get("https://ipinfo.io/json")

	if ipinfo.status_code == 200:
		ipinfo = ipinfo.json()
	if verbose:
		print(ipinfo)
	stloc = ipinfo['loc'].split(",")
	my_coordinates = list(map(float,stloc))
	return tuple(my_coordinates)

def get_nws_data(api_endpoint, my_coordinates:tuple, verbose:bool=True) -> Response:
	
	base_url = "https://api.weather.gov"
	lattitude, longitude = my_coordinates

	# Check if api_endpoint is a complete URL or a relative path
	if api_endpoint.startswith("http"):
		url = api_endpoint
	else:
		# make sure there is only one slash between the paths
		url = f"{base_url.rstrip('/')}/points/{lattitude},{longitude}".lstrip('/')
	
	response = get(url)

	if verbose: 
		print(url)
		print(f"Returned with response status: {response.status_code}")
	if response.status_code == 200:
		return response.json()
	else:
		bad_response = response.json()
		print(f"Error: {bad_response['status']}")
		print(bad_response['detail'])
		return None



def from_coordinates_get_info(coordinates:tuple, verbose:bool=True) -> dict:
	# Takes in latitude and longitude and returns 
	# multiple strings, some of which are API endpoints.

	lattitude, longitude = coordinates
	endpoint = f"points/{lattitude},{longitude}"
	location_in_county = get_nws_data(endpoint, coordinates) 
	if verbose:
		for item, value in location_in_county["properties"].items():
			print(f"{item}: {value}")
	location_properties = location_in_county["properties"]

	location_name = location_properties["relativeLocation"]["properties"]["city"]
	location_timezone = location_properties["timeZone"]
	forecast_endpoint = location_properties["forecast"]
	forecast_hourly_endpoint = location_properties["forecastHourly"]

	information = {
		"name": location_name,
		"timezone": location_timezone,
		"forecast endpoint": forecast_endpoint,
		"hourly forecast endpoint": forecast_hourly_endpoint,
	}

	return information


