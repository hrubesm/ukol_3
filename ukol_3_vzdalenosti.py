from math import sqrt
import statistics
import json
try:
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
                list_vzd.append((f"{((vzd)):.0f}"))
                celk_med.append((f"{((vzd)):.0f}"))
                soucet = soucet + vzd
            prumer = (f"{(soucet/len(kon_sou)):.0f}")
            l_prum.append(prumer)
            medi = [float(i) for i in list_vzd]
            med = statistics.median(medi)      
            l_med.append(f"{(med):.0f}")
            for _ in range (len(list_vzd)):
                if float(list_vzd[_]) < minimum:
                    minimum = float(list_vzd[_])
            minima.append(minimum)

        celk_medi = [float(i) for i in celk_med]
        med_out = [f"{(statistics.median(celk_medi)):.0f}"]
        vystup = (l_prum,l_med,minima,med_out)
        return vystup
except IOError:
    print("Chyba při načtení vstupu")
    exit()
except ValueError:
    print("Chybná hodnota vstupních data.")
    exit()
except TypeError:
    print("Chybný typ vstupních data. Vstup musí obsahovat list of floats.")
    exit()

