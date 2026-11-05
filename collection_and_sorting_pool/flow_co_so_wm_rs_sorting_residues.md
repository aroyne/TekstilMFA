---
layout: default
title: Sorting residues
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 3
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
| Bomull | 47 % | 44 % | 42 % | 37 % | 35 % | 35 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 14 % | 16 % | 18 % | 18 % | 18 % | 18 % |
| Andre fibre | 1 % | 1 % | 1 % | 1 % | 2 % | 2 % |
| Syntetisk | 31 % | 31 % | 32 % | 36 % | 38 % | 38 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 5 % | 6 % |

<iframe src="../output_files/plots/pages/co_so_wm_rs_sorting_residues_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `reuse_fraction_retained` | 18 % | 35 % | 80 % |
| `retained_share_collected` | 10 % | 19 % | 7 % |
| `08801:import:used` | 15 % | 9 % | 5 % |
| `08801_classification:import:used` | 13 % | 8 % | 5 % |
| `recycling_share_sorting_rejects` | 1 % | 1 % | 2 % |
| `gap: reuse_fraction_retained` | 22 % | 16 % | – |
| `gap: retained_share_collected` | 20 % | 11 % | – |
| Halvt 95 %-intervall, førsteordens (kt) | 0.17 | 0.28 | 0.45 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.19 | 0.29 | 0.59 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_sorting_residues_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L96). Dokumentasjonen i koden:

> Balance of CO.SO: rejects from domestic sorting that are not recycled,
> and imported rags, which are used up and discarded.
