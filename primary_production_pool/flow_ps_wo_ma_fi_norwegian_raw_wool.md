---
layout: default
title: Norwegian raw wool
parent: Norwegian wool (PS.WO)
grand_parent: 2. Primary production (PS)
nav_order: 1
---

# Norwegian raw wool

| | |
|---|---|
| Flytkode | `PS.WO-MA.FI-Norwegian raw wool-TOT` |
| Fra | [Norwegian wool (PS.WO)](../primary_production_pool/subpool_ps_wo.html) |
| Til | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Tekstilform | FIB – fibre og garn |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Totalkalkylen for jordbrukssektoren (Budsjettnemnda for jordbruket/NIBIO), 1959-2026 |
| Merknad | Greasy wool as weighed in. Animalia/Norilia annual reports for checking |

## Tidsserie

<iframe src="../output_files/plots/pages/ps_wo_ma_fi_norwegian_raw_wool.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 4.92 | 4.86 – 5.05 |
| 2000 | 4.92 | 4.85 – 5.05 |
| 2010 | 4.33 | 4.27 – 4.45 |
| 2018 | 3.88 | 3.83 – 3.98 |
| 2022 | 3.13 | 3.09 – 3.22 |
| 2025 | 2.84 | 2.80 – 2.92 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Garn til MA.TX er balansen per materiale, klippet til 0 (eksportens sammensetning tar opp differansen).

<iframe src="../output_files/plots/pages/ps_wo_ma_fi_norwegian_raw_wool_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_norwegian_raw_wool_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L32). Dokumentasjonen i koden:

> Norwegian wool (greasy, as weighed in) from Totalkalkylen for
> jordbrukssektoren (Budsjettnemnda for jordbruket, NIBIO), the official
> agricultural account; the series starts in 1959. The last year in the
> file is a budget figure and the one before it preliminary.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
