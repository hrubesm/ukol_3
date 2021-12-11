from math import sqrt
import json

def vzd_med(adr_sou,kon_sou):
    l_prum = []  
    l_med = []
    vystup = ()
    for a in range(len(adr_sou)):
        vzd = 0
        soucet = 0
        prumer = 0
        median = 0
        list_vzd = []
        for b in range(len(kon_sou)):    
            x = abs((adr_sou[a][0])-kon_sou[b][0])
            y = abs((adr_sou[a][1]-kon_sou[b][0]))
            vzd = sqrt((x**2)+(y**2))
            list_vzd.append(f"{(vzd):.0f}")
            soucet = soucet + vzd
        prumer = f"{(soucet/len(adr_sou)):.0f}"
        l_prum.append(prumer)
        list_vzd = sorted(list_vzd, reverse = False)
        if len(list_vzd)%2 == 0:
            median = (list_vzd[int(len(list_vzd)/2)-1] + list_vzd[int(len(list_vzd)/2)])/2
        else:
            median = (list_vzd[int((len(list_vzd)+1)/2)-1])
        l_med.append(median)
    vystup = (l_prum,l_med)
    return vystup



