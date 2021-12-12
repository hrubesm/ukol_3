**Zadání:** <br>
Napište program, který zjistí dostupnost kontejnerů na tříděný odpad v určité čtvrti města. Program musí vypsat počet načtených adres, počet načtených kontejnerů, průměrnou vzdálenost k veřejnému kontejneru a ze které adresy je nejdále nejbližší kontejner a jaká je tato vzdálenost.

Bonusové úkoly:
* odevzdejte úkol přes GitHub.
* program vypíše medián vzdáleností ke kontejneru
* program vytvoří soubor adresy_kontejnery.geojson, který bude obsahovat adresní body a u každého adresního bodu bude uloženo ID nejbližšího kontejneru k adresnímu bodu.
* program bude pracovat i s domovními kontejnery
* soubory budou uvažovány jako parametry programu


**Vypracování:**<br>
Program nejprve načte data a definuje základní operace a základní proměnné. Poté zaznamená některé informace do seznamů (souřadnice adres a kontejnerů, názvy ulic adres, domovní čísla adres). Jsou také vytvořeny čítače, které slouží k zaznamenání počtu adres a kontejnerů. Při tomto načítání je ohlídáno, aby nebyly uvažovány kontejnery, které nejsou veřejné. Jelikož souřadnice adres nejsou v systému JTSK, ale v systému WGS 84, bylo potřeba provést jejich transformaci pomocí funkce "transform" z modulu "ukol_3_transform". Po transformaci došlo k aplikaci funkce "vzd_med" z modulu "ukol_3_vzdalenosti", ve které se odehrávají výpočty jednotlivých vzdáleností ke kontejnerům jednotlivých adres. Vstupem této funkce byly souřadnice adres a kontejnerů v systému JTSK a mezi výstupy funkce patří jednotlivé průměry a mediány vzdáleností, nejmenší vzdálenosti od jednotlivých adres k nejbližšímu kontejneru a celkový medián všech vzdáleností všech adres.
Po načtení výstupu byla určena adresa místa s největší vzdáleností k nejbližšímu kontejneru. Dalé byla také určena kontrola, že žádná z těchto vzdáleností nepřekračuje 10 km a také byl vypočítán celkový průměr ze všech průměrů vzdáleností. Tento průměr můžeme takto vypočítat díky distributivitě operace násobení. Na závěr byly programem vypsány požadované informace.