---
layout: default
title: Export of sorted textiles for reuse
parent: Sorting (CO.SO)
grand_parent: 6. Collection and sorting (CO)
nav_order: 4
---

# Export of sorted textiles for reuse

| | |
|---|---|
| Flytkode | `CO.SO-RW.RW-Export of sorted textiles for reuse-TOT` |
| Fra | [Sorting (CO.SO)](../collection_and_sorting_pool/subpool_co_so.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | None: exports of HS 6309 and 6310 are not split into sorted and unsorted |
| Merknad | 0 in 1988-2025: exports of used textiles count as unsorted (D17), and what is sorted for reuse in Norway is sold here |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_rw_rw_export_of_sorted_textiles_for_reuse.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.SO-RW.RW-Export of sorted textiles for reuse-TOT** er tekstiler som er sortert i Norge til ombruk og eksportert fordi det norske bruktmarkedet ikke tar dem.
- **Flyten er 0 i historikken 1988–2025.** Eksporten av brukte tekstiler (HS 6309+6310) regnes som usortert (D17), og det som holdes tilbake i Norge, selges her eller blir rester.

#### Datakilder (og hvordan kildetallene er produsert)

- Ingen egne data. Utenrikshandelsstatistikken skiller ikke sortert fra usortert eksport av brukte tekstiler, og eksporten av HS 6309 og 6310 regnes som usortert (D17).

#### Antakelser

- Alt som sorteres til ombruk i Norge, selges i Norge (CO.RE). Sortert ombruk eksporteres ikke.

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er blandingen av det som samles inn, som for de andre flytene gjennom CO.

#### Tidsutvikling og sammenligninger

- 0 i alle år 1988–2025.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Blandingen av det som samles inn fra husholdningene (utstrømmen av årgangsmodellen) og usolgte klær som forhandlerne gir til innsamlerne (tilførselssammensetningen).


<iframe src="../output_files/plots/pages/co_so_rw_rw_export_of_sorted_textiles_for_reuse_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorted_reuse_export_mc` i `calculations/co_mc.py`. Dokumentasjonen i koden:

> Textiles sorted in Norway for reuse and exported: 0 in the history.
> Exports of used textiles (HS 6309+6310) are counted as unsorted export
> (D17), and what is kept in Norway is sold here or rejected.
