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
| 1990 | 4.96 | 4.79 – 5.14 |
| 2000 | 4.95 | 4.79 – 5.13 |
| 2010 | 4.36 | 4.22 – 4.52 |
| 2018 | 3.91 | 3.78 – 4.05 |
| 2022 | 3.16 | 3.05 – 3.27 |
| 2025 | 2.86 | 2.77 – 2.97 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX, og ferdigvarer til DI.RT resten av MA.TX per materiale.

<iframe src="../output_files/plots/pages/ps_wo_ma_fi_norwegian_raw_wool_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_norwegian_raw_wool_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L50). Dokumentasjonen i koden:

> Norwegian wool (greasy, as weighed in) from Totalkalkylen for
> jordbrukssektoren (Budsjettnemnda for jordbruket, NIBIO), the official
> agricultural account; the series starts in 1959. The last year in the
> file is a budget figure and the one before it preliminary.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
