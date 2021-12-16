from math import sqrt


def vzd_med(adr_sou,kon_sou,kon_ID):
    kon_min = 0
    l_min_real = []
    min_ID = []

    #Průměry pro všechny adresy
    for a in range(len(adr_sou)):
        vzd = 0
        minimum = 100000
        list_vzd = []

        #Průměry pro jednu adresu
        for b in range(len(kon_sou)):    
            x = abs((adr_sou[a][0])-kon_sou[b][0])
            y = abs((adr_sou[a][1]-kon_sou[b][1]))
            vzd = sqrt((x**2)+(y**2))
            list_vzd.append(round(vzd))
        l_min_real.append(min(list_vzd))      

        #ID nejbližšího kontejneru
        for i in range (len(list_vzd)):
            if float(list_vzd[i]) < minimum:
                minimum = float(list_vzd[i])
                kon_min = (kon_ID[i])
            if i%(len(kon_sou))==(len(kon_sou)-1):
                    min_ID.append(int(kon_min))

    vystup = (l_min_real,min_ID)
    return vystup

