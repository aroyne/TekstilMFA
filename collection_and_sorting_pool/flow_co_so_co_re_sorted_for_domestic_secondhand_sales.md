---
layout: default
title: Sorted for domestic secondhand sales
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Sorted for domestic secondhand sales

| | |
|---|---|
| Flytkode | `CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT` |
| Fra | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Til | [Second-hand retail (CO.RE)](../collection_and_sorting_pool/subpool_co_re.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Collector annual reports |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_co_re_sorted_for_domestic_secondhand_sales.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.SO-CO.RE-Sorted for domestic secondhand sales-TOT** er tekstiler sortert i Norge som selges i norske bruktbutikker.

#### Datakilder (og hvordan kildetallene er produsert)

- Andel av det som sorteres i Norge, fra kartleggingene: 54 % i 2018 (Watson m.fl. 2020: 549 av 1 016 t), 95 % i 2022 (Rubach m.fl. 2023: rest ikke oppgitt, antatt liten) og 82 % i 2025 (de Sadeleer & Rubach 2026: 1 622 av 1 986 t).

#### Antakelser

- Andelen holdes fast før 2018 og interpoleres mellom ankerpunktene (usikkerhet 0,3–1,0).

#### Sammensetning (varetype og materiale)

- Bare CORE, med utstrømmen fra årgangsmodellen.

#### Tidsutvikling og sammenligninger

- Flyten var under 0,5 kt per år fram til 2015, 0,7–0,8 kt i 2018–2022 og 1,5 kt i 2025.
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
| Bomull | 46 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 2 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 17 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 27 % | 26 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 6 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_so_co_re_sorted_for_domestic_secondhand_sales_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorted_for_secondhand_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L41). Dokumentasjonen i koden:

> Share of the retained textiles sold second-hand in Norway (same anchors).
