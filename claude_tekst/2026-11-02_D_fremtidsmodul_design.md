# Fase D: utforming av fremtidsmodulen (forslag)

*Notat 2026-11-02. Besvart samme dag: horisont 2050, start fra medianen, tiltaksrekkefølgen er godkjent, og E1 og E2 er gjort først. Skaleringen i spørsmål 2 er ikke besvart, og anbefalingen (skalert) brukes. Bygger på D12, lagerdiagnosen ([D40](2026-11-02_C_lagerdiagnose.md)), [tiltaksnotatet](2026-11-02_tiltak_sirkularitet_og_MFA.md) og [Weijenberg m.fl. 2026](2026-11-02_Weijenberg_robust_tiltaksvurdering.md).*

## Hva som endrer seg etter 2025

For historikken er statistikken fasit (D8): kasseringer, innsamling og restavfall kommer fra data, og lageret er restleddet. For fremtiden finnes ingen statistikk. Da må modellen snus:

| | Historikk 1988–2025 | Fremtid 2026–2040 |
|---|---|---|
| Tilførsel | Handelsstatistikk, VOEC, grensehandel | Befolkning × kg per innbygger per produkt (baner) |
| Kasseringer fra husholdningene | Statistikk (innsamling + restavfall) | Årgangsmodellen (levetider), kalibrert mot 2018–2025 |
| Fordeling av kasseringer | Data (eksport, plukkanalyser) | Andeler (innsamlingsgrad, sortering, eksport, gjenvinning) som er tiltak eller usikre faktorer |
| Usikkerhet | MC med fordelinger fra data (fase A) | Dyp usikkerhet: vide, flate spenn og mange scenarier (EMA) |

## Struktur (XLRM)

**X – usikre faktorer (ikke styrt av tiltakene):**
* Befolkning: SSBs fremskrivinger (lav, middels og høy).
* Forbruk per innbygger per produkt: årlig endring −3 til +2 % (historisk spenn for klær etter 2005: omtrent flatt).
* Andel direkte netthandel (VOEC) og returandel.
* Levetider i husholdningene: × 1–1,75 (spennet fra lagerdiagnosen) og endring over tid.
* «Usynlige kasseringer»: gapet i 2018–2025 (10–27 kt per år) som andel av kasseringene. Det avgjør om modellen starter fra statistikken eller fra lagermodellen i 2026.
* Eksportmarkedet for brukte tekstiler: andelen av innsamlet som kan eksporteres usortert (blir påvirket av WSR fra 2027).
* Kapasitet og utbytte i sortering og gjenvinning (NTG, nye anlegg).

**L – tiltak (fra tiltaksnotatet):**
* Produsentansvar (WFD 2025/1892, norsk forskrift fra 2027): mål for separat innsamling og finansiering.
* Krav om sortering i Norge eller i EU før eksport (WSR 2024/1157 fra 21.5.2027).
* Forbud mot destruksjon av usolgte klær og sko (ESPR, fra 19.7.2026).
* Holdbarhetskrav og økodesign (ESPR-akt for tekstiler, ca. 2027): lengre levetid.
* Tekstilavgift eller tiltak mot rask mote: lavere forbruk per innbygger.
* Mål for ombruk i Norge.

**R – modellen:** samme register og flyter som i historikken, med årene 2026–2040 lagt til. Fremtidige flyter beregnes med andeler og årgangsmodellen i stedet for statistikk. Startpunktet er 2025.

**M – mål:**
* Innsamlingsgrad (innsamlet ÷ kassert).
* Ombruk i Norge og andel som eksporteres usortert.
* Materialgjenvinning.
* Tekstiler i restavfall og til forbrenning.
* Forbruk per innbygger og lager.
* Grunnlaget for produsentansvaret.

## Metode

* **Scenarier:** Latin hypercube over X (flate fordelinger innenfor spennene), 500–1 000 scenarier, hver kjørt med hvert tiltak og med referansen (ingen nye tiltak). `scipy.stats.qmc` er allerede tilgjengelig, så det trengs ingen ny avhengighet (EMA Workbench er et alternativ).
* **Robusthet:** tilfredsstillelse (andel scenarier der målet nås, for eksempel innsamlingsgrad ≥ X %), anger (avstand til beste tiltak i samme scenario) og feilrate.
* **Sårbarhet:** hvilke X som avgjør om et tiltak lykkes (Spearman, som hos Weijenberg, eller variansbasert).
* **Andeler med sum 1** (for eksempel ombruk, gjenvinning og rester ut av sortering): avkuttet, flat Dirichlet.

## Spørsmål til deg

1. **Horisont:** 2040 (produsentansvarets første målperioder) eller 2050?
2. **Startpunkt i 2025:** Skal kasseringene etter 2025 komme fra årgangsmodellen skalert slik at de treffer statistikken i 2025 (anbefalt, slik at fremtiden starter der dataene slutter)? Alternativet er å bruke årgangsmodellen uskalert. Det gir et brudd på ca. 10 kt i 2026.
3. **Historisk usikkerhet:** Skal den føres videre ved at hvert scenario trekker en historisk MC-iterasjon som startpunkt (konsistent, men tyngre)? Alternativet er at fremtiden starter fra medianen, med den historiske usikkerheten som egne X-faktorer (anbefalt, enklere).
4. **Hvilke tiltak først?** Forslag: produsentansvar med innsamlingsmål, krav om sortering før eksport, og holdbarhet (levetid). Destruksjonsforbudet og avgiften tas etterpå.
5. **E1 og E2 før fase D?** Grunnlaget for produsentansvaret og innsamlingsgraden kan regnes for 1988–2025 med usikkerhet nå, uten fremtidsmodulen. Innsamlingsgraden må regnes per iterasjon for å bevare korrelasjonen. Anbefalt: ja, det er lite arbeid og politisk aktuelt.
