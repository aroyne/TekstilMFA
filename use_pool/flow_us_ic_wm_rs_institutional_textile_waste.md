---
layout: default
title: Institutional textile waste
parent: Institutions and businesses (US.IC)
grand_parent: 5. Use (US)
nav_order: 2
---

# Institutional textile waste

| | |
|---|---|
| Flytkode | `US.IC-WM.RS-Institutional textile waste-TOT` |
| Fra | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented (steady state, see open questions) |
| Prioritet | 2 |
| Kandidatdata | SSB 10513 (textile waste by industry) |
| Merknad | Official waste statistics are the primary source (D8) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_ic_wm_rs_institutional_textile_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.IC-WM.RS-Institutional textile waste-TOT** er kasserte tekstiler fra bedrifter og offentlig sektor: arbeidsklær, uniformer, institusjonstekstiler, tepper, presenninger og sekker.

#### Datakilder (og hvordan kildetallene er produsert)

- Ingen egen datakilde ennå. Flyten er lik salget til institusjoner og bedrifter (DI.RT-US.IC-Sales to institutions and businesses-TOT).
- SSB 10513 (avfallsregnskapet etter materialtype) er en mulig kilde, men tekstiler fra næringslivet ligger mest i blandet avfall og kan ikke skilles ut.

#### Antakelser

- Stasjonær tilstand: alt kasseres samme år som det kjøpes, og lageret i US.IC endrer seg ikke.
- Alt går til restavfall (WM.RS). Innsamling fra institusjoner er ikke implementert.

#### Sammensetning (varetype og materiale)

- Samme som salget til institusjoner og bedrifter: sekker 21–45 % og klær 24–33 %.
- Materialet er sammensetningen til salget samme år.

#### Tidsutvikling og sammenligninger

- Flyten følger salget: 13 kt i 1990 og 28–31 kt i 2018–2025.
- Antakelsen om stasjonær tilstand er et åpent spørsmål. Arbeidsklær har en levetid på omtrent tre år, så kasseringene ligger noe etter salget.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 16 % | 7 % | 7 % | 6 % | 6 % | 6 % |
| Klær | 33 % | 33 % | 32 % | 24 % | 24 % | 23 % |
| Sko | 10 % | 9 % | 9 % | 7 % | 7 % | 6 % |
| Hjemmetekstiler | 14 % | 12 % | 13 % | 11 % | 9 % | 8 % |
| Andre konfeksjonerte varer | 2 % | 2 % | 2 % | 3 % | 4 % | 4 % |
| Sekker | 21 % | 34 % | 33 % | 44 % | 45 % | 48 % |
| Presenninger og telt | 5 % | 3 % | 4 % | 4 % | 4 % | 3 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 32 % | 26 % | 25 % | 16 % | 16 % | 16 % |
| Regenerert cellulose | 2 % | 2 % | 1 % | 2 % | 1 % | 1 % |
| Ikke-tekstil | 15 % | 11 % | 12 % | 11 % | 10 % | 9 % |
| Andre fibre | 3 % | 2 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 46 % | 55 % | 56 % | 66 % | 67 % | 69 % |
| Ull | 3 % | 3 % | 3 % | 3 % | 3 % | 3 % |

<iframe src="../output_files/plots/pages/us_ic_wm_rs_institutional_textile_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_institutional_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L70). Dokumentasjonen i koden:

> All products used by institutions and businesses: discarded in the year supplied.
