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

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.00 | 0.00 – 0.00 |
| 2000 | 0.00 | 0.00 – 0.00 |
| 2010 | 1.85 | 1.09 – 2.65 |
| 2018 | 3.33 | 1.96 – 4.77 |
| 2022 | 0.52 | 0.35 – 0.69 |
| 2025 | 13.94 | 9.38 – 18.77 |

## Materialsammensetning (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden).

<iframe src="../output_files/plots/pages/rw_rw_us_hh_direct_online_imports_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_direct_online_imports_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L63). Dokumentasjonen i koden:

> Low-value parcels bought directly from foreign web shops, which are not in
> 08801 under their HS codes (D7). Official VOEC data 2022-2025, one
> estimate for 2018, and zero around 2000. VOEC figures exist for clothing
> (HS 61+62) and household textiles (HS 63) only, so other products are 0.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
