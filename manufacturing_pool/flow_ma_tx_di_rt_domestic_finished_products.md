---
layout: default
title: Domestic finished products
parent: Textile and apparel manufacturing (MA.TX)
grand_parent: 3. Manufacturing (MA)
nav_order: 1
---

# Domestic finished products

| | |
|---|---|
| Flytkode | `MA.TX-DI.RT-Domestic finished products-TOT` |
| Fra | [Textile and apparel manufacturing (MA.TX)](../manufacturing_pool/subpool_ma_tx.html) |
| Til | [Wholesale and retail (DI.RT)](../distribution_pool/subpool_di_rt.html) |
| Tekstilform | NEW – nye varer |
| Dimensjoner | år × produkt |
| Metode | balance |
| Status | implemented |
| Prioritet | 2 |
| Kandidatdata | Balance of MA.TX; product shares from SSB Industristatistikk Varetall 1988-1989 and Prodcom 10455 2008-2011 (scripts/derive_domestic_product_mass.py) |
| Merknad | Mass shares per product interpolated between 1988, 1989 and 2009 (mean of 2008, 2009 and 2011 per commodity) and held after 2009 (D26) |

## Tidsserie

<iframe src="../output_files/plots/pages/ma_tx_di_rt_domestic_finished_products.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
#### Hva flyten omfatter

- **MA.TX-DI.RT-Domestic finished products-TOT** er ferdige tekstilvarer laget i Norge og solgt gjennom handelen: klær, hjemmetekstiler (blant annet dyner og puter), presenninger, telt og seil, tepper og andre konfeksjonerte varer.

#### Datakilder (og hvordan kildetallene er produsert)

- Mengden er balansen i MA.TX: garn fra MA.FI og importert metervare, minus eksport av metervare og produksjonsavfall.
- Fordelingen på varetyper kommer fra SSBs varestatistikk for store bedrifter: Industristatistikk, Hefte II Varetall, 1988 og 1989 (lest manuelt fra skannede sider), og Prodcom (SSB 10455) for 2008, 2009 og 2011. Koblingen fra varekode til varetype og HS-kode står i `parameters/domestic_production_codes.csv`, og massen er regnet ut i `scripts/derive_domestic_product_mass.py`.
- Varetallene oppgir mengde i tonn, kg, stykk eller par, og verdi i 1 000 kr. Mange celler er skjult av SSB.

#### Antakelser

- Masse per varekode: tonn eller kg brukes direkte. Stykk og par ganges med importvekten per stykk for samme HS-kode samme år. Koder med bare verdi deles på norsk pris per kg, enten fra samme kode i et annet år eller som importprisen × 2,5 (medianforholdet mellom norsk pris og importpris over 71 koder).
- Prodcom-årene 2008, 2009 og 2011 slås sammen til ett ankerpunkt (2009), fordi hvert år for seg dekker for få varer. Andelene interpoleres mellom 1988, 1989 og 2009 og holdes fast etter 2009.
- Sko holdes utenfor, fordi lær og gummi ikke er innsatsvarer i MA.TX.
- **Balansen ser for høy ut.** Varestatistikken gir 7–8 kt for store bedrifter i 1988–89 og omtrent 4,5 kt i 2008–2011, mot 8–18 kt her. En del av metervaren og garnet går trolig til andre næringer (møbeltrekk, madrasser, bil- og båtinteriør, tekniske formål). Lageret i husholdningene, som er restleddet (D8), øker tilsvarende, til omtrent 220 kg per innbygger i 2018–2025. Balansen beholdes inntil videre.

#### Sammensetning (varetype og materiale)

- Varetype (masseandeler): rundt 1988–89 omtrent 30 % klær, 34–37 % hjemmetekstiler, 19–23 % presenninger og telt, 7 % andre konfeksjonerte varer og 2 % tepper. I 2008–2011 omtrent 49 % hjemmetekstiler (mest sengeutstyr), 27 % presenninger og telt, 21 % klær og 3 % andre konfeksjonerte varer.
- Materialet er balansen i MA.TX per materiale, og den er lik for alle varetyper. Bomull falt fra 48 % i 1990 til 11 % i 2022, mens syntetisk økte fra 37 % til 69 %.

#### Tidsutvikling og sammenligninger

- Flyten var 18–20 kt per år fram til 1995, falt til omtrent 8 kt i 2009 og har ligget på 8–11 kt siden.
- SSB 12910 viser at produksjonsverdien i konfeksjon (13.92) og klær (14.1) har vært stabil i 2017–2024, med 2,1–3,1 og 2,7–3,1 mrd. kr.
<!-- MANUAL:FLOW_DESCRIPTION:END -->

## Sammensetning

Andel av summen i nøkkelår (median).

### Varetype

| Varetype | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Tepper | 2 % | 1 % | 0 % | 0 % | 0 % | 0 % |
| Klær | 27 % | 24 % | 21 % | 22 % | 22 % | 22 % |
| Hjemmetekstiler | 40 % | 44 % | 49 % | 49 % | 49 % | 48 % |
| Andre konfeksjonerte varer | 7 % | 5 % | 3 % | 3 % | 3 % | 3 % |
| Presenninger og telt | 24 % | 26 % | 27 % | 27 % | 27 % | 27 % |

### Materiale (fiberlag, D19)

Balansen i MA.TX per materiale (klippet til 0), lik for alle varetyper.

| Materiale | 1990 | 2000 | 2010 | 2018 | 2022 | 2025 |
|---|---|---|---|---|---|---|
| Bomull | 48 % | 45 % | 20 % | 13 % | 11 % | 10 % |
| Regenerert cellulose | 9 % | 9 % | 3 % | 2 % | 2 % | 1 % |
| Andre fibre | 1 % | 4 % | 9 % | 4 % | 9 % | 9 % |
| Syntetisk | 37 % | 37 % | 60 % | 71 % | 69 % | 71 % |
| Ull | 4 % | 4 % | 8 % | 10 % | 10 % | 9 % |

<iframe src="../output_files/plots/pages/ma_tx_di_rt_domestic_finished_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Beregning i koden

Beregnes i `_domestic_finished_products_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L219). Dokumentasjonen i koden:

> Balance of MA.TX: yarn and fabric in, minus fabric exports and
> production waste, split over products by mass shares of finished goods
> made in Norway (D26). The shares come from SSB's commodity statistics
> for large units: Industristatistikk, Varetall, 1988 and 1989, and
> Prodcom 2008, 2009 and 2011 averaged per commodity (anchor 2009). Mass
> is taken as published, from pieces times the import mass per piece, or
> from value divided by a Norwegian price per kg. The shares are
> interpolated between the anchors and held after 2009. Footwear is left
> out, because its main materials (leather, rubber) are not MA.TX inputs.
> Around 1988-89 clothing and household textiles are about a third each
> and tarpaulins and tents about a fifth; in 2008-2011 household textiles
> (mostly bedding) are about half, tarpaulins and tents a quarter and
> clothing a fifth.
>
> The balance seems too high: SSB's commodity statistics give 7-8 kt for
> large units in 1988-89 and about 4.5 kt in 2008-2011, against 8-18 kt
> here, and the household stock rises accordingly. Part of the imported
> fabric and yarn probably goes to other industries (upholstery,
> mattresses, vehicle and boat interiors, technical uses), which are
> outside the scope. The balance is kept until this is resolved.
>
> A negative balance is not physical and is clipped at 0; the clipped
> mass is recorded and reported on the flow page.
>
> `_domestic_product_shares`: Mass share of each product in finished goods made in Norway, array
> (year, product), from SSB's commodity statistics for large units (D26).
> Each product share gets gap noise between and after the anchor years
> (D30), and the shares are scaled to sum to 1 again.
