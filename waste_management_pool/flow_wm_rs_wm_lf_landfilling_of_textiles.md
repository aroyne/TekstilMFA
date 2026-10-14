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

- **WM.RS-WM.LF-Landfilling of textiles-TOT** er tekstiler i restavfall og blandet avfall som deponeres.

#### Datakilder (og hvordan kildetallene er produsert)

- Andel deponert: SSB, Avfallsregnskap for tekstiler 1990–1998 (79 % i 1991) og SSB 05281 (avfall etter materialtype og behandlingsmåte, 1995–2011). Fra 2012 viser SSB 10513 at tekstiler ikke deponeres.
- SSBs avfallsregnskap bygger på data fra avfallsselskaper og forbrenningsanlegg, og for noen materialer før 2012 på beregninger av tilført mengde og levetid (D15).

#### Antakelser

- Andelen gjelder alt som går inn i WM.RS: restavfall fra husholdninger, institusjoner og produksjon, og sorteringsrester.
- Andelen interpoleres mellom ankerpunktene og holdes på 1991-nivå før 1991.

#### Sammensetning (varetype og materiale)

- Flyten er ikke delt på varetype.
- Materialet er blandingen av alt som går inn i WM.RS samme år.

#### Tidsutvikling og sammenligninger

- Deponeringen falt fra 78 kt i 1988 til 30 kt i 2009 og opphørte i 2012, etter forbudet mot å deponere nedbrytbart avfall fra 2009.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 29 % | 32 % | 30 % | nan % | nan % | nan % |
| Regenerert cellulose | 3 % | 2 % | 2 % | nan % | nan % | nan % |
| Ikke-tekstil | 19 % | 16 % | 17 % | nan % | nan % | nan % |
| Andre fibre | 2 % | 3 % | 3 % | nan % | nan % | nan % |
| Syntetisk | 41 % | 40 % | 43 % | nan % | nan % | nan % |
| Ull | 5 % | 6 % | 5 % | nan % | nan % | nan % |

<iframe src="../output_files/plots/pages/wm_rs_wm_lf_landfilling_of_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_landfilling_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L34). Dokumentasjonen i koden:

> Landfilled share from SSB Avfallsregnskap tekstiler 1990-1998, SSB 05281 and 10513 (D15).
