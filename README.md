# TekstilMFA – materialstrømsanalyse for tekstiler i Norge

En dynamisk, probabilistisk MFA (Monte Carlo) for klær, hjemmetekstiler, sko og andre tekstilvarer (tepper, sekker, presenninger m.m.) i Norge 1990–2025. Arbeidsmetodikken, kodestrukturen og dokumentasjonsformen bygger på NitrogenBudsjett, men systemet er definert fra bunnen av: det finnes ingen offisiell struktur for tekstil-MFA, og vi rapporterer ikke i noe offisielt format.

**Status:** tidlig fase. Se [docs/PLAN.md](docs/PLAN.md).

## Struktur

```
system/            Systemregister: processes.csv (pools/subpools) og flows.csv (alle flyter)
parameters/        Parametre med usikkerhet (CSV, samme kolonner som N_parameters.xlsx)
  global_parameters.csv           faste parametre
  time_dependent_parameters.csv   ankerpunkter (år, verdi) for TK-er som endrer seg over tid
  lifetimes.csv                   levetidsfordelinger per produkt og lager
  dataset_uncertainties.csv       støy per datasett
  hs_mapping.csv                  HS-prefiks → produktgruppe
  hs_main_fibre.csv               hovedfiber per HS8-kode (fiberlaget)
  fibre_composition.csv           fibergrupper for HS-koder uten oppgitt fiber
data_files/        Rådata (store filer er ikke i git; se DATA_SOURCES.md)
calculations/      Én modul per pool (rw_mc.py, di_mc.py, ...) og felles hjelpere
  sampling.py      MC-trekk (PERT/lognormal/normal)
  system.py        Bygger flodym-systemet fra registeret og lukker det (kontroll, lagre, massebalanse)
  fibre_layer.py   Fiberlaget (D19): fordeler TOT på fibergrupper og ikke-tekstil, med årgangsmodell for US.HH
  trade.py         Flyter fra SSB 08801
data_loader.py     Laster alle data én gang (DATA_MAP)
main_mc.py         MC-driver → output_files/MC_summary.csv (TOT) og MC_summary_fibre.csv (per materiale)
scripts/           Hjelpeskript (uttrekk av data)
tests/             pytest
docs/              PLAN.md, SYSTEMDEFINISJON.md, METODE.md
claude_tekst/      Notater og analyser skrevet av Claude
litteratur/        Kilder (PDF-er, ikke i git)
```

## Kjøring

Modellen bruker [flodym](https://github.com/pik-piam/flodym) (`pip install flodym`, Python ≥ 3.10) i tillegg til numpy, pandas og scipy.

```bash
python scripts/extract_textile_trade.py                 # én gang: tekstilrader 1988– fra NitrogenBudsjett sin 08801-fil
python scripts/update_trade_ssb_api.py 2023 2024 2025   # nyeste år (og revisjoner) fra SSB API
python -m pytest -q
python main_mc.py --pool all --nsim 1000 --seed 1
python scripts/build_hs_main_fibre.py                   # hovedfiber per HS8-kode fra varetekstene i 08801
python scripts/build_fibre_composition.py               # fibergrupper for HS-koder uten oppgitt fiber
python scripts/plot_core_flows.py                       # figur: kjerneflyter i husholdningene
python scripts/plot_stock_model.py                      # figur: statistikk mot parallell lagermodell
```
