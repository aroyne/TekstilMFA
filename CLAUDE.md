# Claude-instruks: TekstilMFA

Prosjektet bygger på arbeidsmetodikken i `../NitrogenBudsjett`. Konvensjonene under er hentet derfra og gjelder også her, men uten kravene som bare fantes på grunn av den offisielle rapporteringsfilen i N-budsjettet.

## Dokumenter
- Planlegging og metodenotater skrives på norsk: `docs/PLAN.md`, `docs/SYSTEMDEFINISJON.md`, `docs/METODE.md`, `DATA_SOURCES.md`. Oppdater `docs/PLAN.md` (Gjort/Neste) når en arbeidsøkt avsluttes.
- Analyser og notater Claude skriver på forespørsel legges i `claude_tekst/` med datoprefiks (`ÅÅÅÅ-MM-DD_tema.md`).
- Systemet defineres i `system/processes.csv` og `system/flows.csv`. Endres systemet, oppdateres disse først, og deretter `docs/SYSTEMDEFINISJON.md`. `tests/test_system_register.py` skal fortsatt gå gjennom.

## Kode
- **Kommentarer skrives på engelsk.** De forklarer koden slik den er nå: hvorfor, ikke hva. Ingen endringslogg-kommentarer, og ingen referanser til Claude.
- **Modellen skal krasje høylytt.** Ingen `try/except` som svelger feil, ingen stille standardverdier (`.get(key, 0)`), ingen egne `None`-vakter rundt oppslag som uansett gir `KeyError`. En negativ balanseflyt er en feil og skal ikke klippes til 0. Klamping av trukne verdier til ≥ 0 er en domeneregel og er tillatt.
- Én funksjon per flyt, slik at md-siden for flyten kan peke til ett sted i koden.
- Datakilder og metode dokumenteres i koden og i detalj på en md-side per flyt. Resultatene trenger ikke `comment` eller `data_sources` per rad. Den radstrukturen (`{'flow_name', 'product', 'year', 'value', 'comment', 'data_sources'}` med `report_missing_years`) kom fra den offisielle rapporteringsfilen i NitrogenBudsjett, og er ikke et krav her. Den kan erstattes, for eksempel av flodym-arrays.
- Hvert `preloaded_data['<key>']`-oppslag kommenteres med filnavn og en kort beskrivelse hentet fra `DATA_SOURCES.md`.
- Når en flyt bytter datakilde ved en årsgrense, skal periodene ikke overlappe (ellers telles overlappsårene to ganger).
- Flytnavn inneholder ikke `-`, fordi bindestreken skiller feltene i flytkoden.
- Flagg død kode du ser underveis.
