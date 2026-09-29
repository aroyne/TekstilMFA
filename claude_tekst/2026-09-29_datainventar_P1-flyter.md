# Datainventar for P1-flyter (kjerneflyter)

*Notat 2026-09-29. Fase 1 i [PLAN.md](../docs/PLAN.md). Kildehierarki etter D8: SSB/Miljødirektoratet → rapporter bestilt av myndighetene → andre rapporter og aktørdata. Balanseflyter (restledd) er tatt med for å vise hva som bestemmer dem.*

## Viktig funn: bruddet i SSBs avfallsregnskap i 2012

SSBs avfallsregnskap har en materialtype «Tekstiler», men tallene endrer seg helt i 2012:

| kt tekstiler | 1995 | 2000 | 2005 | 2009 | 2011 | 2012 | 2018 | 2024 |
|---|---|---|---|---|---|---|---|---|
| Generert i alt (05281 → 10513) | 115 | 120 | 121 | 115 | 113 | **4** | **6** | **4** |
| – energiutnyttelse / forbrenning | 17 | 24 | 39 | 45 | 75 | 1 | 2 | 1 |
| – deponering | 66 | 58 | 51 | 36 | 6 | 0 | 4 | 0 |
| – materialgjenvinning | 3 | 7 | 10 | 11 | 1 | 3 | 0 | 2 |
| – forbrenning uten energiutnyttelse | 7 | 9 | 14 | 13 | 19 | – | – | – |
| – annen/uspesifisert | 22 | 22 | 6 | 9 | 13 | 0 | 0 | 1 |

(05281 for 1995–2011, 10513 for 2012–2024. Kolonnene er utvalgte år; 1995–2011 er hentet fra NitrogenBudsjett `data_files/05281_*.xlsx`, og 10513 fra SSB API → `data_files/SSB_10513_textiles_mixed_2012_2024.csv`.)

**Bekreftet i SSBs dokumentasjon** ([Om avfallsregnskapet 2014](https://www.ssb.no/natur-og-miljo/statistikker/avfregno/aar/2014-06-27?fane=om), [2016](https://www.ssb.no/natur-og-miljo/statistikker/avfregno/aar/2016-05-25?fane=om)):
* «For 2012 årgangen ble avfallsregnskapet gjennomgått på nytt og nye beregningsmetoder ble tatt i bruk.» «Blandet avfall» ble en egen materialtype.
* Før 2012: «Fram til og med 2011-publiseringen beskrev avfallsmengdene potensialet for utsortering av de forskjellige avfallsfraksjonene. Noen materialer var hovedsakelig beregnet med en varetilførselsmetode basert på estimert levetid. I tillegg ble alt blandet avfall fordelt på de respektive materialtypene utfra en sorteringsanalyse.»
* Fra 2012 bygger regnskapet hovedsakelig på målte verdier fra anlegg. «Tekstiler» dekker dermed i praksis bare utsorterte tekstilfraksjoner. Tekstiler i restavfall ligger i «Blandet avfall».
* SSB: den nye materialinndelingen «gjør sammenlignbarheten med tidligere årganger vanskelig».
* Dokumentasjonen sier ikke hvilke materialer som ble beregnet med varetilførselsmetoden. For tekstiler kan nivået i 05281 derfor være helt eller delvis **modellbasert** (tilførsel × levetid), altså samme type beregning som vår parallelle lagermodell.
* Separat innsamlede tekstiler for ombruk regnes ikke som avfall.

**SSBs eget tekstilregnskap 1990–1998** ([Avfallsregnskap, tekstiler, 1990–1998](https://www.ssb.no/natur-og-miljo/statistikker/avfregntekstil/hvert-2-aar/2001-08-01), publisert 2001), offisiell statistikk:
* SSB brukte to metoder, varetilførsel og avfallsstatistikk, og valgte avfallsstatistikk som «det mest pålitelige bildet».
* 1998: 106 kt tekstilavfall i alt. Husholdninger 83 kt (78 %), fiske/havbruk 7 %, industri 6 %, andre 9 %. Klær 47,2 kt (42 %), klær + fottøy + lær 59 kt, interiørtekstiler 17 %, emballasje 4,3 %.
* Behandling: deponi 72 % i 1998 (79 % i 1991), forbrenning ca. 20 %, gjenvinning/ombruk 8 %.
* Omfanget er bredere enn vårt (fiskeredskap, emballasje, lær), men fordelingen på produkttyper gjør det mulig å avgrense.

**Konsekvens for D8 (forslag til kildekjede for tekstiler i restavfall og behandlingsmåte):**

| Periode | Hovedkilde | Merknad |
|---|---|---|
| 1990–1998 | SSB avfallsregnskap for tekstiler | Offisiell. Ankerår 1991 og 1998. Avgrenses til vårt omfang med produkttypefordelingen |
| 1995–2011 | SSB 05281 | Offisiell, men nivået kan være modellbasert. Brukes primært for **fordelingen** på deponi/forbrenning/gjenvinning. Nivået brukes bare som sammenligning |
| 2012–2017 | – | Ingen offisiell tekstilserie. Interpoleres mellom 2011 og 2018 |
| 2018, 2022, 2025 | Mepex-plukkanalyser via Watson 2020 (Miljødir.) og NORSUS 2023/2026 | Ankerår |

For 2012 og senere gir *ikke* SSBs avfallsregnskap tekstiler i restavfall direkte. Den beste offisielle kilden er da plukkanalyser (Mepex), satt sammen i rapporter bestilt av Miljødirektoratet (Watson 2020 for 2018) og av bransjen (NORSUS 2023 for 2022, NORSUS 2026 for 2025). Totalmengden restavfall kan hentes fra SSB. Tekstilandel fra plukkanalyser × SSBs restavfallsmengde er en variant som følger kildehierarkiet bedre, og den bør vurderes.

## Inventar

| # | Flyt | Kilde(r) | År med data | Hull og merknader | Status |
|---|---|---|---|---|---|
| 1 | RW.RW-DI.RT Finished textile products import | SSB 08801 | 1988–2025 (alle år) | Småpakker (VOEC) og næringslivets varelinjer < 1 000 kr er ikke med under HS-kodene, se egne flyter/parametre | **ferdig** |
| 2 | DI.RT-RW.RW Export of finished textile products | SSB 08801 | 1988–2025 | Gjeneksport og norsk produksjon er ikke skilt (D6) | **ferdig** |
| 3 | RW.RW-US.HH Private imports (grensehandel, reiser) | SSB grensehandelsstatistikk (verifiser tabell og startår); forbruksundersøkelsen | ukjent – sjekkes | NOK → kg med NOK/kg fra 08801 (D7) | ikke startet |
| 4 | RW.RW-US.HH Direct online imports | Tolletaten VOEC via NORSUS 2026; Watson 2020 (Virke) | 2018, 2022–2025 | 1988–2017 og 2019–2021 interpoleres/skaleres. Tallene er «veiledende» | ankerpunkter finnes |
| 5 | DI.RT-US.HH Sales to households | balanse | – | Avhenger av 1, 2, US.IC-andel (88 % husholdninger, dansk fordeling) og usolgte varer | – |
| 6 | US.HH-CO.CO Separate collection | Watson 2020 (Miljødir.); NORSUS 2023; NORSUS 2026 | 2018: 31 690 t; 2022: 29,6 kt; 2025: 33 703 t | **Ingen offisielle tall før 2018.** Kandidater: nordiske TemaNord-rapporter (ca. 2010–2012), årsrapporter fra innsamlerne. Eksport av 6309 fra 08801 (1988–) kan brukes som proxy, siden 85–97 % eksporteres | ankerpunkter 2018+ |
| 7 | US.HH-WM.RS Textiles in residual and bulky waste | Mepex-plukkanalyser via Watson 2020 / NORSUS 2023 / NORSUS 2026; SSB 05281 (1995–2011); SSB restavfallsmengder | 2018: 31 550 t; 2022: 48,8 kt; 2025: 44 461 t; 1995–2011 fra 05281 (annet omfang) | Bruddet i 2012 (se over). 2012–2017 må interpoleres. Nivået i 05281 er for høyt for CL+HT-omfanget | ankerpunkter + historisk serie med annen definisjon |
| 8 | CO.CO-RW.RW Export of unsorted collected textiles | SSB 08801 (6309+6310 eksport) | 1988–2025 | Stemmer med NORSUS for 2025 (34,33 kt). Sortert og usortert er ikke skilt | **data finnes** |
| 9 | CO.CO-CO.SO Collected textiles to domestic sorting | balanse | – | Liten flyt | – |
| 10 | CO.SO-CO.RE Sorted for domestic secondhand sales | Watson 2020; NORSUS 2026 | 2018: 549 t; 2025: 1 622 t | Før 2018: innsamlernes årsrapporter | ankerpunkter |
| 11 | CO.RE-US.HH Secondhand sales to households | balanse | – | | – |
| 12 | WM.RS-WM.IN Domestic incineration | balanse; fordeling fra 05281 | 1995–2011 (andeler) | Andelen eksportert restavfall (D11) trekkes fra | – |
| 13 | WM.RS-WM.LF Landfilling of textiles | SSB 05281 | 1995–2011 | ≈ 0 etter 2009 (forbud). 1988–1994 ekstrapoleres (deponi var dominerende). 10513 viser 0–4 kt | **data finnes** (andeler) |

## Anbefalte neste steg
1. ~~Bekrefte tolkningen av bruddet i 2012~~: bekreftet i SSBs dokumentasjon (se over). Uavklart: om «Tekstiler» i 05281 ble beregnet med varetilførselsmetoden. Det kan bare SSB svare på.
2. Finne SSBs statistikk for grensehandel (flyt 3).
3. Hente NORSUS 2023 (OR.07.23) for detaljene i ankeråret 2022.
4. Finne kilder til innsamling før 2018 (flyt 6), for eksempel TemaNord 2012:545 og 2014:538, og vurdere eksporten av 6309 som proxy.
