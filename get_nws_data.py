from requests import get

def get_nws_data(api_endpoint, my_coordinates:tuple, verbose:bool=True):
	
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