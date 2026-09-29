# Datakilder

Status: **har** = ligger i `data_files/` og brukes · **hent** = kjent kilde, ikke lastet ned · **verifiser** = kilden eller tabellnummeret er ikke bekreftet og må sjekkes før bruk.

Koden kommenterer hvert oppslag i `preloaded_data` med filnavn og en beskrivelse hentet herfra (samme konvensjon som i NitrogenBudsjett).

## Datafiler i bruk

| Fil | Kilde | Innhold | Brukes i |
|---|---|---|---|
| `anchor_values.csv` | Kuraterte ankerpunkter fra rapporter og offisiell statistikk | Direkte netthandel (VOEC, Watson 2020) og restavfall (SSB 1998, Watson 2020, Rubach 2023, de Sadeleer & Rubach 2026) i kt, med kilde, usikkerhet og status per punkt | `rw_mc.py`, `us_mc.py` |
| `SSB_05281_avfallsregnskap_1995_2011.xlsx` | SSB 05281 (kopi fra NitrogenBudsjett) | Avfall etter materialtype og behandlingsmåte 1995–2011. Tekstilradene gir deponiandelen i `parameters/time_dependent_parameters.csv` | parameter `landfill_share_residual` |
| `SSB_10513_textiles_mixed_2012_2024.csv` | SSB tabell 10513, avfallsregnskap (API, 2026-09-29) | Materialtypene «Tekstiler» og «Blandet avfall» etter behandlingsmåte, 2012–2024, 1 000 tonn (latin-1-koding) | ikke ennå (se datainventar) |
| `Tab_08801_textiles.csv` | SSB tabell 08801, utenrikshandel etter land og varenummer (HS8) | HS-kapittel 50–64. 1988–2022 er hentet fra NitrogenBudsjett sin fulle 08801-fil (`scripts/extract_textile_trade.py`). 2023–2025 er hentet fra SSB API 2026-09-29 (`scripts/update_trade_ssb_api.py`). Enhetskode for API-årene er tatt fra siste år med samme varenummer. Kolonner: år; import/eksport; HS8; land; supplerende enhet (S stykk, P par, 1 ingen); nettovekt kg; supplerende mengde; verdi NOK. | `trade.py` (RW, DI) |

## Kandidatkilder per område

### Tilførsel til markedet
| Kilde | Innhold | Status |
|---|---|---|
| SSB 08801 | Import og eksport per HS8, 1988–2025 | har |
| SSB industristatistikk (varestatistikk, NACE 13–15) / Eurostat Prodcom | Norsk produksjon av tekstiler, klær og sko | hent/verifiser tabell |
| SSB 05678 og 14221 (Grensehandel), `data_files/SSB_grensehandel_05678_14221.csv` (kolonner: ssb_table, series, year, mill_nok) | Handlebeløp på dagsturer 2004–2022 (i alt) og klær og sko 2023–2025 (496 / 509 / 458 mill. kr) | har (`rw_mc.py`) |
| SSB forbruksundersøkelsen / nasjonalregnskap (COICOP 03.1, 03.2, 05.2) | Husholdningenes utgifter til klær, sko og hjemmetekstiler, en proxy for trender | hent |
| SSB 08801, varenr. 99.60.1000/2000/3000 | Lavverdisendinger (næringsliv < 1 000 kr, privat, VOEC), 2023–, uten HS-fordeling. Er **ikke** med under HS-kodene i noe år. | har (i NitrogenBudsjett sin fulle 08801-fil) |
| de Sadeleer & Rubach (2026), *2026 Kunnskapsstatus for tekstiler og tekstilavfall i Norge*, NORSUS OR.18.26, **for NORSIRK/Videre Tekstil (bransje)** | Tekstiler via VOEC per kap. 61/62/63 fra Tolletaten 2022–2025 (524 / 4 797 / 3 849 / 13 962 t). Brutto import 2022–2025. Ankerår 2025: innsamlet 33 703 t, restavfall 44 461 t (Mepex), eksport av brukte tekstiler 34 331 t, ombruk i Norge 1 622 t | har (litteratur/, lokalt) |
| Syversen, Klepp m.fl. (2023), *Dypdykk i materialstrømmene for tekstiler fra husholdninger i Norge*, Mepex/SIFO (Wasted Textiles), for Forskningsrådet og Handelens Miljøfond | Ankerår 2021: avhendet 79 007 t (tekstilboks 30 198 t, restavfall hentet 33 536 t, brakt 15 273 t). 44 % syntetisk, 3 % ull i avhendede tekstiler | har (Termo-tekstil/literature) |
| Rubach m.fl. (2023), *2023 Kunnskapsstatus for tekstiler og tekstilavfall i Norge*, NORSUS OR.07.23, for Virke (KLDs arbeidsgruppe for produsentansvar) | Ankerår 2022: satt på markedet 105 913 t, innsamlet 29 643 t, ombruk i Norge 909 t, restavfall 48 809 t (23 + 10 plukkanalyser), eksport 31 642 t | har (litteratur/, lokalt) |
| Norilia / Animalia, NIBIO | Norsk ullmengde | hent/verifiser |

### Bruk og lager
| Kilde | Innhold | Status |
|---|---|---|
| SIFO/OsloMet (Klepp, Laitala m.fl.): garderobestudier, klesforbruk og levetid | Levetid, lager per person, dvalende klær | hent/verifiser |
| WRAP (UK), *Valuing our clothes* | Levetid og lager (sammenligning) | hent |
| Litteratur om institusjonstekstiler, vaskerier | Levetid og mengder i US.IC | hent |

### Innsamling, sortering og ombruk
| Kilde | Innhold | Status |
|---|---|---|
| NORSUS (2023), *Kunnskapsstatus for tekstiler og tekstilavfall i Norge* (= Rubach m.fl. 2023, OR.07.23) | 2022: 105,9 kt satt på markedet (19,3 kg/pers), 78,5 kt avfall, 48,8 kt i restavfall, 29,6 kt separat innsamlet, ca. 85 % eksportert | hent (tallene finnes i TekstilEOL `config/market_volumes.csv`) |
| Årsrapporter fra Fretex, UFF, Kirkens Bymisjon m.fl. | Innsamlede mengder, sortering, ombruk i Norge | hent |
| Watson, Trzepacz, Rubach & Johnsen (2020), *Kartlegging av brukte tekstiler og tekstilavfall i Norge*, NORSUS/PlanMiljø OR 52.20, for Miljødirektoratet | Ankerår 2018: satt på markedet 74 340 t, netthandel 3 300 t, innsamlet 31 690 t, restavfall 25 400 t + gjenbruksstasjoner 6 130 t, usolgt ≥ 700 t | har (litteratur/, lokalt) |
| Mepex-rapporter for Miljødirektoratet om brukte tekstiler og tekstilavfall | Mengder og flyter, flere årganger | verifiser |
| Miljødirektoratets utredning av produsentansvar for tekstiler | Mengder og kanaler | verifiser |
| Nordiske rapporter: Tojo et al. 2012 (TemaNord 2012:545), Palm et al. 2014 (TemaNord 2014:538), Watson et al. 2016 (TemaNord 2016:558) | Historiske nordiske tekstilflyter, blant annet for Norge | hent/verifiser |

### Avfallshåndtering
| Kilde | Innhold | Status |
|---|---|---|
| SSB 05281 (1995–2011) og 10513 (2012–) Avfallsregnskap | Tekstilavfall etter behandlingsmåte, også deponi. **Brudd i 2012:** «Tekstiler» faller fra 113 til 4 kt, trolig fordi tekstiler i restavfall flyttes til «Blandet avfall». Se `claude_tekst/2026-09-29_datainventar_P1-flyter.md` | 10513 har (data_files/); 05281 i NitrogenBudsjett – kopier |
| SSB, *Avfallsregnskap, tekstiler, 1990–1998* (2001) | 1998: 106 kt tekstilavfall (husholdninger 83 kt, klær 47,2 kt), deponi 72 % (79 % i 1991), forbrenning ca. 20 %, gjenvinning/ombruk 8 %. Klær 1991: 34,8 kt | har (bare tallene i nettsideteksten; tabellene er ikke på nett – spør SSB) |
| Plukkanalyser (Mepex, Avfall Norge, kommuner) | Tekstilandel i restavfall | hent |
| SSB husholdningsavfall | Mengder restavfall og grovavfall | hent/verifiser tabell |
| Miljødirektoratet / SSB om avfallseksport | Restavfall eksportert til forbrenning (Sverige) | hent |

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

**Merk:** HS-koden gir hovedfiberen gratis for en stor del av klesimporten. Det gir en empirisk start på fiberlaget.
