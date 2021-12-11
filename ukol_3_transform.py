from pyproj import Transformer
import json

def transform(adr_sir,adr_del):
    
    wgs2jtsk = Transformer.from_crs(4326,5514) #Transformace ze systému WGS do systému JTSK
    vystup = wgs2jtsk.transform(adr_sir,adr_del) 
    return vystup
    

    
    
    
"""
ŠÍŘKA JE X, DÉLKA Y!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    for index, item in enumerate(adr_del):
        adr_del[index] = float(item)
        adr_del[index] = adr_del[index]
    for index, item in enumerate(adr_del):
        adr_sir[index] = float(item)
        adr_sir[index] = adr_sir[index]
    for index in (adr_del and adr_sir):
        transform(adr_sir[index],adr_del[index])
        bla = transform.output
        print(bla)

ODKLADIŠTĚ KÓDU ZDE!!!!
    adr_del = []
    adr_sir = []
    for feature in adresy['features']:
        adr_del.append(feature['geometry']['coordinates'][0])
        adr_sir.append(feature['geometry']['coordinates'][1])
    for index, item in enumerate(adr_del):
        adr_del[index] = float(item)
        adr_del[index] = adr_del[index]
    for index, item in enumerate(adr_del):
        adr_sir[index] = float(item)
        adr_sir[index] = adr_sir[index]
    for index in (adr_del and adr_sir):
        transform(adr_sir[index],adr_del[index])
        bla = transform.output
        print(bla)
    
    print("Ahojda")






"""    
print("Ahojda")