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

## Nøkkeltall (sum over produkter)

| År | Median (kt) | 95 %-intervall (kt) |
|---|---|---|
| 1990 | 18.16 | 17.32 – 19.07 |
| 2000 | 15.01 | 14.28 – 15.80 |
| 2010 | 8.31 | 7.95 – 8.68 |
| 2018 | 11.09 | 10.74 – 11.48 |
| 2022 | 9.97 | 9.62 – 10.35 |
| 2025 | 8.08 | 7.76 – 8.41 |

## Klipping av negative verdier

Flyten er en balanseflyt. Negative verdier er ikke-fysiske og klippes til 0. Massen som da oppstår, tas opp av klippelageret i prosessen flyten går ut fra (rapportert som «Clipping imbalance»), og flyttes ikke til andre flyter.

I TOT: ikke klippet i noen av de 1000 MC-iterasjonene eller i det deterministiske løpet.

## Materialsammensetning (fiberlag, D19)

Råull er ull (uvasket ull regnes som ull, inkludert fettet, så vaskesvinnet er også ull). Fiber og garn i handelen har hovedfiberen fra HS-koden. Norsk spunnet håndstrikkegarn er ull. Metervare har hovedfiberen fra HS-koden. Garn til MA.TX er balansen per materiale, klippet til 0. Produksjonsavfall har blandingen av garn og metervare inn i MA.TX, og ferdigvarer til DI.RT resten av MA.TX per materiale.

<iframe src="../output_files/plots/pages/ma_tx_di_rt_domestic_finished_products_materials.html" width="100%" height="420px" frameborder="0" scrolling="no"></iframe>

## Beregning i koden

Beregnes i `_domestic_finished_products_mc` i [calculations/ma_mc.py](https://github.com/aroyne/TekstilMFA/blob/main/calculations/ma_mc.py#L213). Dokumentasjonen i koden:

> Balance of MA.TX: yarn and fabric in, minus fabric exports and
> production waste, split over products by mass shares of finished goods
> made in Norway (D26). The shares come from SSB's commodity statistics
> for large units: Industristatistikk, Varetall, 1988 and 1989, and
> Prodcom 2008, 2009 and 2011 averaged per commodity (anchor 2009). Mass
> is taken as published, from pieces times the import mass per piece, or
> from value divided by a Norwegian price per kg. The shares are
> interpolated between the anchors and held after 2009. Footwear is left
> out, because its main materials (leather, rubber) are not MA.TX inputs.
> Around 1988-89
> clothing and household textiles are about a third each and tarpaulins
> and tents about a fifth; in 2008-2011 household textiles (mostly
> bedding) are about half, tarpaulins and tents a quarter and clothing a
> fifth. A negative balance is not physical and is clipped at 0; the
> clipped mass is recorded and reported on the flow page.
>
> `_domestic_product_shares`: Mass share of each product in finished goods made in Norway, array
> (year, product), from SSB's commodity statistics for large units (D26).

## Beskrivelse

<!-- MANUAL:FLOW_DESCRIPTION:START -->
*Ingen manuell beskrivelse ennå.*
<!-- MANUAL:FLOW_DESCRIPTION:END -->
