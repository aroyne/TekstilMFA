---
layout: default
title: Recycled fibre to domestic spinning
parent: Material recycling (WM.RC)
grand_parent: 7. Waste management (WM)
nav_order: 1
---

# Recycled fibre to domestic spinning

| | |
|---|---|
| Flytkode | `WM.RC-MA.FI-Recycled fibre to domestic spinning-TOT` |
| Fra | [Material recycling (WM.RC)](../waste_management_pool/subpool_wm_rc.html) |
| Til | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | de Sadeleer & Rubach 2026: Norsk Tekstilgjenvinning (NTG, Sandefjord) recycled 93 t in 2024 and 364 t in 2025 mechanically to fibre for spinning, sold to Norwegian and European customers |
| Merknad | Norwegian share of NTG fibre 50 % (0-100 %); zero before 2024 (D34) |

## Tidsserie

<iframe src="../output_files/plots/pages/wm_rc_ma_fi_recycled_fibre_to_domestic_spinning.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **WM.RC-MA.FI-Recycled fibre to domestic spinning-TOT** er gjenvunnet fiber fra NTG som selges til norske kunder og spinnes til garn.

#### Datakilder (og hvordan kildetallene er produsert)

- Norsk Tekstilgjenvinning AS (NTG) i Sandefjord er det første anlegget i Norge for mekanisk materialgjenvinning av tekstiler til fiber som kan spinnes til nytt garn. Det startet kommersiell drift i 2024 og gjenvant 93 t i 2024 og 364 t i 2025 (de Sadeleer & Rubach 2026, kapittel 3.2.9.7, figur 3-8 og 3-9).
- NTG har solgt fiber til norske og europeiske kunder. Fordelingen er ikke oppgitt.

#### Antakelser

- Den norske andelen er 50 % (0–100 %, PERT), resten eksporteres (D34).
- Ingen fiber-til-fiber-gjenvinning i Norge før 2024.
- Flyten tas med som innsatsvare i balansen til MA.FI.

#### Sammensetning (varetype og materiale)

- Ingen varetype.
- Materialet er fibergruppene i importerte hjemmetekstiler og klær, vektet etter NTGs innstrømning i 2025 (55 % fra industri, mest sengetøy, og 45 % fra husholdninger og produksjon). Det er en antakelse. Eksporten til gjenvinning tar opp forskjellen per materiale.

#### Tidsutvikling og sammenligninger

- 0 fram til 2023, 0,05 kt i 2024 og 0,18 kt i 2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)



| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | nan % | nan % | nan % | nan % | nan % | 51 % |
| Regenerert cellulose | nan % | nan % | nan % | nan % | nan % | 2 % |
| Andre fibre | nan % | nan % | nan % | nan % | nan % | 3 % |
| Syntetisk | nan % | nan % | nan % | nan % | nan % | 40 % |
| Ull | nan % | nan % | nan % | nan % | nan % | 4 % |

<iframe src="../output_files/plots/pages/wm_rc_ma_fi_recycled_fibre_to_domestic_spinning_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_recycled_fibre_to_spinning_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L146). Dokumentasjonen i koden:

> Fibre from mechanical textile recycling at Norsk Tekstilgjenvinning
> (Sandefjord), which can be spun to new yarn: 93 t in 2024 and 364 t in
> 2025, sold to Norwegian and European customers (de Sadeleer & Rubach
> 2026). The Norwegian share is unknown and set to 50 % (0-100 %); the
> rest is exported (WM.RC-RW.RW-Export for recycling-TOT). There was no
> textile-to-fibre recycling in Norway before 2024 (D34).
