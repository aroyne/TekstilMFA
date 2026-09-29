# PLAN – TekstilMFA

*Levende dokument, oppdateres fortløpende. Sist oppdatert: 2026-09-29.*
System: [SYSTEMDEFINISJON.md](SYSTEMDEFINISJON.md) · Metode: [METODE.md](METODE.md) · Data: [../DATA_SOURCES.md](../DATA_SOURCES.md)

**Mål:** En dynamisk, probabilistisk MFA for tekstiler i Norge 1990–2024. Den skal identifisere pools, subpools, flyter og lagre, kvantifisere dem med data og parametre, beregne tidsutviklingen med Monte Carlo og dokumentere hver flyt slik det er gjort i NitrogenBudsjett.

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
- [ ] Sjekke hvordan kasserte sekker registreres i avfallsstatistikken (plastemballasje eller tekstil), før validering.

## Neste

### Fase 1 – Låse systemdefinisjonen
- [ ] Ta beslutningene D1–D12 i [SYSTEMDEFINISJON.md](SYSTEMDEFINISJON.md).
- [ ] Litteraturgjennomgang av eksisterende tekstil-MFA-er: nordiske (Tojo 2012, Palm 2014, Watson 2016), NORSUS 2023, svenske og danske nasjonale tekstilflyter, JRC og EEA. Notér systemgrenser og tall til sammenligning (`claude_tekst/`).
- [ ] Lage en datainventar per P1-flyt: hvilke år som er dekket, hvilke kilder, og hvor hullene er.
- [ ] Sjekke om 08801 dekker lavverdiforsendelser før og etter VOEC (2020). Nedgangen i klesimport 2022→2024 (64 → 54 kt) må forklares.

### Fase 2 – Kjerneflyter (P1)
- [ ] Privatimport og direkte netthandel (D7).
- [ ] DI.RT-balanse, som gir salg til husholdninger.
- [ ] Lagermodell for US.HH per produktgruppe, med innsvinging og levetidsparametre.
- [ ] Innsamling (ankerpunkter), restavfall, deponi og forbrenning, eksport av usortert.
- [ ] CO-balanser (sortering, bruktbutikk og tilbake til US.HH).
- [ ] Validering: 2022 mot NORSUS, lager per innbygger mot garderobestudier, kg per plagg over tid fra 08801.

### Fase 3 – P2- og P3-flyter
- [ ] MA (norsk ull, produksjon), US.IC, sorteringsdetaljer, avfallseksport, materialgjenvinning.
- [ ] Mikrofibre: vask → avløpsrensing → vann og jord.
- [ ] Fiberlag (HS6-hovedfiber + sammensetningsmatrise).

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
