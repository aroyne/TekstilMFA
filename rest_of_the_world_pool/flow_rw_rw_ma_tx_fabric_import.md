---
layout: default
title: Fabric import
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 2
---

# Fabric import

| | |
|---|---|
| Flytkode | `RW.RW-MA.TX-Fabric import-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Tekstilform | FAB – metervare og halvfabrikata |
| Dimensjoner | år |
| Metode | data |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | SSB 08801 (woven fabric in HS 50-55, HS 58 and 60) |
| Merknad | HS 59 (coated and technical fabrics) is outside the scope |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_ma_tx_fabric_import.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **RW.RW-MA.TX-Fabric import-TOT** er import av metervare til norsk tekstil- og konfeksjonsindustri: vevnader i HS 50–55, spesialvevnader, blonder og broderier (HS 58) og trikotasjestoff (HS 60).
- Belagte, impregnerte og tekniske stoffer (HS 59) er utenfor omfanget (D3, D22).

#### Datakilder (og hvordan kildetallene er produsert)

- SSB tabell 08801, nettovekt i kg (se RW.RW-MA.FI-Fibre and yarn import-TOT).

#### Antakelser

- All importert metervare brukes i MA.TX. Noe går trolig til andre næringer (møbeltrekk, madrasser, bil- og båtinteriør), men det er ikke skilt ut ennå (se MA.TX-DI.RT-Domestic finished products-TOT).
- Datasettusikkerhet ±5 % (plassholder).

#### Sammensetning (varetype og materiale)

- Ingen varetype.
- Materialet er hovedfiberen i HS-koden. Bomull falt fra 68 % i 1990 til 18 % i 2022, mens syntetisk økte fra 23 % til 73 %.

#### Tidsutvikling og sammenligninger

- Importen var 10–14 kt per år i 1988–2004 (høyest i 1998 med 14,1 kt) og har falt til 5,5 kt i 2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Hovedfiberen fra HS-koden (metervare, FA).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 68 % | 60 % | 34 % | 19 % | 18 % | 14 % |
| Regenerert cellulose | 5 % | 5 % | 3 % | 2 % | 2 % | 2 % |
| Andre fibre | 1 % | 1 % | 3 % | 2 % | 3 % | 2 % |
| Syntetisk | 23 % | 31 % | 55 % | 73 % | 73 % | 79 % |
| Ull | 3 % | 4 % | 4 % | 5 % | 4 % | 3 % |

<iframe src="../output_files/plots/pages/rw_rw_ma_tx_fabric_import_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_fabric_import_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L177). Dokumentasjonen i koden:

> Registered imports of fabric, SSB 08801 (woven fabric in HS 50-55, HS 58 and 60).
