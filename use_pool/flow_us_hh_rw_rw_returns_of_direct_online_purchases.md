---
layout: default
title: Returns of direct online purchases
parent: Households (US.HH)
grand_parent: 5. Use (US)
nav_order: 8
---

# Returns of direct online purchases

| | |
|---|---|
| Flytkode | `US.HH-RW.RW-Returns of direct online purchases-TOT` |
| Fra | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Til | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | parameter |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Direct online imports (VOEC) x return share (0.2, 0.05-0.5: EEA about 20 % for clothing bought online, Zalando about 50 %, Temu and Shein probably lower) |
| Merknad | VOEC figures are deliveries to Norway; returns to foreign web shops leave the country (D38) |

## Tidsserie

<iframe src="../output_files/plots/pages/us_hh_rw_rw_returns_of_direct_online_purchases.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **US.HH-RW.RW-Returns of direct online purchases-TOT** er klær og hjemmetekstiler som husholdningene har kjøpt direkte fra utenlandske nettbutikker, og som sendes tilbake.
- Returer til norske nettbutikker er ikke med. De går tilbake til DI.RT, og det som destrueres der, er med i `DI.RT-WM.RS-Unsold goods discarded` (D38).

#### Datakilder (og hvordan kildetallene er produsert)

- Direkte netthandel er VOEC-tallene fra Tolletaten (via de Sadeleer & Rubach 2026). De er leveranser til Norge, ikke justert for returer.
- EEA (2024) anslår at ca. 20 % av klærne som kjøpes på nett, returneres. Zalando har ca. 50 %, og en tysk undersøkelse (Bamberg) fant 24 % av pakkene.
- Returandelen for Temu og Shein, som dominerer VOEC-tallene fra 2024, er ukjent og trolig lav.

#### Antakelser

- Returandelen er 0,2 (0,05–0,5, triangulær med spennet mellom kildene) og lik for alle år.
- Lagermodellen for husholdningene får nye varer minus returer.

#### Sammensetning (varetype og materiale)

- Klær og hjemmetekstiler, som direkte netthandel.
- Materialet er sammensetningen til tilførselen: ca. 46 % bomull og 41 % syntetisk i 2025.

#### Tidsutvikling og sammenligninger

- 0 før VOEC-ordningen, 0,8–1,1 kt i 2022–2024 og 3,2 kt i 2025 (1,0–7,1), når VOEC-tallene øker kraftig.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær | nan % | nan % | nan % | nan % | 96 % | 93 % |
| Hjemmetekstiler | nan % | nan % | nan % | nan % | 4 % | 7 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | nan % | nan % | nan % | nan % | 45 % | 46 % |
| Regenerert cellulose | nan % | nan % | nan % | nan % | 4 % | 3 % |
| Ikke-tekstil | nan % | nan % | nan % | nan % | 2 % | 3 % |
| Andre fibre | nan % | nan % | nan % | nan % | 1 % | 1 % |
| Syntetisk | nan % | nan % | nan % | nan % | 42 % | 41 % |
| Ull | nan % | nan % | nan % | nan % | 6 % | 6 % |

<iframe src="../output_files/plots/pages/us_hh_rw_rw_returns_of_direct_online_purchases_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Usikkerhetsbidrag

Andel av variansen fra hver kilde (førsteordens analyse: hver kilde settes alene til 2,5- og 97,5-persentilen, D39). Kilder med `gap:` er usikkerheten i år uten publiserte tall (D30). Årlige datasett (for eksempel `08801:import:finished`) er summert over år.

| Kilde | 2025 |
|---|---|
| `online_return_share` | 74 % |
| `voec (shared method)` | 14 % |
| `online_direct_CL` | 12 % |
| Halvt 95 %-intervall, førsteordens (kt) | 2.85 |
| Halvt 95 %-intervall, Monte Carlo (kt) | 3.06 |

Når de to intervallene avviker mye, er førsteordens bildet grovt (restledd nær null, klipping, skjeve kilder eller produkter av usikre faktorer).

## Beregning i koden

Beregnes i `_online_returns_mc` i [calculations/us_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/us_mc.py#L138). Dokumentasjonen i koden:

> Goods bought directly from foreign web shops and sent back (D38). The
> VOEC figures are deliveries to Norway, and returns to the web shop leave
> the country. Return share 0.2 (0.05-0.5): the EEA (2024) gives about
> 20 % for clothing bought online, Zalando about 50 % and a German study
> (Bamberg) 24 % of parcels; Temu and Shein, which dominate the VOEC
> figures from 2024, are probably lower.
