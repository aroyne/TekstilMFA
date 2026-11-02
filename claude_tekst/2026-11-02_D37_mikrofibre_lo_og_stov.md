# D37 (forslag): Fiberutslipp fra vask, tørketrommel og husstøv

*Notat 2026-11-02. Besluttet og implementert samme dag (D37 i SYSTEMDEFINISJON): ja til husstøv, tøymengden følger folketallet, andel tørket 0,6 (0,4–0,8). Gjelder `US.HH-EN.WA-Fibre release in laundry`, `US.HH-EN.AI-Fibre release to air and dust` og `US.IC-EN.WA-Fibre release in industrial laundry` ([calculations/us_mc.py](../calculations/us_mc.py)), og to nye flyter til WM.RS.*

## Slik er det nå

* **Vask:** kalibrert slik at syntetisk utslipp i 2014 er 600 t (Mepex, Sundt m.fl. 2014). Andre fibre slipper like mye per kt i lageret. 2025: ca. 1,5 kt i alt (SYN 0,66, CO 0,66, WO 0,13, CV og annet 0,08).
* **Luft og støv:** samme nivå som vask (faktor 1, 0,3–3), ut av systemet til EN.AI. 2025: ca. 1,7 kt.
* **Lo fra tørketrommel:** finnes ikke.

## Hva kildene sier

### Mepex 2014 (M321) er et grovt anslag og trolig for høyt

Utdrag fra rapporten (s. 36–37):
* 70 vasker per innbygger per år à 4 kg gir 280 kg tøy per innbygger. Halvparten antas syntetisk.
* To anslag: 276 t (nederlandsk test: 260 mg fra ett plagg på 660 g, altså ca. 390 mg/kg) og 315 t (britiske fibertall i avløpsvann). Verste tilfelle 980 t. Mepex valgte **600 t som «mer realistisk gjetning»**, altså over begge de to anslagene.
* Det tilsvarer ca. 860 mg syntetisk fiber per kg syntetisk tøy (ppm), basert på enkeltplagg i laboratorieforsøk.

### Lant m.fl. (2020), PLOS ONE 15(6): e0233332, ekte skittentøy fra britiske husholdninger

* **114 ± 67 ppm** (mg fiber per kg tøy), n = 79 vasker. Små vasker (1–3,5 kg) gir 132 ppm, store (3,5–6 kg) gir 66 ppm.
* **96 % naturfibre** (90–99 %): bomull, ull og viskose. Bare 4 % syntetisk (1–10 %).
* Fleece som er vasket mange ganger, faller til 29 ppm etter 8 vasker.
* Med Mepex' tøymengde (280 kg per innbygger, 5,6 mill. innbyggere, ca. 1,6 Mt) gir det **ca. 180 t i alt (100–210 t), hvorav ca. 7 t syntetisk**. Modellen har 1,5 kt i alt og 0,66 kt syntetisk.

### Tørketrommel

* **Lant m.fl. (2022), PLOS ONE 17(4): e0265912.** Nye T-skjorter, 48 % bomull og 52 % polyester, fire sykluser:
  * Avløp ved vask: 64–79 ppm.
  * Lofilter: 106 ppm.
  * Avtrekk til luft: 50 ppm.
  * Det som havner på lofilteret, er **83–96 % bomull**.
  * Forholdet mellom lofilter og avløp er ca. 1,4–1,7.
* **Cummins m.fl. (2023), PLOS ONE 18(5): e0285548.** Ekte skittentøy:
  * Tørking frigjør **256 ± 74 ppm** (trommel med avtrekk) og **342 ± 126 ppm** (kondenstrommel).
  * Lofilteret fanger **86 ± 6 %** (avtrekk) og **91 ± 3 %** (kondens).
  * Resten går til luft (avtrekk) eller til kondensvannet og avløpet (kondens).
* **Kärkkäinen & Sillanpää (2021), Environ. Sci. Pollut. Res. 28: 16253–16263.** Bare syntetiske stoffer: 10–1 700 mg/kg ved første tørking. Fleece slipper mest, og mengden avtar med antall tørkinger.
* **Andel norske husholdninger med tørketrommel:** 44 % (1996) og 47 % (2012), ifølge SSB via [SNL](https://snl.no/tørketrommel). Nyere tall er ikke funnet.
* **Hvor loet havner:** Filteret tømmes for hånd i restavfallet, eller skylles i vasken (Cummins).

**Overslag:**
* 1,6 Mt tøy × 47 % i husholdninger med trommel × 60 % av vaskene tørket i trommel (0,4–0,8, antakelse) × 300 ppm (256–342) × 0,88 på filteret ≈ **ca. 120 t lo per år (60–200 t), mest bomull**.
* Avtrekk til luft blir ca. 10–20 t.

### Husstøv

* Mepex 2014: 2 g mikroplast per m² boligflate per år (en antakelse ut fra avsetningsrater) × 210 mill. m² ≈ 450 t syntetisk. Rapporten nevner selv at de største partiklene støvsuges og går med restavfallet til forbrenning, mens våtvask av gulv går til avløp.
* De Falco m.fl. (2020): Utslipp ved bruk er av samme størrelsesorden som ved vask, målt per plagg.
* Fibre i husstøv målt i masse per husholdning er ikke funnet. Kunnskapen er svak.

## Konsekvenser

1. **Fiberutslippene i modellen er trolig rundt ti ganger for høye.** Med ekte skittentøy (Lant 2020) blir vask ca. 0,1–0,2 kt, ikke 1,5 kt. Det syntetiske utslippet blir ca. 0,01 kt, ikke 0,66 kt. Mepex' 600 t er et anslag for syntetisk fiber basert på enkeltplagg i laboratoriet. Det bør bli en øvre følsomhet, ikke kalibreringen.
2. **Fiberfordelingen er feil.** Modellen gir ca. 45 % syntetisk fordi alle fibre er antatt å slippe like mye per kt. Målingene gir 4 % i avløpet og 4–17 % på lofilteret. Bomull og annen cellulose slipper mye mer per kg enn syntetiske fibre.
3. **Lo fra tørketrommel (ca. 0,1 kt) er på samme nivå som utslippet til avløp.** Det havner hovedsakelig i restavfallet. Det er nytt i modellen og relevant for avfallsbildet, men lite i massebalansen.
4. **Effekten på lageret går motsatt vei av det jeg skrev tidligere.** Vask og støv faller fra ca. 3,2 til ca. 0,4 kt per år. Til sammen gir det ca. 2,8 kt mer per år i det restleddet lageret i husholdningene, ca. 100 kt over perioden. Det forklarer ikke lageravviket, men det gjør det litt større. Overslaget i forrige svar (2–10 kt lo per år, og ca. 6 ganger utslippet ved vask) var feil. Målt forhold mellom lofilter og avløp er 1,4–3.

## Forslag (D37)

| Flyt | Ny metode | Parametre (forslag) |
|---|---|---|
| `US.HH-EN.WA-Fibre release in laundry` | tøymengde × utslipp per kg, ikke kalibrering mot Mepex | tøy per innbygger 280 kg/år (Mepex 2014 etter Pakula & Stamminger 2010; 200–350); utslipp 114 ppm (66–132, Lant 2020); fiberfordeling: naturfibre slipper ca. 20 ganger mer per kg enn syntetiske, slik at andelen syntetisk blir ca. 4 % (1–10 %) |
| **ny** `US.HH-WM.RS-Tumble dryer lint` (form MFR) | tøymengde × andel med trommel × andel tørket × utslipp ved tørking × andel på filteret | andel med trommel 0,44 (1996), 0,47 (2012), holdes fast etter 2012; andel av vaskene som tørkes 0,6 (0,4–0,8, antakelse); 300 ppm (256–342, Cummins 2023); filter 0,88 (0,86–0,91); bomullsandel 83–96 % (Lant 2022) |
| `US.HH-EN.AI-Fibre release to air and dust` | deles: det som støvsuges, går til WM.RS (**ny** `US.HH-WM.RS-Household dust fibres`), resten til EN.AI | nivå som i dag relativt til vask (faktor 1, 0,3–3), men med det nye, lavere vaskeutslippet; andel støvsuget 0,8 (0,5–0,95, antakelse); avtrekk fra trommel (ca. 12 % av tørkeutslippet) legges til EN.AI |
| `US.IC-EN.WA-Fibre release in industrial laundry` | samme utslipp per kg som husholdningsvask, men på tøymengden i US.IC | antall vasker i US.IC mangler. Alternativt beholdes dagens metode (per kt lager), skalert med samme faktor |
| Mepex 600 t | følsomhet (øvre grense for syntetisk) | |

**Hvor de nye flytene havner:** WM.RS fordeler dem til forbrenning, deponi og eksport sammen med resten av restavfallet. Plukkanalysene teller lo og støv som finstoff eller rest, ikke som tekstil. Flytene kommer derfor i tillegg til tekstilene i restavfallet, og blir ikke telt to ganger.

**Fiberlaget:** Sammensetningen kan ikke lenger tas fra lageret alene. Vi trenger relative utslippsfaktorer per fibergruppe (SYN, CO, CV, WO). Det er en ny tabell eller et nytt sett parametre.

## Åpne spørsmål

1. Skal tøymengden per innbygger være fast eller følge tekstillageret, slik den gjør i dag? Den bør trolig være fast eller følge folketallet. Det er vaskevaner som styrer, ikke hvor mye tekstil folk eier.
2. Andel med tørketrommel etter 2012: SSBs forbruksundersøkelse, eller Elektronikkbransjen og Enova.
3. Husstøv: finnes det målinger av tekstilfibre i masse i støvsugerposer?
4. Bør vi følge Mepex' oppdatering (Sundt m.fl. 2016, M545) og sjekke om 600 t ble justert der?

## Kilder

* Sundt, P., Schulze, P.-E. & Syversen, F. (2014). *Sources of microplastic pollution to the marine environment*. Mepex for Miljødirektoratet, M-321. https://www.miljodirektoratet.no/globalassets/publikasjoner/M321/M321.pdf
* Lant, N. J. m.fl. (2020). Microfiber release from real soiled consumer laundry and the impact of fabric care products and washing conditions. *PLOS ONE* 15(6): e0233332. PMC7274375.
* Lant, N. J. m.fl. (2022). The impact of fabric conditioning products and lint filter pore size on airborne microfiber pollution arising from tumble drying. *PLOS ONE* 17(4): e0265912. doi:10.1371/journal.pone.0265912.
* Cummins, A. M. m.fl. (2023). Impact of vented and condenser tumble dryers on waterborne and airborne microfiber pollution. *PLOS ONE* 18(5): e0285548. doi:10.1371/journal.pone.0285548.
* Kärkkäinen, N. & Sillanpää, M. (2021). Quantification of different microplastic fibres discharged from textiles in machine wash and tumble drying. *Environ. Sci. Pollut. Res.* 28: 16253–16263. doi:10.1007/s11356-020-11988-2.
* Store norske leksikon, «tørketrommel» (SSB-tall for 1996 og 2012). https://snl.no/tørketrommel
