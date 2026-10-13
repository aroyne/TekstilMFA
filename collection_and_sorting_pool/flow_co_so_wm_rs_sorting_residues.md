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

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 45 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 17 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorting_residues_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L49). Dokumentasjonen i koden:

> Balance of CO.SO. Recycling and rejects are not yet separated (WM.RC is
> P2); both go to residual waste here.
