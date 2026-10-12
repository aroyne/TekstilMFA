# Gjennomgang av PS.WO og MA.FI (fiber og garn)

*2026-10-12. Første subpool i gjennomgangen flyt for flyt. Rekkefølgen følger materialet: PS.WO/MA.FI → MA.TX → DI.RT → US.HH → US.IC → CO.CO → CO.SO → CO.RE → WM.RS → WM.RC → WM.WW/EN.*

Beslutningene står som D21–D24 i [SYSTEMDEFINISJON](../docs/SYSTEMDEFINISJON.md). Alle flytene er implementert og kjørt med N = 10.

## Flytene

| Flyt | Kilde | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|---|
| Norsk råull (PS.WO → MA.FI) | Totalkalkylen (NIBIO) | 4,95 | 4,94 | 4,35 | 3,90 | 3,15 | 2,85 |
| Import av fiber og garn (RW → MA.FI) | SSB 08801, HS 50–55 uten metervare og detaljgarn | 16,5 | 16,9 | 11,3 | 10,7 | 9,5 | 9,9 |
| Eksport av fiber og garn (MA.FI → RW) | SSB 08801 | 5,23 | 5,10 | 4,58 | 4,07 | 3,26 | 3,05 |
| Vaskesvinn (MA.FI → WM.WW), ny | Periodesnitt × svinnandel 0,33 | 0,99 | 1,29 | 0,10 | 0,10 | 0,10 | 0,10 |
| Garn til tekstilindustrien (MA.FI → MA.TX) | Balanse | 15,2 | 15,5 | 11,0 | 10,5 | 9,3 | 9,6 |

kt per år, median av MC-kjøringen.

### 1. Norsk råull

Kilden er Totalkalkylen for jordbrukssektoren (Budsjettnemnda for jordbruket). Den er hentet fra NIBIOs statistikktjeneste og gir tonn, kr/kg og verdi per år fra 1959. Tallene gjelder innveid, uvasket ull. Produksjonen faller fra 5,7 kt (1994) til 2,9 kt (2025).

### 2. Import av fiber og garn, delt med data

HS-mappingen skiller nå mellom tre grupper:
- **FY:** fiber og garn.
- **FA:** metervare, som går til MA.TX i neste runde.
- **YA:** garn i detaljopplegg (HS 5109, 5207, 5204.20, 5406, 5511).

YA går RW → DI.RT → US.HH og regnes til CORE etter bruk, fordi hjemmelagde plagg kasseres som klær. Flyten er liten: import 0,8 kt (1990) og 2,7 kt (2025), eksport 0,4 og 2,1 kt.

### 3. Eksport av fiber og garn: problemet med gjeneksport

Handelsstatistikken registrerer varer som krysser grensen, uansett hvor de er produsert. Garn som et norsk garnmerke får spunnet i utlandet, kan derfor importeres til et lager i Norge og eksporteres videre til forhandlere i Norden. Det registreres da både som import og som eksport.

- **Når det ikke skaper feil:** Garnet er registrert som samme vare begge veier, for eksempel FY inn og FY ut. Da utlignes det i balansen til MA.FI. Garnflyten til MA.TX blir riktig, men eksportflyten overvurderer hvor mye garn som er spunnet i Norge.
- **Når det skaper feil:** Varen skifter gruppe på veien, eller norsk produksjon eksporteres. To tilfeller er viktige:
  - **Norsk spunnet håndstrikkegarn som eksporteres** (YA ut fra DI.RT). Det trekkes fra importen av detaljgarn, men den norske produksjonen er aldri lagt til i DI.RT. Salget av garn til husholdningene blir da for lavt, og garnflyten til MA.TX for høy med samme mengde. Eksporten av detaljgarn har økt fra 0,7 kt i 2018 til 2,1 kt i 2025, så dette kan ha betydning.
  - **Garn importert som industrigarn (FY) og pakket for detaljsalg i Norge.** Det går ut som YA.
- **Hvorfor statistikken ikke løser det:** 08801 har ikke et eget felt for gjeneksport. SSB skiller gjeneksport bare i enkelte tabeller og ikke per HS8. Dette er det samme problemet som for ferdigvarer (D6).
- **Forslag:** Ta det opp med MA.TX, og innfør en flyt MA.FI → DI.RT for norsk spunnet håndstrikkegarn (se punkt 4).

Råullen er ikke rammet. Uvasket ull (5101.11/19) importeres nesten ikke, og eksporten tilsvarer produksjonen.

### 4. Garn til tekstilindustrien: andre kilder

Balansen er hovedkilden, fordi den bygger på offisielle data (08801 og Totalkalkylen). Andre kilder kan brukes til kontroll eller til å dele flyten:

| Kilde | Hva den gir | Vurdering |
|---|---|---|
| SSB 10455 (Prodcom, 2008–2025) | Solgt produksjon per prodcomkode i store foretak: ullgarn i detaljopplegg (13.10.50.50) 0,80–0,92 kt i 2008–2020, karde- og kamgarn (13.10.50.10/30) | Mange celler er skjult (`:`), og små foretak er ikke med. Gir en nedre grense for norsk spunnet håndstrikkegarn |
| SSBs eldre varestatistikk for industrien (NOS, 1988–2007) | Samme type tall før 2008 | Må hentes fra PDF |
| SSB 12910 (2017–2024), 08675 (2007–2024) | Omsetning, sysselsatte og varekostnader for næring 13.1 (spinning) og 13–15 | Varekostnad ÷ NOK/kg for importert fiber gir et grovt massetall. Modellbasert, bare til sammenligning |
| Årsrapporter og regnskap for spinneriene (Sandnes Garn, Rauma, Hillesvåg, Dale, Selbu, Gjestal) | Sandnes Garn: ca. 600 t garn per år, 18 % av norsk ull | Kan summeres nedenfra for håndstrikkegarn. Ufullstendig og uten tidsserie |
| Ullialt (Norges Husflidslag 2018), Norilia | Omtrent 20 % av norsk ull brukes i Norge. Norilia selger vasket ull og topper (Svanemerket) tilbake til norske spinnerier | Stemmer med 08801: import av vasket ull og topper ca. 0,6 kt |
| SSB 10455, kode 13.94 (tau og nett) | Tauverk av syntetiske fibre (13.94.11.60) 3,4–4,4 kt | **Viktig:** En stor del av garnet til MA.TX går trolig til tau og nett (se under) |

Anbefaling: Behold balansen. Bruk Prodcom og tallene fra spinneriene til kontroll. Del flyten etter bruksområde i MA.TX-runden.

## Funn som må tas opp i MA.TX-runden

1. **Syntetisk garn til tau og nett.** 6–8 kt av garnet til MA.TX er syntetisk (8,4 kt i 1990, 6,4 kt i 2022). Norsk tekstilindustri er i stor grad tau og nett til fiske og havbruk (NACE 13.94). Ferdigvarene i HS 56 er utenfor omfanget (D22), men garnet de lages av er med. MA.TX trenger enten en flyt ut av omfanget for garn til tau og nett, eller så må FY deles etter bruksområde.
2. **Norsk spunnet håndstrikkegarn** går til husholdningene, ikke til MA.TX. Det trengs en flyt MA.FI → DI.RT med data fra Prodcom 13.10.50.50 og spinneriene.
3. **Midlertidig lager i MA.TX** (D24). Lagerendringen er nå lik garnflyten og skal bort når utstrømmene fra MA.TX er implementert.

## Antakelser som bør vurderes

- Svinnandel ved vasking: 0,33 (0,20–0,45). Norwegian Wool Book sier en tredjedel. Et norsk vaskeutbytte er ikke dokumentert.
- Uvasket ull vasket i Norge, som periodesnitt: 2,8 / 3,7 / 1,3 / 0,3 kt (1988–95 / 1996–2000 / 2001–06 / 2007–25). Eksport av karbonisert ull (5101.30) på 1,5–2,2 kt i 1997–2000 viser at det ble vasket og karbonisert ull i Norge da. Hvilke anlegg som ble lagt ned rundt 2001–2007, er ikke dokumentert.
- Levetid for YA i lagermodellen: 8 år (5–15), en antakelse.
- Fibersammensetning for YA og FY når HS-koden ikke oppgir fiber: brukes nesten ikke, fordi nesten alle kodene oppgir fiber.

## Kilder

- [Totalkalkylen for jordbrukssektoren, NIBIO](https://nibio.no/tema/landbruksokonomi/totalkalkylen) (statistikktjenesten, post «Ull»)
- [Totalkalkylen 2020, tabellutgave, vedleggstabell 1.8](https://www.nibio.no/tema/landbruksokonomi/budsjettnemnda-for-jordbruket/_/attachment/inline/5c8ec94b-beeb-45f2-95c4-3ca7503a09f3:3b31d8c5c16609ecbc87d43ba33d58f2a15c563b/Totalkalkylen%202020.%20Tabellutgave.pdf)
- [SSB 10455](https://www.ssb.no/statbank1/table/10455/), SSB 12910, SSB 08675
- [Norwegian Wool Book (Flokk)](https://focus.flokk.com/hubfs/Download%20Files/Norwegian_Wool_Book.pdf)
- [Ullialt-rapporten 2018 (Norges Husflidslag)](https://husflid.no/wp-content/uploads/2021/11/Ullialt_rapport_2018.pdf)
- [Haworth Scouring, Bradford](https://katedaviesdesigns.com/2015/08/31/at-haworth-scouring/)
- [Norilia Norwegian Wool scoured and tops (Svanemerket)](https://svanen.se/en/product-types/fabric-and-yarn/norilia-norwegian-wool-scoured-and-tops)
- [SNL: Sandnes Garn](https://snl.no/Sandnes_Garn)

## Oppfølging (samme dag): norsk spunnet garn og garn til tau og nett

### Kilder for norsk spunnet garn

| Kilde | Hva den sier | Bruk |
|---|---|---|
| SSB 10455, Prodcom 13.10.50.50 (ullgarn i detaljopplegg) | 0,92 / 0,73 / 0,80 / 0,64 / 0,91 / 0,61 / 0,59 / 0,80 / 1,03 / 0,59 / 0,69 kt (2008, 09, 12, 13, 16, 18, 19, 20, 21, 22, 23). Andre år er skjult. Gjelder bare store foretak | **hovedkilde** for MA.FI → DI.RT |
| SSB 10455, 13.10.61.60 og 13.10.81.50 (bomulls- og syntetisk garn i detaljopplegg) | Skjult i alle år | ikke brukt |
| SNL («garn», «Sandnes Garn») | Omtrent 1 000 t håndstrikkegarn per år, og over 500 mill. kr i omsetning (uten årstall). Sandnes Garn ca. 600 t | usikkerheten på 10455 skjevfordelt oppover (−10 / +50 %) |
| SSB Industristatistikk 1988 og 1989, Hefte II Varetall (NOS B 943, B 999) | Varetall før Prodcom | skannet uten tekstlag, krever OCR. Etter 1989 publiserte SSB bare næringstall (17 Tekstiler samlet) |
| Eksport av detaljgarn 5109 (08801) | I 1990 eksporterte Norge mer ullgarn i detaljopplegg (0,27 kt) enn det ble importert (0,08 kt). Det viser at norsk produksjon var betydelig også da | indikator, ikke brukt |

Implementert: **MA.FI → DI.RT «Domestic hand knitting yarn»** (produkt YA), med interpolering mellom publiserte år. Verdien holdes på 2008-nivå før 2008 og på 2023-nivå etter 2023. Salget av detaljgarn til husholdningene blir da 1,1–2,2 kt (før: 0,2–1,5 kt). I fiberlaget er det norske garnet ull, og flytene ut av DI.RT får blandingen av import og norsk garn.

### Feilklassifisert karbonisert ull

Den nye flyten gjorde ullbalansen i MA.FI negativ i 2000 i 36 % av trekkene. Årsaken var eksport deklarert som **karbonisert ull (5101.30) i 1996–2000 og 2002, 0,4–2,2 kt per år**. Den er nesten helt sikkert uvasket ull:
- Prisen er 7,5–10 kr/kg, som for uvasket ull (8,5–11) og lavere enn for vasket ull (13–23).
- Den går til Storbritannia, som den uvaskede ulla.
- Eksporten av uvasket ull faller like mye i de samme årene.

Den regnes nå som uvasket når prisen per kg er lavere enn for vasket ull samme år. Mengden uvasket ull som vaskes i Norge i 1996–2000, faller da fra 3,7 til 2,2 kt. Usikkerheten på periodesnittene er satt til standardfeilen (6–18 %). Med dette feiler 2 av 1 000 trekk, i 1989, fordi håndstrikkegarnet før 2008 er holdt på 2008-nivå.

### Spørsmål 1: kan garnet til tau og nett ekskluderes?

Ja, det kan gjøres med HS-koder. Høyfast filamentgarn av nylon, polyester og aramid (5402.10, 5402.11, 5402.19, 5402.20) er typisk garn til tau, nett og industriformål. Norge har ingen dekkindustri, som ellers er den andre store brukeren.

| | 1990 | 2000 | 2008 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Import av høyfast garn (kt) | 1,3 | 4,8 | 5,6 | 2,9 | 2,1 | 2,9 |
| Eksport (kt) | 0,0 | 0,0 | 0,1 | 0,1 | 0,1 | 0,1 |
| Syntetisk i garn til MA.TX nå (kt) | 8,6 | 11,0 | 10,6 | 7,9 | 6,6 | 7,0 |

- **Hvordan:** Kodene settes til `in_scope = no` i `hs_mapping.csv` (seks sifre), både for import og eksport, så balansen er symmetrisk.
- **Hva som blir igjen:** Omtrent 4–6 kt syntetisk. Det er mest polyester stapelfiber (5503.20, ca. 2,5 kt), som trolig er fyll til dyner og puter (innenfor omfanget, HT) eller fiberduk (utenfor). Resten er tvunnet nylongarn (5402.61), som også kan være nettgarn.
- **Hvorfor ikke trekke fra Prodcom:** Prodcom 13.94 gir 4–10 kt tau og 1–3 kt nett. Det er mer enn importen av høyfast garn, fordi tau og nett i stor grad lages av polyetylen og polypropylen som ekstruderes fra granulat i Norge, ikke av importert tekstilgarn. Å trekke produksjonen fra garnbalansen ville gjort den negativ.
- **Anbefaling:** Ekskluder høyfast filamentgarn med HS-koder, og ta 5402.61 og 5503.x med i MA.TX-runden.

## Beslutninger og implementering (samme dag, runde 3)

1. **Høyfast filamentgarn er tatt ut** (5402.10, 5402.11, 5402.19, 5402.20, `in_scope = no`, både import og eksport). Importen av fiber og garn faller med 1,3–5,6 kt per år. Garnet til MA.TX er nå 13,5 kt (1988), 10,4 kt (2000) og 6,2–7,3 kt (2008–2025). Syntetisk er 4,2–7,2 kt av det, mest polyester stapelfiber og tvunnet nylongarn, som tas opp i MA.TX-runden.
2. **Håndstrikkegarn før 2008 er interpolert.** Tallene for 1988 og 1989 er lest manuelt fra SSBs Industristatistikk, Hefte II Varetall (NOS B 941, s. 27, og NOS B 998, s. 22), varenummer 5109.1001 og 5109.1002 (ullgarn i detaljopplegg, store bedrifter):

   | År | 5109.1001 (t) | 5109.1002 (t) | Sum (t) | Verdi (1 000 kr) |
   |---|---|---|---|---|
   | 1988 | 422 | 571 | 993 | 112 105 |
   | 1989 | 366 | 527 | 893 | 113 106 |

   Nivået er det samme som i Prodcom 2008 (922 t), så 1990–2007 interpoleres mellom 1989 og 2008. Varetall for 1985–87 finnes også (NOS B 689, B 781, B 876), men ligger før modellperioden. Fra 1990 publiserte SSB bare næringstall.

**Gjenstående:** Ullbalansen i MA.FI er stram i 1989 (0,62 kt margin) og i 2000 (0,58 kt). 2 av 1 000 trekk feiler i 1989, når svinnandelen (opptil 0,45), håndstrikkegarnet (opptil +50 %) og handelsstøyen trekkes høyt samtidig. Modellen krasjer som den skal. Før en full MC-kjøring bør vi vurdere om usikkerhetene er for vide eller burde være korrelerte.

**Oppdatering:** Balansestrømmer kan klippes til 0 i stedet for å krasje (godkjent av Anja 2026-10-12). Garnet til MA.TX i fiberlaget klippes nå per materiale. Ull blir 0 når ulla ikke strekker til, de andre materialene skaleres slik at TOT-massen beholdes, og eksportens sammensetning tar opp differansen, så alle materialer fortsatt balanserer. Ingen feil i 1 000 trekk.
