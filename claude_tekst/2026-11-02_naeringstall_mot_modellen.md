# Næringstall mot modellen: MA.TX og salg til husholdningene

*Notat 2026-11-02. Data: `data_files/SSB_industri_tekstil_1999_2024.csv` og `data_files/SSB_09296_varehandelsindeks_2000_2025.csv` (`scripts/fetch_ssb_industry_series.py`), `data_files/BRREG_*_2026-11-02.csv` (`scripts/fetch_brreg_actors.py`). Modelltall: medianer fra `output_files/MC_summary.csv`.*

## Kjeding av industritallene

Hvert år hentes fra én tabell: 03325 for 1999–2006, 08596 for 2007–2016 og 12910 for 2017–2024. I overlappsårene er produksjonsverdien lik innenfor 0–4 % for spinning, stoff, tekstilvarer unntatt klær (17.4/13.92), klær (18 + 17.7 / 14) og skotøy. Unntaket er SN2002 17.54 («tekstiler ellers»), som delvis gikk til 13.95/13.96 i SN2007. Tepper, andre tekstiler og tekniske tekstiler må derfor slås sammen hvis de skal kjedes.

## MA.TX: implisitt pris per kg

Produksjonsverdien delt på massen modellen sender MA.TX → DI.RT:

| År | Klær: mill. kr | CL, kt | kr/kg | Import CL, kr/kg | 13.92: mill. kr | HT+TA+OM, kt | kr/kg | Import HT, kr/kg |
|---|---|---|---|---|---|---|---|---|
| 1999 | 1 414 | 4 | ca. 380 | 204 | 1 115 | 12 | ca. 95 | 70 |
| 2008 | 2 553 | 2 | ca. 1 070 | 191 | 1 483 | 9 | ca. 170 | 59 |
| 2017 | 2 988 | 2 | ca. 1 290 | 309 | 2 127 | 8 | ca. 250 | 84 |
| 2024 | 3 363 | 2 | ca. 1 730 | 474 | 2 700 | 7 | ca. 380 | 120 |

* Den implisitte prisen ligger 1,4–4 ganger over importprisen i alle år. Hvis modellen sendte for mye masse gjennom MA.TX, ville prisen blitt lavere enn importprisen. Det skjer ikke, så **produksjonsverdien gir ikke grunnlag for å si at MA.TX-balansen er for høy**. Norsk produksjon (bunad, arbeidstøy, dyner, seil og presenninger) er trolig dyrere per kg enn importen, men det er ikke kontrollert.
* Det svekker antakelsen fra notatet om MA.TX og fra vurderingen mot NORSUS (samme dag) om at MA.TX er hovedmistenkt for det høye lageret. Prodcom-tallene for store foretak (0,07 mrd. kr for klær i 2024) dekker bare en liten del av produksjonsverdien i industristatistikken (3,4 mrd. kr), så de er ikke en god øvre grense.
* Forbehold: Produksjonsverdien kan omfatte lønnsarbeid og varer laget av underleverandører i utlandet for norske foretak. Klesmerkene ligger delvis i 14.x (Brønnøysund: 2,7 mrd. kr omsetning i 14.210 yttertøy i 2025). Hvis en stor del av verdien er slike varer, er norsk produksjon i kg mindre enn verdien antyder, og da kan MA.TX likevel være for høy.

Sysselsettingen i klesindustrien falt fra 2 735 (1999) til 1 760 (2024), og i 13.92 fra 1 390 til 1 180. Modellen har CL fra MA.TX fra ca. 4 til ca. 2 kt i samme periode.

## Salg til husholdningene mot varehandelsindeksen

Indeks, 2010 = 100:

| År | 47.71 klær, volum | Modell CL (inkl. netthandel) | 47.72 sko, volum | Modell FW | 47.51 tekstiler, volum | Modell HT |
|---|---|---|---|---|---|---|
| 2000 | 40 | 76 | 58 | 71 | 60 | 72 |
| 2010 | 100 | 100 | 100 | 100 | 100 | 100 |
| 2018 | 112 | 85 | 91 | 91 | 85 | 95 |
| 2025 | 139 | 97 | 85 | 75 | 79 | 70 |

* Volumindeksen er omsetning deflatert med KPI for varegruppen, ikke masse. KPI for klær falt kraftig 2000–2010, og den er kvalitetsjustert, så «volumet» vokser mye raskere enn massen. Indeksen måler dessuten bare bedriftene i 47.71, og handelen flytter mellom næringer (sportskjeder, varehus, netthandel fra utlandet).
* For sko og hjemmetekstiler følger modellen indeksen rimelig godt etter 2010. For klær skiller de lag (+39 % mot −3 % fra 2010 til 2025). Det skyldes mest trolig deflatoren og prisfall per plagg, ikke feil i massen.
* **Konklusjon:** Varehandelsindeksen kan ikke brukes til å kontrollere nivå eller trend i masse. Den kan høyst brukes kvalitativt, for eksempel for brudd som pandemiåret 2020, som både modellen og indeksen viser.

## Hva det betyr for lageret

Ingen av næringsseriene peker på tilførselssiden som forklaring på det høye lageret i husholdningene (ca. 275 kg per innbygger). Det styrker forklaringen at **kasseringene før 2018 er for lave** (restavfall fast per innbygger før 2009 og innsamlingen tidlig i perioden).

## Neste steg

* Spør SNF om tilgang til regnskapsdatabasen (regnskapsdatabasen@snf.no, SNF-rapport 02/26). Tilgang gis «primarily» til forhåndsdefinerte institusjoner. Med data per foretak kan vi skille merkevarer (som produserer i utlandet) fra faktisk produksjon i 14.x.
* Følsomhetskjøring: MA.TX → DI.RT halvert og doblet, og hvor mye det endrer lageret.
