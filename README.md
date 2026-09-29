# TekstilMFA – materialstrømsanalyse for tekstiler i Norge

En dynamisk, probabilistisk MFA (Monte Carlo) for klær, hjemmetekstiler og sko i Norge 1990–2024. Arbeidsmetodikken, kodestrukturen og dokumentasjonsformen bygger på NitrogenBudsjett, men systemet er definert fra bunnen av: det finnes ingen offisiell struktur for tekstil-MFA, og vi rapporterer ikke i noe offisielt format.

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
  fibre_composition.csv           fiberandeler (fase 3)
data_files/        Rådata (store filer er ikke i git; se DATA_SOURCES.md)
calculations/      Én modul per pool (rw_mc.py, di_mc.py, ...) og felles hjelpere
  sampling.py      MC-trekk (PERT/lognormal/normal)
  stock_model.py   Dynamisk lagermodell (innstrømsdrevet, Weibull/lognormal)
  trade.py         Flyter fra SSB 08801
data_loader.py     Laster alle data én gang (DATA_MAP)
main_mc.py         MC-driver → output_files/MC_summary.csv
scripts/           Hjelpeskript (uttrekk av data)
tests/             pytest
docs/              PLAN.md, SYSTEMDEFINISJON.md, METODE.md
claude_tekst/      Notater og analyser skrevet av Claude
litteratur/        Kilder (PDF-er, ikke i git)
```

## Kjøring

```bash
python scripts/extract_textile_trade.py        # én gang: henter tekstilrader fra NitrogenBudsjett sin 08801-fil
python -m pytest -q
python main_mc.py --pool all --nsim 1000 --seed 1
```
