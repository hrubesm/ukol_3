from pyproj import Transformer
import json

def transform(adr_sir,adr_del):
        
    wgs2jtsk = Transformer.from_crs(4326,5514) #Transformace ze systému WGS do systému JTSK
    vystup = wgs2jtsk.transform(adr_sir,adr_del) 
    return vystup
#pozn: zem. šířka je x, zem. délka je y