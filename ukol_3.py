from ukol_3_transform import transform
from ukol_3_vzdalenosti import vzd_med
import json

#Otevření a načtení souborů s daty
with open ('adresy.geojson', encoding="utf-8") as geofile1,\
    open ('kontejnery.geojson', encoding="utf-8") as geofile2:
    adresy = json.load(geofile1)
    kontejnery = json.load(geofile2)

    #Vytvoření proměnných pro adresy 
    adresa = []
    adr_count = 0
    adr_del = []
    adr_sir = []
    na_del = []
    na_sir = []
    adr_sou = []

    #Vytvoření proměnných pro kontejnery
    kontejner = []
    kon_count = 0
    kon_del = []
    kon_sir = [] 
    nk_del = []
    nk_sir = [] 
    kon_sou = []

    out_vzd_med = ()
    #Načtení a převod souřadnic adres  
    for feature in adresy['features']:
        adr_del.append(feature['geometry']['coordinates'][0])
        adr_sir.append(feature['geometry']['coordinates'][1])
        adresa.append(feature['properties']['addr:street'])
        adr_count += 1
    na_del = [float(i) for i in adr_del]
    na_sir = [float(i) for i in adr_sir]
    for _ in range(len(na_del)):
        adr_sou.append(transform(na_sir[_],na_del[_]))
    #print(adr_sou[0][0]) 
     
    #Načtení a převod souřadnic kontejnerů
    for feature in kontejnery['features']:
        kon_del.append(feature['geometry']['coordinates'][0])
        kon_sir.append(feature['geometry']['coordinates'][1])
        pristup = (feature['properties']['PRISTUP'])
        kon_count += 1

        #Ošetření že používáme pouze veřejné kontejnery
        if pristup == "obyvatelům domu":
            kon_del.pop()
            kon_sir.pop()
            kon_count -= 1    
            
    nk_del = [float(i) for i in kon_del]
    nk_sir = [float(i) for i in kon_sir]
    for _ in range(len(nk_del)):
        l = []
        l.append(nk_sir[_])
        l.append(nk_del[_])
        kon_sou.append(l)
    for _ in range (len(kon_sou)):
        print(kon_sou[_])
    
    out_vzd_med=(vzd_med(adr_sou,kon_sou))
    print(out_vzd_med)

print("Ahojda")

