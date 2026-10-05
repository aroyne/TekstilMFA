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
| 1990 | 58.58 | 46.60 – 71.77 |
| 2000 | 52.52 | 42.20 – 63.42 |
| 2010 | 45.27 | 38.97 – 51.83 |
| 2018 | 44.08 | 39.32 – 49.16 |
| 2022 | 55.57 | 48.16 – 63.80 |
| 2025 | 53.42 | 46.99 – 60.57 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/us_hh_wm_rs_worn_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_worn_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L48). Dokumentasjonen i koden:

> CORE: residual textiles that are not reusable. CA, TA and OM: discarded
> in the year supplied. Sacks (SA) are not used by households (D13).
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste, SSB and Mepex pick analyses (D15).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
