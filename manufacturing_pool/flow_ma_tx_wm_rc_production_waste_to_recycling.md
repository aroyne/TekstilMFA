---
layout: default
title: Production waste to recycling
parent: Textile and apparel manufacturing (MA.TX)
grand_parent: 3. Manufacturing (MA)
nav_order: 4
---

# Production waste to recycling

| | |
|---|---|
| Flytkode | `MA.TX-WM.RC-Production waste to recycling-TOT` |
| Fra | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Til | [Material recycling (WM.RC)](../waste_management_pool/subpool_wm_rc.html) |
| Tekstilform | PCW – produksjonsavfall |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | de Sadeleer & Rubach 2026, fig. 3-8 and 3-9: NTG intake of production waste (mainly wool production) 20 t (2024) and 39 t (2025); recycled share as for all NTG intake |
| Merknad | Zero before 2024 (D34) |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_tx_wm_rc_production_waste_to_recycling.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.TX-WM.RC-Production waste to recycling-TOT** er produksjonsavfall fra norsk tekstilindustri, mest fra ullproduksjon, som gjenvinnes hos NTG.

#### Datakilder (og hvordan kildetallene er produsert)

- Norsk Tekstilgjenvinning AS (NTG) i Sandefjord er det første anlegget i Norge for mekanisk materialgjenvinning av tekstiler til fiber som kan spinnes til nytt garn. Det startet kommersiell drift i 2024 og gjenvant 93 t i 2024 og 364 t i 2025 (de Sadeleer & Rubach 2026, kapittel 3.2.9.7, figur 3-8 og 3-9).
- NTG tok inn 20 t produksjonsavfall i 2024 og 39 t i 2025.

#### Antakelser

- Det gjenvunne fordeles etter andelen av det som kom inn: 20 av 153 t × 93 t = 12 t i 2024 og 39 av 651 t × 364 t = 22 t i 2025 (±50 %).
- Ingen gjenvinning før 2024 (D34).
- Flyten trekkes fra balansen i MA.TX (ferdigvarer til handelen).

#### Sammensetning (varetype og materiale)

- Ingen varetype. Materialet er blandingen av garn og metervare inn i MA.TX, som for produksjonsavfallet til restavfall. Kilden sier at det mest er ull, så andelen ull er trolig undervurdert.

#### Tidsutvikling og sammenligninger

- 0 fram til 2023, 0,012 kt i 2024 og 0,022 kt i 2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)



| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | nan % | nan % | nan % | nan % | nan % | 9 % |
| Regenerert cellulose | nan % | nan % | nan % | nan % | nan % | 1 % |
| Andre fibre | nan % | nan % | nan % | nan % | nan % | 7 % |
| Syntetisk | nan % | nan % | nan % | nan % | nan % | 70 % |
| Ull | nan % | nan % | nan % | nan % | nan % | 13 % |

<iframe src="../output_files/plots/pages/ma_tx_wm_rc_production_waste_to_recycling_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_production_waste_to_recycling_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L214). Dokumentasjonen i koden:

> Production waste (mainly from wool production) recycled at Norsk
> Tekstilgjenvinning: its share of the plant's intake (20 of 153 t in
> 2024, 39 of 651 t in 2025) times the mass recycled (93 and 364 t),
> i.e. 12 and 22 t (de Sadeleer & Rubach 2026, fig. 3-8 and 3-9). Zero
> before 2024 (D34).
