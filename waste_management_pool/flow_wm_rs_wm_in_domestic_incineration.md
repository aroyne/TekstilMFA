---
layout: default
title: Domestic incineration
parent: Residual and mixed waste collection (WM.RS)
grand_parent: 7. Waste management (WM)
nav_order: 1
---

# Domestic incineration

| | |
|---|---|
| Flytkode | `WM.RS-WM.IN-Domestic incineration-TOT` |
| Fra | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Til | [Incineration (WM.IN)](../waste_management_pool/subpool_wm_in.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of WM.RS; SSB 10513 treatment by material |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/wm_rs_wm_in_domestic_incineration.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 16.81 | 12.42 – 22.95 |
| 2000 | 30.71 | 26.77 – 35.45 |
| 2010 | 56.87 | 50.83 – 62.23 |
| 2018 | 71.92 | 65.41 – 76.16 |
| 2022 | 92.20 | 86.45 – 99.29 |
| 2025 | 85.78 | 80.64 – 92.19 |

## Materialsammensetning (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

<iframe src="../output_files/plots/pages/wm_rs_wm_in_domestic_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_domestic_incineration_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L50). Dokumentasjonen i koden:

> Balance of WM.RS.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
