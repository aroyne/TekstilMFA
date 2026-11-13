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

- Andelen holdes på 2018-nivået før 2018, med usikkerhet som øker bakover (D30), og interpoleres mellom ankerpunktene, med usikkerhet ±50 %. Bruktbutikker har eksistert hele perioden, så andelen var neppe null tidlig (D31).

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
| Bomull | 47 % | 44 % | 42 % | 37 % | 35 % | 35 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 13 % | 16 % | 18 % | 18 % | 18 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 1 % | 2 % | 2 % |
| Syntetisk | 31 % | 31 % | 32 % | 36 % | 38 % | 38 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 5 % | 6 % |

<iframe src="../output_files/plots/pages/co_co_co_so_collected_textiles_to_domestic_sorting_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2000 | 2010 | 2025 |
|---|---|---|---|
| `retained_share_collected` | 34 % | 62 % | 98 % |
| `08801:export:used` | – | 1 % | 1 % |
| `08801_classification:export:used` | – | – | 1 % |
| `gap: retained_share_collected` | 65 % | 37 % | – |
| Halvt 95 %-intervall, førsteordens (kt) | 0.26 | 0.42 | 1.08 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 0.26 | 0.42 | 1.02 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_to_domestic_sorting_mc` i `calculations/co_mc.py`. Dokumentasjonen i koden:

> Collected textiles kept in Norway, as a share of the export. Anchors from
> Watson 2020, Rubach 2023 and de Sadeleer & Rubach 2026.
