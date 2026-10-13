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
| 1990 | 19.80 | 14.04 – 26.41 |
| 2000 | 33.60 | 26.78 – 40.70 |
| 2010 | 59.96 | 52.97 – 66.58 |
| 2018 | 74.05 | 67.93 – 80.63 |
| 2022 | 97.56 | 87.44 – 107.54 |
| 2025 | 89.62 | 80.10 – 98.14 |

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
| Bomull | 36 % | 37 % | 28 % | 23 % | 24 % | 24 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 18 % | 16 % | 17 % | 15 % | 15 % | 15 % |
| Andre fibre | 2 % | 3 % | 3 % | 3 % | 3 % | 3 % |
| Syntetisk | 35 % | 36 % | 45 % | 52 % | 51 % | 51 % |
| Ull | 6 % | 6 % | 5 % | 4 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/wm_rs_wm_in_domestic_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_domestic_incineration_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L50). Dokumentasjonen i koden:

> Balance of WM.RS. A negative balance (landfill and export shares
> summing to more than 1) is not physical and is clipped at 0; the
> clipped mass is recorded and reported on the flow page.
