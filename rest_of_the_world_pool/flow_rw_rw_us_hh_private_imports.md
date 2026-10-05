---
layout: default
title: Private imports
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 4
---

# Private imports

| | |
|---|---|
| Flytkode | `RW.RW-US.HH-Private imports-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 05678 (cross-border day trips total 2004-2022) and 14221 (clothing and shoes 2023-2025); NOK-to-kg via 08801 unit values x retail markup |
| Merknad | Not in trade statistics; small (about 0.2-0.5 kt/yr); purchases on overnight travel not covered |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_us_hh_private_imports.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.94 | 0.71 – 1.21 |
| 2000 | 0.94 | 0.71 – 1.21 |
| 2010 | 1.02 | 0.77 – 1.31 |
| 2018 | 0.90 | 0.69 – 1.17 |
| 2022 | 0.47 | 0.36 – 0.61 |
| 2025 | 0.41 | 0.32 – 0.53 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/rw_rw_us_hh_private_imports_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_private_imports_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L25). Dokumentasjonen i koden:

> Clothing and shoes bought on cross-border day trips (D16). SSB reports
> shopping in NOK at Swedish retail prices; it is converted to mass with the
> customs import value per kg of CL+FW times a retail markup, and split
> between CL and FW by their shares of registered import mass. The
> statistics cover clothing and shoes only, so other products are 0.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
