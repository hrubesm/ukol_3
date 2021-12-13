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
        adr_ulice = []
        adr_cislo = []
        adr_count = 0
        adr_del = []
        adr_sir = []
        adr_sou = []

        #Vytvoření proměnných pro kontejnery
     
        kon_count = 0
        kon_del = []
        kon_sir = [] 
        kon_sou = []
        
        #Vytvoření ostatních proměnných
        out_vzd_med = ()
        fin_prum = 0
        max_of_min = 0

        #Načtení a převod souřadnic adres  
        for feature in adresy['features']:
            adr_del.append(feature['geometry']['coordinates'][0])
            adr_sir.append(feature['geometry']['coordinates'][1])
            adr_ulice.append(feature['properties']['addr:street'])
            adr_cislo.append(feature['properties']['addr:housenumber'])
            adr_count += 1
        for j in range(len(adr_del)):
            adr_sou.append(transform(adr_sir[j],adr_del[j]))
        
        #Načtení a převod souřadnic volně přístupných kontejnerů 
        for feature in kontejnery['features']:
            pristup = (feature['properties']['PRISTUP'])
            if pristup == "volně":    
                kon_sir.append(feature['geometry']['coordinates'][0])
                kon_del.append(feature['geometry']['coordinates'][1])               
                kon_count += 1   
        for j in range(len(kon_del)):
            l = []
            l.append(kon_sir[j])
            l.append(kon_del[j])
            kon_sou.append(l)
        
        #Načtení dat z funkce počítající se vzdálenostmi a s mediánem
        out_vzd_med=(vzd_med(adr_sou,kon_sou))

        #Určení adresy místa s největší vzdáleností k nejbližšímu kontejneru a kotrola, že jsou tyto vzdálenosti menší než 10 km
        for i in range (len(adr_sir)):
            if int(out_vzd_med[2][i]) > max_of_min:
                max_of_min = int(out_vzd_med[2][i])
                max_idx = i
                if max_of_min > 10000:
                    print("Pravděpodobná chyba v souřadnicích. Jedna z nejmenších vzdáleností ke kontejneru je větší než 10 km.")
                    exit()
        #Celkový průměr - můžeme ho vypočítat takto díky distributivitě operace násobení
        for _ in range(len(adr_sir)):
            fin_prum = fin_prum + int(out_vzd_med[0][_])
        fin_prum = fin_prum/(len(adr_sir))   

        #Načtení mediánu
        med_out = out_vzd_med[3][0] 

    #Výpis požadovaných informací
    print("Nacteno",adr_count,"adresnich bodu.")
    print("Nacteno",kon_count,"kontejneru na trideny odpad.")
    print()
    print("Prumerna vzdalenost ke kontejneru je",round(fin_prum),"m.")
    print("Median vzdalenosti ke kontejneru je",med_out,"m.")
    print("Nejdale je to k nejblizsimu kontejneru na adrese",adr_ulice[max_idx],adr_cislo[max_idx],"a to konkrétně",max_of_min,"m.")
except IOError:
    print("Chyba při načtení vstupu. Ve složce s programem musí být obsaženy soubory 'adresy.geojson' a 'kontejnery.geojson'.")
    exit()