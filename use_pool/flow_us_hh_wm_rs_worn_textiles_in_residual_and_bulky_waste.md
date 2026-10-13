---
layout: default
title: Worn textiles in residual and bulky waste
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 3
---

# Worn textiles in residual and bulky waste

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Worn textiles in residual and bulky waste-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Pick analyses (Mepex/Avfall Norge) x SSB household waste amounts; SSB 10513; Reusable share of pick analyses: Laitala et al. 2012 (via Huygens et al. 2023), Rubach et al. 2023, de Sadeleer & Rubach 2026 |
| Merknad | D18. CORE residual textiles not reusable, plus CA/TA/OM discarded in the year supplied |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 63.90 | 52.47 – 76.56 |
| 2000 | 56.90 | 47.49 – 67.65 |
| 2010 | 47.79 | 41.49 – 54.33 |
| 2018 | 47.24 | 42.89 – 52.60 |
| 2022 | 58.60 | 51.61 – 67.46 |
| 2025 | 55.61 | 48.88 – 62.68 |

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- *Ikke skrevet ennå.*

#### Datakilder (og hvordan kildetallene er produsert)

- *Ikke skrevet ennå.*

#### Antakelser

- *Ikke skrevet ennå.*

#### Sammensetning (varetype og materiale)

- *Ikke skrevet ennå.*

#### Tidsutvikling og sammenligninger

- *Ikke skrevet ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 24 % | 18 % | 26 % | 27 % | 23 % | 23 % |
| Klær, hjemmetekstiler og sko | 66 % | 68 % | 51 % | 41 % | 45 % | 48 % |
| Andre konfeksjonerte varer | 3 % | 5 % | 9 % | 13 % | 15 % | 16 % |
| Presenninger og telt | 7 % | 8 % | 14 % | 19 % | 16 % | 12 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 34 % | 38 % | 27 % | 22 % | 23 % | 25 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 19 % | 17 % | 19 % | 18 % | 17 % | 17 % |
| Andre fibre | 2 % | 3 % | 4 % | 4 % | 3 % | 3 % |
| Syntetisk | 35 % | 32 % | 43 % | 49 % | 49 % | 47 % |
| Ull | 6 % | 7 % | 5 % | 5 % | 5 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_worn_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L48). Dokumentasjonen i koden:

> CORE: residual textiles that are not reusable. CA, TA and OM: discarded
> in the year supplied. Sacks (SA) are not used by households (D13).
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste, SSB and Mepex pick analyses (D15).
