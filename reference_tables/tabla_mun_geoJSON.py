import pandas as pd
from urllib.request import urlopen
import json

# Crear Data Frame con la información geoJSON de cada municipio.
# La información proviene de: https://api-features.ign.es/collections/administrativeunit/items?offset=0&limit=100 
# He creado un Data Frame solo con los municipios que nos atañen porque la api de IGN no funciona bien.


df_geoJSON = pd.DataFrame({
    "municipio": ["almería", 
                  "cádiz", 
                  "granada", 
                  "málaga", 
                  "huesca", 
                  "gijón", 
                  "oviedo", 
                  "zaragoza", 
                  "tenerife", 
                  "santander", ],
    "nationalcode": [34010404013, 
                     34011111012, 
                     34011818087, 
                     34012929067, 
                     34022222125, 
                     34033333024, 
                     34033333044, 
                     34025050297, 
                     34053838038, 
                     34063939075],
    "api": ["https://api-features.ign.es/collections/administrativeunit/items/1058427?f=json", 
            "https://api-features.ign.es/collections/administrativeunit/items/1058529?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1058712?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1059058?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1059299?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1059958?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1059978?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1059930?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1060151?f=json",
            "https://api-features.ign.es/collections/administrativeunit/items/1060242?f=json",

            ]
})





# EJEMPLO para leer JSON y unirlo a DF con plotly https://plotly.com/python/tile-county-choropleth/