# Fase D, trinn 2: scenarier for referansebanen (forslag)

*Notat 2026-11-05. Bygger på [designnotatet](2026-11-02_D_fremtidsmodul_design.md) (XLRM, latin hypercube, flate spenn), [Weijenberg m.fl. 2026](2026-11-02_Weijenberg_robust_tiltaksvurdering.md), [trinn 1](2026-11-05_D1_referansebane.md) og D42. Ingenting er implementert.*

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
