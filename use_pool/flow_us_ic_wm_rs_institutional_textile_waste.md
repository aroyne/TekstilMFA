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

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 10.99 | 9.12 – 12.60 |
| 2000 | 17.25 | 14.80 – 19.42 |
| 2010 | 23.98 | 20.46 – 27.09 |
| 2018 | 26.89 | 23.63 – 29.93 |
| 2022 | 29.17 | 25.70 – 32.41 |
| 2025 | 26.29 | 23.32 – 29.11 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/us_ic_wm_rs_institutional_textile_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_institutional_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L61). Dokumentasjonen i koden:

> All products used by institutions and businesses: discarded in the year supplied.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
