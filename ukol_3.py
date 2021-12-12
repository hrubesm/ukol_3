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
        na_del = [float(i) for i in adr_del]
        na_sir = [float(i) for i in adr_sir]
        for _ in range(len(na_del)):
            adr_sou.append(transform(na_sir[_],na_del[_]))
        
        #Načtení a převod souřadnic kontejnerů
        for feature in kontejnery['features']:
            kon_sir.append(feature['geometry']['coordinates'][0])
            kon_del.append(feature['geometry']['coordinates'][1])
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
        
        #Načtení dat z funkce počítající se vzdálenostmi a s mediánem
        out_vzd_med=(vzd_med(adr_sou,kon_sou))

        #Určení adresy místa s největší vzdáleností k nejbližšímu kontejneru a kotrola, že jsou tyto vzdálenosti menší než 10 km
        for _ in range (len(adr_sir)):
            if int(out_vzd_med[2][_]) > max_of_min:
                max_of_min = int(out_vzd_med[2][_])
                max_idx = _
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
    print("Prumerna vzdalenost ke kontejneru je",f"{(fin_prum):.0f}","m.")
    print("Median vzdalenosti ke kontejneru je",med_out,"m.")
    print("Nejdale je to k nejblizsimu kontejneru na adrese",adr_ulice[max_idx],adr_cislo[max_idx],"a to konkrétně",max_of_min,"m.")
except IOError:
    print("Chyba při načtení vstupu. Ve složce s programem musí být obsaženy soubory 'adresy.geojson' a 'kontejnery.geojson'.")
    exit()
