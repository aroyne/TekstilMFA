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

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **WM.RS-WM.IN-Domestic incineration-TOT** er tekstiler i restavfall og blandet avfall som forbrennes med energiutnyttelse i Norge.

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i WM.RS: alt som går inn, minus deponi og eksport til forbrenning i utlandet.

#### Antakelser

- WM.IN er et sluk: aske og utslipp følges ikke videre (D11).
- En negativ balanse (deponi- og eksportandel over 1) er ikke-fysisk og klippes til 0. Det har ikke skjedd.

#### Sammensetning (varetype og materiale)

- Flyten er ikke delt på varetype.
- Materialet er blandingen av alt som går inn i WM.RS. Syntetisk økte fra 35 % i 1990 til 51 % i 2022.

#### Tidsutvikling og sammenligninger

- Forbrenningen økte fra omtrent 20 kt per år rundt 1990 til 75 kt i 2012, da deponeringen opphørte, og til 90–98 kt i 2022–2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Blandingen av alt som går inn i WM.RS samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 29 % | 31 % | 29 % | 24 % | 25 % | 24 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 19 % | 16 % | 16 % | 15 % | 15 % | 15 % |
| Andre fibre | 3 % | 3 % | 3 % | 3 % | 3 % | 3 % |
| Syntetisk | 41 % | 41 % | 44 % | 51 % | 51 % | 52 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/wm_rs_wm_in_domestic_incineration_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_domestic_incineration_mc` i [calculations/wm_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/wm_mc.py#L51). Dokumentasjonen i koden:

> Balance of WM.RS. A negative balance (landfill and export shares
> summing to more than 1) is not physical and is clipped at 0; the
> clipped mass is recorded and reported on the flow page.
