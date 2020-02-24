import pandas as pd
import matplotlib.pyplot as plt
import folium
import folium.plugins as plugins

m = folium.Map(
    location=[45.372, -121.6972],
    zoom_start=12,
    tiles='Stamen Terrain'
)

folium.Marker([45.372, -121.6972],
    icon=plugins.BeautifyIcon(icon='leaf',
    iconShape= 'marker'),
    draggable=True,
    popup='popup',
    tooltip='This is a beatifyMarker'
).add_to(m)
