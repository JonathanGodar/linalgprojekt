import requests
import json
# URL for the API endpoint
url = "https://api.pullpush.io/reddit/submission/search?html_decode=True&subreddit=techsupport&until=1700780209&size=3000"

# Making the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # You can now process this data or save it for later analysis
    # For example, save it to a file
    with open('data.json', 'w') as file:
        json.dump(data, file)
else:
    print(f"Request failed with status code: {response.status_code}")

# Note: Ensure you handle exceptions and errors as needed.