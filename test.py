import numpy as np

print(np.mean([0,1]))




## folium 띄우기!
import folium
import os, settings
# from selenium import webdriver
#
# driver_path = os.path.join(settings.BASE_DIR, 'chromedriver.exe')
# driver = webdriver.Chrome(driver_path)
#
#
# # folium 띄우기 : https://github.com/python-visualization/folium/issues/946
#
# LDN_COORDINATES = (51.5074, 0.1278)
# filepath = os.path.join(settings.BASE_DIR, 'output', 'map.html')
# m = folium.Map(location=LDN_COORDINATES, zoom_start=19)
# m.save(filepath)
# driver.get('file://' + filepath)

#
# map_co = [35.689872, 139.694406]
# map = folium.Map(location=map_co, zoom_start=13)
# folium.CircleMarker(location=map_co, radius=200, color = '#000000', fill_color = '#000000' ).add_to(map)
# map.save('test.html')

import webbrowser
filepath = os.path.join(settings.BASE_DIR, 'output', 'map.html')
webbrowser.open('file://' + filepath)
