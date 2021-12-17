#Konstanta omezující vzdálenost mezi adresou a kontejnerem. V tomto případě je limit 10 km
LIMIT = 10000   


#Import funkcí a modulů
from pyproj import Transformer
from ukol_3_vzdalenosti import vzd_med
import statistics
import json


#Funkce na transformaci souřadnic ze systému WGS do systému JTSK
def transform(adr_sir,adr_del):
    wgs2jtsk = Transformer.from_crs(4326,5514) 
    vystup = wgs2jtsk.transform(adr_sir,adr_del) 
    return vystup


#Otevření a načtení souborů s daty - vstupní formát souboru musí být geojson či json
#Předpokládá se, že vstupní soubor adres je v souřadnicovém systému WGS 84 a že vstupní soubor kontejnerů je v souřadnicovém systému JTSK
try:
    with open ('adresy.geojson', encoding="utf-8") as geofile1,\
        open ('kontejnery.geojson', encoding="utf-8") as geofile2:
        adresy = json.load(geofile1)
        kontejnery = json.load(geofile2)
        adresy_kontejnery = adresy
except IOError:
    print("Chyba při načtení vstupu. Ve složce s programem musí být obsaženy soubory 'adresy.geojson' a 'kontejnery.geojson'.")
    exit()
except json.decoder.JSONDecodeError:
    print("Chyba při dekódování souboru. Je možné že soubor neobsahuje žádná data. Zkontrolujte vstupní soubory.")
    exit()
except UnicodeDecodeError:
    print("Vstupní soubor není typu .json nebo .geojson.")
    exit()
else:
    pass


#Vytvoření proměnných pro adresy 
adresy_dict = {
    "citac" : 0,
    "zem_delka" : [],
    "zem_sirka" : [], 
    "souradnice" : [],
    "ulice" : [],
    "cislo_domu" : [],
    "adresa" : [],
    "ID_nejblizsi_kontejner" : [],
    "domovni_kontejner" : []}    
    
#Vytvoření proměnných pro kontejnery
kontejner_dict = {
    "citac" : 0,
    "zem_delka" : [],
    "zem_sirka" : [], 
    "souradnice" : [],
    "ID_volne" : [],
    "ID_all" : []}
        
      


#Načtení a převod souřadnic adres z WGS 84 do JTSK 
i = 0
for feature in adresy['features']:
    adresy_dict["zem_delka"].append(feature['geometry']['coordinates'][0])
    adresy_dict["zem_sirka"].append(feature['geometry']['coordinates'][1])
    adresy_dict["ulice"].append(feature['properties']['addr:street'])
    adresy_dict["cislo_domu"].append(feature['properties']['addr:housenumber'])
    k = str(adresy_dict["ulice"][i])
    l = str(adresy_dict["cislo_domu"][i])
    n = k +" "+ l
    adresy_dict["adresa"].append(n)
    adresy_dict["citac"] += 1
    i+=1
for j in range(len(adresy_dict["zem_delka"])):
    adresy_dict["souradnice"].append(transform(adresy_dict["zem_sirka"][j],adresy_dict["zem_delka"][j]))       
    adresy_dict["domovni_kontejner"].append('False')


#Načtení a převod souřadnic volně přístupných kontejnerů 
for feature in kontejnery['features']:
    pristup = (feature['properties']['PRISTUP'])
    adr_kon = (feature['properties']['STATIONNAME'])
    kontejner_dict["ID_all"].append(int(feature['properties']['ID']))
    if pristup == "volně":    
        kontejner_dict["zem_sirka"].append(feature['geometry']['coordinates'][0])
        kontejner_dict["zem_delka"].append(feature['geometry']['coordinates'][1])               
        kontejner_dict["citac"] += 1   
        kontejner_dict["ID_volne"].append(int(feature['properties']['ID']))
    for i in range(len(adresy_dict["souradnice"])):
        if pristup == "obyvatelům domu" and adr_kon == adresy_dict["adresa"][i]:
            adresy_dict["domovni_kontejner"][i] = 'True'      
        i += 1
for j in range(len(kontejner_dict["zem_delka"])):
    l = [kontejner_dict["zem_sirka"][j],kontejner_dict["zem_delka"][j]]
    kontejner_dict["souradnice"].append(l)


#Načtení dat z funkce počítající se vzdálenostmi a s mediánem
out_vzd_med=(vzd_med(adresy_dict["souradnice"],kontejner_dict["souradnice"],kontejner_dict["ID_volne"]))

#Načtení průměru a mediánu
#Určení adresy místa s největší vzdáleností k nejbližšímu kontejneru a kotrola, že jsou tyto vzdálenosti menší než 10 km
max_of_min = 0
vzd_l = out_vzd_med[0]
for i in range (len(adresy_dict["zem_sirka"])):
    if int(out_vzd_med[0][i]) > max_of_min:
        max_of_min = int(out_vzd_med[0][i])
        max_idx = i
        if max_of_min > LIMIT:
            print("Pravděpodobná chyba v souřadnicích. Jedna z nejmenších vzdáleností ke kontejneru je větší než 10 km.")
            exit()       
    if adresy_dict["domovni_kontejner"][i] == 'True':  #Započítání domovních kontejnerů na adresách
        vzd_l[i] = (int(0))
mean_out = statistics.mean(vzd_l)
med_out = round(statistics.median(vzd_l)) 


#Načtení ID nejbližších kontejnerů z výstupu funkce "vzd_med" do slovníku "adresy_dict"
for i in range((len(adresy_dict["souradnice"]))):
    adresy_dict["ID_nejblizsi_kontejner"].append(int(out_vzd_med[1][i]))
    if  adresy_dict["domovni_kontejner"][i] == 'True':   #Započítání domovních kontejnerů na adresách
        adresy_dict["ID_nejblizsi_kontejner"].pop()
        adresy_dict["ID_nejblizsi_kontejner"].append(kontejner_dict["ID_all"][i])


#Zápis ID nejbližších kontejnerů do proměnné "adresy_kontejnery"
adr_kon_pro = []
for feature in adresy_kontejnery['features']:
    adr_kon_pro.append(feature['properties'])
for j in range (adresy_dict["citac"]):
    adr_kon_pro[j]["kontejner"] = adresy_dict["ID_nejblizsi_kontejner"][j]
j = 0
for feature in adresy_kontejnery['features']:
    adresy_kontejnery['properties'] = (adr_kon_pro[j])
    j += 1   


#Zápis proměné "adresy_kontejnery" do výstupního souboru formágu geojson
try:   
    with open("adresy_kontejnery.geojson", "w",encoding="utf-8") as outfile:
        json.dump(adresy_kontejnery, outfile, indent=3)
except IOError:
    print("Chyba při načtení výstupu.")
    exit()
except json.decoder.JSONDecodeError:
    print("Chyba při dekódování souboru.")
    exit()
except UnicodeDecodeError:
    print("Výstupní soubor není typu .json nebo .geojson.")
    exit()
else:
    pass  
    
#Výpis požadovaných informací
print("Nacteno",adresy_dict["citac"],"adresnich bodu.")
print("Nacteno",kontejner_dict["citac"],"verejnych kontejneru na trideny odpad.")
print()
print("Prumerna vzdalenost ke kontejneru je",round(mean_out),"m.")
print("Median vzdalenosti ke kontejneru je",med_out,"m.")
print("Nejdale je to k nejblizsimu kontejneru na adrese",adresy_dict["ulice"][max_idx],adresy_dict["cislo_domu"][max_idx],"a to konkrétně",max_of_min,"m.")



