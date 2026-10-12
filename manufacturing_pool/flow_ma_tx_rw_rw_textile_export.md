---
layout: default
title: Textile export
parent: Textile and apparel manufacturing (MA.TX)
grand_parent: 3. Manufacturing (MA)
nav_order: 2
---

# Textile export

| | |
|---|---|
| Flytkode | `MA.TX-RW.RW-Textile export-TOT` |
| Fra | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (fabric export: woven fabric in HS 50-55, HS 58 and 60) |
| Merknad | Fabric only. Exports of finished products stay with DI.RT, because the trade statistics do not separate re-export from Norwegian production (D6) |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_tx_rw_rw_textile_export.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 3.52 | 3.40 – 3.64 |
| 2000 | 5.57 | 5.38 – 5.77 |
| 2010 | 2.88 | 2.78 – 2.98 |
| 2018 | 0.87 | 0.84 – 0.90 |
| 2022 | 0.71 | 0.69 – 0.74 |
| 2025 | 2.36 | 2.28 – 2.45 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX.

<iframe src="../output_files/plots/pages/ma_tx_rw_rw_textile_export_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_textile_export_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L152). Dokumentasjonen i koden:

> Registered exports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58
> and 60). Exports of finished goods are counted from DI.RT, because the
> trade statistics do not separate re-export from Norwegian production
> (D6).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
