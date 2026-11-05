# PLAN – TekstilMFA

*Levende dokument, oppdateres fortløpende. Sist oppdatert: 2026-11-05.*

> **Her fortsetter vi (2026-11-05):** Fase D, trinn 1 og D42 er gjort. Referansebanen 2026–2050 har fiberlaget med, og lageret i husholdningene vokser med 0,5 kg per innbygger per år, mens resten av gapet går til en ny flyt for næringsavfall og grovavfall ([notat](../claude_tekst/2026-11-05_opphopning_hos_forbruker.md)). **Neste er trinn 2:** scenarier og robusthet (XLRM/EMA, latin hypercube over X). Fordelingen mellom lagervekst og næringsavfall er en av faktorene. Svar fra Mepex om sko og næringsavfall kan endre 2018-ankeret og flyten.
> **Påminnelse:** Usendte henvendelser (SSB, OsloMet, SNF, PostNord, Tolletaten) samles i [HENVENDELSER.md](HENVENDELSER.md). **Ingenting er sendt** per 2026-11-02.

System: [SYSTEMDEFINISJON.md](SYSTEMDEFINISJON.md) · Metode: [METODE.md](METODE.md) · Data: [../DATA_SOURCES.md](../DATA_SOURCES.md)

**Mål:** En dynamisk, probabilistisk MFA for tekstiler i Norge 1990–2025. Den skal identifisere pools, subpools, flyter og lagre, kvantifisere dem med data og parametre, beregne tidsutviklingen med Monte Carlo og dokumentere hver flyt slik det er gjort i NitrogenBudsjett. Deretter skal den forlenges med en fremtidsmodul som bygger på den kalibrerte lagermodellen, og brukes til å analysere foreslåtte tiltak for sirkulære tekstiler (beslutning 2026-11-02).

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

### 2026-10-05 – Litteraturgjennomgangen oppdatert
- [x] Zotero-utvalget (NFTA, tekstil, MFA, sirkulær økonomi; 176 referanser) er gått gjennom ([notat](../claude_tekst/2026-10-05_litteraturgjennomgang_oppdatert.md)). Napolano 2025 er lest i fulltekst. Nye parameterkilder: andel brukbart i restavfall (2022, 2025), feilmargin for plukkanalyser (±22,8 %), NT per tollposisjon for sko (Gottfridsson & Zhang 2015) og arbeidstøy ≈ 1,5 % av klærne (ECAP 2017).
- [x] Kildene som manglet (Kawecki 2021, Laitala & Klepp 2020, Laitala 2018, Napolano SM, PEFCR 2025, Huygens 2023, van Oorschot 2020) er lagt inn i Zotero og lest. Forslag til levetider, NT-andeler og ankerpunkter for brukbart i restavfall står i notatet (avsnitt 5.4).
- [ ] Ta stilling til parameterforslagene i avsnitt 5.4 i litteraturnotatet. Laitala m.fl. 2012 er lagt inn: Oslo 32 % (2010) og 23 % (2011), ankerpunkt 27,5 %.
- [ ] Vurdere `institutional_share` (12 %) per produkt.

### 2026-10-05 – D18 og D19 i modellen
- [x] D18: `form` på alle flyter. Restavfall fra husholdningene er delt i brukbart og utslitt, med ankerpunkter 2011, 2022 og 2025.
- [x] Parametre (status forslag, litteratur eller antakelse): levetider i US.HH (CL 6, HT 7, FW 4, CA 10, TA 4, OM 2 år; CL i US.IC 3 år), NT-andeler (CL 1,7 %, FW 80 %, PEFCR/Gottfridsson; HT, CA, TA, OM, SA er antakelser), `mmf_synthetic_share` 0,92, `fibre_composition.csv` fra `scripts/build_fibre_composition.py`.
- [x] D19: fiberlaget i `calculations/fibre_layer.py` (eget flodym-system med dimensjon `m`, årgangsmodell for CL+HT+FW, massebalanse per materiale). Utdata: `MC_summary_fibre.csv`. Syntetisk andel i kasserte tekstiler ca. 40–42 % (målt 38–44 %).
- [x] Død kode fjernet: `prototype/` og `calculations/stock_model.py` (erstattet av flodym, D20).
- [x] Levetidene trekkes nå i MC. Det endrer rekkefølgen av tilfeldige tall, så MC-tallene er ikke identiske med tidligere kjøringer med samme frø.

### 2026-10-12 – Gjennomgang flyt for flyt: PS.WO og MA.FI
- [x] Gjennomgangen går én subpool av gangen, i den rekkefølgen materialet går ([notat](../claude_tekst/2026-10-12_gjennomgang_MA.FI.md)).
- [x] Norsk råull fra Totalkalkylen (NIBIO), 1959–2026 (`data_files/NIBIO_totalkalkylen_ull.csv`).
- [x] Import og eksport av fiber og garn fra 08801. HS-mappingen skiller fiber og garn (FY), metervare (FA) og detaljgarn (YA).
- [x] D21: Detaljgarn (YA) går RW → DI.RT → US.HH og hører til CORE etter bruk. Levetiden på 8 år er en antakelse.
- [x] D22: HS 56 er utenfor, også som innsatsvare.
- [x] D23: Ny flyt for vaskesvinn MA.FI → WM.WW (form BYP), med periodesnitt fra `scripts/derive_wool_scouring_anchors.py` og svinnandel 0,33.
- [x] D24: Midlertidige lagre i MA.TX og WM.WW, slik at systemet lukker.
- [x] Garn til MA.TX som balanse (ca. 10 kt i 2018–2025, 6–8 kt av det syntetisk). MC-kjøring med N = 10, figurer og sider er oppdatert.
- [x] Ny flyt MA.FI → DI.RT for norsk spunnet håndstrikkegarn (SSB 10455, Prodcom 13.10.50.50, 0,6–1,0 kt). Datafil: `SSB_10455_prodcom_garn_tau_nett_2008_2025.csv`.
- [x] Eksport deklarert som karbonisert ull i 1996–2000 og 2002 er uvasket ull etter pris per kg. Den er regnet som uvasket, og ankerpunktet for 1996–2000 er rettet fra 3,7 til 2,2 kt. Usikkerheten er standardfeilen til periodesnittet.

### 2026-10-26 – Systemdiagram og B2B/B2C (D36)
- [x] Systemdiagrammet genereres fra registeret (`scripts/plot_system_diagram.py`): Mermaid i SYSTEMDEFINISJON med alle flytene, og PNG for en A4-side i portrett med flytene med prioritet 1 og 2.
- [x] D36: B2B og B2C holdes ikke adskilt i egne noder ([notat](../claude_tekst/2026-10-26_b2b_og_b2c.md)). Nedre grense for `institutional_share` er 4 % (Eurostat ext_tec05: 3–4 % av klærne importeres direkte av næring og offentlig sektor). Flyter med sekker vises med og uten sekker på flytsidene (`TOTAL_EXCL_SA` i MC_summary).
- [ ] Plukkanalyser av næringsavfall (tekstilandel) for US.IC → WM.RS: venter, årgangsmodellen (D29) beholdes foreløpig.

### 2026-11-02 – Posisjonering, kontrolldata, D37 og D38 (ingen modellendringer)
- [x] Vurdering av hva som er nytt sammenlignet med NORSUS 2026 ([notat](../claude_tekst/2026-11-02_nytt_mot_NORSUS.md)). Det sterkeste bidraget er gapet mellom det som settes på markedet og det som kasseres. Det meste av NORSUS' gap på 25 kt er gjeneksport (ca. 10 kt) og institusjoner (ca. 10 kt). Lageret i husholdningene står for ca. 10 kt. Forutsetningen er at lageravviket løses.
- [x] Litteratursøk om lagermodeller i tekstil-MFA ([notat](../claude_tekst/2026-11-02_litteratur_lagermodell_tekstil.md)): Napolano 2025 (EU), Zhou 2025 (Kina 1978–2022), WUR 2026 (NL, garderobelager), Millward-Hopkins 2023 (UK, restledd mot WRAP-garderober). Ingen avstemming over flere tiår mellom restledd, lagermodell og garderober er funnet.
- [x] Aktører per node fra Brønnøysundregistrene (`scripts/fetch_brreg_actors.py`, 19 117 enheter og regnskap for 2023–2025). SN2025-koder. API-et støtter ikke regnskap for ideelle organisasjoner (UFF m.fl.).
- [x] Næringstall fra SSB 1999–2024 og varehandelsindeksen 2000–2025 (`scripts/fetch_ssb_industry_series.py`) ([notat](../claude_tekst/2026-11-02_naeringstall_mot_modellen.md)). Produksjonsverdien gir 2–4 ganger importprisen per kg for massen i MA.TX → DI.RT, så den gir ikke grunnlag for å si at MA.TX er for høy. Varehandelsindeksen er en volumindeks deflatert med prisindeks, ikke masse, og kan ikke kontrollere massen.
- [x] Regnskapsdatabasen til SNF og NHH (1992–2024, næringskode per år) er kartlagt: regnskapsdatabasen@snf.no, SNF-rapport 02/26. Tilgang gis «primarily» til forhåndsdefinerte institusjoner.
- [x] D37 (forslag): Fiberutslippene er trolig ca. 10 ganger for høye (Mepex' 600 t er et anslag basert på laboratorieforsøk; Lant 2020 målte 114 ppm og 96 % naturfibre i ekte vask). Lo fra tørketrommel (ca. 0,1 kt) og støvsuget støv bør gå til WM.RS.
- [x] D38 (forslag): Returer fra direkte netthandel (returandel ca. 20 %, 5–50 %) og destruksjon av usolgte varer (median ca. 1 %, opp til EEA 4–9 %) mangler eller er minimumstall.
- [x] Tiltak for sirkularitet i Norge og EU, og hva MFA-en kan si om dem ([notat](../claude_tekst/2026-11-02_tiltak_sirkularitet_og_MFA.md)).

### 2026-11-02 – Fase A: usikkerhet, første runde (D39)
- [x] Plan for fase A ([notat](../claude_tekst/2026-11-02_PLAN_usikkerhet_fase_A.md)) og vurdering av Weijenberg m.fl. 2026 ([notat](../claude_tekst/2026-11-02_Weijenberg_robust_tiltaksvurdering.md)). Alle fire beslutninger er tatt.
- [x] A0: Én tilfallsstrøm per element (`item_rng`). Konvergenstest med to frø: medianene ligger 0,4 % fra hverandre og bredden 2–8 %. Seks ubrukte rader er fjernet fra parametertabellene (`lowvalue_undercoverage_CL` er beholdt for følsomhet, D14).
- [x] A1–A3 (D39): 95 %-intervall og fordelingsregelen fra NitrogenBudsjett. Kildetype per rad, flat fordeling for type 4, årlige trekk for 08801, grensehandel og totalkalkylen, egen faktor for klassifisering av handelsdata, og felles metodefaktor for ankerpunkter. Tabellene er konvertert med `claude_tekst/_convert_uncertainty_D39.py`. Handelsflytene går fra ±3,6 % til ±7 %, innsamlingen fra ±4 % til ±8 % og lageret i husholdningene 2025 fra ±53 % til ±56 %.
- [x] Bidragsanalyse (`uncertainty_contributions.py`, 485 kilder, ca. 80 s), vist på flytsidene. Hovedfunn:
  - Lageret i husholdningene (restledd): gap-støy i restavfallet (år uten anker, i praksis før 2009) 75–84 %, restavfallsankrene 11–14 %, institusjonsandelen 2–5 %. Usikkerheten i lageret er altså nesten bare at vi ikke vet restavfallet før 2009.
  - Lagerendringen: restavfallsankrene ca. 55 %, import av ferdigvarer (årlig og klassifisering) 15–25 %, institusjonsandelen 6–15 %, VOEC ca. 17 % i 2025.
  - Salg til husholdningene: institusjonsandelen ca. 40 %, import av ferdigvarer ca. 60 %.
  - Separat innsamling: eksport av brukte tekstiler (årlig og klassifisering) ca. 85 %, `retained_share_collected` ca. 16 %.
  - Lagermodellen: levetiden for klær ca. 66 % og hjemmetekstiler ca. 23 %.

### 2026-11-02 – D37 og D38 implementert
- [x] D37: Vask = 280 kg tøy per innbygger × folketall × 114 mg/kg (Lant 2020): 0,16 kt i 2025 (0,11–0,22), mot 1,56 kt med Mepex-kalibreringen. Naturfibre slipper ca. 20 ganger mer per kg, så ca. 3–4 % av utslippet er syntetisk. Nye flyter til WM.RS: lo fra tørketrommel (0,11 kt) og fibre i husstøv (0,12 kt). Luft og støv faller fra 1,4 til 0,06 kt.
- [x] D38: Ny flyt med returer fra direkte netthandel (3,2 kt i 2025, 1,0–7,1). Destruksjon av usolgte varer er lognormal med median 1,3 % (95 %-intervall 0,2–9 %) av klær, hjemmetekstiler og sko på markedet: 1,1 kt i 2025 (0,2–8,1), mot 0,3 kt. Lagermodellen får nye varer minus returer.
- [x] Effekt på lageret i husholdningene (restledd) 2025: 1 638 kt mot 1 591 kt. Lavere fiberutslipp løfter lageret mer enn returer og destruksjon trekker det ned.

### 2026-11-02 – Fase A avsluttet: skjøter, utfylte år og strukturkjøringer
- [x] A4: Nivåene i D30 følger `fill_uncertainties` i NitrogenBudsjett (95 %-grense 5 % + 2 % per år ved interpolasjon, 10 % + 5 % per år for verdier som holdes flatt, uten tak og uten avkutting). Ankerserier med skjøt mellom kilder har egne metodegrupper på hver side (deponiandelen, brukbart i restavfall). Lageret i husholdningene 2025 går fra 1 638 kt (389–2 265) til 1 617 kt (997–2 210), og intervallet rundt 2000 er ikke lenger negativt. Bidrag 2025: restavfallsankrene 37 %, restavfallet før 2009 33 %, institusjonsandelen 12 %.
- [x] D38: medianen for destruksjon økt til 1,3 % (geometrisk snitt av 0,2 og 9 %), etter ønske.
- [x] A5 og innsvingingstest (`structural_sensitivity.py`, `output_files/structural_sensitivity.csv`). Effekt på lageret i husholdningene 2025: destruksjon på EEA-nivå −176 kt, tilførsel før 1988 på 60 % −130 kt (konstant, startlageret), fiberutslipp på Mepex-nivå −86 kt, ingen returer +6 kt, Weibull-form 1,5 eller 3 ca. 0. Innsvingingen påvirker lagermodellen bare til ca. 2000 (kasseringer −19 kt i 1990, −1 kt i 2000).

### 2026-11-02 – Fase B (rest) og fase C: diagnose
- [x] Forslag for resten av fase B ([notat](../claude_tekst/2026-11-02_fase_B_resterende.md)): fjerne de tre planlagte flytene uten data, hente ext_tec05 for kap. 63 og 64, ta sekkespørsmålet med til SSB, la fiberandelene vente. Fire spørsmål venter på svar.
- [x] Lagerdiagnose ([notat](../claude_tekst/2026-11-02_C_lagerdiagnose.md)): Avviket på ca. 1 030 kt mellom restledd og lagermodell i 2025 kommer fra 1988–2008 (553 kt, restavfallet holdt flatt per innbygger mens innsamlingen vokser), 2009–2017 (330 kt, lavt anker for 2018) og 2018–2025 (131 kt, 10–27 kt per år). Levetidene styrer ikke kasseringene når tilførselen er flat, bare lagernivået (× 1–1,75 mot garderobeanslagene). Forslag D40: substitusjon før 2009 (−183 kt), vurdere 2018-ankeret, rapportere det vedvarende gapet som funn.
- [x] Rettelse: «110–140 kg klær etter SIFO» bygger på antatt 0,3–0,4 kg per plagg. Med importvekten (0,276 kg) blir det ca. 99 kg for voksne.

### 2026-11-02 – D40, D41 og resten av fase B
- [x] D40 (1): Restavfallet før 2009 får det som ennå ikke ble samlet inn. Lageret som restledd 2025: 1 433 kt (807–2 032), mot 1 617 kt. Restavfall med utslitte tekstiler i 1990: 56 kt, mot 47 kt.
- [x] D40 (2) vurdert, ikke endret: Ankeret for gjenvinningsstasjonene i 2018 (tre analyser) er trolig for lavt (NORSUS 2023 sier det selv). Med forholdet fra 2022–2025 blir ankrene 38,3 (2018) og 40,7 kt (2009), og lageret 218 kt lavere. **Besluttet og implementert samme dag.** Lageret som restledd 2025 er nå 1 220 kt (495–1 871), ca. 218 kg per innbygger. Bidrag til usikkerheten: restavfallsankrene 40 %, restavfallet før 2009 37 %, institusjonsandelen 9 %.
- [x] D40 (3, 4): Gapet i 2018–2025 rapporteres som funn. Garderobedata: 200–400 plagg per voksen (Haugrønning, OsloMet), 55–110 kg med importvekten per plagg. Lagermodellen gir 56 kg per innbygger. Vekt per plagg og tall for barn mangler. Neste steg er å spørre OsloMet.
- [x] D41: Matrise for fiberandeler i ferdigvarer (hovedfiber 0,89, Ward m.fl. 2013). Ull i innsamlet masse går fra 6,1 til 5,7 %.
- [x] B: De tre planlagte flytene uten data er fjernet (42 flyter). Ext_tec05 gir ingen ny nedre grense per produkt (D36). Spørsmål til SSB samles i [HENVENDELSER.md](HENVENDELSER.md).

### 2026-11-02 – Fase D besluttet, E1 og E2 gjort
- [x] Fase D: horisont 2050, fremtiden starter fra medianen i 2025 (historisk usikkerhet som egne faktorer), lagermodellen skaleres til statistikken i 2025, tiltak i rekkefølgen produsentansvar med innsamlingsmål, sortering før eksport, holdbarhet ([designnotat](../claude_tekst/2026-11-02_D_fremtidsmodul_design.md)).
- [x] E1 og E2 ([notat](../claude_tekst/2026-11-02_E1_E2_produsentansvar_og_innsamlingsgrad.md), `calculations/indicators.py`, `output_files/MC_indicators.csv`): grunnlaget for produsentansvaret etter vedlegg 1 i forskriftsforslaget er 104 kt brutto (95–113) og 95 kt netto (87–103) i 2025. Innsamlingsgraden fra husholdningene er 45 % (38–55) i 2025, 50 % i 2018 og 40 % i 2022.

### 2026-11-05 – Fase D, trinn 1: referansebane 2026–2050
- [x] Forslag og beslutninger ([notat](../claude_tekst/2026-11-05_D1_referansebane.md)): egen fremtidsmodul på samme register, start fra iterasjon 0, kg per innbygger fra 2025, gapet går til restlageret inntil videre, ingen nye regimer.
- [x] SSBs befolkningsframskriving 2026 (tabell 14740, MMM/LLL/HHH) i `data_files/SSB_14740_befolkningsframskriving_2026_2051.csv` (`scripts/fetch_population_projection.py`). 6,22 mill. i 2050 (MMM).
- [x] `calculations/future.py` og `main_future.py`. `make_system(years=...)` og `use_cohorts` tar nå vilkårlige år. Historikken er uendret (MC_summary identisk). Fire nye tester (29 i alt).
- [x] Fiberlaget forlenget til 2050: tilførselen beholder sammensetningen fra 2025, og lagermodellene får historikken per materiale. Fiberlaget for historikken er identisk med før.
- [x] Opphopning hos forbruker ([notat](../claude_tekst/2026-11-05_opphopning_hos_forbruker.md)): Danmark 2018 (Watson m.fl.) hadde et gap på 10 kt (1,8 kg per innbygger) og mener det meste er dataproblemer (grovavfall, videresalg), ikke lagervekst. Kandidater i Norge: sko i plukkanalysene, grovavfall og næringsavfall fra husholdningene, institusjonsandelen, privat utførsel.
- [x] D42: Sko lagt til 2018-ankeret (7,5 kt, 5–10). Restlageret i 2025 er 1 169 kt (440–1 816). Ny flyt for husholdningstekstiler i næringsavfall og grovavfall: 0 i hovedresultatet og 1 kg per innbygger i strukturkjøringen (−183 kt i lageret, innsamlingsgrad 41,9 %). I fremtiden vokser lageret med 0,5 kg per innbygger per år, og resten går til flyten (10–11 kt per år). Innstrømmene til WM.RS hentes nå fra registeret, og fremtidssystemet nullstilles før flytene settes.
- [x] Resultat (før D42): Kassert CL+HT+FW 80,6 kt (2025) → 85,6 kt (2050), innsamling 36 → 38 kt, netto grunnlag for produsentansvaret 95 → 106 kt. Restlageret 1 160 → 1 502 kt, lagermodellen 529 → 576 kt. Plott: `output_files/plots/future_reference.png`.

## Neste

### Veikart (besluttet 2026-11-02)

Prinsipper:
* **Data er fasit (D8 står).** Kasseringene kommer fra statistikken. Lagermodellen kalibreres ikke slik at den overstyrer data, og strømmer justeres ikke for å passe modellen.
* **Lagermodellen er et diagnoseverktøy.** Avvik mellom restleddet, lagermodellen og garderobedata brukes til å finne åpenbare problemer i hvordan inndata er valgt og behandlet (feil avgrensning, dobbelttelling, manglende strømmer, ankerpunkter som ikke er representative). Arbeidet er iterativt: diagnose → gjennomgang av inndata → ny kjøring. Det som endres, er valg og behandling av data, med kilde. Tallene justeres ikke mot modellen.
* **Usikkerheten følger prinsippene fra NitrogenBudsjett** ([plan for usikkerhetshåndtering](../../NitrogenBudsjett/claude_tekst/2026-10-14_PLAN_usikkerhetshaandtering.md)). Koden skrives her og deles ikke med nitrogenprosjektet.
* **Fremtidsmodulen bygges fra grunnen.** Nitrogenprosjektet har ingen modell for dette. Den bygger på den kalibrerte lagermodellen og eksplisitte antakelser.

Fasene A og B går parallelt. Bidragsanalysen i A brukes til å prioritere i B.

#### Fase A – Robust usikkerhet (prinsippene fra NitrogenBudsjett)
Detaljert plan med dagens oppsett, problemer (T1–T9), arbeidspakker A0–A5 og fire beslutninger: [notat 2026-11-02](../claude_tekst/2026-11-02_PLAN_usikkerhet_fase_A.md). **Fase A er ferdig** (D39, D30 revidert, `uncertainty_contributions.py`, `structural_sensitivity.py`). Videre arbeid med usikkerhet følger av diagnosen i fase C: restavfallet før 2009 og startlageret er de største kildene til usikkerhet i lageret.
1. Én tolkning av grensene. Anbefalt: alle grenser er 95 %-intervall, også for PERT (problem P1 i N-planen).
2. Usikkerhet per datasett og periode etter **hvordan tallet er laget**, ikke hvem som publiserer det: registrert eller tellet, utvalgsundersøkelse, modellbasert statistikk, ekspertanslag (en lett pedigree, AP3 og P9 i N-planen). Begrunnelse i en egen kolonne.
3. Systematisk og årlig del av datasettstøyen, og egne faktorer for uavhengige deler av samme datasett (AP2).
4. Usikkerhet i skjøter mellom datakilder (for eksempel 05281 → plukkanalyser, VOEC-bruddet, SN2002 → SN2007) og i utfylte år. Nivåene i D30 vurderes på nytt i samme runde.
5. Strukturusikkerhet (avgrensninger og metodevalg) som egne følsomhetskjøringer, ikke inne i MC.
6. Bidragsanalyse: hvilke kilder driver usikkerheten per flyt, i lageret, i innsamlingsgraden og i grunnlaget for produsentansvaret (som `uncertainty_contributions.py` og `aggregate_uncertainty.py` i N). Krever at trekkene lagres.
7. Konvergenstest og innsvingingstest (D2).

#### Fase B – Strømmer uten bestemt data eller metode
1. ~~D37: fiberutslipp, lo og husstøv~~ (gjort 2026-11-02).
2. ~~D38: returer og destruksjon~~ (gjort 2026-11-02).
3. ~~Planlagte flyter~~ (fjernet 2026-11-02).
4. ~~Parameterforslag og institusjonsandel per produkt~~ (levetidene flyttet til fase C, ext_tec05 vurdert 2026-11-02).
5. ~~Sekker~~ (lagt i HENVENDELSER.md).
6. ~~Fiberlaget~~ (D41, 2026-11-02). Ull er fortsatt ca. 7 % av tekstildelen mot 3 % målt.

#### Fase C – Lagermodellen som diagnose
1. ~~Oppdatere notatet om lagermodellen~~ (erstattet av [lagerdiagnosen](../claude_tekst/2026-11-02_C_lagerdiagnose.md) 2026-11-02).
2. Bryte ned avviket per periode og produkt. Følsomhet: restavfall før 2009, innsamling før 2018, MA.TX, D38 (EEA-nivå), startlageret.
3. Levetidene settes innenfor det litteraturen tillater, slik at lagermodellen treffer garderobedata (nivå) og statistikken der den er god (2018–2025). Der den ikke treffer, er det et diagnosefunn om inndata, ikke en grunn til å endre data.
4. Uavhengig kontroll av nivået: garderobestudier (SIFO/OsloMet, Laitala & Klepp), og WRAP og WUR som referanse.
5. Fiberspesifikke levetider (syntetisk lengre enn bomull), hvis diagnosen tilsier det.
6. Resultat: kalibrerte levetidsfordelinger med usikkerhet, og en liste over endringer i inndata med begrunnelse.

#### Fase D – Fremtidsmodul (D12)
0. Designnotat med fem spørsmål: [notat 2026-11-02](../claude_tekst/2026-11-02_D_fremtidsmodul_design.md).
1. ~~Utforming og referansebane 2026–2050~~ (gjort 2026-11-05, deterministisk). Åpent: hvor gapet (1 − s) går.
2. Usikkerhet i referansebanen som scenarier (trinn 2).
3. Regimeskifter som harde brudd: produsentansvar 2027, eksportregler 2027, destruksjonsforbud 2026.
4. Usikkerheten om framtiden er dyp: flate, vide plausible spenn og mange scenarier (EMA), ikke MC med fordelinger som for historikken. Avkuttet Dirichlet for koeffisienter med sum lik 1 ([Weijenberg m.fl. 2026](../claude_tekst/2026-11-02_Weijenberg_robust_tiltaksvurdering.md)).

#### Fase E – Tiltak
Rekkefølge fra [notatet om tiltak](../claude_tekst/2026-11-02_tiltak_sirkularitet_og_MFA.md):
1. ~~Grunnlaget for produsentansvaret med usikkerhet~~ (gjort 2026-11-02, E1).
2. ~~Innsamlingsgrad~~ (gjort 2026-11-02, E2). Etterkontroll av kravet fra 2025 krever kartlegginger i 2026–2028.
3. Scenarier for eksport og sortering.
4. Tiltak på tilførsel og levetid (avgift, rask mote, holdbarhet), med forsinkelse.

Metode: XLRM-struktur og robusthetsmål (tilfredsstillelse, anger, feilrate) etter Weijenberg m.fl. (2026). Tiltakseffekten begrunnes fra kilder og er selv en usikker faktor.

#### Fase F – Dokumentasjon og publisering
1. Artikkel om avstemmingen av lageret (restledd, lagermodell, garderober). Mulig etter fase C ([notat](../claude_tekst/2026-11-02_nytt_mot_NORSUS.md)).
2. `library.bib` og siteringer, og GitHub Pages.

#### Startes nå (lang ledetid)
Henvendelsene står samlet i [HENVENDELSER.md](HENVENDELSER.md).
* Spørre SSB om tekstiltallene i 05281 (1995–2011) og tekstilregnskapet 1990–1998 er beregnet ut fra tilførselen.
* Garderobedata fra SIFO/OsloMet (lagernivå i kg per innbygger).
* Søke tilgang til SNFs regnskapsdatabase (skille merkevarer fra produksjon i 14.x).
* EEA-rapporten om destruksjon og PostNords returtall (D38). Andel husholdninger med tørketrommel etter 2012 (D37). Plukkanalyser av næringsavfall (US.IC).

#### Eldre punkter
Punktene under fra fase 1–3 er beholdt som historikk. Åpne punkter der er tatt inn i fasene A–F over.

### Fase 1 – Låse systemdefinisjonen (beslutningene D1–D13 er tatt 2026-09-29)
- [x] Litteraturgjennomgang ([notat](../claude_tekst/2026-09-29_litteraturgjennomgang_tekstil-MFA.md)): norske kartlegginger, nasjonale MFA-er (DK, SE, FI, NL, UK, CH), dynamiske og probabilistiske MFA-er (EU DPMFA 2024, Kina, Abbasi 2023 for norsk plast) og levetidsstudier (Laitala & Klepp). Nytt ankerår 2021 (Syversen m.fl. 2023). Ingen norsk tekstil-MFA har tidsserier.
- [x] Lest i fulltekst 2026-10-05: Napolano m.fl. 2025, Kawecki m.fl. 2021 og Laitala & Klepp 2020 (se litteraturnotatet 2026-10-05).
- [x] Datainventar for P1-flytene ([notat](../claude_tekst/2026-09-29_datainventar_P1-flyter.md)). Handelsflytene er ferdige for 1988–2025. Kasseringene har ankerpunkter 2018, 2022 og 2025.
- [x] Bruddet i SSBs avfallsregnskap i 2012 er bekreftet i SSBs dokumentasjon: blandet avfall ble en egen materialtype, og før 2012 ble noen materialer beregnet med varetilførsel og levetid. SSBs tekstilregnskap 1990–1998 gir ankerår 1991 og 1998. Forslag til kildekjede står i datainventaren.
- [x] D15 er besluttet: kildekjede for tekstiler i restavfall og behandlingsmåte (se SYSTEMDEFINISJON).
- [ ] Spørre SSB om «Tekstiler» i 05281 (1995–2011) ble beregnet med varetilførselsmetoden (nivået kan være modellbasert). Samlet i [HENVENDELSER.md](HENVENDELSER.md).
- [x] Grensehandel: SSB 05678 (2004–2022) og 14221 (klær og sko 2023–2025). Flyten er liten (≈ 0,2–0,5 kt per år). Metode foreslått i [notat](../claude_tekst/2026-09-29_grensehandel_og_innsamling_for_2018.md).
- [x] Innsamling før 2018: eksport av 6309+6310 fra 08801 ÷ eksportandel (ankerpunkter). Serien stemmer med innsamlingen i 2018, 2022 og 2025.
- [x] D16 og D17 er besluttet: metodene for grensehandel og for innsamling før 2018 er godkjent.
- [x] **Første steg for D7:** Lavverdisendinger er undersøkt ([notat](../claude_tekst/2026-09-29_lavverdisendinger_VOEC_og_klesimport.md)). De er ikke med under HS-kodene i noe år. SSB har egne koder (99.60.x) fra 2023. Tekstiler via VOEC (Tolletaten, via NORSUS 2026) var 0,5 / 4,8 / 3,8 / 14,0 kt i 2022–2025. Fallet i klesimport kom i 2023 (mest fra Kina, færre plagg), og VOEC forklarer omtrent en tredjedel av det.
- [x] Kontroll mot Watson m.fl. (2020): Netto import CL+HT 2018 er 74,0 kt, mot 74,3 kt satt på markedet der.
- [x] NORSUS 2026 (OR.18.26) er gjennomgått. Brutto import stemmer med våre tall (≈ 2 kt lavere i alle år). Ankerår 2025 for kasseringer er hentet ut.
- [x] NORSUS 2023 (OR.07.23) er hentet. Ankeråret 2022 er lagt inn, og alle ankerårene (1991, 1998, 2018, 2022, 2025) er samlet i datainventaren.
- [ ] Spørre SSB om de detaljerte tabellene i tekstilregnskapet 1990–1998 (kan tas sammen med spørsmålet om 05281). Samlet i [HENVENDELSER.md](HENVENDELSER.md).
- [x] Klesandelen i 99.60.1000 er verifisert: 23,6 % av **verdien** i 2024 (SSB). Varelinjene var utelatt før mai 2025. Det gir ca. 3,5 mrd NOK, som tilsvarer ca. 7 kt med gjennomsnittlig NOK/kg for klær. Prisen per kg for små varelinjer er ukjent. Lagt inn som forslag til parameter `lowvalue_undercoverage_CL` (status `proposal`).
- [x] D14 er besluttet: Underdekningen for varelinjer under 1 000 kr holdes utenfor hovedresultatet. Den brukes som diskusjonspunkt og i følsomhetsanalyse.
- [x] 08801 er oppdatert med 2023–2025 fra SSB API (`scripts/update_trade_ssb_api.py`). 2023 er uendret og 2024 marginalt revidert. Modellperioden er utvidet til 2025.
  - Brutto import CL+HT+FW 2025: 85,7 kt (NORSUS 87,5 kt, samme avstand på ca. 2 kt som i 2022–2024).
  - Eksport av brukte tekstiler (6309+6310) 2025: 34,33 kt, nøyaktig det samme som NORSUS (34 331 t).

### Fase 2 – Kjerneflyter (P1)
- [x] 2026-09-29: Alle 13 P1-flyter er implementert og kjører i MC for 1988–2025, med massebalansesjekk i hver iterasjon. Nye moduler: `co_mc`, `us_mc`, `wm_mc`, `timeseries`, `balances`. Ankerpunkter ligger i `data_files/anchor_values.csv` og `parameters/time_dependent_parameters.csv`. 11 tester.
- [x] P2: Eksport av restavfall til forbrenning i utlandet (D11) med eksportandel fra SSB 13035 (KOSTRA, 2015–2025).
- [x] Åpne spørsmål (A1–D3) i [claude_tekst/2026-09-29_sporsmal_fase2.md](../claude_tekst/2026-09-29_sporsmal_fase2.md): A2 er løst med D28, A3 med D31, A4 med D33, B2 med D28 og D29, og C1–C2 med levetidene og startlageret. Spørsmålet til SSB om A1 står igjen (punkt 5 i listen over åpne tråder).
- [x] Privatimport og direkte netthandel (D7).
- [x] DI.RT-balanse, som gir salg til husholdninger.
- [x] Kasseringer fra offisiell statistikk: innsamling, restavfall, deponi og forbrenning, eksport av usortert. Hull interpoleres mellom ankerpunkter.
- [x] Lagerendring i bruk (US.HH, US.IC) som restledd. Lagernivået er akkumulert fra 0 i 1988. Startlageret (D2) mangler.
- [x] Parallell lagermodell per produktgruppe (innsvinging og levetider), og sammenligning per år med restleddet og kasseringene (se fase 3).
- [x] CO-balanser (sortering, bruktbutikk og tilbake til US.HH).
- [ ] Validering: 2022 mot NORSUS, lager per innbygger mot garderobestudier, kg per plagg over tid fra 08801.

### Fase 3 – P2- og P3-flyter
- [x] Høyfast filamentgarn (5402.10/11/19/20) er tatt ut som garn til tau og nett (D22).
- [x] Håndstrikkegarn 1988–89 fra SSBs varetall (NOS B 941, B 998: 0,99 og 0,89 kt), interpolert til Prodcom 2008.
- [x] Ny regel (CLAUDE.md): Negative flyter er ikke-fysiske og klippes til 0. Underskuddet tas opp av klippelagre i MA.FI, DI.RT og WM.RS («Clipping imbalance») og flyttes ikke til andre flyter. Hvor ofte og hvor mye det klippes, står på flytsidene. N = 1000: bare ull i garnet til MA.TX i fiberlaget klippes (1989: 2 av 1 000, maks 0,08 kt; 2000: 2 av 1 000, maks 0,03 kt).
- [x] MA.TX: import og eksport av metervare (08801) og produksjonsavfall (SSB 08604/14457) er implementert (D25). 5402.61, 5402.49 og 5503.40 er tatt ut (D22). Balansen i MA.TX er 8–11 kt i 2008–2025 og 18 kt i 1990 ([notat](../claude_tekst/2026-10-12_gjennomgang_MA.TX.md)).
- [x] D26 er besluttet: massebasert produktfordeling for MA.TX → DI.RT, og dyner og puter (9404.40/9404.90) er HT.
- [x] D26 er implementert (2026-10-13): HS 9404.40/9404.90 (dyner og hodeputer) er med i HT. Varetall for ferdigvarer i 1988–89 er lest, og Prodcom 2008–2011 er koblet til produkter (`scripts/derive_domestic_product_mass.py`). `MA.TX-DI.RT-Domestic finished products-TOT` er implementert, og MA.TX har klippelager i stedet for midlertidig lager.
- [x] Flytsidene har fått ny struktur (2026-10-13): manuell beskrivelse etter malen fra NitrogenBudsjett, med fem overskrifter (hva flyten omfatter, datakilder, antakelser, sammensetning, tidsutvikling), og genererte tabeller for sammensetning per varetype og materiale. Prøve: de 11 flytene inn til og ut av MA er skrevet.
- [x] Beskrivelser er skrevet for alle 29 implementerte flyter (2026-10-13). Nøkkeltallstabellen er fjernet, fordi plottet viser de samme verdiene. De 14 planlagte flytene får beskrivelse når de implementeres.
- [x] DI.RT er gjennomgått (D27, 2026-10-13): usolgte klær gitt til innsamlere og kastet er implementert og følger klesimporten. Donerte varer trekkes fra innsamlingen fra husholdningene. Andelen til institusjoner, gjeneksport og små varelinjer beholdes.
- [ ] Følsomhetsanalyse (fase 4): usolgte varer etter EEA (4–9 % av det som settes på markedet). Tas nå med D38.
- [x] US.HH er gjennomgått (D28, 2026-10-13): restavfall fast per innbygger før 2009, netthandel fra VOEC 2023–2025, årgangsmodell for tepper, presenninger og andre konfeksjonerte varer, fiberutslipp ved vask (Mepex 2014) og til luft (samme nivå). Lageret (restledd) er nå ca. 275 kg per innbygger i 2018–2025, mot 98–119 kg i lagermodellen og ca. 110–140 kg klær etter SIFOs garderobestudier.
- [x] US.IC (D29, 2026-10-13): kasseringer med årgangsmodell og levetider per varetype (arbeidsklær 3, vernesko 2, institusjonstekstiler 2, tepper 10, presenninger 5, andre 2 år; alle unntatt arbeidsklær er antakelser). Fiberutslipp fra industrivask med samme utslipp per kt som husholdningsvask (0,12–0,15 kt). Innsamling fra institusjoner står som planlagt.
- [x] D30 (2026-10-13): år uten publiserte tall får usikkerhet som vokser med avstanden til nærmeste tall (2 %/år mellom, 5 %/år utenfor, tak 100 %, ±2 sd). Medianene er uendret. CO.CO har fått klippelager.
- [x] CO.CO er gjennomgått (D31, 2026-10-14): metoden beholdes (eksporten er hovedserien), med begrunnelse på flytsidene.
- [x] CO.SO er gjennomgått (D32, 2026-10-14): import av brukte klær og filler er implementert. Eksport av sortert står som planlagt, og materialgjenvinning tas med WM.RC.
- [x] CO.RE og WM.RS er gjennomgått (D33, 2026-10-14): ingen endringer i beregningen, begrunnelser lagt inn på flytsidene.
- [x] WM.RC er gjennomgått (D34, 2026-10-14): gjenvinning fra sortering, institusjoner og produksjon, NTGs fiber til norsk spinning og eksport til gjenvinning er implementert.
- [x] WM.WW og EN (D35, 2026-10-14): WM.WW og EN.SO er fjernet, EN er systemgrense, og mikrofibre og vaskesvinn går ut av systemet til avløp og luft. Rensing og slam behandles ikke. Gjennomgangen flyt for flyt er dermed ferdig.
- [ ] **Til senere (fase 4):** se nærmere på nivåene i D30 (2 %/år, 5 %/år, tak 100 %). Lageret i husholdningene får 95 %-intervall fra under 0 til 290 kg per innbygger i 2005, og innsamlingen klippes i opptil 22 % av trekkene i 1988–1992. Mulig: lavere tak eller lavere økning per år utenfor dataene.
- [ ] Diskusjon: lageret i husholdningene er høyt. Mulige bidrag: restavfallet før 2009, balansen i MA.TX, møbelputer i HT, innsamlingen fra husholdningene, og destruksjon og returer (D38). Samlet i punkt 4 i listen over åpne tråder.
- [ ] Balansen i MA.TX beholdes inntil videre. *2026-11-02: Produksjonsverdien fra SSBs industristatistikk gir en pris per kg 2–4 ganger importprisen, så den gir ikke grunnlag for å si at MA.TX er for høy ([notat](../claude_tekst/2026-11-02_naeringstall_mot_modellen.md)). Forbeholdet er at merkevarer som produserer i utlandet, kan ligge i produksjonsverdien.* Det er kommentert i docstringen og på flytsiden at den ser for høy ut. Ferdigvarer fra MA.TX er 8–18 kt per år, og lageret i husholdningene øker fra ca. 135 til ca. 206 kg per innbygger (2018–2025). Trolig går en del av metervaren og garnet til produkter utenfor omfanget eller til andre næringer (møbeltrekk, madrasser, bil- og båtinteriør, tekniske formål). Prodcom og varetall gir 4–8 kt i store foretak. Se notatet om MA.TX.
- [x] Soveposer (9404.30, TA) og møbelputer (9404.90, HT, materiale NT) er med (2026-10-13). Lageret i husholdningene er da ca. 220 kg per innbygger i 2018–2025.
- [x] Gjennomgangen av DI.RT, US.HH, US.IC, CO.CO, CO.SO, CO.RE, WM.RS, WM.RC og WM.WW/EN er gjort (D27–D35). WM.WW er fjernet (D35).
- [x] US.IC, sortering, avfallseksport og materialgjenvinning (D29, D32–D34).
- [x] Mikrofibre: avløpsrensing, vann og jord behandles ikke (D35). Nivå og fordeling på fiber vurderes på nytt i D37.
- [x] Fiberlag: D18 og D19 er besluttet og implementert.
- [ ] Fiberlag: Matrise for restposter og koder uten fiber (RES/UNK) per produkt, fra plukkanalyser med fibersortering eller JRC. Sko trenger egen behandling.
- [ ] Fiberlag: Sammensetningsmatrise hovedfiber → fiberandeler (et «bomullsplagg» er ikke 100 % bomull).
- [x] D20 er besluttet: Flyter er summer per kalenderår, lageret er nivået ved årsslutt, og innstrømmen regnes som om den kom midt i året (flodym-standard).
- [x] MC med flodym er testet (se notatet). Ett system per iterasjon tar 5 ms. Full vektorisering sprenger minnet, men en levetidsmodell over (år, iterasjon, produkt) fungerer. Flaskehalsen er dagens pooler (400 ms per iterasjon), fordi 08801 summeres på nytt i hver iterasjon.
- [x] Handelsdataene (08801) summeres én gang før MC-løkka.
- [x] D19 er delvis besluttet: fem fibergrupper (SYN, CO, WO, CV, OTH). `fibre_composition.csv` har fått de samme kolonnene.
- [x] Andel SYN i HS-klassen MMF: `mmf_synthetic_share` = 0,92 (Textile Exchange 2024).
- [x] Fiberlaget er flyttet inn i modellen som dimensjon `m`.
- [x] `calculations/stock_model.py` er erstattet av flodyms `InflowDrivenDSM` (i fiberlaget).
- [x] Den parallelle lagermodellen rapporteres (utstrøm, lager, lagerendring) og er sammenlignet med statistikken ([notat](../claude_tekst/2026-10-05_lagermodell_mot_statistikk.md)). Anslagene var enige fra 2019. I 2008–2017 lå lagermodellen 20–25 kt over statistikken, og i 1988–2000 lå statistikken over tilførselen. *2026-11-02: utdatert. Etter D21–D28 ligger statistikken 12–40 kt under lagermodellen i alle år (2025: 81 mot 93 kt kassert).*
- [x] Ankerpunkt for restavfall 2009 (33,5 kt, Laitala m.fl. 2012). Avviket mot lagermodellen i 2005–2017 øker (51 mot 77 kt i 2009). Restavfallet forklarer det ikke.
- [x] Startlager i 1988 (D2) fra lagermodellen. Lagernivået rapporteres (`US.HH-US.HH-Stock-TOT`): ca. 120 kg per innbygger i 2018–2025, mot 84–96 kg i lagermodellen. *2026-11-02: nå ca. 275 kg (restledd) mot ca. 97 kg (lagermodell) i 2025.*
- [ ] Sammenligne lagernivået med garderobestudier (SIFO). Følsomhet: lengre levetider for CL i 2005–2015 (dvalelager).
- [ ] Fiberlag: fiberspesifikke levetider (syntetisk lengre enn bomull), matrise hovedfiber → fiberandeler, usikkerhet på `fibre_composition.csv`, og egen sammensetning for brukbart og utslitt i restavfall.
- [ ] Ull i kasseringer blir ca. 5 %, mot 3 % målt. Undersøk hvilke HS-koder som gir ull.

### Fase 4 – Usikkerhet (erstattet av fase A i veikartet)
- [ ] Pedigree-basert usikkerhet for alle datasett og parametre.
- [ ] Lagre MC-trekk og gjøre følsomhetsanalyse (Spearman).
- [ ] Konvergenstest og innsvingingstest (D2).

### Fase 5 – Resultater og dokumentasjon
- [x] `utils_stat.py`: balanseplott per pool og subpool, tidsserie per flyt (per produkt, 95 % for summen), materialsammensetning per flyt (2026-10-05).
- [x] `report_generator.py`: just-the-docs med 8 pool-, 18 subpool- og 41 flytsider, generert fra `system/*.csv`, resultatene og docstringene i koden. `MANUAL`-blokker bevares (2026-10-05).
- [x] Sankey-diagrammer (2026-10-14): nasjonalt på pool-nivå på forsiden og ett per pool med subpoolene, med årsglider, farge etter tekstilform eller materiale, og valg for å skjule import og eksport av ferdigvarer. Malen er hentet fra NitrogenBudsjett (`templates/sankey_template.html`), og dataene lages i `utils_stat.py`.
- [ ] `library.bib` og siteringer (`<!--cite:nøkkel-->`) som i NitrogenBudsjett.
- [ ] Skrive manuelle beskrivelser per flyt i `MANUAL`-blokkene.
- [ ] Slå på GitHub Pages for repoet (Settings → Pages, gren `main`, rotmappe) når grenen er merget.

### Fase 6 – Scenarier (erstattet av fase D og E i veikartet; ikke lenger valgfritt)
- [ ] Framskriving 2025–2035 med produsentansvar, innsamlingsmål og tiltak mot fast fashion (D12).

## Løse tråder
- `sampling.py`: For `uncertainty_type == 'abs'` bruker NitrogenBudsjett `(low + upp)/2/1.96` som standardavvik. Her er det rettet til `(upp − low)/2/1.96`. I NitrogenBudsjett gjelder det bare waste_fractions hazardous, metal og common_sludge (normal/lognormal med abs-grenser). Der er nedre grense ≈ 0, så de to formlene gir nesten samme resultat. Det er en formelfeil med ubetydelig effekt i dag, men den bør rettes i NitrogenBudsjett.
- `sampling.py`: Reserven `cv = 0.1` for lognormal når verdien er 0 er fjernet (koden skal krasje høylytt).
