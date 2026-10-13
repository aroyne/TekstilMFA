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

- **RW.RW-US.HH-Direct online imports-TOT** er klær og hjemmetekstiler kjøpt direkte fra utenlandske nettbutikker i lavverdisendinger. Disse er ikke med under HS-kodene i 08801 (D7).

#### Datakilder (og hvordan kildetallene er produsert)

- 2022–2025: sendinger til privatpersoner under VOEC-ordningen (forenklet mva-ordning for netthandel), HS-kapittel 61+62 og 63, fra Tolletaten via de Sadeleer & Rubach (2026). Tolletaten beskriver tallene som veiledende.
- 2018: Watson m.fl. (2020) anslo 3,3 kt (3,2 mrd. kr i utenlandsk netthandel med klær, regnet om til masse). Anslaget kan overlappe med deklarerte pakker i 08801.
- SSB 08801 har egne varenumre for lavverdisendinger fra 2023 (99.60.x), men uten fordeling på varer.

#### Antakelser

- Null rundt 2000, lineært mellom ankerpunktene og holdt fast etter 2025.
- Usikkerhet ±50–60 % per ankerpunkt.
- Hjemmetekstiler har ikke eget anslag før 2022.

#### Sammensetning (varetype og materiale)

- Omtrent 90 % klær og 10 % hjemmetekstiler.
- Materialet er sammensetningen til registrert import av samme varetype.

#### Tidsutvikling og sammenligninger

- Flyten øker fra 0 rundt 2000 til 3,3 kt i 2018. VOEC-tallene er svært ujevne: 0,5 kt i 2022, 4,8 kt i 2023, 3,8 kt i 2024 og 14,0 kt i 2025.
- Hvorfor 2022 er så mye lavere enn årene etter, er ikke avklart. VOEC-ordningen har gjeldt siden 2020.
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
