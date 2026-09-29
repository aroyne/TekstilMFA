# Claude-instruks: TekstilMFA

Prosjektet bygger på arbeidsmetodikken i `../NitrogenBudsjett`. Konvensjonene under er hentet derfra og gjelder også her.

## Dokumenter
- Planlegging og metodenotater skrives på norsk: `docs/PLAN.md`, `docs/SYSTEMDEFINISJON.md`, `docs/METODE.md`, `DATA_SOURCES.md`. Oppdater `docs/PLAN.md` (Gjort/Neste) når en arbeidsøkt avsluttes.
- Analyser og notater Claude skriver på forespørsel legges i `claude_tekst/` med datoprefiks (`ÅÅÅÅ-MM-DD_tema.md`).
- Systemet defineres i `system/processes.csv` og `system/flows.csv`. Endres systemet, oppdateres disse først, og deretter `docs/SYSTEMDEFINISJON.md`. `tests/test_system_register.py` skal fortsatt gå gjennom.

## Kode
- **Kommentarer skrives på engelsk.** De forklarer koden slik den er nå: hvorfor, ikke hva. Ingen endringslogg-kommentarer, og ingen referanser til Claude.
- **Modellen skal krasje høylytt.** Ingen `try/except` som svelger feil, ingen stille standardverdier (`.get(key, 0)`), ingen egne `None`-vakter rundt oppslag som uansett gir `KeyError`. En negativ balanseflyt er en feil og skal ikke klippes til 0. Klamping av trukne verdier til ≥ 0 er en domeneregel og er tillatt.
- Én funksjon per flyt. `flow_code`, `collected_years`, `comment` og `data_sources` deklareres tidlig. Resultater legges til som `{'flow_name', 'product', 'year', 'value', 'comment', 'data_sources'}`, og funksjonen avsluttes med `report_missing_years(...)`.
- `comment` er et rent statusflagg (`'ok'`, `'not done'`). Forklaringer hører hjemme i kodekommentarer eller i `data_sources`.
- Hvert `preloaded_data['<key>']`-oppslag kommenteres med filnavn og en kort beskrivelse hentet fra `DATA_SOURCES.md`.
- Når en flyt bytter datakilde ved en årsgrense, skal periodene ikke overlappe (ellers blir det doble rader per iterasjon).
- Flytnavn inneholder ikke `-`, fordi bindestreken skiller feltene i flytkoden.
- Flagg død kode du ser underveis.
