---
layout: default
title: Institutional textiles to recycling
parent: Institutions and businesses (US.IC)
grand_parent: 5. Use (US)
nav_order: 4
---

# Institutional textiles to recycling

| | |
|---|---|
| Flytkode | `US.IC-WM.RC-Institutional textiles to recycling-TOT` |
| Fra | [Institutions and businesses (US.IC)](../use_pool/subpool_us_ic.html) |
| Til | [Material recycling (WM.RC)](../waste_management_pool/subpool_wm_rc.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år × produkt |
| Metode | data |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | de Sadeleer & Rubach 2026, fig. 3-8 and 3-9: NTG intake from industry (mainly hotels and health care) 75 t (2024) and 358 t (2025); recycled share as for all NTG intake |
| Merknad | Household textiles (HT) only; zero before 2024 (D34) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_ic_wm_rc_institutional_textiles_to_recycling.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.IC-WM.RC-Institutional textiles to recycling-TOT** er brukte tekstiler fra industri og offentlig sektor, mest fra hotell og helse, som gjenvinnes hos NTG.

#### Datakilder (og hvordan kildetallene er produsert)

- Norsk Tekstilgjenvinning AS (NTG) i Sandefjord er det første anlegget i Norge for mekanisk materialgjenvinning av tekstiler til fiber som kan spinnes til nytt garn. Det startet kommersiell drift i 2024 og gjenvant 93 t i 2024 og 364 t i 2025 (de Sadeleer & Rubach 2026, kapittel 3.2.9.7, figur 3-8 og 3-9).
- NTG tok inn 75 t fra industri i 2024 og 358 t i 2025.

#### Antakelser

- Det gjenvunne fordeles på opprinnelse etter andelen av det som kom inn: 75 av 153 t × 93 t = 46 t i 2024 og 358 av 651 t × 364 t = 200 t i 2025 (±50 %).
- Alt regnes som hjemmetekstiler (sengetøy og håndklær) og trekkes fra institusjonsavfallet til restavfall.
- Ingen gjenvinning før 2024 (D34).

#### Sammensetning (varetype og materiale)

- Bare hjemmetekstiler, med utstrømmen av årgangsmodellen for US.IC.

#### Tidsutvikling og sammenligninger

- 0 fram til 2023, 0,05 kt i 2024 og 0,2 kt i 2025. NTG planlegger å skalere opp til titusener av tonn per år.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Hjemmetekstiler | nan % | nan % | nan % | nan % | nan % | 100 % |

### Materiale (fiberlag, D19)



| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | nan % | nan % | nan % | nan % | nan % | 37 % |
| Regenerert cellulose | nan % | nan % | nan % | nan % | nan % | 1 % |
| Ikke-tekstil | nan % | nan % | nan % | nan % | nan % | 12 % |
| Andre fibre | nan % | nan % | nan % | nan % | nan % | 6 % |
| Syntetisk | nan % | nan % | nan % | nan % | nan % | 42 % |
| Ull | nan % | nan % | nan % | nan % | nan % | 2 % |

<iframe src="../output_files/plots/pages/us_ic_wm_rc_institutional_textiles_to_recycling_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_institutional_recycling_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L171). Dokumentasjonen i koden:

> Textiles from industry (mainly hotels and health care) recycled at Norsk
> Tekstilgjenvinning: their share of the plant's intake (75 of 153 t in
> 2024, 358 of 651 t in 2025) times the mass recycled (93 and 364 t),
> i.e. 46 and 200 t (de Sadeleer & Rubach 2026, fig. 3-8 and 3-9). Counted
> as household textiles (linen) and zero before 2024 (D34).
