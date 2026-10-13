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

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 36 % | 37 % | 28 % | nan % | nan % | nan % |
| Regenerert cellulose | 3 % | 3 % | 2 % | nan % | nan % | nan % |
| Ikke-tekstil | 18 % | 16 % | 17 % | nan % | nan % | nan % |
| Andre fibre | 2 % | 3 % | 3 % | nan % | nan % | nan % |
| Syntetisk | 35 % | 36 % | 46 % | nan % | nan % | nan % |
| Ull | 6 % | 6 % | 5 % | nan % | nan % | nan % |

<iframe src="../output_files/plots/pages/wm_rs_wm_lf_landfilling_of_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_landfilling_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L33). Dokumentasjonen i koden:

> Landfilled share from SSB Avfallsregnskap tekstiler 1990-1998, SSB 05281 and 10513 (D15).
