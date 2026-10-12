---
layout: default
title: Yarn to textile manufacturing
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 1
---

# Yarn to textile manufacturing

| | |
|---|---|
| Flytkode | `MA.FI-MA.TX-Yarn to textile manufacturing-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | balance |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Balance of MA.FI; SSB 10455 (Prodcom, yarn produced in large enterprises 2008-) for checking |
| Merknad | MA.TX has a temporary stock until its outflows are implemented |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_ma_tx_yarn_to_textile_manufacturing.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 12.13 | 11.65 – 12.62 |
| 2000 | 9.96 | 9.54 – 10.36 |
| 2010 | 5.20 | 4.95 – 5.41 |
| 2018 | 5.04 | 4.83 – 5.22 |
| 2022 | 5.16 | 4.97 – 5.34 |
| 2025 | 5.24 | 5.03 – 5.44 |

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

I fiberlaget (per materiale):

| År | Iterasjoner med klipping | Snitt klippet (kt) | Maks klippet (kt) | Deterministisk (kt) |
|---|---|---|---|---|
| 1989 | 1 av 1000 | 0.000 | 0.055 | 0.000 |
| 2000 | 1 av 1000 | 0.000 | 0.114 | 0.000 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX.

<iframe src="../output_files/plots/pages/ma_fi_ma_tx_yarn_to_textile_manufacturing_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_yarn_to_manufacturing_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L130). Dokumentasjonen i koden:

> Balance of MA.FI: Norwegian wool and imported fibre and yarn minus
> exports, the scouring loss and hand knitting yarn sold through retail.
> A negative balance is not physical and is clipped at 0; the clipped
> mass is recorded and reported on the flow page.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
