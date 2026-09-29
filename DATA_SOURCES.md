# Datakilder

Status: **har** = ligger i `data_files/` og brukes · **hent** = kjent kilde, ikke lastet ned · **verifiser** = kilden eller tabellnummeret er ikke bekreftet og må sjekkes før bruk.

Koden kommenterer hvert oppslag i `preloaded_data` med filnavn og en beskrivelse hentet herfra (samme konvensjon som i NitrogenBudsjett).

## Datafiler i bruk

| Fil | Kilde | Innhold | Brukes i |
|---|---|---|---|
| `Tab_08801_textiles_1988_2024.csv` | SSB tabell 08801, utenrikshandel etter land og varenummer (HS8) | Uttrekk av HS-kapittel 50–64 fra NitrogenBudsjett sin fulle 08801-fil (`scripts/extract_textile_trade.py`). Kolonner: år; import/eksport; HS8; land; supplerende enhet; nettovekt kg; supplerende mengde; verdi NOK. 1988–2024. | `trade.py` (RW, DI) |

## Kandidatkilder per område

### Tilførsel til markedet
| Kilde | Innhold | Status |
|---|---|---|
| SSB 08801 | Import og eksport per HS8, 1988–2024 | har |
| SSB industristatistikk (varestatistikk, NACE 13–15) / Eurostat Prodcom | Norsk produksjon av tekstiler, klær og sko | hent/verifiser tabell |
| SSB grensehandelsstatistikk | Grensehandel i NOK, per varegruppe der det finnes | hent/verifiser |
| SSB forbruksundersøkelsen / nasjonalregnskap (COICOP 03.1, 03.2, 05.2) | Husholdningenes utgifter til klær, sko og hjemmetekstiler, en proxy for trender | hent |
| Tolletaten / SSB om lavverdiforsendelser, VOEC | Direkte netthandel; dekningsgrad i 08801 før og etter 2020 | verifiser |
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
| NORSUS (2023), *Kunnskapsstatus for tekstiler og tekstilavfall i Norge* | 2022: 105,9 kt satt på markedet (19,3 kg/pers), 78,5 kt avfall, 48,8 kt i restavfall, 29,6 kt separat innsamlet, ca. 85 % eksportert | hent (tallene finnes i TekstilEOL `config/market_volumes.csv`) |
| Årsrapporter fra Fretex, UFF, Kirkens Bymisjon m.fl. | Innsamlede mengder, sortering, ombruk i Norge | hent |
| Mepex-rapporter for Miljødirektoratet om brukte tekstiler og tekstilavfall | Mengder og flyter, flere årganger | verifiser |
| Miljødirektoratets utredning av produsentansvar for tekstiler | Mengder og kanaler | verifiser |
| Nordiske rapporter: Tojo et al. 2012 (TemaNord 2012:545), Palm et al. 2014 (TemaNord 2014:538), Watson et al. 2016 (TemaNord 2016:558) | Historiske nordiske tekstilflyter, blant annet for Norge | hent/verifiser |

### Avfallshåndtering
| Kilde | Innhold | Status |
|---|---|---|
| SSB 05281 (1995–2011) og 10513 (2012–) Avfallsregnskap | Tekstilavfall etter behandlingsmåte, også deponi | har i NitrogenBudsjett – kopier |
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
