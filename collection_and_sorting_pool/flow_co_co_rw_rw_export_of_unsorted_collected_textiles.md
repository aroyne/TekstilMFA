---
layout: default
title: Export of unsorted collected textiles
parent: Separate collection (CO.CO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 1
---

# Export of unsorted collected textiles

| | |
|---|---|
| Flytkode | `CO.CO-RW.RW-Export of unsorted collected textiles-TOT` |
| Fra | [Separate collection (CO.CO)](../collection_and_sorting_pool/subpool_co_co.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 08801 (HS 6309/6310 export); collector reports; NORSUS 2023 (about 85 % exported) |
| Merknad | HS 6309 export may also contain sorted grades - split needed |

## Tidsserie

<iframe src="../output_files/plots/pages/co_co_rw_rw_export_of_unsorted_collected_textiles.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.CO-RW.RW-Export of unsorted collected textiles-TOT** er eksport av brukte klær, hjemmetekstiler og sko og filler (HS 6309 og 6310), for det meste usortert til sortering i utlandet.

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, nettovekt i kg (se RW.RW-DI.RT-Finished textile products import-TOT).

#### Antakelser

- Eksporten av 6309 og 6310 kommer fra separat innsamling fra husholdningene og fra usolgte klær som forhandlerne gir til innsamlerne (D27). Noe kan være sortert, og noe kan være filler fra industri og institusjoner.
- Flyten er bare i produktgruppen CORE.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er blandingen av det som samles inn fra husholdningene (utstrømmen fra årgangsmodellen) og donerte usolgte klær.

#### Tidsutvikling og sammenligninger

- Eksporten økte fra 0,6 kt i 1988 til 37,7 kt i 2019 og var 31–34 kt i 2022–2025.
- Eksporten i 2025 (34,33 kt) er nøyaktig det samme som i de Sadeleer & Rubach (2026). For 2018 oppgir Watson m.fl. (2020) 30,7 kt, mot 36,4 kt i 08801.
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
| Bomull | 50 % | 48 % | 44 % | 40 % | 37 % | 36 % |
| Regenerert cellulose | 3 % | 3 % | 2 % | 2 % | 2 % | 2 % |
| Ikke-tekstil | 14 % | 16 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/co_co_rw_rw_export_of_unsorted_collected_textiles_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_export_unsorted_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L24). Dokumentasjonen i koden:

> Export of used textiles and rags (HS 6309+6310), SSB 08801.
