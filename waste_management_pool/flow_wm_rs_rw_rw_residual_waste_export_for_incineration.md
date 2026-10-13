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

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **WM.RS-RW.RW-Residual waste export for incineration-TOT** er tekstiler i restavfall som eksporteres til forbrenning i utlandet, mest til Sverige.

#### Datakilder (og hvordan kildetallene er produsert)

- Andel eksportert: SSB 13035 (KOSTRA), restavfall levert til forbrenning i utlandet delt på restavfall i alt, 2015–2025. Kommunene rapporterer tallene til KOSTRA.

#### Antakelser

- Andelen som gjelder husholdningenes restavfall, brukes for alle tekstiler i WM.RS, også fra institusjoner og produksjon.
- Andelen er satt til 0 i 2005 og interpoleres til 2015-verdien.

#### Sammensetning (varetype og materiale)

- Flyten er ikke delt på varetype.
- Materialet er blandingen av alt som går inn i WM.RS.

#### Tidsutvikling og sammenligninger

- Eksporten økte fra 0 i 2005 til 16 kt i 2017 og var 12–14 kt i 2020–2025.
- Eksportandelen falt fra 16–19 % i 2015–2019 til 11–13 % i 2020–2025.
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
