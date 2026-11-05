# Hva kan ankerårene si om lageret? Og nevnerproblemet

*Notat 2026-11-05. MC med 1 000 iterasjoner etter D42 (frø 1). Fordelingene for lagerendring, lagernivå og lagermodell er tatt per iterasjon, ikke som medianer per flyt. CL+HT+FW i husholdningene. Intervallene er 95 %.*

## 1. Hvor datafattig er tidsserien?

| Ledd i balansen | Data | Hvor ofte | Usikkerhet |
|---|---|---|---|
| Tilførsel (import − eksport, VOEC, norsk produksjon) | SSB 08801, registrert | **Hvert år 1988–2025** | ca. ±5–10 % per år, institusjonsandelen er en skjønnsparameter |
| Separat innsamling | Eksport av HS 6309+6310 (08801) + andel som holdes tilbake | **Hvert år** | ca. ±5–10 % |
| Tekstiler i restavfallet | Plukkanalyser | **Fire ankerår: 2009, 2018, 2022, 2025** | ±30 % per anker, delvis felles metodefeil. 2009 og 2018 er justert (D40, D42) |
| Restavfall før 2009 | Ingen målinger. Fylt ut med en regel (D40) | – | Gap-støy som vokser med avstanden |
| Startlager 1987 | Lagermodell med innsvinging fra 1950 (D2) | – | 350 kt (244–459), styrt av levetidene |

Lageret er summen over tid av «tilført − kassert». Tilførselen er godt kjent hvert år. Kasseringene er kjent fire ganger på 37 år, og bare tre av dem er moderne kartlegginger (2018 med få analyser og uten sko).

## 2. Hva ankerårene kan si om lageret

### Lagernivået i 2025: ikke solid

| | kt | kg per innbygger |
|---|---|---|
| Restledd 2025 | 1 169 (440–1 816) | 209 (79–325) |
| Lagermodell 2025 | 566 (384–755) | 101 (69–135) |
| Garderobedata (klær, voksne) | – | 55–110 |

Nivået er bygget av tre deler med svært ulik kvalitet:

| Del av nivået | kt (median og 95 %) | Grunnlag |
|---|---|---|
| Startlager 1987 | 350 (244–459) | Modell (D2) |
| Sum av lagerendringene 1988–2008 | 479 (−161 til 910) | **Restavfallet fylt ut uten målinger** |
| Sum av lagerendringene 2009–2025 | 354 (123–590) | Fire ankre, interpolert |

* Intervallene for restleddet og lagermodellen **overlapper**. Restleddet er større enn lagermodellen i 95 % av iterasjonene og mer enn 1,5 ganger større i 83 %.
* Perioden før 2009 bidrar med 479 kt, men intervallet går fra −161 til +910 kt. Den sier i praksis ingenting.
* **Konklusjon:** Data alene kan ikke fastslå nivået på lageret. Vi kan si at restleddet **trolig** er større enn lagermodellen og garderobedataene tilsier, men ikke at de ikke kan forenes. Formuleringen i ISIE-notatet er rettet.

### Lagerendringen i årene med ankre: mer solid, men ikke sikker

| År | Lagerendring (kt) | P(> 0) | P(> 0,5 kg/innb., ca. 2,8 kt) | P(> 1 kg/innb., ca. 5,6 kt) |
|---|---|---|---|---|
| 2009 | 36,9 (16,9–56,6) | 1,00 | 1,00 | 1,00 |
| 2018 | 11,3 (−4,2–27,2) | 0,93 | 0,86 | 0,77 |
| 2022 | 16,4 (−1,7–36,9) | 0,96 | 0,94 | 0,88 |
| 2025 | 9,6 (−6,9–27,0) | 0,88 | 0,78 | 0,67 |
| Sum 2018–2025 | 75 (−32–200) | 0,91 | – | 0,70 (> 8 × 1 kg) |

* **Ingen av de moderne ankerårene alene viser et gap som er signifikant på 95 %-nivå.** Intervallet går under 0 i 2018, 2022 og 2025.
* Medianen er positiv i alle år, og godt over en realistisk lagervekst (0,5–1 kg per innbygger per år). Feilene i ankrene for restavfallet er delvis felles (korrelasjonen mellom 2018 og 2025 er 0,55), så tre positive år er ikke tre uavhengige bevis.
* Usikkerheten domineres av tekstilene i restavfallet (±30 % av 44 kt er ±13 kt, altså like mye som selve gapet).
* 2009 skiller seg ut med 37 kt, men det kommer delvis av at tilførselen var på topp (2008–2011) mens restavfallet bare har ett anker.

**Konklusjon:** Ankerårene gir **odds på ca. 3:1 til 7:1** for at gapet i nyere tid er større enn det garderobene kan ta opp (P = 0,67–0,88 med 1 kg per innbygger per år). Det er et rimelig sterkt indisium, men ikke et bevis. Det mest solide vi kan si, er:
1. Den lange tidsserien gir verdi først og fremst på **tilførselssiden** (registrert hvert år) og som **diagnose**. Ingen fylleregel for restavfallet før 2009 gir et lager som stemmer med garderobedata uten at det også oppstår et gap etter 2009.
2. Avviket i nyere tid er sannsynligvis reelt, men størrelsen er usikker (median ca. 10–16 kt per år, ca. 2–3 kg per innbygger).
3. **Det som ville gjort konklusjonen solid,** er bedre restavfallsdata. Med ±10 % i stedet for ±30 % på ankrene ville gapet i 2022 og 2025 bli signifikant hvis medianen holder. I tillegg trengs data for næringsavfall og grovavfall fra husholdningene.

### Hva det betyr for formidlingen
* Ikke skriv: «Lageret som restledd kan ikke forenes med garderobedata.»
* Skriv heller: «Restleddet er trolig 1,5–3 ganger det lagermodellen og garderobedataene tilsier. Gapet i nyere tid (ca. 10–16 kt per år) er positivt i 88–96 % av iterasjonene og større enn en realistisk lagervekst i 67–88 %. Det er mer forenlig med kasseringer som ikke fanges, enn med oppmagasinering.»
* Den lange tidsserien er en styrke for å vise at dataene **ikke lukker** over tid. Den er ikke et mål på lagernivået.

## 3. Nevnerproblemet

Innsamlingsgraden er det innsamlede delt på noe. **Telleren er godt kjent, nevneren er det ikke.**

**Telleren:** Separat innsamlet fra husholdningene var ca. 36 kt i 2025. Den kommer fra eksportstatistikken (HS 6309+6310), som veies og registreres, og innsamlerne sender nesten alt ut av landet. Usikkerheten er ca. ±5–10 %.

**Nevneren:** Det finnes tre mulige nevnere, og de gir forskjellige svar med samme teller:

| Nevner | Hva den er | 2025 | Innsamlingsgrad |
|---|---|---|---|
| **A. Registrerte kasseringer** | Innsamlet + tekstiler i restavfallet (plukkanalyser) | 36 + 44 = 80 kt | **45 %** (38–55 %) |
| **B. Alle kasseringer** | A + kasseringer som plukkanalysene ikke ser (næringsavfall og grovavfall, D42) | 80 + 5–10 = 85–90 kt | **40–42 %** |
| **C. Satt på markedet** (grunnlaget for produsentansvaret) | Nye tekstiler i året, netto (gross) | 95 (104) kt | **38 %** (35 %). NORSUS: 33 % |

Hvorfor de er forskjellige:
* **A mot B:** Plukkanalysene dekker bare husholdningsavfall som kommunene håndterer. Tekstiler som går som næringsavfall (flytting, dødsbo, containere og grovavfall som private firmaer henter), er usynlige. Hvis de finnes, er dagens grad overvurdert, og den overvurderingen kan ikke rettes med flere plukkanalyser av husholdningsavfall.
* **A og B mot C:** Det som settes på markedet i år, kasseres om noen år. C blander derfor innsamlingen med lagerendringen og med gapet. C er lett å måle, men måler ikke det tiltaket skal påvirke, altså hvor stor del av det som kasseres som samles inn.
* **Usikkerheten innenfor A:** Graden er 36/(36 + R), der R er tekstilene i restavfallet. Én kt mer i R senker graden med ca. 0,56 prosentpoeng. Med dagens ±30 % på R (±13 kt) er graden usikker med **±7 prosentpoeng**.

Hva det betyr for produsentansvaret:
1. **Et mål på 50 % kan være nådd eller ikke, avhengig av definisjonen.** Med samme innsamling er graden 35 %, 40 % eller 45 %.
2. **En forbedring på 5 prosentpoeng kan ikke påvises** med dagens plukkanalyser (±7 pp). Hvis den skal kunne påvises med rimelig sikkerhet (±2,5 pp), må tekstilene i restavfallet kjennes til ca. ±10 % (±4–5 kt). Det krever flere og mer representative plukkanalyser, også fra gjenvinningsstasjonene, som var svakt dekket i 2018.
3. **Næringsavfall og grovavfall fra husholdningene må kartlegges** før nevner B kan brukes. Ellers vil graden virke bedre enn den er.
4. Nevner C kan brukes som et enkelt og stabilt mål, men da må det sies tydelig at den ikke er en innsamlingsgrad for det som kasseres.

Dette er punktet med størst overføringsverdi for et abstract. Det gjelder alle land som skal følge opp innsamlingsmål under WFD 2025/1892, og vi kan tallfeste det for Norge.
