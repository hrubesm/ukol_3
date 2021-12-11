
from ukol_3_transform import transform
import json


with open ('adresy.geojson', encoding="utf-8") as geofile1,\
    open ('kontejnery.geojson', encoding="utf-8") as geofile2:
    adresy = json.load(geofile1)
    kontejnery = json.load(geofile2)
    
    adr_count = 0
    adresa = []
    kontejner = []
    kon_del = []
    
    n_del = []
    n_sir = []
    adr_del = []
    adr_sir = []
    for feature in adresy['features']:
        adr_del.append(feature['geometry']['coordinates'][0])
        adr_sir.append(feature['geometry']['coordinates'][1])
        adresa.append(feature['properties']['addr:street'])
        adr_count += 1
    for feature in kontejnery['features']:
        adr_del.append(feature['geometry']['coordinates'][0])
        adr_sir.append(feature['geometry']['coordinates'][1])
    n_del = [float(i) for i in adr_del]
    n_sir = [float(i) for i in adr_sir]
    list_sou = []
    for _ in range(len(n_del)):
        list_sou.append(transform(n_sir[_],n_del[_]))
        print(list_sou[_], adresa[_])
  
    
print("Ahojda")
