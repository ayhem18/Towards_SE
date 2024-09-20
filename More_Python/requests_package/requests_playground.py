"""
The sole aim of this script is to better understand the 'requests' python package
"""


import requests 

# response = requests.get('https://github.com/ayhem18', allow_redirects=True)

# print(response.__repr__())

# make sure to run the MusicControllerApp 

response = requests.get(url='http://127.0.0.1:8000/rooms/list/u1/')

print(response.json())
