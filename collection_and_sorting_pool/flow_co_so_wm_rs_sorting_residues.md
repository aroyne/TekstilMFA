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
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Reject share from collector reports |
| Merknad | Rejects from domestic sorting not recycled, and imported rags |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.SO-WM.RS-Sorting residues-TOT** er tekstiler sortert i Norge som ikke selges brukt i Norge (utsortert avfall og tekstiler til materialgjenvinning), og importerte filler (HS 6310), som brukes opp og kastes.

#### Datakilder (og hvordan kildetallene er produsert)

- Flyten er balansen i CO.SO: det som sorteres i Norge og importeres, minus det som går til bruktbutikk.

#### Antakelser

- Det som går til materialgjenvinning, er skilt ut (CO.SO-WM.RC-Sorted for recycling-TOT, D34). Resten går til restavfall (WM.RS).

#### Sammensetning (varetype og materiale)

- Bare CORE, med blandingen av det som samles inn fra husholdningene (utstrømmen fra årgangsmodellen) og donerte usolgte klær.

#### Tidsutvikling og sammenligninger

- Flyten er 1,2 kt i 1988 og 2,1–2,5 kt etter 2018. Det meste er importerte filler. Rester fra sortering i Norge er under 0,5 kt per år.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær, hjemmetekstiler og sko | 100 % | 100 % | 100 % | 100 % | 100 % | 100 % |

### Materiale (fiberlag, D19)

Blandingen av det som samles inn fra husholdningene (utstrømmen av årgangsmodellen) og usolgte klær som forhandlerne gir til innsamlerne (tilførselssammensetningen).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 49 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 14 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorting_residues_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L84). Dokumentasjonen i koden:

> Balance of CO.SO: rejects from domestic sorting that are not recycled,
> and imported rags, which are used up and discarded.
