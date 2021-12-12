from math import sqrt
import statistics
import json

#Definování funkce
def vzd_med(adr_sou,kon_sou):
    l_prum = []  
    l_med = []
    vystup = ()
    #Průměry pro všechny adresy
    for a in range(len(adr_sou)):
        vzd = 0
        soucet = 0
        prumer = 0
        median = 0
        list_vzd = []

        #Průměry pro jednu adresu
        for b in range(len(kon_sou)):    
            x = abs((adr_sou[a][0])-kon_sou[b][0])
            y = abs((adr_sou[a][1]-kon_sou[b][1]))
            vzd = sqrt((x**2)+(y**2))
            list_vzd.append((f"{((vzd)):.0f}"))
            soucet = soucet + vzd
        prumer = (f"{(soucet/len(kon_sou)):.0f}")
        l_prum.append(prumer)
        medi = [float(i) for i in list_vzd]
        med = statistics.median(medi)      
        l_med.append(f"{(med):.0f}")
    
    vystup = (l_prum,l_med)
    return vystup



