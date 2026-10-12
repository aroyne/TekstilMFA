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
| 1990 | 13.19 | 12.79 – 13.49 |
| 2000 | 10.38 | 10.08 – 10.67 |
| 2010 | 5.90 | 5.60 – 6.00 |
| 2018 | 7.12 | 6.92 – 7.26 |
| 2022 | 6.75 | 6.57 – 6.89 |
| 2025 | 6.15 | 5.94 – 6.28 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Garn til MA.TX er balansen per materiale, klippet til 0 (eksportens sammensetning tar opp differansen).

<iframe src="../output_files/plots/pages/ma_fi_ma_tx_yarn_to_textile_manufacturing_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_yarn_to_manufacturing_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L123). Dokumentasjonen i koden:

> Balance of MA.FI: Norwegian wool and imported fibre and yarn minus
> exports, the scouring loss and hand knitting yarn sold through retail.
> A negative balance is not physical: the flow is clipped at 0 and the
> export of fibre and yarn is reduced by the deficit.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
