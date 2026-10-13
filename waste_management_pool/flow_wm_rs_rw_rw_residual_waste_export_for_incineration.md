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
| 2010 | 6.69 | 5.82 – 7.54 |
| 2018 | 14.51 | 12.93 – 16.15 |
| 2022 | 14.34 | 12.52 – 16.20 |
| 2025 | 11.79 | 10.39 – 13.32 |

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
| Bomull | nan % | nan % | 28 % | 23 % | 24 % | 24 % |
| Regenerert cellulose | nan % | nan % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | nan % | nan % | 17 % | 15 % | 15 % | 15 % |
| Andre fibre | nan % | nan % | 3 % | 3 % | 3 % | 3 % |
| Syntetisk | nan % | nan % | 45 % | 52 % | 51 % | 51 % |
| Ull | nan % | nan % | 5 % | 4 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/wm_rs_rw_rw_residual_waste_export_for_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_residual_export_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L39). Dokumentasjonen i koden:

> Share of residual waste exported, SSB 13035 (D11). The share is measured
> for household residual waste and is applied to all textiles in WM.RS,
> including institutional waste.
