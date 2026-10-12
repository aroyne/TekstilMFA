---
layout: default
title: Wool scouring loss
parent: Fibre and yarn production (MA.FI)
grand_parent: 3. Manufacturing (MA)
nav_order: 4
---

# Wool scouring loss

| | |
|---|---|
| Flytkode | `MA.FI-WM.WW-Wool scouring loss-TOT` |
| Fra | [Fibre and yarn production (MA.FI)](../manufacturing_pool/subpool_ma_fi.html) |
| Til | [Wastewater treatment (WM.WW)](../waste_management_pool/subpool_wm_ww.html) |
| Tekstilform | BYP – biprodukt, ikke tekstil |
| Dimensjoner | år |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 3 |
| Kandidatdata | Greasy wool scoured in Norway (Totalkalkylen + SSB 08801 greasy wool trade, period means) x loss share (Norwegian Wool Book) |
| Merknad | Grease, suint and dirt, not textile. WM.WW has a temporary stock until its outflows are implemented |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_fi_wm_ww_wool_scouring_loss.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 0.93 | 0.68 – 1.17 |
| 2000 | 0.74 | 0.53 – 0.96 |
| 2010 | 0.09 | 0.07 – 0.12 |
| 2018 | 0.09 | 0.07 – 0.12 |
| 2022 | 0.09 | 0.07 – 0.12 |
| 2025 | 0.09 | 0.07 – 0.12 |

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX.

<iframe src="../output_files/plots/pages/ma_fi_wm_ww_wool_scouring_loss_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_wool_scouring_loss_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L77). Dokumentasjonen i koden:

> Grease, suint and dirt removed when greasy wool is scoured in Norway,
> sent with the scouring water to wastewater treatment. The greasy wool
> scoured in Norway is Norwegian wool plus imports minus exports of greasy
> wool, as a mean over periods because the annual balance is dominated by
> the timing of shearing, storage and export (anchors derived by
> scripts/derive_wool_scouring_anchors.py): about 2.8 kt in 1988-1995,
> 2.2 kt in 1996-2000, 1.3 kt in 2001-2006 and 0.3 kt from 2007, when
> nearly all Norwegian wool is exported greasy. Exports declared as
> carbonised wool in 1996-2000 and 2002 are counted as greasy, because
> they are priced like greasy wool. The loss share is about a third of the
> greasy weight.

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
