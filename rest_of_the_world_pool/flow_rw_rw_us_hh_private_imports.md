---
layout: default
title: Private imports
parent: Rest of the world (RW.RW)
grand_parent: 1. Rest of the world (RW)
nav_order: 4
---

# Private imports

| | |
|---|---|
| Flytkode | `RW.RW-US.HH-Private imports-TOT` |
| Fra | [Rest of the world (RW.RW)](../rest_of_the_world_pool/subpool_rw_rw.html) |
| Til | [Households (US.HH)](../use_pool/subpool_us_hh.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | data+parameter |
| Status | implemented |
| Prioritet | 1 |
| Kandidatdata | SSB 05678 (cross-border day trips total 2004-2022) and 14221 (clothing and shoes 2023-2025); NOK-to-kg via 08801 unit values x retail markup |
| Merknad | Not in trade statistics; small (about 0.2-0.5 kt/yr); purchases on overnight travel not covered |

## Tidsserie

<iframe src="../output_files/plots/pages/rw_rw_us_hh_private_imports.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **RW.RW-US.HH-Private imports-TOT** er klær og sko kjøpt av husholdninger på dagsturer til utlandet (grensehandel), som ikke er med i handelsstatistikken.
- Kjøp på reiser med overnatting er ikke med.

#### Datakilder (og hvordan kildetallene er produsert)

- SSB 05678 (grensehandel på dagsturer i alt, mill. kr, 2004–2022) og SSB 14221 (klær og sko, mill. kr, 2023–2025).
- Grensehandelsstatistikken bygger på en utvalgsundersøkelse av husholdningene, oppblåst til hele befolkningen.

#### Antakelser

- 2004–2022: grensehandelen i alt × klesandelen, som er snittet av 2023–2025 (4,7 %, D16).
- Kroner regnes om til kg med tollverdien per kg for importerte klær og sko samme år × et påslag for utsalgspris (2,5, usikkerhet 1,8–3,5).
- Massen fordeles mellom klær og sko etter andelen av registrert import.
- Før 2004 holdes mengden på 2004-nivå.

#### Sammensetning (varetype og materiale)

- Omtrent 75 % klær og 25 % sko.
- Materialet er sammensetningen til registrert import av samme varetype.

#### Tidsutvikling og sammenligninger

- Flyten er liten: 0,9–1,0 kt per år i 2004–2019, 0,1 kt i 2020–2021 da grensene var stengt, og 0,4–0,5 kt i 2022–2025.
- Nivået etter 2023 bygger på det direkte tallet for klær og sko, mens nivået før bygger på klesandelen av all grensehandel. Overgangen kan derfor delvis skyldes metoden.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Klær | 74 % | 78 % | 78 % | 77 % | 77 % | 78 % |
| Sko | 26 % | 22 % | 22 % | 23 % | 23 % | 22 % |

### Materiale (fiberlag, D19)

Sammensetningen til registrert import av produktet samme år (hovedfiber fra HS-koden). Flytene ut av DI.RT er blandet med norske ferdigvarer og norsk spunnet håndstrikkegarn (ull).

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 46 % | 40 % | 44 % | 35 % | 36 % | 37 % |
| Regenerert cellulose | 2 % | 3 % | 3 % | 3 % | 3 % | 3 % |
| Ikke-tekstil | 22 % | 19 % | 19 % | 20 % | 20 % | 19 % |
| Andre fibre | 0 % | 0 % | 0 % | 0 % | 0 % | 0 % |
| Syntetisk | 26 % | 33 % | 29 % | 36 % | 36 % | 35 % |
| Ull | 3 % | 5 % | 5 % | 6 % | 5 % | 5 % |

<iframe src="../output_files/plots/pages/rw_rw_us_hh_private_imports_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_private_imports_mc` i [calculations/rw_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/rw_mc.py#L25). Dokumentasjonen i koden:

> Clothing and shoes bought on cross-border day trips (D16). SSB reports
> shopping in NOK at Swedish retail prices; it is converted to mass with the
> customs import value per kg of CL+FW times a retail markup, and split
> between CL and FW by their shares of registered import mass. The
> statistics cover clothing and shoes only, so other products are 0.
