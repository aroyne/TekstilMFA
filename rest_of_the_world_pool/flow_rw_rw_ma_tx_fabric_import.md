---
layout: default
title: Fabric import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 2
---

# Fabric import

| | |
|---|---|
| Flytkode | `RW.RW-MA.TX-Fabric import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Tekstilform | FAB – metervare og halvfabrikata |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (woven fabric in HS 50-55, HS 58 and 60) |
| Merknad | HS 59 (coated and technical fabrics) is outside the scope |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_ma_tx_fabric_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 11.04 | 10.67 – 11.44 |
| 2000 | 12.05 | 11.65 – 12.48 |
| 2010 | 6.62 | 6.39 – 6.85 |
| 2018 | 7.22 | 6.98 – 7.48 |
| 2022 | 5.78 | 5.58 – 5.98 |
| 2025 | 5.45 | 5.26 – 5.64 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX, og ferdigvarer til DI.RT resten av MA.TX per materiale.

<iframe src="../output_files/plots/pages/rw_rw_ma_tx_fabric_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fabric_import_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L157). Dokumentasjonen i koden:

> Registered imports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58 and 60).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
