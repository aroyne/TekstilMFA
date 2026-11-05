# Fase D, trinn 2: scenarier for referansebanen (forslag)

*Notat 2026-11-05.* **Besluttet og implementert samme dag**, se resultatene til slutt.

*Bygger på [designnotatet](2026-11-02_D_fremtidsmodul_design.md) (XLRM, latin hypercube, flate spenn), [Weijenberg m.fl. 2026](2026-11-02_Weijenberg_robust_tiltaksvurdering.md), [trinn 1](2026-11-05_D1_referansebane.md) og D42.*

## Hva trinn 2 skal gi

* Et utfallsrom for referansebanen (ingen nye tiltak) i 2026–2050. Fremtiden har dyp usikkerhet, så det blir **spenn over plausible verdier, ikke sannsynligheter**. Vifta tolkes som «hva som er mulig», ikke som et 95 %-intervall.
* **Hvilke usikre faktorer (X) som styrer hvert mål (M).** Dette er sårbarhetsanalysen, og den prioriterer både datainnhenting og trinn 3.
* Et oppsett der tiltakene (L) i trinn 3 kjøres i de samme scenariene, så tilfredsstillelse, anger og feilrate kan regnes direkte.

## Usikre faktorer (X)

Hver faktor trekkes flatt innenfor spennet, med latin hypercube. Faktorer som endrer seg over tid, går lineært fra 2025-verdien til målverdien i 2035 og holdes der. Det er en enkel og gjennomsiktig form for en «bane».

| # | Faktor | Spenn | Begrunnelse | Hvor i modellen |
|---|---|---|---|---|
| X1 | Befolkning | LLL – MMM – HHH (kontinuerlig: −1 = LLL, 0 = MMM, +1 = HHH) | SSB 14740. 5,50–6,91 mill. i 2050 | `Reference.population` |
| X2 | Forbruk per innbygger, CL+HT+FW+YA | −3 til +2 % per år | Designnotatet. Klær har vært omtrent flate siden 2005, med topp i 2011 og fall i 2023 | `_per_capita_flows` (CORE-produkter) |
| X3 | Forbruk per innbygger, andre varer (CA, SA, TA, OM) | −2 til +2 % per år | Ingen trend i dataene etter 2010 | det samme (andre produkter) |
| X4 | Levetider i husholdningene | × 1,0 til × 1,75 for alle produkter (hele perioden, s regnes på nytt) | Spennet fra lagerdiagnosen (garderobedata 55–110 kg klær) | `lifetime_mean_US.HH_*` |
| X5 | Lagervekst i husholdningene (D42) | 0,3–1 kg per innbygger per år | D42 | `future_stock_growth_kg_per_capita` |
| X6 | Kasseringsnivå 2025 (historisk usikkerhet) | ×0,85 til ×1,15 på s | MC 2025: innsamling + restavfall 80 kt, summen av 95 %-grensene ca. 62–99 kt | `Reference.scale` |
| X7 | Innsamlingsgrad uten nye tiltak, i 2035 | 38–55 % (2025: 45 %) | MC-intervallet 2025 (38–55 %) og effekten av kravet om separat innsamling fra 2025, som er ukjent (de Sadeleer & Rubach 2026: 12,8 % mindre i restavfallet) | andelene i `_household_discards` |
| X8 | Andel av innsamlet som sorteres i Norge, i 2035 | 5–30 % (2025: 5,5 %) | Fallende priser i eksportmarkedet og nye sorteringsanlegg (NTG og andre), uten krav | CO.CO-andelene |
| X9 | Utfall av sortering i Norge: ombruk, gjenvinning, rester | avkuttet flat Dirichlet (ombruk 25–80 %, gjenvinning 2–40 %, rester 10–70 %) | I modellen 2025: ca. 37 % ombruk, 6 % gjenvinning og 57 % rester av det som sorteres i Norge (innsamlet i Norge + importerte brukte tekstiler). Weijenberg m.fl. 2026 | CO.SO-andelene |
| X10 | Kapasitet for materialgjenvinning, i 2035 | 0,4–5 kt (2025: 0,36 kt) | NTG og planlagte anlegg. Øvre grense er et skjønn | `HELD_FLOWS` (NTG) |
| X11 | Andel av restavfallet som forbrennes i utlandet | 5–25 % (2025: 11 %) | SSB 13035, 2015–2025: 10–16 % | WM.RS-andelene |
| X12 | Andel syntetisk i ny tilførsel, endring til 2035 | 0 til +10 prosentpoeng | Trenden 2010–2018 (+7 pp), som har flatet ut etter 2018 | `future_composition_data` (bare fiberlaget) |

Ikke med som egne X:
* **Direkte netthandel.** Den inngår i X2 og påvirker bare returer og grunnlaget for produsentansvaret, som begge er proporsjonale.
* **Returandel og destruksjon.** Destruksjonen er en del av trinn 3 (forbudet), og returene er små.
* **Fiberutslipp.** De påvirker ikke målene.

## Mål (M)

Rapporteres for 2030, 2035, 2040 og 2050:
1. Innsamlingsgrad, separat fra husholdningene (E2, med D42-flyten i nevneren).
2. Kasseringer fra husholdningene i alt (statistikk + D42-flyten).
3. Ombruk i Norge (salg av brukt i Norge).
4. Eksport av usortert, som andel av innsamlet.
5. Materialgjenvinning (NTG og eksport til gjenvinning).
6. Tekstiler til forbrenning (Norge + utlandet).
7. Grunnlaget for produsentansvaret (E1, netto).
8. Lager i husholdningene (restledd og lagermodell).
9. Andel syntetisk i det som kasseres (fiberlaget, hvis det tas med).

## Metode

* **Utvalg:** latin hypercube (`scipy.stats.qmc`) med 1 000 scenarier, ett trekk per X. Frøet er fast, så scenariene er de samme i trinn 3.
* **Kjøring:** Historikken kjøres én gang (iterasjon 0). Hvert scenario kjører fremtidssystemet med sine X. Med TOT tar ett scenario ca. 0,1–0,3 s, så 1 000 scenarier tar et par minutter. Fiberlaget kan regnes for alle scenariene, eller bare for et utvalg (se spørsmål 4).
* **Resultater:** `output_files/future_scenarios.csv` med én rad per scenario, X-verdiene og målene per år. Et vifteplott per mål med referansebanen (alle X på midtverdien), medianen og 5–95-persentilene over scenariene, merket som spenn og ikke sannsynlighet.
* **Sårbarhet:** Spearman-korrelasjon mellom hver X og hver M, som hos Weijenberg, og en enkel avgjørelse av hvilke X som gir de 10 % laveste innsamlingsgradene (scenario discovery, PRIM light). Variansbasert analyse (Sobol) er et alternativ, men krever flere kjøringer.
* **Kode:** `calculations/future_scenarios.py` (X → overstyringer i `Reference`) og `future_scenarios.py` (kjøring og tabell). Referansebanen fra trinn 1 er scenarioet med alle X på midtverdien. Den skal fortsatt være lik `future_reference.csv` (test).

## Spørsmål

1. **Faktorene og spennene:** Er listen X1–X12 riktig? Er det noe som mangler, eller noe som bør ut? Spesielt X7, innsamlingsgraden uten nye tiltak: Skal den kunne øke av seg selv etter kravet fra 2025, eller skal all økning komme fra tiltak i trinn 3?
2. **Historisk usikkerhet:** Skal den føres inn som to X-faktorer (X6 kasseringsnivå og X7 innsamlingsgrad, med spennet fra MC 2025), som anbefalt i D12? Alternativet er å trekke en historisk MC-iterasjon per scenario, noe som er tyngre.
3. **Befolkningen:** Kontinuerlig mellom LLL og HHH (anbefalt), eller tre diskrete alternativer?
4. **Fiberlaget i scenariene:** Med for alle (tregere, gir M9 og X12), bare for et utvalg på 100, eller bare TOT i trinn 2?
5. **Bane til 2035 og deretter flat:** Er det en grei forenkling for faktorene som endrer seg over tid? Alternativet er en egen trend helt til 2050.

## Beslutninger (2026-11-05)

1. Faktorene og spennene er godkjent, med to endringer:
   * **X4** er delt i to. X4 er levetidsnivået for CORE, × 1–1,75 for hele perioden. **X4b** er levetiden for nye årganger fra 2026, × 0,75–1,0 i 2035. Ultra fast fashion kan gi kortere levetider. Lengre levetider er holdbarhetstiltaket i trinn 3.
   * **X7** er bare usikkerheten i innsamlingsandelen i 2025 (38–55 %), og den holdes flat. **All økning kommer fra tiltak i trinn 3.**
2. Den historiske usikkerheten føres inn som egne faktorer (X6 og X7).
3. Befolkningen bruker SSBs tre baner, LLL, MMM og HHH, i hver sin tredjedel av scenariene.
4. Fiberlaget kjøres for alle scenariene. Det tar 0,06 s per scenario, så 1 000 scenarier tar ca. 64 s.
5. Faktorene som endrer seg over tid, går lineært til 2035 og holdes flate etter det. Forbrukstrenden (X2, X3) er en årlig endring som akkumuleres til 2035.

## Implementering

* `calculations/future.py`: `Scenario` (alle X eksplisitt). `Scenario.reference` fører 2025-verdiene videre og gir nøyaktig trinn 1 (test). Alle flytfunksjonene leser scenarioet.
* `calculations/future_scenarios.py`: utvalg (latin hypercube, frø 2027; X9 med forkastning på simplekset) og mål M1–M9.
* `future_scenarios.py`: Historikken kjøres én gang, deretter referansebanen og 1 000 scenarier. Resultatene ligger i `output_files/future_scenarios*.csv`. Plottet lages med `scripts/plot_future_scenarios.py` og ligger i `output_files/plots/future_scenarios.png`.
* `use_cohorts` har fått levetid per årgang (`cohort_factor`). flodym regner overlevelse per årgang, så det trengs ingen egen kode for det.

### Endringer i regler som scenariene avdekket
* **Oppstrøms:** Mellomflytene i MA (garn til MA.TX, eksport av metervare og produksjonsavfall) følger nå innenlandsk ferdigproduksjon, ikke bare folketallet. Ellers går fabrikkbalansen i minus når forbruket faller.
* **Resirkulert fiber spunnet i Norge** begrenses av kapasiteten (X10), av det som kommer inn til gjenvinning og av norsk spinning utover norsk ull. Det som er igjen, eksporteres til gjenvinning.
* **Fiberlaget i fremtiden:** Eksporten av fiber og garn får sammensetningen av det MA.FI tar inn, og eksporten av metervare sammensetningen av det MA.TX tar inn. Det finnes ingen handelsdata for fremtiden, og ellers kan et materiale gå i minus når resirkulert fiber erstatter import. Referansebanen får opptil 0,4 kt flyttet mellom materialer i de to flytene og i norskproduserte ferdigvarer. Totalene er uendret, og historikken er uendret.
* **D42-flyten blir 0** i 401 av 1 000 scenarier i noen år. Da er de skalerte kasseringene større enn tilførselen minus lagerveksten (høyt X6 eller kort X4b), og lageret vokser mindre enn X5. Det er et utfall, ikke en feil, og rapporteres som `stock_growth_shortfall_kt` (opptil 22 kt i 2035). Ingen andre flyter klippes.

## Resultater (1 000 scenarier, uten nye tiltak)

| Mål | Ref. 2035 | 5–95 % 2035 | Ref. 2050 | 5–95 % 2050 | Viktigste faktorer (Spearman 2050) |
|---|---|---|---|---|---|
| Innsamlingsgrad | 39 % | 32–52 % | 40 % | 32–50 % | X7 +0,74, X6 +0,55 |
| Kassert fra husholdningene (kt) | 92 | 74–112 | 96 | 69–124 | X2 +0,85, befolkning +0,54 |
| Ombruk i Norge (kt) | 2,0 | 1,8–8,4 | 2,2 | 1,8–8,6 | X8 +0,66, ombruksandel +0,66 |
| Andel eksportert usortert | 95 % | 71–94 % | 95 % | 71–94 % | X8 −1,00 |
| Materialgjenvinning (kt) | 0,37 | 0,5–4,2 | 0,38 | 0,5–4,3 | gjenvinningsandel +0,88, X8 +0,39 |
| Til forbrenning (kt) | 118 | 98–139 | 124 | 96–154 | befolkning +0,66, X2 +0,63 |
| Produsentansvar, netto (kt) | 101 | 75–121 | 106 | 74–135 | X2 +0,84, befolkning +0,56 |
| Lagerendring (kt/år) | 3,0 | −8,4–5,6 | 3,1 | 1,9–6,1 | X5 +0,85 |
| Andel syntetisk i kasseringer | 45,8 % | 46,0–47,5 % | 45,6 % | 45,7–50,1 % | X12 +1,00 |

Hovedpunkter:
* **Uten tiltak ligger innsamlingsgraden på ca. 40 % (32–50 %).** Det er lavere enn 45 % i 2025, fordi D42-flyten kommer med i nevneren. Spennet styres nesten bare av usikkerheten i 2025 (X6, X7), altså av hvor godt vi kjenner dagens kasseringer. Det samme gjelder måloppnåelsen for produsentansvaret, og det er et sterkt argument for kartleggingene i 2026–2028.
* **Mengdene (kasseringer, forbrenning, grunnlaget for produsentansvaret) styres av forbruket per innbygger og befolkningen**, ikke av levetidene. Det skyldes at kasseringene skaleres til 2025.
* **Ombruk og gjenvinning i Norge styres av sorteringen i Norge** (andelen som sorteres og utfallet). Uten krav eller tiltak er det i referansebanen ingen grunn til at de vokser. Spennet viser hva markedet alene kan gi.
* **Lagerendringen** ligger mellom −17 og +7 kt per år, mot 10–45 kt per år i historikken (restledd). Med høyt X6 eller kort X4b krymper lageret frem mot 2035.
* **Lagernivået** styres av X4, fordi startlageret (D2) avhenger av levetidene. Plottet viser derfor endringen.

Neste er trinn 3: tiltakene (produsentansvar med innsamlingsmål, krav om sortering før eksport, holdbarhet) kjørt i de samme 1 000 scenariene, med tilfredsstillelse, anger og feilrate.
