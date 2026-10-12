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
