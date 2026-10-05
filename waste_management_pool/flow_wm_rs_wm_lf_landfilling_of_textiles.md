---
layout: default
title: Landfilling of textiles
parent: Residual and mixed waste collection (WM.RS)
grand_parent: 7. Waste management (WM)
nav_order: 3
---

# Landfilling of textiles

| | |
|---|---|
| Flytkode | `WM.RS-WM.LF-Landfilling of textiles-TOT` |
| Fra | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Til | [Landfill (WM.LF)](../waste_management_pool/subpool_wm_lf.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 05281 (1995-2011) and 10513 (2012-); earlier years extrapolated |
| Merknad | Dominant route before 2009 landfill ban - important for the time series |

## Tidsserie

<iframe src="../output_files/plots/pages/wm_rs_wm_lf_landfilling_of_textiles.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 67.89 | 53.97 – 83.03 |
| 2000 | 53.86 | 44.26 – 64.36 |
| 2010 | 15.58 | 13.49 – 17.57 |
| 2018 | 0.00 | 0.00 – 0.00 |
| 2022 | 0.00 | 0.00 – 0.00 |
| 2025 | 0.00 | 0.00 – 0.00 |

## Materialsammensetning (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

<iframe src="../output_files/plots/pages/wm_rs_wm_lf_landfilling_of_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_landfilling_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L33). Dokumentasjonen i koden:

> Landfilled share from SSB Avfallsregnskap tekstiler 1990-1998, SSB 05281 and 10513 (D15).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
