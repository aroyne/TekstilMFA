# Fase C: Hvor kommer lageravviket fra?

*Notat 2026-11-02. Deterministisk kjøring etter D37, D38 og fase A. Erstatter tallene i [notatet fra 2026-10-05](2026-10-05_lagermodell_mot_statistikk.md). Utforskende kjøringer er ikke en del av modellen.*

## Utgangspunkt (CL+HT+FW, 2025)

| | kt | kg per innbygger |
|---|---|---|
| Lager som restledd (statistikk, D8) | 1 562 | ca. 280 |
| Lagermodell (levetider fra litteraturen) | 529 | ca. 94, hvorav klær 56 |
| Millward-Hopkins m.fl. (2023), klær i UK | – | ca. 55 (3,6 Mt) |
| SIFO 2016: 359 plagg per person × 0,276 kg per plagg (importvekt per stykk, 08801) | – | ca. 99 klær |

**Presisering:** Tidligere notater oppga 110–140 kg klær etter SIFOs garderobestudier ([gjennomgang US.HH](2026-10-13_gjennomgang_US.HH.md)). Det bygger på 359 plagg per person og en antatt vekt på 0,3–0,4 kg per plagg. Importvekten per plagg er 0,276 kg, og da blir det ca. 99 kg. Utvalget i garderobestudiene er voksne, så tallet per innbygger (med barn) er trolig lavere. Lagermodellen (56 kg klær) ligger altså mellom UK-tallet og dette anslaget.

## Nedbryting av avviket

Lagrene starter likt i 1987, og tilførselen er den samme. Avviket i 2025 (ca. 1 030 kt) er derfor summen over årene av kasseringer i lagermodellen minus kasseringer i statistikken:

| Periode | Avvik i sum | Per år | Hva statistikken bygger på |
|---|---|---|---|
| 1988–2008 | 553 kt | 26 kt | Restavfallet holdes flatt per innbygger på 2009-nivået. Innsamlingen er eksport av brukte tekstiler, 1 kt i 1990 og 8 kt i 2000 |
| 2009–2017 | 330 kt | 37 kt | Rett linje mellom restavfallsankrene 2009 (Laitala, 33,5 kt) og 2018 (Mepex, 31,6 kt) |
| 2018–2025 | 131 kt | 16 kt, fallende til 10 kt | De tre kartleggingene (2018, 2022, 2025) |

### 1. Før 2009: restavfallet tar ikke opp det som senere ble samlet inn

Innsamlingen øker fra 1 kt i 1990 til 17 kt i 2009, mens restavfallet per innbygger holdes fast. Det betyr at husholdningene skal ha kassert mye mindre per innbygger i 1990 enn i 2009 (31 mot 51 kt i alt). Det er lite trolig. Det som senere ble samlet inn, gikk tidligere i restavfallet.

**Utforsket:** Hvis restavfallet før 2009 får det som ikke ble samlet inn sammenlignet med 2009-nivået per innbygger («substitusjon»), øker det med 14 kt i 1990 og 7 kt i 2000. Avviket før 2009 faller da fra 553 til ca. 370 kt (−183 kt).

### 2. 2009–2017: et lavt anker for 2018

Restavfallet i 2018 (31,6 kt) er lavere enn i 2009 (33,5 kt) og mye lavere enn i 2022 (48,8 kt). Watson m.fl. (2020) hadde bare tre analyser fra gjenvinningsstasjoner (6,1 kt, mot 15,2 kt i 2022). Med andelen fra gjenvinningsstasjonene i 2022 ville 2018 vært ca. 40 kt. Hele perioden 2009–2021 henger på dette ankeret. **Ikke utforsket ennå.** Det krever en vurdering av Mepex-tallene for 2018.

### 3. 2018–2025: levetidene forklarer ikke avviket

| Levetider (alle US.HH) | Lager 2025 | Kasseringer i modellen 2018/2022/2025 | Statistikk |
|---|---|---|---|
| × 1,0 | 94 kg/innb. | 97 / 93 / 91 | 69 / 82 / 81 |
| × 1,5 | 143 kg/innb. | 95 / 94 / 93 | |
| × 1,75 | 168 kg/innb. (klær 99) | 93 / 94 / 93 | |

Tilførselen har vært omtrent flat siden 2005. Da blir kasseringene i lagermodellen omtrent lik tilførselen, uansett levetid. Levetidene styrer nivået på lageret, men ikke avviket i kasseringene. Avviket i nyere tid (10–27 kt per år) er derfor tilførsel minus kasseringer i statistikken. Enten er tilførselen 10–25 % for høy, eller så mangler 10–25 % på kasseringssiden. Kandidater:
* **Tilførsel:** institusjonsandelen (12 %, kan være høyere), gjeneksport som ikke er registrert, og direkte netthandel (VOEC brutto, nå med returer).
* **Kasseringer:** destruksjon av usolgte varer (EEA-nivå gir −176 kt i lageret i 2025), tekstiler i næringsavfall fra husholdningene (for eksempel flytting og dødsbo), uformell videreføring og privat bruktsalg ut av landet, og et lavt anker for 2018 (punkt 2).
* NORSUS tolker gapet som oppmagasinering i hjemmene (ca. 4,5 kg per innbygger per år). Lagermodellen gir ingen vekst i lageret etter 2015, fordi tilførselen er flat.

### 4. Strukturvalg (A5) og usikkerhet (fase A)

* Innsvingingen flytter begge lagrene likt og endrer ikke avviket.
* Lageret som restledd i 2025 er 1 617 kt med 95 %-intervall 997–2 210. Selv nedre grense er over 1,7 ganger lagermodellen. Avviket er altså ikke et usikkerhetsspørsmål.

## Konklusjon

1. Levetidene styrer nivået på lageret, men ikke kasseringene, så de kan kalibreres mot garderobedata uten å endre avviket. Lagermodellen (56 kg klær) ligger mellom UK-tallet (55 kg) og anslaget fra SIFOs plagg-tall (ca. 99 kg for voksne). Det gir et spenn i levetidene fra × 1 til × 1,75. Selv det høyeste lagernivået (168 kg for CL+HT+FW) er langt under lageret som restledd (ca. 280 kg).
2. Mer enn halvparten av avviket (553 kt) kommer fra perioden før 2009. Der finnes ingen data, og fyllregelen for restavfallet er lite fysisk.
3. En tredel (330 kt) kommer fra 2009–2017 og henger på restavfallsankeret for 2018.
4. Resten (131 kt) er et vedvarende gap i nyere tid på 10–27 kt per år. Det er det mest interessante funnet, fordi data er best der. Det er også det NORSUS kaller oppmagasinering.

## Forslag (D40, til avklaring)

1. **Restavfall før 2009, substitusjon:** Restavfallet før 2009 = 2009-nivået per innbygger + (innsamling per innbygger i 2009 − innsamling det året) × folketall. Med andre ord: det som ikke ble samlet inn, gikk i restavfallet. Det er fortsatt en antakelse, men den er mer fysisk enn dagens, og D30-usikkerheten beholdes. Effekt: −183 kt i lageret som restledd.
2. **Ankeret for 2018:** vurdere andelen fra gjenvinningsstasjonene i Mepex 2018 (tre analyser) mot 2022, eventuelt med bredere usikkerhet for 2018-ankeret i stedet for å endre tallet.
3. **Det vedvarende gapet:** beholdes som et funn og rapporteres med usikkerhet og kandidater. Det er dette en artikkel kan bygge på (jf. [nytt mot NORSUS](2026-11-02_nytt_mot_NORSUS.md), artikkel 1).
4. **Levetider mot garderobedata:** skaffe vekt per plagg og antall plagg per innbygger, med barn, fra SIFO og OsloMet (Laitala & Klepp). Deretter skaleres levetidene i US.HH slik at lageret av klær treffer, med usikkerhet. Inntil da beholdes levetidene, og spennet × 1–1,75 rapporteres.
