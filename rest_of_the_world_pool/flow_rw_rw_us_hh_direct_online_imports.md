---
layout: default
title: Direct online imports
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 5
---

# Direct online imports

| | |
|---|---|
| Flytkode | `RW.RW-US.HH-Direct online imports-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Tolletaten VOEC data for HS 61/62/63 2022-2025 via NORSUS 2026; Watson et al. 2020 (3300 t in 2018); SSB 08801 codes 99603000 (VOEC total 2023-) |
| Merknad | Low-value shipments are not in 08801 under HS codes; see claude_tekst/2026-09-29_lavverdisendinger_VOEC_og_klesimport.md |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_us_hh_direct_online_imports.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- *Ikke skrevet ennå.*

#### Datakilder (og hvordan kildetallene er produsert)

- *Ikke skrevet ennå.*

#### Antakelser

- *Ikke skrevet ennå.*

#### Sammensetning (varetype og materiale)

- *Ikke skrevet ennå.*

#### Tidsutvikling og sammenligninger

- *Ikke skrevet ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær | nan % | nan % | 100 % | 100 % | 92 % | 93 % |
| Hjemmetekstiler | nan % | nan % | 0 % | 0 % | 8 % | 7 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | nan % | nan % | 57 % | 45 % | 45 % | 46 % |
| Regenerert cellulose | nan % | nan % | 3 % | 4 % | 3 % | 3 % |
| Ikke-tekstil | nan % | nan % | 2 % | 2 % | 3 % | 2 % |
| Andre fibre | nan % | nan % | 1 % | 0 % | 1 % | 1 % |
| Syntetisk | nan % | nan % | 32 % | 42 % | 42 % | 41 % |
| Ull | nan % | nan % | 6 % | 7 % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/rw_rw_us_hh_direct_online_imports_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_direct_online_imports_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L63). Dokumentasjonen i koden:

> Low-value parcels bought directly from foreign web shops, which are not in
> 08801 under their HS codes (D7). Official VOEC data 2022-2025, one
> estimate for 2018, and zero around 2000. VOEC figures exist for clothing
> (HS 61+62) and household textiles (HS 63) only, so other products are 0.
