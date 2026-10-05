---
layout: default
title: Reusable textiles in residual and bulky waste
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 2
---

# Reusable textiles in residual and bulky waste

| | |
|---|---|
| Flytkode | `US.HH-WM.RS-Reusable textiles in residual and bulky waste-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Residual and mixed waste collection (WM.RS)](../waste_management_pool/subpool_wm_rs.html) |
| Tekstilform | USE – brukte, ombrukbare |
| Dimensjoner | år × produktgruppe |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | Pick analyses (Mepex/Avfall Norge) x SSB household waste amounts; SSB 10513; Reusable share of pick analyses: Laitala et al. 2012 (via Huygens et al. 2023), Rubach et al. 2023, de Sadeleer & Rubach 2026 |
| Merknad | D18. CORE group only: residual textiles x reusable share; CA/TA/OM are counted as worn |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_wm_rs_reusable_textiles_in_residual_and_bulky_waste.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 15.95 | 10.60 – 22.35 |
| 2000 | 14.73 | 10.21 – 20.24 |
| 2010 | 9.15 | 6.49 – 12.35 |
| 2018 | 12.26 | 8.96 – 15.96 |
| 2022 | 21.85 | 15.73 – 29.48 |
| 2025 | 17.63 | 12.92 – 22.69 |

## Materialsammensetning (fiberlag, D19)

For klær, hjemmetekstiler og sko: utstrømmen av årgangsmodellen for husholdningene. For andre produkter: tilførselssammensetningen samme år.

<iframe src="../output_files/plots/pages/us_hh_wm_rs_reusable_textiles_in_residual_and_bulky_waste_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_reusable_residual_waste_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L37). Dokumentasjonen i koden:

> Part of the CORE residual textiles that could have been reused (D18),
> share from the pick analyses. The analyses cover CL+HT+FW only, so the
> other products are 0 here and counted as worn.
>
> `_residual_core`: CL+HT+FW in household residual and bulky waste, SSB and Mepex pick analyses (D15).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
