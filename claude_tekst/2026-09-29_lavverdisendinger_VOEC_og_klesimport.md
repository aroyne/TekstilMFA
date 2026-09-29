# Lavverdisendinger (VOEC) i SSB 08801 og fallet i klesimport 2022→2023

*Notat 2026-09-29. Første steg for beslutning D7.*

## Spørsmål
1. Dekker SSB 08801 småpakker fra utenlandske nettbutikker (VOEC) og andre lavverdisendinger, og har dekningen endret seg over tid?
2. Hva forklarer fallet i registrert klesimport fra 2022 til 2023/2024?

## Hva SSB sier
Kilde: [SSB – Lavverdisendinger i statistikken](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer/artikler/lavverdisendinger-i-statistikken)

* «Frem til publiseringen 15. mai 2025 har statistikken ikke dekket lavverdisendinger der tollregelverket gir deklarasjonsfritak.» SSB har heller ikke tatt med deklarerte varelinjer under 1 000 kr, og har slått sammen fortollinger til privatpersoner.
* Fra mai 2025 er det tre nye varenumre, men bare for **2023 og senere** (ikke tilbakeført til tidligere år):
  * `99.60.1000`: deklarerte varelinjer under 1 000 kr, **næringsliv**
  * `99.60.2000`: varelinjer under 1 000 kr og sammenslåtte fortollinger, **privatpersoner**
  * `99.60.3000`: **VOEC**-sendinger under 3 000 kr til privatpersoner (estimert)
* Tallene er aggregert **uten HS-fordeling**. SSB viser en fordeling av 99.60.1000 på varegrupper for 2023–2024, der klær utgjør 23,6 % (trolig av verdi – må verifiseres).
* VOEC ble innført i 2020 da 350-kronersgrensen ble avviklet. Overgangsordningen ble først avviklet 1.1.2024.

## Hva som ligger i vår 08801-fil (nedlastet juni 2025)
Fila inneholder de nye kodene for 2023 og 2024 (import, alle varer, ikke bare tekstiler):

| Kode | 2023 kt | 2023 mrd NOK | 2024 kt | 2024 mrd NOK |
|---|---|---|---|---|
| 99601000 (næringsliv < 1 000 kr) | 269,5 | 13,9 | 177,3 | 14,6 |
| 99602000 (privat) | 1,9 | 1,6 | 2,4 | 1,0 |
| 99603000 (VOEC) | 13,6 | 5,1 | 24,6 | 8,3 |

Kodene ligger i HS-kapittel 99, så de er **ikke** med i tekstiluttrekket (kapittel 50–64).

## Klær i VOEC
Ifølge ny NORSUS-kartlegging (2026, gjengitt av [Framtiden i våre hender](https://www.framtiden.no/artikler/tredobling-av-temu-varer-til-norge) og [Norsirk](https://aktuelt.norsirk.no/den-norske-temu-boomen-sender-tekstilavfallet-til-v%C3%A6rs-44-000-tonn-g%C3%A5r-rett-til-forbrenning)):
* Import av klær via VOEC: **3 849 t i 2024** og **13 961 t i 2025** (+263 %).
* Satt på markedet i 2025: 87 531 t (varenumrene i det planlagte produsentansvaret), 15,6 kg per person.
* Tekstiler i restavfall 2025: 44 405 t.
* Selve rapporten er ikke lastet ned ennå. Den må hentes for å se metoden.

**Merk:** Nettadressen `or1120-kartlegging-...` viser til den *eldre* rapporten: Watson, Trzepacz, Rubach & Johnsen (2020), OR 52.20 (versjon 2 av OR 11.20), bestilt av Miljødirektoratet. Den er lagret lokalt som `litteratur/Watson_2020_NORSUS_OR5220_kartlegging_brukte_tekstiler.pdf`.

## Ankerår 2018 fra Watson m.fl. (2020)
* Satt på markedet 2018: 74 340 t (klær 57 448 t, boligtekstiler 16 891 t), fra Comtrade og ProdCom.
  * **Vår 08801 netto import CL+HT 2018: 74,0 kt.** Det er nesten identisk, og bekrefter HS-mappingen.
* Justeringer: norsk produksjon som er skjult i ProdCom, opptil 2 500 t. Utenlandsk netthandel 3 300 t (Virke: 3,2 mrd NOK omregnet med gjennomsnittlig NOK/kg for klær). Totalt ca. 80 000 t (15 kg per person).
* Husholdningenes andel ca. 88 % (dansk fordeling): 70 400 t.
* Separat innsamlet 31 690 t (uten sko og vesker). 30 635 t av dette ble eksportert til sortering. I Norge ble 549 t ombrukt, 93 t gjenvunnet og 374 t brent.
* Restavfall fra husholdninger ca. 25 400 t (8 plukkanalyser, > 16 t avfall). Brennbart fra gjenbruksstasjoner ca. 6 130 t (3 analyser, 44 t, 4,05 % tekstil). Til sammen 31 550 t i blandet avfall. 6 745 t kan ikke gjøres rede for i massebalansen.
* Usolgte varer: minst 700 t per år hos forhandlere. 600 t donert til innsamlere.

## Fallet i klesimport 2022→2023

| | 2018 | 2022 | 2023 | 2024 |
|---|---|---|---|---|
| Netto import CL (kt) | 57,1 | 60,7 | 48,1 | 50,4 |
| Netto import CL+HT (kt) | 74,0 | 76,3 | 62,2 | 66,7 |
| Importerte plagg (mill. stk, HS 61/62 med enhet S) | – | 205 | 158 | 162 |
| NOK/kg klær | 328 | 411 | 470 | 474 |

* Fallet kommer i **2023**, og nesten hele det kommer fra **Kina** (28,3 → 20,8 kt). Bangladesh, Tyrkia og andre faller mindre.
* Vekten per plagg er uendret (0,276 kg), så det er færre plagg, ikke lettere plagg.
* Det er ingen økning i registrert import i 2020, da VOEC startet. Det stemmer med at VOEC-sendinger *ikke* har vært med i 08801 under HS-kodene.
* **VOEC forklarer bare en liten del:** Klær via VOEC var 3,8 kt i 2024, mens registrert klesimport falt med ca. 12 kt. Resten er trolig et reelt fall i forbruket (kraftig prisøkning i NOK, 2023 er et år med dyrtid). Det kan også skyldes at handel flyttet til kanaler som ikke fanges opp (lavverdi-varelinjer i 99.60.1000).

## Konsekvenser for modellen (forslag)
1. **Flyten `RW.RW-US.HH-Direct online imports`:**
   * 2024–2025: NORSUS 2026 (klær via VOEC) er offisielt forankret hovedkilde (D8-prinsippet).
   * 2018: Watson m.fl. (2020), 3 300 t, basert på Virke.
   * 2020–2023: interpoleres mellom ankerpunktene, med brudd ved VOEC 2020 og ved 1.1.2024.
   * Før 2018: skaleres ned mot null rundt år 2000, med stor usikkerhet.
2. **Varelinjer fra næringsliv under 1 000 kr** mangler i HS-statistikken i *alle* år før 2023. Hvis 23,6 % av verdien i 99.60.1000 er klær, tilsvarer det ca. 3,5 mrd NOK i 2024. Med 474 NOK/kg blir det i størrelsesorden 7 kt klær, altså ca. 13 % av registrert klesimport. Tallet er svært usikkert (andelen kan være av verdi, og prisen per kg for små varelinjer er ukjent). Dette kan være en **systematisk underdekning over hele tidsserien**, og det bør bli en egen parameter (`lowvalue_undercoverage_CL`) med stor usikkerhet. Må verifiseres mot SSB før bruk.
3. Oppdatere 08801 med 2025-data, slik at vi kan sammenligne med NORSUS 2026 (87,5 kt satt på markedet 2025).

## Kilder
* SSB: [Lavverdisendinger i statistikken](https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/utenrikshandel-med-varer/artikler/lavverdisendinger-i-statistikken)
* Framtiden i våre hender: [Tredobling av Temu-varer til Norge](https://www.framtiden.no/artikler/tredobling-av-temu-varer-til-norge)
* Norsirk: [Den norske Temu-boomen sender tekstilavfallet til værs](https://aktuelt.norsirk.no/den-norske-temu-boomen-sender-tekstilavfallet-til-v%C3%A6rs-44-000-tonn-g%C3%A5r-rett-til-forbrenning)
* Watson, D., Trzepacz, S., Rubach, S. & Johnsen, F. M. (2020). *Kartlegging av brukte tekstiler og tekstilavfall i Norge*. NORSUS/PlanMiljø, OR 52.20, for Miljødirektoratet. [PDF](https://norsus.no/wp-content/uploads/or1120-kartlegging-av-brukte-tekstiler-og-tekstilavfall-i-norge_Versjon-2.pdf)
