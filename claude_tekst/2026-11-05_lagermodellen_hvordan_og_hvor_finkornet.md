# Lagermodellen: hvordan den virker, og hvor finkornet den er

*Notat 2026-11-05. Beskriver `calculations/cohorts.py`, `parameters/lifetimes.csv` og bruken i `us_mc.py`, `fibre_layer.py` og `future.py`.*

## Hvordan den virker

**Prinsipp:** Lagermodellen er en innstrømsdrevet årgangsmodell (flodym `InflowDrivenDSM`). Hvert år er en årgang: kg av et produkt som kommer inn i bruk det året. Hver årgang overlever etter en Weibull-fordeling, og det som ikke overlever, er kasseringene. Tilførselen regnes som kommet midt i året. Lageret er summen av det som er igjen av alle årgangene.

**Hvor den brukes:**

| Lager | Produkter | Rolle i historikken | Rolle i fremtiden |
|---|---|---|---|
| Husholdninger (US.HH), CORE | CL, HT, FW, YA | **Diagnose.** Kasseringene kommer fra statistikken (D8), og lagermodellen er en parallell kontroll | Gir kasseringene, skalert til 2025. Gir kjøpene med lagerdrevet etterspørsel |
| Husholdninger, andre varer | CA, TA, OM | Gir kasseringene (ingen statistikk, unntak fra D8) | Det samme |
| Institusjoner (US.IC) | CL, HT, FW, CA, TA, OM | Gir kasseringene | Det samme |
| Sekker (SA) | – | Kasseres samme år (emballasje, D13) | Det samme |

**Hva som går inn:**
* **Tilførsel per produkt og år:** salg + privatimport + direkte netthandel − returer, fra 1988.
* **Sammensetning per materiale** fra fiberlaget. Årgangene har derfor med seg fiberblandingen fra innkjøpsåret, og sammensetningen av kasseringene henger etter tilførselen.
* **Innsvinging:** Tilførselen 1950–1987 er holdt på 1988-nivået (D2). Det gir et startlager på ca. 350 kt (244–459) i 1987.

**Levetider** (`parameters/lifetimes.csv`): Hvert produkt har én gjennomsnittlig levetid, trukket flatt innenfor et spenn i MC. Formparameteren er 2 for alle produkter (en antakelse).

| Husholdninger | Gjennomsnitt (spenn) | Kilde |
|---|---|---|
| Klær (CL) | 6 år (4–9) | Laitala & Klepp 2020 (5,2 år per eier), WRAP 2023 (4,3), Napolano 2025 (4,7). Lengre fordi uformell videreføring og dvalelager er med (D9, D10) |
| Hjemmetekstiler (HT) | 7 år (3–10) | WRAP 2023, Napolano 2025 |
| Sko (FW) | 4 år (3–6) | Napolano 2025 (Laitala m.fl. 2018) |
| Garn og strikkede plagg (YA) | 8 år (5–15) | Antakelse |
| Tepper, presenninger, andre (CA, TA, OM) | 10, 4, 2 år | Napolano 2025, van Oorschot 2020 |

Institusjonene har kortere levetider (arbeidsklær 3 år, sengetøy 2 år), stort sett antakelser.

**I fremtidsmodulen** kan levetidene endres på tre måter:
* **Nivå (X4):** hele perioden × 1–1,75.
* **Årgangseffekt:** Nye årganger fra 2026 kan få kortere levetid (X4b, ultrarask mote) eller lengre (L3 holdbarhet, bare klær fra 2029).
* **Periodeeffekt (ny):** Reparasjon (L7) senker risikoen for å kassere i en gitt alder for alle plagg i bruk fra 2027, også de som er kjøpt tidligere. Overlevelsen bygges da opp år for år. Med faktor 1 er den nøyaktig lik Weibull-modellen (test).

## Hvor finkornet er den?

**Kort sagt: grov.** Den har fire produktgrupper for husholdningene, én levetidsfordeling per gruppe, og ingen endring over tid i historikken. Det passer til spørsmålene vi stiller (mengder og forsinkelser på nasjonalt nivå), men den kan ikke skille mellom typer plagg, brukere eller kvalitet.

| Dimensjon | I modellen | Ikke i modellen |
|---|---|---|
| Produkter | 4 grupper i CORE (klær, hjemmetekstiler, sko, garn) | Typer plagg (sokker, undertøy, jakker). Klær er én gruppe, selv om tilførselen finnes på HS8-nivå |
| Tid | Årlige årganger, tilførsel midt i året | Endring i levetid i historikken (ultrarask mote 2000–2025). Levetidene er like fra 1950 til 2025 |
| Materiale | Fiberblandingen følger årgangene | Levetid som avhenger av fiber (syntetiske plagg kan leve kortere eller lenger) |
| Enhet | kg | Antall plagg og vekt per plagg over tid (08801 har stykk, men det brukes ikke i lagermodellen) |
| Lager | Ett lager per produkt | Aktivt lager og dvalelager (WRAP: 26–30 % ikke brukt på et år) |
| Ombruk | Uformell videreføring regnes som lengre levetid (D9). Bruktkjøp er med i lagermodellen bare med lagerdrevet etterspørsel i fremtiden | Egne sløyfer for videreføring og andre eiere |
| Levetidsfordeling | Weibull, form 2 for alt | Form estimert fra data. Det finnes ingen norske overlevelsesdata |
| Kalibrering | Ingen. Levetidene er fra litteraturen | Kalibrering mot lagernivå. Nivået kan ikke fastslås fra data ([notat](2026-11-05_lagerets_datagrunnlag_og_nevnerproblemet.md)) |
| Brukere | Ett gjennomsnitt | Forskjeller etter alder, kjønn og inntekt |

**Hva grovheten betyr:**
* For **mengder og forsinkelser** er den tilstrekkelig. Usikkerheten i den gjennomsnittlige levetiden (for eksempel klær 4–9 år) er langt større enn det en finere oppdeling ville løst uten nye data.
* For **holdbarhet og reparasjon** er den svak. Kravene (ESPR) og reparasjonen gjelder bestemte typer plagg. Når klær er én gruppe med én levetid, blir effekten et gjennomsnitt over sokker og vinterjakker. Effekten av tiltakene er derfor et grovt anslag.
* For **suffisiens** mangler skillet mellom aktivt lager og dvalelager. Utleie og deling (L8) virker trolig mest på det som ikke brukes.
* Levetidene er konstante i historikken. Det betyr at fallet i bruk per plagg, som litteraturen beskriver for perioden med rask mote, ikke er med. Det kan bidra til avviket mellom restleddet og lagermodellen.

## Mulige forbedringer, med nytte og kostnad

| Forbedring | Nytte | Data | Kostnad |
|---|---|---|---|
| **Del klær i 2–3 grupper** (for eksempel undertøy og sokker, trikotasje og hverdagsklær, ytterklær) | Gjør holdbarhet og reparasjon mer meningsfulle. Tilførselen finnes per HS-kode | Levetider per type: Laitala & Klepp (garderobestudier), WRAP, Napolano SM4 | Middels. Krever nye produkter i registeret, eller en undergruppe bare i lagermodellen |
| **Aktivt lager og dvalelager** | Kobler direkte til garderobedata og suffisiens (L8) | WRAP, Vermeyen 2025 (22 % dvale), OsloMet | Middels. To lagre per produkt, med overgang fra aktivt til dvale |
| **Trend i levetid i historikken** (som strukturkjøring) | Tester om kortere levetid etter 2000 forklarer noe av avviket i lageret | Litteratur om bruk per plagg (kvalitativ) | Lav. `cohort_factor` finnes allerede |
| Formparameter som usikker faktor (1,5–3) | Er allerede testet i A5 (strukturkjøring) | – | Gjort |
| Levetid etter fiber | Liten nytte uten data | Mangler | Ikke anbefalt nå |

**Anbefaling:** Den beste neste forbedringen er å dele klær i 2–3 grupper. Det gjør L3 og L7 mer realistiske, og tilførselsdataene finnes. Deretter kan aktivt lager og dvalelager knyttes til garderobedataene fra OsloMet når de kommer. En trend i levetiden i historikken er billig å teste som strukturkjøring.
