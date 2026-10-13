---
layout: default
title: Collected textiles to domestic sorting
parent: Separate collection (CO.CO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 2
---

# Collected textiles to domestic sorting

| | |
|---|---|
| Flytkode | `CO.CO-CO.SO-Collected textiles to domestic sorting-TOT` |
| Fra | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Til | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | balance |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Balance of CO.CO |
| Merknad | – |

## Tidsserie

<iframe src="../output_files/plots/pages/co_co_co_so_collected_textiles_to_domestic_sorting.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.CO-CO.SO-Collected textiles to domestic sorting-TOT** er innsamlede tekstiler som sorteres i Norge i stedet for å eksporteres usortert.

#### Datakilder (og hvordan kildetallene er produsert)

- Andel av eksporten av brukte tekstiler, fra kartleggingene: 3,3 % i 2018 (Watson m.fl. 2020: 549 t ombruk, 93 t gjenvinning og 374 t rest), 2,9 % i 2022 (Rubach m.fl. 2023: 909 t ombruk) og 5,8 % i 2025 (de Sadeleer & Rubach 2026: 1 622 t ombruk og 364 t annet).
- Kartleggingene bygger på tall fra innsamlerne (Fretex, UFF, Kirkens Bymisjon m.fl.).

#### Antakelser

- Andelen holdes fast før 2018 og interpoleres mellom ankerpunktene, med usikkerhet ±50 %.

#### Sammensetning (varetype og materiale)

- Bare CORE, med blandingen av det som samles inn fra husholdningene (utstrømmen fra årgangsmodellen) og donerte usolgte klær.

#### Tidsutvikling og sammenligninger

- Flyten var under 1 kt per år fram til 2015, 1,2 kt i 2018 og 2,0 kt i 2025.
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
| Bomull | 51 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 12 % | 15 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_co_co_so_collected_textiles_to_domestic_sorting_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_to_domestic_sorting_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L30). Dokumentasjonen i koden:

> Collected textiles kept in Norway, as a share of the export. Anchors from
> Watson 2020, Rubach 2023 and de Sadeleer & Rubach 2026.
