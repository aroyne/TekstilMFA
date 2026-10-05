# PLAN – TekstilMFA

*Levende dokument, oppdateres fortløpende. Sist oppdatert: 2026-10-05.*
System: [SYSTEMDEFINISJON.md](SYSTEMDEFINISJON.md) · Metode: [METODE.md](METODE.md) · Data: [../DATA_SOURCES.md](../DATA_SOURCES.md)

**Mål:** En dynamisk, probabilistisk MFA for tekstiler i Norge 1990–2025. Den skal identifisere pools, subpools, flyter og lagre, kvantifisere dem med data og parametre, beregne tidsutviklingen med Monte Carlo og dokumentere hver flyt slik det er gjort i NitrogenBudsjett.

---

## Gjort

### 2026-09-29 – Oppsett
- [x] Gikk gjennom NitrogenBudsjett (struktur, MC-motor, parameterformat, dokumentasjon per flyt) og tilpasset til tekstil.
- [x] Systemregister: 18 prosesser ([system/processes.csv](../system/processes.csv)) og 40 flyter med prioritet, metode og kandidatdata ([system/flows.csv](../system/flows.csv)).
- [x] Parametermaler med samme kolonner som `N_parameters.xlsx`: globale parametre, tidsavhengige ankerpunkter, levetider, datasettusikkerhet, fibersammensetning og HS-mapping.
- [x] Kjernekode: MC-trekking (portert fra NitrogenBudsjett), dynamisk lagermodell, parameterlaster, datalaster og MC-driver.
- [x] Første flyter fra ende til ende: import og eksport av ferdigvarer per produktgruppe fra SSB 08801, 1988–2024, med MC.
- [x] Tester: massebalanse og stasjonær tilstand i lagermodellen, og konsistens i systemregisteret (6 bestått).
- [x] Første kontroll: netto import 2022 (CL+HT+FW) ≈ 94,7 kt mot NORSUS 105,9 kt satt på markedet.

### 2026-09-29 – D1: OT tas med
- [x] OT (HS 57, 6305–6308) er i omfanget: hs_mapping, import- og eksportflyter, levetider (US.HH og US.IC), ikke-tekstilandel og fibersammensetning.
- [x] Import av OT: ca. 23 kt (2000) → 48 kt (2022) → 44 kt (2024). Tepper ca. 16 kt, sekker ca. 15 kt, presenninger og telt ca. 8 kt og andre konfeksjonerte varer ca. 10 kt i 2022. 6307 øker i 2020–21 (munnbind).
- [x] OT er delt i CA (tepper, 57), SA (sekker, 6305), TA (presenninger og telt, 6306) og OM (andre konfeksjonerte varer, 6307–6308), med egne levetider, ikke-tekstilandeler og fiberrader. Import 2022: CA 15,7, SA 14,5, OM 10,0 og TA 8,1 kt.
- [x] Ferdige tekniske varer i HS 56/59 er besluttet holdt utenfor.
- [x] Sekker (SA) behandles som emballasje (D13): levetiden `immediate` er lagt til i lagermodellen (med test), og PP-kolonnen er lagt til i fibersammensetningen.
- [x] D2 er besluttet: rapportering 1990–2024, innstrøm før 1988 settes til 1988-nivået (alternativt en trend), og startlageret testes i en følsomhetsanalyse.
- [x] D3 er besluttet: MA (MA.FI og MA.TX) modelleres som enkel balanse med prioritet 2.
- [x] D4 er besluttet: Produktmasse (nettovekt) er primær enhet, tekstilmasse beregnes via `nontextile_share_*`, og fiberlaget kommer i fase 3.
- [x] D5 er besluttet: Produktgruppe er en egen kolonne (`product`) i resultatene.
- [x] D6 er besluttet: Eksport av ferdigvarer føres fra DI.RT. En andel flyttes til MA.TX når norsk produksjon er kvantifisert.
- [x] D7 er besluttet: Privatimport regnes om fra NOK til kg med enhetsverdier fra 08801. Direkte netthandel får stor usikkerhet med brudd i 2020 (VOEC).
- [x] D8 er besluttet: Offisiell avfallsstatistikk er hovedkilden for kasseringer, og lagerendringen i bruk er restleddet. Lagermodellen kjøres parallelt og brukes til sammenligning og diskusjon.
- [x] D9 er besluttet: Uformell ombruk inngår i levetiden i US.HH og er ikke en egen flyt.
- [x] D10 er besluttet: Dvalende lager ligger i US.HH, og levetiden inkluderer lagringstid.
- [x] D11 er besluttet: Forbrenning i Norge er et sluk. Forbrenning i utlandet er en RW-flyt (eksportert restavfall × tekstilandel).
- [x] D12 er besluttet: Scenarier venter til den historiske modellen er ferdig.
- [ ] Sjekke hvordan kasserte sekker registreres i avfallsstatistikken (plastemballasje eller tekstil), før validering.

### 2026-10-05 – Lag for tekstilform og materiale, flodym-prototype
- [x] Forslag til to nye lag ([notat](../claude_tekst/2026-10-05_lag_tekstilform_og_materiale.md)): tekstilform som kolonne i `flows.csv` (D18) og fiber som lag beregnet etter TOT (D19). Ikke besluttet.
- [x] Vurdert åpne MFA-pakker: flodym (PIK, MIT) passer best. Den har dimensjoner per flyt, årgangslager og balanse per felles dimensjon, men ikke MC.
- [x] Hovedfiber per HS8-kode fra varetekstene i 08801 (`scripts/build_hs_main_fibre.py` → `parameters/hs_main_fibre.csv`). Klær 2025: 40 % bomull og 33 % kjemiske fibre (NORSUS 2026: 41 % og 32 %).
- [x] Prototype av fiberlaget med flodym (`prototype/fibre_layer_flodym.py`) for CL+HT+FW i husholdningene. Massebalansen holder. Årgangseffekten på kasseringene er liten (≤ 3 prosentpoeng) og forklarer ikke 44 % syntetisk hos Syversen 2023. Mest sannsynlig skjuler det seg syntetiske fibre i restposter og koder uten fiber (ca. 35 %).

### 2026-10-05 – Overgang til flodym
- [x] Systemet bygges fra registeret i flodym (`calculations/system.py`). `flows.csv` har fått `dims` og `processes.csv` har fått `stock_dims`. Produktgruppe `g` (CORE, CA, SA, TA, OM) erstatter etikettene `CORE` og `ALL` etter bruk.
- [x] Alle poolene er skrevet om til å fylle flodym-flyter. Radstrukturen med `comment` og `data_sources`, `flow_by_year` og `calculations/balances.py` er fjernet. flodym sjekker NaN, negative flyter og massebalanse i hver iterasjon.
- [x] Handelsdata summeres én gang før MC-løkka. 1 000 iterasjoner tar 6 s (før: ca. 7 min).
- [x] Resultatene er identiske med modellen før overgangen (avvik ≤ 10⁻¹³, deterministisk og MC med samme frø). `MC_summary.csv` og figuren er laget på nytt med 1 000 iterasjoner.
- [x] Nye tester: systemet lukkes, en flyt uten verdi gir feil, ubalanse gir feil, og lagerendringen i US.HH er tilført minus kassert (15 tester).

## Neste

### Fase 1 – Låse systemdefinisjonen (beslutningene D1–D13 er tatt 2026-09-29)
- [x] Litteraturgjennomgang ([notat](../claude_tekst/2026-09-29_litteraturgjennomgang_tekstil-MFA.md)): norske kartlegginger, nasjonale MFA-er (DK, SE, FI, NL, UK, CH), dynamiske og probabilistiske MFA-er (EU DPMFA 2024, Kina, Abbasi 2023 for norsk plast) og levetidsstudier (Laitala & Klepp). Nytt ankerår 2021 (Syversen m.fl. 2023). Ingen norsk tekstil-MFA har tidsserier.
- [ ] Lese i fulltekst: Napolano m.fl. 2024, Kawecki m.fl. 2021 og Laitala & Klepp 2020 (levetidsparametre).
- [x] Datainventar for P1-flytene ([notat](../claude_tekst/2026-09-29_datainventar_P1-flyter.md)). Handelsflytene er ferdige for 1988–2025. Kasseringene har ankerpunkter 2018, 2022 og 2025.
- [x] Bruddet i SSBs avfallsregnskap i 2012 er bekreftet i SSBs dokumentasjon: blandet avfall ble en egen materialtype, og før 2012 ble noen materialer beregnet med varetilførsel og levetid. SSBs tekstilregnskap 1990–1998 gir ankerår 1991 og 1998. Forslag til kildekjede står i datainventaren.
- [x] D15 er besluttet: kildekjede for tekstiler i restavfall og behandlingsmåte (se SYSTEMDEFINISJON).
- [ ] Spørre SSB om «Tekstiler» i 05281 (1995–2011) ble beregnet med varetilførselsmetoden (nivået kan være modellbasert).
- [x] Grensehandel: SSB 05678 (2004–2022) og 14221 (klær og sko 2023–2025). Flyten er liten (≈ 0,2–0,5 kt per år). Metode foreslått i [notat](../claude_tekst/2026-09-29_grensehandel_og_innsamling_for_2018.md).
- [x] Innsamling før 2018: eksport av 6309+6310 fra 08801 ÷ eksportandel (ankerpunkter). Serien stemmer med innsamlingen i 2018, 2022 og 2025.
- [x] D16 og D17 er besluttet: metodene for grensehandel og for innsamling før 2018 er godkjent.
- [x] **Første steg for D7:** Lavverdisendinger er undersøkt ([notat](../claude_tekst/2026-09-29_lavverdisendinger_VOEC_og_klesimport.md)). De er ikke med under HS-kodene i noe år. SSB har egne koder (99.60.x) fra 2023. Tekstiler via VOEC (Tolletaten, via NORSUS 2026) var 0,5 / 4,8 / 3,8 / 14,0 kt i 2022–2025. Fallet i klesimport kom i 2023 (mest fra Kina, færre plagg), og VOEC forklarer omtrent en tredjedel av det.
- [x] Kontroll mot Watson m.fl. (2020): Netto import CL+HT 2018 er 74,0 kt, mot 74,3 kt satt på markedet der.
- [x] NORSUS 2026 (OR.18.26) er gjennomgått. Brutto import stemmer med våre tall (≈ 2 kt lavere i alle år). Ankerår 2025 for kasseringer er hentet ut.
- [x] NORSUS 2023 (OR.07.23) er hentet. Ankeråret 2022 er lagt inn, og alle ankerårene (1991, 1998, 2018, 2022, 2025) er samlet i datainventaren.
- [ ] Spørre SSB om de detaljerte tabellene i tekstilregnskapet 1990–1998 (kan tas sammen med spørsmålet om 05281).
- [x] Klesandelen i 99.60.1000 er verifisert: 23,6 % av **verdien** i 2024 (SSB). Varelinjene var utelatt før mai 2025. Det gir ca. 3,5 mrd NOK, som tilsvarer ca. 7 kt med gjennomsnittlig NOK/kg for klær. Prisen per kg for små varelinjer er ukjent. Lagt inn som forslag til parameter `lowvalue_undercoverage_CL` (status `proposal`).
- [x] D14 er besluttet: Underdekningen for varelinjer under 1 000 kr holdes utenfor hovedresultatet. Den brukes som diskusjonspunkt og i følsomhetsanalyse.
- [x] 08801 er oppdatert med 2023–2025 fra SSB API (`scripts/update_trade_ssb_api.py`). 2023 er uendret og 2024 marginalt revidert. Modellperioden er utvidet til 2025.
  - Brutto import CL+HT+FW 2025: 85,7 kt (NORSUS 87,5 kt, samme avstand på ca. 2 kt som i 2022–2024).
  - Eksport av brukte tekstiler (6309+6310) 2025: 34,33 kt, nøyaktig det samme som NORSUS (34 331 t).

### Fase 2 – Kjerneflyter (P1)
- [x] 2026-09-29: Alle 13 P1-flyter er implementert og kjører i MC for 1988–2025, med massebalansesjekk i hver iterasjon. Nye moduler: `co_mc`, `us_mc`, `wm_mc`, `timeseries`, `balances`. Ankerpunkter ligger i `data_files/anchor_values.csv` og `parameters/time_dependent_parameters.csv`. 11 tester.
- [x] P2: Eksport av restavfall til forbrenning i utlandet (D11) med eksportandel fra SSB 13035 (KOSTRA, 2015–2025).
- [ ] **Åpne spørsmål (A1–D3) i [claude_tekst/2026-09-29_sporsmal_fase2.md](../claude_tekst/2026-09-29_sporsmal_fase2.md).** Viktigst: restavfall før 2018 (A1), 2018-ankeret for netthandel (A2) og formelen for innsamling (A3).
- [ ] Privatimport og direkte netthandel (D7).
- [ ] DI.RT-balanse, som gir salg til husholdninger.
- [ ] Kasseringer fra offisiell statistikk: innsamling, restavfall, deponi og forbrenning, eksport av usortert. Hull interpoleres mellom ankerpunkter.
- [ ] Lager i bruk (US.HH, US.IC) som akkumulert restledd fra startlageret.
- [ ] Parallell lagermodell per produktgruppe (innsvinging og levetider), og sammenligning per år med restleddet og kasseringene. Dette er diskusjonsgrunnlaget.
- [ ] CO-balanser (sortering, bruktbutikk og tilbake til US.HH).
- [ ] Validering: 2022 mot NORSUS, lager per innbygger mot garderobestudier, kg per plagg over tid fra 08801.

### Fase 3 – P2- og P3-flyter
- [ ] MA (norsk ull, produksjon), US.IC, sorteringsdetaljer, avfallseksport, materialgjenvinning.
- [ ] Mikrofibre: vask → avløpsrensing → vann og jord.
- [ ] Fiberlag: Ta stilling til D18, D19 og flodym (se notat 2026-10-05). Hovedfiber fra HS er ferdig, og prototypen kjører.
- [ ] Fiberlag: Matrise for restposter og koder uten fiber (RES/UNK) per produkt, fra plukkanalyser med fibersortering eller JRC. Sko trenger egen behandling.
- [ ] Fiberlag: Sammensetningsmatrise hovedfiber → fiberandeler (et «bomullsplagg» er ikke 100 % bomull).
- [x] D20 er besluttet: Flyter er summer per kalenderår, lageret er nivået ved årsslutt, og innstrømmen regnes som om den kom midt i året (flodym-standard).
- [x] MC med flodym er testet (se notatet). Ett system per iterasjon tar 5 ms. Full vektorisering sprenger minnet, men en levetidsmodell over (år, iterasjon, produkt) fungerer. Flaskehalsen er dagens pooler (400 ms per iterasjon), fordi 08801 summeres på nytt i hver iterasjon.
- [x] Handelsdataene (08801) summeres én gang før MC-løkka.
- [ ] Flytte fiberlaget fra `prototype/` inn i modellen som dimensjon `m` (etter beslutning om D19).
- [ ] Erstatte `calculations/stock_model.py` med flodyms `InflowDrivenDSM` for den parallelle lagermodellen (D20). Den egne modellen brukes nå bare i testene og er død kode.

### Fase 4 – Usikkerhet
- [ ] Pedigree-basert usikkerhet for alle datasett og parametre.
- [ ] Lagre MC-trekk og gjøre følsomhetsanalyse (Spearman).
- [ ] Konvergenstest og innsvingingstest (D2).

### Fase 5 – Resultater og dokumentasjon
- [ ] `utils_stat.py`: balanseplott per pool/subpool, tidsserier per flyt, Sankey med årsglider og lagerkurver.
- [ ] `report_generator.py`: GitHub Pages (just-the-docs), med pool-, subpool- og flytsider generert fra `system/*.csv`, `<!-- MANUAL:... -->`-blokker og `library.bib`. Pool-mappene (`rest_of_the_world_pool/` osv.) opprettes av generatoren.
- [ ] Metodebeskrivelse per flyt.

### Fase 6 (valgfritt) – Scenarier
- [ ] Framskriving 2025–2035 med produsentansvar, innsamlingsmål og tiltak mot fast fashion (D12).

## Løse tråder
- `sampling.py`: For `uncertainty_type == 'abs'` bruker NitrogenBudsjett `(low + upp)/2/1.96` som standardavvik. Her er det rettet til `(upp − low)/2/1.96`. I NitrogenBudsjett gjelder det bare waste_fractions hazardous, metal og common_sludge (normal/lognormal med abs-grenser). Der er nedre grense ≈ 0, så de to formlene gir nesten samme resultat. Det er en formelfeil med ubetydelig effekt i dag, men den bør rettes i NitrogenBudsjett.
- `sampling.py`: Reserven `cv = 0.1` for lognormal når verdien er 0 er fjernet (koden skal krasje høylytt).
