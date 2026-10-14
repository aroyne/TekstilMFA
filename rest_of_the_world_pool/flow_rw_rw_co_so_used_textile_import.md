---
layout: default
title: Used textile import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 6
---

# Used textile import

| | |
|---|---|
| Flytkode | `RW.RW-CO.SO-Used textile import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Tekstilform | MIX – brukte, usortert |
| Dimensjoner | år × produktgruppe |
| Metode | data |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | SSB 08801 (HS 6309 and 6310 import) |
| Merknad | Used clothing (6309, 0.02-0.35 kt) goes to second-hand sales; rags (6310, 1.1-2.1 kt, mostly wiping rags) are discarded with the sorting residues (D32) |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_co_so_used_textile_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **RW.RW-CO.SO-Used textile import-TOT** er import av brukte klær og andre brukte tekstilvarer (HS 6309) og filler (HS 6310).
- Brukte klær selges i bruktbutikker og vintagebutikker. Filler er mest tørkefiller til industrien, som brukes opp og kastes.

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, nettovekt i kg (se RW.RW-DI.RT-Finished textile products import-TOT).

#### Antakelser

- Importerte brukte klær går videre til bruktbutikk (CO.RE) og selges samme år.
- Importerte filler går via sorteringsrestene til restavfall (D32).
- Flyten er i produktgruppen CORE.

#### Sammensetning (varetype og materiale)

- Bare CORE.
- Materialet er det samme som for innsamlede tekstiler (blandingen av det som samles inn fra husholdningene og donerte usolgte klær). Det er en antakelse, fordi HS-kodene ikke oppgir fiber.

#### Tidsutvikling og sammenligninger

- Importen økte fra 1,2 kt i 1988 til 2,4 kt i 2022–2025. Nesten alt er filler (1,1–2,1 kt). Importen av brukte klær er 0,02–0,35 kt, men har økt etter 2020.
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
| Ikke-tekstil | 14 % | 15 % | 18 % | 17 % | 17 % | 17 % |
| Andre fibre | 1 % | 1 % | 1 % | 2 % | 2 % | 2 % |
| Syntetisk | 28 % | 27 % | 30 % | 33 % | 36 % | 37 % |
| Ull | 5 % | 6 % | 5 % | 5 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/rw_rw_co_so_used_textile_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_used_textile_import_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L47). Dokumentasjonen i koden:

> Imports of used clothing (HS 6309) and rags (HS 6310), SSB 08801. The
> used clothing is sold in second-hand and vintage shops, and the rags
> (mostly wiping rags for industry) are used up and discarded.
