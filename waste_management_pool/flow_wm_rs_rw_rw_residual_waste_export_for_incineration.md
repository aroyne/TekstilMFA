---
layout: default
title: Residual waste export for incineration
parent: Residual and mixed waste collection (WM.RS)
grand_parent: 7. Waste management (WM)
nav_order: 2
---

# Residual waste export for incineration

| | |
|---|---|
| Flytkode | `WM.RS-RW.RW-Residual waste export for incineration-TOT` |
| Fra | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 13035 (KOSTRA): residual waste exported / residual waste total, 2015-2025 |
| Merknad | Mainly to Sweden |

## Tidsserie

<iframe src="../output_files/plots/pages/wm_rs_rw_rw_residual_waste_export_for_incineration.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.00 | 0.00 – 0.00 |
| 2000 | 0.00 | 0.00 – 0.00 |
| 2010 | 6.35 | 5.47 – 7.20 |
| 2018 | 13.71 | 12.16 – 15.20 |
| 2022 | 13.68 | 12.07 – 15.50 |
| 2025 | 11.34 | 9.92 – 12.83 |

## Materialsammensetning (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

<iframe src="../output_files/plots/pages/wm_rs_rw_rw_residual_waste_export_for_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_residual_export_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L39). Dokumentasjonen i koden:

> Share of residual waste exported, SSB 13035 (D11). The share is measured
> for household residual waste and is applied to all textiles in WM.RS,
> including institutional waste.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
