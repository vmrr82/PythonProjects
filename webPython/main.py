import folium
from geopandas import *

marcadores = geopandas.read_file("data\AccidentesCalvia.geojson")
m = folium.Map(location=[39.52802630451034, 2.5076734630661597],
                tiles= "OpenStreetMap",
                zoom_start= 13,
                min_zoom= 13,
                max_zoom= 20,
                control_scale= True)



controlCapas = folium.LayerControl().add_to(m)
#-----guardar-------
m.save("index.html")