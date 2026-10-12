---
layout: default
title: Sorting residues
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 4
---

# Sorting residues

| | |
|---|---|
| Flytkode | `CO.SO-WM.RS-Sorting residues-TOT` |
| Fra | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | WRN – brukte, utslitte |
| Dimensjoner | år × produktgruppe |
| Metode | parameter |
| Status | implemented (incl. recycling until WM.RC is split) |
| Prioritet | 2 |
| Kandidatdata | Reject share from collector reports |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.02 | 0.01 – 0.03 |
| 2000 | 0.11 | 0.06 – 0.19 |
| 2010 | 0.25 | 0.14 – 0.41 |
| 2018 | 0.49 | 0.28 – 0.80 |
| 2022 | 0.06 | 0.02 – 0.25 |
| 2025 | 0.27 | 0.11 – 0.79 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorting_residues_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L49). Dokumentasjonen i koden:

> Balance of CO.SO. Recycling and rejects are not yet separated (WM.RC is
> P2); both go to residual waste here.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
