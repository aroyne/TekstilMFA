# Fase D, trinn 1: forlengelse til 2050 og referansebane (forslag)

*Notat 2026-11-05. Bygger på [designnotatet](2026-11-02_D_fremtidsmodul_design.md) og D12: horisont 2050, start fra medianen i 2025, lagermodellen skalert til statistikken i 2025. Tallene i forslaget er medianer fra `MC_summary.csv` (N = 1000).*

**Besluttet 2026-11-05:** (1) egen modul, (2) iterasjon 0 som startpunkt, (3) 2025 alene som basisår, (4) gapet går til restlageret inntil videre og utforskes nærmere senere, (5) referansebanen uten nye regimer. Implementert samme dag, se resultatene til slutt.

## 1. Arkitektur: egen fremtidsmodul, ikke lengre `YEARS`

**Forslag:** Historikken (`main_mc.py`, `YEARS` = 1988–2025) står urørt. Fremtiden kjøres av et eget skript (`main_future.py`) med egne flytfunksjoner (`calculations/future/`), på det samme registeret (`system/flows.csv`) og i et eget flodym-system med t = 2026–2050.

Begrunnelse:
* De 42 flytfunksjonene i historikken bygger på data (handel, ankerpunkter, plukkanalyser). Hvis `YEARS` forlenges, må hver av dem få en egen gren for årene etter 2025. Da blandes to metoder i samme funksjon, og flytsidene kan ikke lenger peke til ett sted for hver metode.
* D12 sier at fremtiden starter fra medianen. Den trenger derfor ikke å kjøres inne i MC-løkken for historikken.
* Med samme register og `close()` får fremtiden den samme sjekken av massebalansen og den samme regelen om at hver flyt skal settes, og flytkodene er de samme. Det gjør det enkelt å sette sammen historikk og fremtid til én tidsserie.

Én funksjon per flyt gjelder også her. De fleste fremtidige flytene er en andel fra 2025 ganger det som kommer inn i kildeprosessen, så de deler en hjelpefunksjon. Docstringen sier hvilken andel som brukes og hvor den kommer fra.

**Startpunkt:** Den deterministiske kjøringen (iterasjon 0) er et lukket system med massebalanse. Medianer per flyt er det ikke, fordi medianene av to flyter ikke summerer til medianen av summen. Jeg foreslår derfor at iterasjon 0 brukes som «medianen» i D12. Avstanden mellom iterasjon 0 og medianen for hovedflytene i 2025 rapporteres.

## 2. Tilførsel: folketall × kg per innbygger

* **Folketall:** SSBs befolkningsframskriving (tabell 14740, 2026-utgaven; 12882 er 2020-utgaven), hovedalternativet MMMM i referansebanen. Lav (LLML) og høy (HMMH) brukes som X i trinn 2. Det blir en ny datafil og en ny oppføring i `DATA_SOURCES.md`.
* **Kg per innbygger per produkt:** For hver tilførselsflyt (salg til husholdninger og til institusjoner, direkte netthandel, privatimport, garn) holdes 2025-nivået per innbygger fast i referansebanen. Spennet −3 til +2 % per år er X i trinn 2.
* **Valg av basisår.** Direkte netthandel hoppet fra 3,6 kt (CL, 2024) til 13,0 kt (2025), og klesimporten falt i 2023. Én verdi for 2025 kan derfor være tilfeldig høy eller lav. Alternativet er snittet per innbygger for 2023–2025. Anbefaling: **2025 alene**, fordi det er der dataene slutter og der skaleringen av kasseringene gjøres (punkt 3). Snittet 2023–2025 tas med som følsomhetskjøring.
* **Oppstrøms** (import, eksport og egen produksjon i MA og DI): andelene fra 2025 av det som går ut av DI.RT til bruk. Det er ikke viktig for målene (M), men gjør at systemet lukkes.

## 3. Kasseringer: lagermodellen skalert til 2025

* **CORE i husholdningene:** Lagermodellen (`use_cohorts`) med tilførsel fra 1950 til 2050. Tilførselen til og med 2025 er historikken fra iterasjon 0, og tilførselen fra 2026 kommer fra punkt 2. Det betyr at årgangene i lageret i 2025 er de samme som i historikken.
* **Skalering:** Kasseringene i statistikken er s × kasseringene i lagermodellen, med s = statistikk ÷ lagermodell i 2025. Med medianene er det (36,0 + 17,6 + 26,4) ÷ 92,3 = 80,0 ÷ 92,3 ≈ **0,87**. Faktoren holdes fast i referansebanen.
* **Fordeling av kasseringene** mellom separat innsamling, ombrukbart i restavfall og slitt i restavfall: andelene fra 2025 (innsamlingsgrad ca. 45 %).
* **Hvor blir differansen (1 − s) av?** I historikken teller gapet mellom tilførsel og statistikk som lagervekst (restleddet, D8). Det samme skjer i fremtiden hvis ingenting annet gjøres: restlageret vokser med ca. 12 kt per år, mens lagermodellen holder seg nesten flat. Det er konsistent med D8, men det betyr at referansebanen fører «de usynlige kasseringene» videre som oppmagasinering i hjemmene til 2050. Det er NORSUS' tolkning. Jeg foreslår å beholde dette i referansebanen, rapportere begge lagrene og la s være en usikker faktor i trinn 2 (fra 0,75 til 1, og om s går mot 1 over tid).
* **CA, TA og OM i husholdningene og alt i US.IC:** De har allerede egne lagermodeller, og tilførselen forlenges. Sekker (SA) kasseres samme år som de tilføres (D13).
* **Fiberutslipp:** Vasken følger folketallet slik den gjør nå, og utslippet per kg er det samme som i 2025.

## 4. Etter kassering: andelene fra 2025

Andelene holdes på 2025-nivået: eksport av usortert, andelen som blir i Norge, ombruk og gjenvinning av det som sorteres, eksport av restavfall og forbrenning. Deponi er 0. Gjenvinningen ved NTG blir på 2025-nivået (0,36 kt).

**Hva referansebanen inneholder.** Bare dagens politikk, uten de nye regimene. Destruksjonsforbudet (19.7.2026), produsentansvaret (2027) og eksportreglene (WSR, 21.5.2027) legges inn som tiltak (L) i trinn 2 og 3. Da blir effekten av hvert tiltak synlig mot én felles referanse. Destruksjonsforbudet er allerede vedtatt, så en egen bane med vedtatt politikk kan legges ved siden av.

## 5. Usikkerhet, resultater og tester

* Trinn 1 er deterministisk. Usikkerheten kommer i trinn 2 som scenarier (flate spenn, latin hypercube).
* Bare TOT i trinn 1. Fiberlaget forlenges senere, hvis målene krever materialer (for eksempel for gjenvinning).
* **Resultater:** `output_files/future_reference.csv` med samme kolonner som `MC_summary.csv` (flow_name, product, year, value). Et plott av historikk og fremtid for kasseringer, innsamlingsgrad, lager og forbrenning (`scripts/plot_future.py`).
* **Tester:**
  * `close()` går gjennom for alle år 2026–2050.
  * Kasseringene i 2026 ligger nær 2025 (det skal ikke være noe brudd).
  * Med konstant folketall og fast nivå per innbygger blir tilførselen flat.
* Registeret endres ikke i trinn 1, så `tests/test_system_register.py` påvirkes ikke.

## Spørsmål

1. **Arkitektur:** Egen fremtidsmodul på det samme registeret (anbefalt), eller å forlenge `YEARS` med en fremtidsgren i hver flytfunksjon?
2. **Startpunkt:** Iterasjon 0 som «medianen» (anbefalt)?
3. **Basisår for kg per innbygger:** 2025 alene (anbefalt), med 2023–2025 som følsomhet?
4. **Gapet (1 − s):** Skal det gå inn i restlageret som i historikken (anbefalt for referansebanen), eller være en egen flyt for «uregistrerte kasseringer»?
5. **Referansebanen:** Uten de nye regimene (anbefalt), med en egen bane for vedtatt politikk, eller med destruksjonsforbudet inkludert fra 2026?

## Resultat (implementert 2026-11-05)

`main_future.py` → `output_files/future_reference.csv`, plott med `scripts/plot_future.py`. Systemet lukkes i alle år, og det klippes ikke. Kjøretiden er ca. 5 s. Deterministisk kjøring (iterasjon 0), CL+HT+FW i husholdningene:

| | 2025 | 2026 | 2030 | 2040 | 2050 |
|---|---|---|---|---|---|
| Folketall (mill., MMM) | 5,61 | 5,64 | 5,76 | 6,03 | 6,22 |
| Salg til husholdningene, alle produkter (kt) | 105,6 | 106,2 | 108,5 | 113,7 | 117,1 |
| Kassert, statistikk/skalert (kt) | 80,6 | 79,9 | 78,9 | 82,3 | 85,6 |
| Kassert, lagermodell uskalert (kt) | 90,7 | 89,9 | 88,8 | 92,6 | 96,3 |
| Separat innsamling (kt) | 36,2 | 35,8 | 35,4 | 36,9 | 38,4 |
| Lagerendring, restledd (kt per år) | 9,2 | 10,4 | 13,3 | 14,3 | 13,9 |
| Lager, restledd (kt) | 1 160 | 1 171 | 1 220 | 1 361 | 1 502 |
| Lager, lagermodell (kt) | 529 | 528 | 532 | 556 | 576 |
| Forbrenning i Norge (kt) | 94,2 | 93,5 | 92,6 | 96,3 | 99,9 |
| Produsentansvar, netto grunnlag (kt) | 95,4 | 96,0 | 98,1 | 102,7 | 105,8 |

* Skaleringen er s = 0,889 i iterasjon 0, mot 0,87 med medianene.
* Det er ikke noe brudd i 2026. Kasseringene i lagermodellen faller litt til ca. 2030, fordi tilførselen var lav i 2023–2024 og lagermodellen henger etter. Deretter følger de folketallet.
* Innsamlingsgraden ligger fast på 45 %, fordi andelene fra 2025 holdes.
* **Restlageret vokser med ca. 340 kt til 2050** (fra 207 til 241 kg per innbygger), mens lagermodellen bare vokser med folketallet. Det er konsekvensen av punkt 4 og må utforskes før resultatene brukes. Alternativene er en egen flyt for uregistrerte kasseringer, eller at s går mot 1.

### Forenklinger i implementeringen
* Oppstrøms (MA, DI) følger folketallet. Norsk ull og eksport av fiber og garn holdes fast. Import av ferdigvarer, metervare og fiber/garn er balanseflyter.
* Fiberutslippet i industrivask er utslippet per kt lager i US.IC i 2025 × det fremtidige lageret.
* Grunnlaget for produsentansvaret bruker andelene i tollkodene fra 2025.
* Strømmer som bare er andeler, er samlet i én funksjon per prosess (CO.CO, CO.SO, CO.RE, WM.RS), og flyter per innbygger og faste flyter er samlet i lister. Det avviker fra regelen om én funksjon per flyt. Alle flytene med egen logikk (kasseringer, balanser, US.IC) har egen funksjon. Fremtidsfunksjonene vises ikke på flytsidene ennå.

### Fiberlaget (lagt til samme dag)
* Fiberlaget kjøres også for 2026–2050 (`output_files/future_reference_fibre.csv`). Tilførselen beholder fibersammensetningen fra 2025. Lagermodellene får historikken per materiale, så kasseringene følger årgangene. Ingen klipping.
* Andel syntetisk av tekstilet i kasseringene (CL+HT+FW): 40 % (2010), 44 % (2018), 47 % (2025), 47 % (2030), 46 % (2050). Det går mot sammensetningen av det som kjøpes inn i 2025, fordi den holdes fast. En trend i fibersammensetningen er en usikker faktor for trinn 2.
* Historikken er identisk med før (kontrollert med samme frø, N = 200).

### Opphopningen
Se [notatet om opphopning hos forbruker](2026-11-05_opphopning_hos_forbruker.md). Litteraturen (særlig Danmark 2018) tilsier at gapet stort sett er kasseringer som ikke fanges opp, ikke lagervekst. Det foreslås å dele gapet i referansebanen.
