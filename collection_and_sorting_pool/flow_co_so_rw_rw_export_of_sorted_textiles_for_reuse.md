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
| Kandidatdata | Future module only: sorted for reuse beyond the Norwegian second-hand market (X13) |
| Merknad | Phase D step 3. 0 in the history, where exports of HS 6309 count as unsorted (D17); in the future what is sorted in Norway for reuse beyond the domestic second-hand market |

## Tidsserie

<iframe src="../output_files/plots/pages/co_so_rw_rw_export_of_sorted_textiles_for_reuse.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **CO.SO-RW.RW-Export of sorted textiles for reuse-TOT** er tekstiler som er sortert i Norge til ombruk og eksportert fordi det norske bruktmarkedet ikke tar dem.
- **Flyten er 0 i historikken 1988–2025.** Eksporten av brukte tekstiler (HS 6309+6310) regnes som usortert (D17), og det som holdes tilbake i Norge, selges her eller blir rester.

#### Datakilder (og hvordan kildetallene er produsert)

- Ingen. Flyten brukes bare i fremtidsmodulen (fase D, trinn 3).

#### Antakelser

- I fremtiden går det som sorteres til ombruk i Norge, til bruktsalg i Norge opp til markedets størrelse (X13: 1,6 kt i 2025, 1,6–10 kt i 2035). Resten eksporteres sortert.
- I referansebanen har markedet ingen grense, som i trinn 1 og 2, og flyten er 0.

#### Sammensetning (varetype og materiale)

- Flyten er i produktgruppen CORE.
- Materialet er blandingen av det som samles inn, som for de andre flytene gjennom CO.

#### Tidsutvikling og sammenligninger

- Med sortering av alt innsamlet i Norge (L2) blir flyten den største strømmen ut av sorteringen. Ombruk i Norge er begrenset av markedet (Spearman 1,0 med X13 under L2).
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

*Flyten er ikke delt på varetype.*

### Materiale (fiberlag, D19)

Blandingen av det som samles inn fra husholdningene (utstrømmen av årgangsmodellen) og usolgte klær som forhandlerne gir til innsamlerne (tilførselssammensetningen).


<iframe src="../output_files/plots/pages/co_so_rw_rw_export_of_sorted_textiles_for_reuse_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_sorted_reuse_export_mc` i [calculations/co_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/co_mc.py#L85). Dokumentasjonen i koden:

> Textiles sorted in Norway for reuse and exported: 0 in the history.
> Exports of used textiles (HS 6309+6310) are counted as unsorted export
> (D17), and what is kept in Norway is sold here or rejected. The flow is
> used by the future module, where sorting in Norway can exceed what the
> Norwegian second-hand market takes (phase D, step 3).
