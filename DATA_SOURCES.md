# Datakilder

Status: **har** = ligger i `data_files/` og brukes · **hent** = kjent kilde, ikke lastet ned · **verifiser** = kilden eller tabellnummeret er ikke bekreftet og må sjekkes før bruk.

Koden kommenterer hvert oppslag i `preloaded_data` med filnavn og en beskrivelse hentet herfra (samme konvensjon som i NitrogenBudsjett).

## Datafiler i bruk

| Fil | Kilde | Innhold | Brukes i |
|---|---|---|---|
| `anchor_values.csv` | Kuraterte ankerpunkter fra rapporter og offisiell statistikk | Direkte netthandel (VOEC, Watson 2020), restavfall (SSB 1998, Watson 2020, Rubach 2023, de Sadeleer & Rubach 2026) og uvasket ull vasket i Norge (periodesnitt fra Totalkalkylen og 08801, `scripts/derive_wool_scouring_anchors.py`) i kt, med kilde, usikkerhet og status per punkt | `rw_mc.py`, `us_mc.py`, `ma_mc.py` |
| `SSB_13035_restavfall_eksport_2015_2025.csv` | SSB 13035 (KOSTRA, hele landet, API 2026-09-29) | Restavfall i alt og eksportert til utlandet (tonn), og tekstiler til ombruk rapportert av kommunene (13–21 kt per år), 2015–2025 | parameter `residual_export_share`. Tekstiler til ombruk er ikke brukt ennå – mulig kontroll av innsamlingen |
| `SSB_05281_avfallsregnskap_1995_2011.xlsx` | SSB 05281 (kopi fra NitrogenBudsjett) | Avfall etter materialtype og behandlingsmåte 1995–2011. Tekstilradene gir deponiandelen i `parameters/time_dependent_parameters.csv` | parameter `landfill_share_residual` |
| `SSB_10513_textiles_mixed_2012_2024.csv` | SSB tabell 10513, avfallsregnskap (API, 2026-09-29) | Materialtypene «Tekstiler» og «Blandet avfall» etter behandlingsmåte, 2012–2024, 1 000 tonn (latin-1-koding) | ikke ennå (se datainventar) |
| `NIBIO_totalkalkylen_ull.csv` | Totalkalkylen for jordbrukssektoren (Budsjettnemnda for jordbruket), NIBIOs statistikktjeneste (API `statisticsNewTK`, post 8462 «Ull», hentet 2026-10-12) | Norsk ull per år 1959–2026: tonn (innveid, uvasket), kr/kg og verdi (1 000 kr). Siste år er budsjett, året før er foreløpig regnskap | `ma_mc.py` (PS.WO → MA.FI), `scripts/derive_wool_scouring_anchors.py` |
| `SSB_10455_prodcom_garn_tau_nett_2008_2025.csv` | SSB 10455, solgt produksjon av varer for store foretak i industri (API, hentet 2026-10-12) | Alle prodcomkoder 13.10 (garn) og 13.94 (tau og nett), mengde, verdi og solgt produksjon i alt, 2008–2025, med SSBs statuskoder (`:` skjult, `..` mangler). Ullgarn i detaljopplegg (13.10.50.50) 0,59–1,03 kt i 2008–2023 | `ma_mc.py` (MA.FI → DI.RT). 13.94 er kandidat for MA.TX |
| `SSB_industristatistikk_varetall_1988_1989.csv` | SSB, Industristatistikk 1988 og 1989, Hefte II Varetall (NOS B 941 og B 998), tabell 3, lest manuelt fra skannede sider (`scripts/tools/render_pdf_pages.swift`) | Varer produsert i store bedrifter: ullgarn i detaljopplegg (5109.10: 993 t i 1988, 893 t i 1989) og ferdigvarer i kapittel 57, 61–64 og 9404 med enhet, mengde, verdi og side per linje. Grupperte varenumre står som intervall | `ma_mc.py` (MA.FI → DI.RT), `scripts/derive_domestic_product_mass.py` |
| `SSB_10455_prodcom_ferdigvarer_2008_2025.csv` | SSB 10455 (API, hentet 2026-10-12) | Alle prodcomkoder 13.92, 13.93, 13.99, 14 og 15.2: mengde, verdi og statuskoder, 2008–2025 | `scripts/derive_domestic_product_mass.py` |
| `domestic_production_mass.csv` | Avledet: `scripts/derive_domestic_product_mass.py` fra de to filene over, `parameters/domestic_production_codes.csv` og 08801 | Masse per varekode og ankerår (1988, 1989, 2008, 2009, 2011) for ferdigvarer produsert i Norge, med metode (publisert masse, stk × importvekt per stk, eller verdi ÷ norsk pris per kg) | `ma_mc.py` (MA.TX → DI.RT, produktandeler) |
| `SSB_05803_befolkning_1985_2026.csv` | SSB 05803, befolkning 1. januar (API, hentet 2026-10-13) | Folketall 1985–2026. Årssnitt = snitt av 1. januar i år og neste år | `us_mc.py` (restavfall per innbygger før 2009) |
| `Tab_08801_textiles.csv` | SSB tabell 08801, utenrikshandel etter land og varenummer (HS8) | HS-kapittel 50–64 og sengeutstyr 9404.30/40/90 (soveposer, dyner, puter og møbelputer; hentet 2026-10-13). 1988–2022 er hentet fra NitrogenBudsjett sin fulle 08801-fil (`scripts/extract_textile_trade.py`). 2023–2025 er hentet fra SSB API 2026-09-29 (`scripts/update_trade_ssb_api.py`). Enhetskode for API-årene er tatt fra siste år med samme varenummer. Kolonner: år; import/eksport; HS8; land; supplerende enhet (S stykk, P par, 1 ingen); nettovekt kg; supplerende mengde; verdi NOK. | `trade.py` (RW, MA, DI) |

## Kandidatkilder per område

### Tilførsel til markedet
| Kilde | Innhold | Status |
|---|---|---|
| SSB 08801 | Import og eksport per HS8, 1988–2025 | har |
| SSB 10455 (Prodcom, solgt produksjon i store foretak, 2008–2025) | Norsk produksjon per prodcomkode, mengde (kg, m² eller stk) og verdi. Mange celler er skjult | 13.10 og 13.94 har (`SSB_10455_prodcom_garn_tau_nett_2008_2025.csv`); andre koder for MA.TX hentes ved behov |
| Eurostat ext_tec05, handel etter vare (CPA) og importørens næring (TEC), Norge 2016–2024 | Importverdi for klær, tekstiler og lærvarer etter næringen til importøren: klær 54–56 % detaljhandel, 35–37 % engros, ca. 5 % industri, 3–4 % andre næringer og offentlig. 2018, 2019 og 2021 delvis skjult. Se `claude_tekst/2026-10-26_b2b_og_b2c.md` | hent (mulig nedre grense for `institutional_share`) |
| SSB 08604 (2008, 2015) og 14457 (2015, 2022), industriavfall etter næring og materialtype | Tekstilavfall fra NACE 13–15: 1 / 0 / 0 kt (avrundet til hele tusen tonn), blandet avfall 1–4 kt | ankerpunkter `preconsumer_waste_textile_industry` i `anchor_values.csv` |
| SSB 12910, hovedtall for foretak og bedrifter etter næring (2017–2024) | Sysselsatte og produksjonsverdi per næring: 13.92 konfeksjonerte tekstilvarer ~2,1–3,1 mrd. kr, 14.1 klær ~2,7–3,1 mrd. kr, 13.94 tau og nett ~1,7–3,3 mrd. kr | kandidat for produktfordelingen i MA.TX (ikke hentet til data_files) |
| SNL, «garn» og «Sandnes Garn» | Omtrent 1 000 t håndstrikkegarn produseres i Norge per år, og omsetningen er over 500 mill. kr (begge uten årstall). Sandnes Garn produserer ca. 600 t | brukes til usikkerheten på 10455 |
| SSB, Industristatistikk 1985–1989, Hefte II Varetall (NOS B 689, B 781, B 876, B 941, B 998) | Varetall for industrien før Prodcom, etter HS fra 1988 | 1988–89 har (`SSB_industristatistikk_varetall_1988_1989.csv`). Skannet uten tekstlag. Fra 1990 til 2007 publiserte SSB bare næringstall |
| SSB 12910 (hovedtall for foretak og bedrifter etter næring, 2017–2024) og 08675 (resultatposter for NACE 13–15, 2007–2024) | Omsetning, sysselsatte og varekostnader for næring 13.1 (spinning) og 13–15 | kandidat for MA (ikke hentet) |
| SSB 05678 og 14221 (Grensehandel), `data_files/SSB_grensehandel_05678_14221.csv` (kolonner: ssb_table, series, year, mill_nok) | Handlebeløp på dagsturer 2004–2022 (i alt) og klær og sko 2023–2025 (496 / 509 / 458 mill. kr) | har (`rw_mc.py`) |
| SSB forbruksundersøkelsen / nasjonalregnskap (COICOP 03.1, 03.2, 05.2) | Husholdningenes utgifter til klær, sko og hjemmetekstiler, en proxy for trender | hent |
| SSB 08801, varenr. 99.60.1000/2000/3000 | Lavverdisendinger (næringsliv < 1 000 kr, privat, VOEC), 2023–, uten HS-fordeling. Er **ikke** med under HS-kodene i noe år. | har (i NitrogenBudsjett sin fulle 08801-fil) |
| de Sadeleer & Rubach (2026), *2026 Kunnskapsstatus for tekstiler og tekstilavfall i Norge*, NORSUS OR.18.26, **for NORSIRK/Videre Tekstil (bransje)** | Tekstiler via VOEC per kap. 61/62/63 fra Tolletaten 2022–2025 (524 / 4 797 / 3 849 / 13 962 t). Brutto import 2022–2025. Ankerår 2025: innsamlet 33 703 t, restavfall 44 461 t (Mepex), eksport av brukte tekstiler 34 331 t, ombruk i Norge 1 622 t | har (litteratur/, lokalt) |
| Syversen, Klepp m.fl. (2023), *Dypdykk i materialstrømmene for tekstiler fra husholdninger i Norge*, Mepex/SIFO (Wasted Textiles), for Forskningsrådet og Handelens Miljøfond | Ankerår 2021: avhendet 79 007 t (tekstilboks 30 198 t, restavfall hentet 33 536 t, brakt 15 273 t). 44 % syntetisk, 3 % ull i avhendede tekstiler | har (Termo-tekstil/literature) |
| Rubach m.fl. (2023), *2023 Kunnskapsstatus for tekstiler og tekstilavfall i Norge*, NORSUS OR.07.23, for Virke (KLDs arbeidsgruppe for produsentansvar) | Ankerår 2022: satt på markedet 105 913 t, innsamlet 29 643 t, ombruk i Norge 909 t, restavfall 48 809 t (23 + 10 plukkanalyser), eksport 31 642 t; usolgt: ca. 200 t mottatt av innsamlere, 337 t rapportert av forhandlere (116 t donert) | har (litteratur/, lokalt); usolgt brukt i `anchor_values.csv` (D27) |
| Totalkalkylen (NIBIO) | Norsk ullmengde 1959– | har (`NIBIO_totalkalkylen_ull.csv`) |
| Norilia / Animalia (årsrapporter FFULL), Norwegian Wool Book (Flokk), Ullialt-rapporten (Norges Husflidslag 2018) | Kvalitetsklasser, vasking i Bradford, ca. 20 % av norsk ull brukt i Norge, vaskesvinn ca. 1/3 | kontroll og parameter `wool_scouring_loss_share` |

### Bruk og lager
| Kilde | Innhold | Status |
|---|---|---|
| SIFO/OsloMet (Klepp, Laitala m.fl.): garderobestudier, klesforbruk og levetid | Levetid, lager per person, dvalende klær | hent/verifiser |
| WRAP (UK), *Valuing our clothes* | Levetid og lager (sammenligning) | hent |
| Litteratur om institusjonstekstiler, vaskerier | Levetid og mengder i US.IC | hent |
| ECAP 2017, *European Textiles & Workwear Market* | Arbeidstøy ca. 1,5 % av klesforbruket i EU og UK, levetid litt over 3 år (WRAP 2015) | har (Zotero) |
| Kawecki m.fl. 2021; Laitala & Klepp 2020; vedlegget til Napolano m.fl. 2025 (SM4) | Levetidsfordelinger per produkttype | hent (ikke i Zotero) |
| Leiden U, CBS, CML 2020, *Voorraden in de maatschappij* | Lager og levetider for tekstiler i Nederland | hent |

### Innsamling, sortering og ombruk
| Kilde | Innhold | Status |
|---|---|---|
| NORSUS (2023), *Kunnskapsstatus for tekstiler og tekstilavfall i Norge* (= Rubach m.fl. 2023, OR.07.23) | 2022: 105,9 kt satt på markedet (19,3 kg/pers), 78,5 kt avfall, 48,8 kt i restavfall, 29,6 kt separat innsamlet, ca. 85 % eksportert | hent (tallene finnes i TekstilEOL `config/market_volumes.csv`) |
| Årsrapporter fra Fretex, UFF, Kirkens Bymisjon m.fl. | Innsamlede mengder, sortering, ombruk i Norge | hent |
| de Sadeleer & Rubach (2026), kap. 3.2.9.7, fig. 3-8 og 3-9 (lest fra figurene) | Norsk Tekstilgjenvinning (Sandefjord): inn fra industri 75/358 t, husholdninger 58/254 t, produksjonsavfall 20/39 t; gjenvunnet 93/364 t; ombruk 0/52 t; avfall 60/234 t (2024/2025) | ankerpunkter `recycling_*` i `anchor_values.csv` (D34) |
| EEA (2024), *The destruction of returned and unsold textiles in Europe's circular economy*, og ETC CE Report 2024/4 | 4–9 % av tekstilene som settes på markedet i Europa, destrueres ubrukt (264–594 kt per år i EU) | bare følsomhetsanalyse (D27) |
| Watson, Trzepacz, Rubach & Johnsen (2020), *Kartlegging av brukte tekstiler og tekstilavfall i Norge*, NORSUS/PlanMiljø OR 52.20, for Miljødirektoratet | Ankerår 2018: satt på markedet 74 340 t, netthandel 3 300 t, innsamlet 31 690 t, restavfall 25 400 t + gjenbruksstasjoner 6 130 t, usolgt ≥ 714 t (600 t donert til én innsamler, 95 t forbrent hos forhandlere som svarte) | har (litteratur/, lokalt); usolgt brukt i `anchor_values.csv` (D27) |
| Mepex-rapporter for Miljødirektoratet om brukte tekstiler og tekstilavfall | Mengder og flyter, flere årganger | verifiser |
| Miljødirektoratets utredning av produsentansvar for tekstiler | Mengder og kanaler | verifiser |
| Nordiske rapporter: Tojo et al. 2012 (TemaNord 2012:545), Palm et al. 2014 (TemaNord 2014:538), Watson et al. 2016 (TemaNord 2016:558) | Historiske nordiske tekstilflyter, blant annet for Norge | hent/verifiser |

### Avfallshåndtering
| Kilde | Innhold | Status |
|---|---|---|
| SSB 05281 (1995–2011) og 10513 (2012–) Avfallsregnskap | Tekstilavfall etter behandlingsmåte, også deponi. **Brudd i 2012:** «Tekstiler» faller fra 113 til 4 kt, trolig fordi tekstiler i restavfall flyttes til «Blandet avfall». Se `claude_tekst/2026-09-29_datainventar_P1-flyter.md` | 10513 har (data_files/); 05281 i NitrogenBudsjett – kopier |
| SSB, *Avfallsregnskap, tekstiler, 1990–1998* (2001) | 1998: 106 kt tekstilavfall (husholdninger 83 kt, klær 47,2 kt), deponi 72 % (79 % i 1991), forbrenning ca. 20 %, gjenvinning/ombruk 8 %. Klær 1991: 34,8 kt | har (bare tallene i nettsideteksten; tabellene er ikke på nett – spør SSB) |
| Plukkanalyser (Mepex, Avfall Norge, kommuner) | Tekstilandel i restavfall | hent |
| Sundt m.fl. (2016), *Primary microplastic-pollution: Measures and reduction potentials in Norway*, Mepex for Miljødirektoratet (M545), som gjengir Sundt m.fl. (2014) | Ca. 600 t syntetiske mikrofibre per år fra husholdningsvask i Norge | ankerpunkt `laundry_release_synthetic` (D28) |
| Lant m.fl. (2020), *Microfiber release from real soiled consumer laundry*, PLoS ONE | 114 mg fibre per kg tøy i ekte vask, mest naturfibre | begrunnelse for å ta med naturfibre (D28) |
| De Falco m.fl. (2020), *Microfibers released into the air from synthetic textiles*, Scientific Reports | Utslipp til luft ved bruk av samme størrelse som ved vask | parameter `air_release_relative_to_laundry` (D28) |
| SSB 07355 (2008–2022), 14342 (2020–2025) og 10514 (2012–2024), avfall etter næring og materialtype | Tekstiler fra tjenesteytende næringer er skjult i 07355 og 14342. I 10514 er de 0–1 kt (hele tusen tonn, bare separat sortert tekstilavfall). Ingen tekstilandel i blandet næringsavfall | sjekket, ikke brukbar som nivå for US.IC |
| SSB husholdningsavfall | Mengder restavfall og grovavfall | hent/verifiser tabell |
| Miljødirektoratet / SSB om avfallseksport | Restavfall eksportert til forbrenning (Sverige) | hent |

### Usikkerhet
| Kilde | Innhold | Status |
|---|---|---|
| Avfall Norge 2015, *Veileder plukkanalyser*, rapport 10/2015 | Feilmargin for tekstilandel i restavfall ±22,8 % (90 % konfidens, 3 000 kg prøve, Oslo) | har (Zotero) |

### Mikrofibre
| Kilde | Innhold | Status |
|---|---|---|
| Sundt, Schulze & Syversen (2014), Mepex for Miljødirektoratet: *Sources of microplastic-pollution to the marine environment* | Norske anslag for fibre fra klesvask | hent |
| SSB 05280 (avløp) | Rensegrad og slamdisponering | har i NitrogenBudsjett – kopier |

### Fibersammensetning (fase 3)
| Kilde | Innhold | Status |
|---|---|---|
| Plukkanalyser med fibersortering; JRC (Köhler et al. 2021; Huygens et al. 2023) | Fiberandeler i EU-forbruk og -avfall | hent |
| Textile Exchange, *Materials Market Report* | Globale fiberandeler (polyester 59 % i 2024) | har (via TekstilEOL) |
| SSB 08801 på HS6-nivå | Mange HS-koder angir hovedfiber (for eksempel 6109.10 bomull, 6109.90 annet) | har |
| Laitala m.fl. 2012, *Potensiale for økt materialgjenvinning av tekstilavfall …*, SIFO for Klif, TA-2994 | Brukbart i restavfall, Oslo, hentet: 32 % (2010) og 23 % (2011). Tekstiler i restavfall i norske plukkanalyser 2006–2011: 2,8–9,2 kg per innbygger | har (Zotero) |
| Rubach m.fl. 2023 (tab. 3.17) og de Sadeleer & Rubach 2026 (tab. 3-10), Mepex-data | Brukbart i restavfall: 15 185 av 33 624 t (2022, bare hjemme), 17 707 av 44 461 t (2025). Fiber i avhendet: 38 % syntetisk og 3 % ull (2022), 48,3 % fossilbasert (2025) | har (litteratur/) |
| Gottfridsson & Zhang 2015, masteroppgave Chalmers | Materialsammensetning av sko per tollposisjon 6401–6405 (tekstilandel 5–35 %, resten gummi, plast, lær osv.). Delvis antatt | har (Zotero) |
| Quantis 2021, *PEFCR Apparel and Footwear*; Huygens m.fl. 2023 (JRC) | Sammensetning med ikke-tekstile deler per underkategori | hent |
| `parameters/hs_main_fibre.csv` | Hovedfiber for alle 1 406 HS8-koder i kapittel 50–64, klassifisert etter regler ut fra de engelske varetekstene i metadataene til SSB 08801 (API 2026-10-05, `scripts/build_hs_main_fibre.py`). Klasser: CO, WO, SYN, ART, MMF (kjemiske fibre uten nærmere angivelse), OTH (annen navngitt fiber), RES (restpost «of other textile materials»), UNK (fiber ikke oppgitt). Kolonnen `rule` viser hvilken regel som slo til | har (brukes i `fibre_layer.py`) |

**Merk:** HS-koden gir hovedfiberen for en stor del av klesimporten. For klær (kap. 61/62) i 2025 er 40 % bomull og 33 % kjemiske fibre, mot 41 % og 32 % i NORSUS 2026. Restposter og koder uten fiber (RES+UNK) er 24 % for klær og 13 % for hjemmetekstiler (2025). For sko oppgir ingen koder fiber.
