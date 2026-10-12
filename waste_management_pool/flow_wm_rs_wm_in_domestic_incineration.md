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
| 1990 | 18.01 | 12.39 – 24.62 |
| 2000 | 30.65 | 24.67 – 37.53 |
| 2010 | 56.52 | 50.10 – 62.98 |
| 2018 | 69.73 | 63.52 – 76.33 |
| 2022 | 92.91 | 83.46 – 102.33 |
| 2025 | 86.24 | 77.40 – 94.63 |

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Materialsammensetning (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

<iframe src="../output_files/plots/pages/wm_rs_wm_in_domestic_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_domestic_incineration_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L49). Dokumentasjonen i koden:

> Balance of WM.RS. A negative balance (landfill and export shares
> summing to more than 1) is not physical and is clipped at 0; the
> clipped mass is recorded and reported on the flow page.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
