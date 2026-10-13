# Gjennomgang av MA.TX (tekstil-, klær- og skoindustri)

*2026-10-12. Andre subpool i gjennomgangen flyt for flyt. Beslutningene står som D22 (utvidet) og D25 i [SYSTEMDEFINISJON](../docs/SYSTEMDEFINISJON.md).*

## Implementert

| Flyt | Kilde | 1990 | 2000 | 2008 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|---|
| Garn fra MA.FI (balanse) | – | 12,1 | 9,9 | 6,7 | 5,0 | 5,1 | 5,2 |
| Import av metervare (RW → MA.TX) | SSB 08801: vevnader i HS 50–55, HS 58, 60 | 11,0 | 12,0 | 8,7 | 7,2 | 5,8 | 5,4 |
| Eksport av metervare (MA.TX → RW) | SSB 08801 | 3,5 | 5,6 | 3,4 | 0,9 | 0,7 | 2,4 |
| Produksjonsavfall (MA.TX → WM.RS) | SSB 08604/14457, per kt innsatsvare | 1,4 | 1,3 | 0,9 | 0,25 | 0,25 | 0,24 |
| **Rest = ferdigvarer til DI.RT** (nå i det midlertidige lageret) | balanse | 18,4 | 15,2 | 11,2 | 11,2 | 10,1 | 8,2 |

kt per år, median av N = 10.

- **Garn utenfor omfanget (D22):** Tvunnet nylongarn (5402.61), annet enkelt syntetisk filamentgarn (5402.49) og polypropylen stapelfiber (5503.40) er tatt ut, både for import og eksport. Til sammen er det 0,6–2 kt per år, og det går mest til nett, tau, fiberduk og geotekstil.
- **Eksport (D6):** MA.TX eksporterer bare metervare. Eksporten av ferdigvarer blir værende i DI.RT.
- **Produksjonsavfall:** SSB oppgir tekstilavfall fra næringene 13–15 i hele tusen tonn: 1 kt i 2008 og 0 kt i 2015 og 2022. Ankerpunktene er derfor 1,0 kt (±50 %) i 2008 og 0,25 kt (0–0,5) i 2015 og 2022. Avfallet er uttrykt per kt garn og metervare inn i MA.TX i ankerårene, og forholdstallet interpoleres. Før 2008 følger avfallet dermed innsatsen, med 2008 som referanse.

## Industrien i tall (SSB 12910, 2017–2024)

| Næring | Sysselsatte | Produksjonsverdi (mrd. kr) |
|---|---|---|
| 13.92 Konfeksjonerte tekstilvarer | ~1 250 | 2,1–3,1 |
| 13.94 Tau og nett (utenfor) | ~1 100 | 1,7–3,3 |
| 14.1 Klær | ~1 550 | 2,7–3,1 |
| 13.93 Tepper | ~20 | 0,01 |
| 15.2 Sko | ~25 | 0,02–0,06 |

## Forslag: ferdigvarer til DI.RT fordelt på produkter

Å fordele etter verdi er for grovt, fordi prisen per kilo varierer mye mellom produkter. Forslaget er å regne ut **masse per produkt** i ankerår fra SSBs varestatistikk, og bruke masseandelene til å fordele balansen.

1. **Ankerår med best dekning:**
   - 1988 og 1989: SSB Industristatistikk, Hefte II Varetall, etter HS. Sidene for kapittel 57–64 og 94 leses manuelt, som for garnet.
   - 2008, 2009 og 2011: Prodcom (SSB 10455), der 9–12 ferdigvarekoder har mengde. Etter 2012 har bare 1–3 koder det.
2. **Masse per varekode i ankerårene:**
   - *kg:* brukes direkte, for eksempel presenninger (13.92.22.10, ~1,1 kt) og telt.
   - *stk og par:* antall × kg per stykk fra importen av samme HS-kode samme år (08801 har antall for klær). Eksempler er arbeidsklær, dresser, skjorter, T-skjorter, sokker og dyner (13.92.24.99: 3,2 millioner stk i 2008).
   - *bare verdi:* verdi ÷ norsk pris per kg for samme kode i år der både mengde og verdi er publisert. Dette er de «typiske prisene», men hentet fra statistikken selv.
3. **Fordeling:** Kodene kobles til produktene CL, HT, CA, TA, OM og FW, og masseandelene regnes ut per ankerår. Andelene interpoleres mellom 1989 og 2008 og holdes på 2011-nivå etter 2011.
4. **Kontroll:** 12910 viser at forholdet mellom 13.92 og 14.1 er stabilt i 2017–2024, så det er rimelig å holde andelene fast etter 2011. Summen av massene i Prodcom sammenlignes med balansen. Prodcom dekker bare store foretak, så summen bør ligge under balansen.

Det mest krevende er koblingen fra Prodcom-kode til HS-kode for kg per stykk, og å lese varetallene for 1988–89. Begge deler er overkommelig, fordi det er få koder med data (25 ferdigvarekoder har tall i minst ett år).

Et enklere alternativ er å koble innsatsvarene til produkter: polyester stapelfiber går til dyner (HT), ullgarn og strikket metervare til klær (CL), og så videre. Det krever flere antakelser og er ikke anbefalt.

## Spørsmål om omfang: dyner og puter (HS 9404)

En stor del av norsk produksjon av hjemmetekstiler er dyner og puter (Prodcom 13.92.24: 3,2 millioner stk i 2008). Importen av disse ligger i HS 94, som ikke er med i modellen i dag:

| HS | Vare | Import 2008 | Import 2022 | Eksport 2022 |
|---|---|---|---|---|
| 9404.90 (fra 2022 delt med 9404.40) | Dyner, puter, puff og lignende | 6,5 kt | 6,0 + 1,6 kt | 2,9 + 1,3 kt |
| 9404.30 | Soveposer | 0,4 kt | 0,7 kt | 0,1 kt |
| 9404.10, 9404.2x | Madrasser og madrassunderlag | – | – | – (ikke tekstil som hovedmateriale) |

Hvis norsk dyneproduksjon føres som HT til DI.RT mens importen av dyner ikke er med, blir HT skjevt. Forslaget er å ta med 9404.40 og 9404.90, og eventuelt 9404.30 soveposer, i HT. Det krever at handelsdataene hentes for disse kodene. Alternativet er å holde dyner utenfor og trekke dem fra MA.TX-produksjonen.

## Beslutning (samme dag)

Den massebaserte produktfordelingen er godkjent. Dyner og puter er hjemmetekstiler, og 9404.40 og 9404.90 tas med i HT (D26). Om soveposer (9404.30) skal med, er ikke avklart. Rekkefølgen for implementeringen står i [PLAN](../docs/PLAN.md) under fase 3.

## Implementert 2026-10-13 (D26)

**Dyner og hodeputer** (9404.40 og 9404.90 unntatt møbelputer) er med i HT. Importen er 0,7–4,3 kt og eksporten 0,5–2,6 kt per år. Dun og fjær regnes som OTH, annet fyll som SYN (antakelse: polyester). Soveposer (9404.30) og møbelputer ligger i dataene, men er utenfor inntil det er avklart.

**Produktandeler** fra SSBs varestatistikk for store foretak (`data_files/domestic_production_mass.csv`):

| Ankerår | CL | HT | TA | OM | CA | Sum masse (store foretak) |
|---|---|---|---|---|---|---|
| 1988 (Varetall) | 35 % | 30 % | 18 % | 7 % | 2 % | 8,0 kt (pluss sko 0,7 kt) |
| 1989 (Varetall) | 30 % | 30 % | 24 % | 8 % | 2 % | 7,3 kt (pluss sko 0,5 kt) |
| 2008–2011 (Prodcom, snitt per kode) | 21 % | 49 % | 27 % | 3 % | 0 % | 4,5 kt |

- Masse per kode: kg eller tonn som publisert, stk/par × importvekt per stk for samme HS-kode, eller verdi ÷ norsk pris per kg. Den norske prisen tas fra samme kode i et annet år, eller er importprisen × 2,5, som er medianforholdet over 71 koder der begge er kjent.
- Sko er holdt utenfor, fordi lær og gummi ikke er innsatsvarer i MA.TX.
- Andelene interpoleres mellom 1988, 1989 og 2009 og holdes fast etter 2009.

**Ferdigvarer til DI.RT** (median, N = 1000):

| | 1990 | 2000 | 2008 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| CL | 5,7 | 3,9 | 2,4 | 2,4 | 2,1 | 1,7 |
| HT | 6,0 | 6,2 | 5,3 | 5,4 | 4,8 | 3,9 |
| TA | 4,6 | 3,9 | 3,0 | 3,0 | 2,7 | 2,2 |
| OM | 1,5 | 0,8 | 0,4 | 0,4 | 0,3 | 0,3 |
| CA | 0,4 | 0,2 | 0,0 | 0,0 | 0,0 | 0,0 |
| Sum | 18,2 | 15,0 | 11,0 | 11,1 | 10,0 | 8,1 |

## Diskusjonspunkt: balansen i MA.TX ser for høy ut

Balansen i MA.TX er 8–18 kt per år. Varestatistikken for store foretak gir 7–8 kt i 1988–89 og omtrent 4,5 kt i 2008–2011. Små foretak mangler i statistikken, men forskjellen er stor. Konsekvensen er at lageret i husholdningene (restledd, D8) øker fra ca. 135 til ca. 206 kg per innbygger i 2018–2025.

Mulige årsaker:
- **Metervare til andre næringer.** Importert vevd metervare går også til møbeltrekk (møbelindustri, NACE 31), madrasser, bil- og båtinteriør, fallskjermer og tekniske formål. Dette er ikke tekstilindustri og ikke forbrukertekstiler i vår avgrensning.
- **Garn til tekniske produkter** utover kodene som allerede er tatt ut (D22).
- **Produksjon for eksport.** Den er med, siden eksporten av ferdigvarer føres fra DI.RT.

Mulige grep:
1. **Øvre grense fra varestatistikken.** Ferdigvarer til DI.RT settes til massen fra varetall og Prodcom, skalert opp for små foretak med forholdet mellom produksjonsverdien i 12910 og verdien som er publisert i Prodcom. Resten av balansen går til en ny flyt for innsatsvarer som brukes i andre næringer (utenfor omfanget).
2. **Andel metervare til andre næringer** som parameter (fra litteratur eller anslag), trukket fra før balansen.
3. **Behold balansen** og bruk lagernivået mot garderobestudier (SIFO) som kontroll.
