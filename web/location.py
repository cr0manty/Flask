import re
import requests
from bs4 import BeautifulSoup
import folium


def get_location():
    raw = requests.get('http://www.geoiptool.com/').text
    soup = BeautifulSoup(raw, 'html.parser')
    row = []
    text = soup.find_all('div', {'class': 'data-item'})
    for i in text:
        for j in ('Latitude', 'Longitude'):
            data = i.find_all('span', text=re.compile(j))
            if data:
                row.append(i.find('span', text=re.compile(r'\d')).text)
    return row[0:2]


def make_map():
    location = get_location()
    map = folium.Map(location=[location[0], location[1]],
                     zoom_start=8, tiles='CartoDB dark_matter')
    for coordinates in [[location[0], location[1]]]:
        folium.Marker(location=coordinates, icon=folium.Icon(color='red')).add_to(map)
    map.save('map.html')
