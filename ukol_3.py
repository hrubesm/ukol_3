#Import funkcí z modulů a modulu json
from ukol_3_transform import transform
from ukol_3_vzdalenosti import vzd_med
import json

try:
    #Otevření a načtení souborů s daty
    with open ('adresy.geojson', encoding="utf-8") as geofile1,\
        open ('kontejnery.geojson', encoding="utf-8") as geofile2:
        adresy = json.load(geofile1)
        kontejnery = json.load(geofile2)

    #Vytvoření proměnných pro adresy 
    adresy_dict = {
        "citac" : "0",
        "zem_delka" : [],
        "zem_sirka" : [], 
        "souradnice" : [],
        "ulice" : [],
        "cislo_domu" : []}    
    
    #Vytvoření proměnných pro kontejnery
    kontejner_dict = {
        "citac" : "0",
        "zem_delka" : [],
        "zem_sirka" : [], 
        "souradnice" : []}
    
    #Vytvoření ostatních proměnných
    out_vzd_med = ()
    fin_prum = 0
    max_of_min = 0

        #Načtení a převod souřadnic adres  
    for feature in adresy['features']:
        adresy_dict["zem_delka"].append(feature['geometry']['coordinates'][0])
        adresy_dict["zem_sirka"].append(feature['geometry']['coordinates'][1])
        adresy_dict["ulice"].append(feature['properties']['addr:street'])
        adresy_dict["cislo_domu"].append(feature['properties']['addr:housenumber'])
        adresy_dict["citac"] = int(adresy_dict["citac"])+1
    for j in range(len(adresy_dict["zem_delka"])):
        adresy_dict["souradnice"].append(transform(adresy_dict["zem_sirka"][j],adresy_dict["zem_delka"][j]))
        
    #Načtení a převod souřadnic volně přístupných kontejnerů 
    for feature in kontejnery['features']:
        pristup = (feature['properties']['PRISTUP'])
        if pristup == "volně":    
            kontejner_dict["zem_sirka"].append(feature['geometry']['coordinates'][0])
            kontejner_dict["zem_delka"].append(feature['geometry']['coordinates'][1])               
            kontejner_dict["citac"] = int(kontejner_dict["citac"])+1   
    for j in range(len(kontejner_dict["zem_delka"])):
        l = []
        l.append(kontejner_dict["zem_sirka"][j])
        l.append(kontejner_dict["zem_delka"][j])
        kontejner_dict["souradnice"].append(l)
        
    #Načtení dat z funkce počítající se vzdálenostmi a s mediánem
    out_vzd_med=(vzd_med(adresy_dict["souradnice"],kontejner_dict["souradnice"]))

    #Určení adresy místa s největší vzdáleností k nejbližšímu kontejneru a kotrola, že jsou tyto vzdálenosti menší než 10 km
    for i in range (len(adresy_dict["zem_sirka"])):
        if int(out_vzd_med[2][i]) > max_of_min:
            max_of_min = int(out_vzd_med[2][i])
            max_idx = i
            if max_of_min > 10000:
                print("Pravděpodobná chyba v souřadnicích. Jedna z nejmenších vzdáleností ke kontejneru je větší než 10 km.")
                exit()
    #Celkový průměr - můžeme ho vypočítat takto díky distributivitě operace násobení
    for _ in range(len(adresy_dict["zem_sirka"])):
        fin_prum = fin_prum + int(out_vzd_med[0][_])
    fin_prum = fin_prum/(len(adresy_dict["zem_sirka"]))   

    #Načtení mediánu
    med_out = out_vzd_med[3][0] 

    #Výpis požadovaných informací
    print("Nacteno",adresy_dict["citac"],"adresnich bodu.")
    print("Nacteno",kontejner_dict["citac"],"kontejneru na trideny odpad.")
    print()
    print("Prumerna vzdalenost ke kontejneru je",round(fin_prum),"m.")
    print("Median vzdalenosti ke kontejneru je",med_out,"m.")
    print("Nejdale je to k nejblizsimu kontejneru na adrese",adresy_dict["ulice"][max_idx],adresy_dict["cislo_domu"][max_idx],"a to konkrétně",max_of_min,"m.")
except IOError:
    print("Chyba při načtení vstupu. Ve složce s programem musí být obsaženy soubory 'adresy.geojson' a 'kontejnery.geojson'.")
    exit()