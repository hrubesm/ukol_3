from math import sqrt
import statistics
import json

#Definování funkce
def vzd_med(adr_sou,kon_sou):
    minima = []
    l_prum = []  
    l_med = []
    vystup = ()
    celk_med = []
    #Průměry pro všechny adresy
    for a in range(len(adr_sou)):
        vzd = 0
        soucet = 0
        prumer = 0
        minimum = 100000
        list_vzd = []

        #Průměry pro jednu adresu
        for b in range(len(kon_sou)):    
            x = abs((adr_sou[a][0])-kon_sou[b][0])
            y = abs((adr_sou[a][1]-kon_sou[b][1]))
            vzd = sqrt((x**2)+(y**2))
            list_vzd.append(round(vzd))
            celk_med.append(round(vzd))
            soucet = soucet + vzd
        prumer = (round(soucet/len(kon_sou)))
        l_prum.append(prumer)
        med = statistics.median(list_vzd)      
        l_med.append(round(med))
        for i in range (len(list_vzd)):
            if float(list_vzd[i]) < minimum:
                minimum = float(list_vzd[i])
        minima.append(minimum)

   
    med_out = [round(statistics.median(celk_med))]
    vystup = (l_prum,l_med,minima,med_out)
    return vystup


