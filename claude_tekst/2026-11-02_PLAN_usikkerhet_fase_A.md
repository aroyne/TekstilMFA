# Plan for fase A: robust usikkerhet

*Notat 2026-11-02. Beslutningene i avsnitt 5 er tatt (alle «ja»), og A0 (strømmer, rydding, konvergens) og A1–A3 er implementert samme dag (D39). Bygger på prinsippene fra NitrogenBudsjett ([plan 2026-10-14](../../NitrogenBudsjett/claude_tekst/2026-10-14_PLAN_usikkerhetshaandtering.md) og det som faktisk ble implementert i `mc_sampler.py` og `uncertainty_contributions.py` der). Tallene er fra `output_files/MC_summary.csv` (N = 1000, frø 1), slik modellen står etter D36.*

## 1. Dagens oppsett

| Element | Slik er det nå | Hvor |
|---|---|---|
| Parametre | Én trekning per parameter og iterasjon, felles for alle år og flyter. 20 globale parametre, hvorav 14 trekkes | `parameters/global_parameters.csv`, `params.py` |
| Datasett | Én multiplikativ faktor per datasett og iterasjon, felles for alle år og flyter. Bare fire datasett har grenser: 08801 (±5 %), grensehandel (±10 %), totalkalkylen (±5 %), vareproduksjon (−10/+50 %) | `dataset_uncertainties.csv` |
| Ankerpunkter | Hvert ankerpunkt trekkes **uavhengig** av de andre i samme serie (75 rader) | `time_dependent_parameters.csv`, `anchor_values.csv` |
| År mellom og utenfor ankerpunkter | Lognormal faktor med CV 2 % per år fra nærmeste anker (interpolasjon) og 5 % per år (ekstrapolasjon), tak 100 %, én trekning per serie og gap, klippet ved ±2σ (D30) | `timeseries.py` (GapNoise) |
| Levetider | Middelverdien trekkes (PERT), formparameteren er fast lik 2 | `lifetimes.csv` |
| Fordelinger | PERT nesten overalt, én lognormal (ikke i bruk) | kolonnen `distribution_type` |
| Tolkning av grensene | PERT: **min og maks**. Lognormal og normal med `abs`: 95 %-intervall. Lognormal og normal med `perc`: **±1 standardavvik** | `sampling.py` |
| Trekk | Én felles RNG-strøm. Rekkefølgen av trekkene avhenger av rekkefølgen i tabellene | `main_mc.py`, `params.py` |
| Rådata | `MC_Raw_Simulations.csv.gz` har flytene per iterasjon, ikke de trukne verdiene | `main_mc.py --export-raw-mc` |

### Bredden i resultatene i dag (halvt 95 %-intervall, CORE)

| Flyt | 1995 | 2010 | 2018 | 2025 |
|---|---|---|---|---|
| Import av ferdigvarer (CL) | 4 % | 4 % | 4 % | 4 % |
| Separat innsamling fra husholdningene | 33 % | 6 % | 4 % | 4 % |
| Restavfall, utslitte tekstiler | 191 % | 27 % | 26 % | 25 % |
| Lagerendring, husholdningene (restledd) | 131 % | 20 % | 39 % | 115 % |
| Lager, husholdningene (restledd) | 82 % | 64 % | 53 % | 52 % |
| Lager, lagermodellen (CL) | 26 % | 25 % | – | 30 % |

## 2. Hva NitrogenBudsjett valgte (beslutninger 2026-10-18 og senere)

* **Grensene er 95 %-intervall** (2,5- og 97,5-persentil), som hos Schäppi og IPCC. PERT er faset ut. Fordelingen følger av hvordan grensene er gitt: normal for symmetriske grenser opp til ±40 % (avkuttet ved 0), lognormal for grenser som er symmetriske i log-rom (faktor 2 osv.), triangulær ellers og for størrelser med en hard grense ved 0 eller 1. Kolonnen `bounds = minmax` markerer litteraturspenn som er min og maks.
* **Én RNG-strøm per element**, avledet fra hovedfrøet og (gruppe, id). Når et element legges til eller endres, påvirker det ikke trekkene for de andre.
* **`annual_draw` per datasett** (ja eller nei, ikke en andel). Registrerte data og utvalgsundersøkelser trekkes på nytt hvert år, mens modellbaserte kilder, inventarer, antakelser og skjøtefaktorer trekkes én gang.
* **Deler av et datasett** (et anlegg, en sektor) kan få egne, uavhengige faktorer fra samme rad (`sub_factor`).
* **Utfylte år** får `u(d) = u0 + k·d` (øvre 95 %-grense, med tak) per type utfylling (interpolasjon, flatt, ekstrapolasjon), med én normaltrekning per flyt og periode. Det tilsvarer vår GapNoise (D30).
* **Bidragsanalyse uten lagrede trekk:** én sporet kjøring registrerer hvilke kilder hver flyt leser. Hver kilde økes med 10 %, og elastisiteten ganget med kildens relative standardavvik gir variansbidraget. Resultatet vises i et usikkerhetsavsnitt på flytsiden og aggregeres for balanser og totaler.

## 3. Problemer i TekstilMFA

**T1. Grensene betyr ulike ting, og én gren er feil.**
* PERT med ±X % som min/maks tilsvarer omtrent ±0,7X som 95 %-intervall. ±5 % på 08801 gir altså ±3,5 % i praksis.
* I `sampling.py` blir `perc` med normal eller lognormal regnet som ±1 standardavvik (`std_dev = X/100 · val`), mens `abs` regnes som 95 % (`/1.96`). Det har ingen effekt i dag, fordi ingen rad med `perc` bruker lognormal. **Men D37 og D38 foreslår lognormal**, så dette må rettes før de implementeres.

**T2. Handelsdataene (08801) har én faktor på ±5 % for alt.**
* Den samme faktoren brukes for import og eksport, for alle produkter og for alle år, og den gjelder også eksporten av brukte tekstiler (6309). Feilen er dermed fullt korrelert mellom import og gjeneksport, og den forsvinner i trender.
* Innsamlingen fra husholdningene er eksport ÷ eksportandel (D31), og får derfor bare ±4 % fra 2018. Kalibreringspunkt: SSBs eksport er 5,6 kt (ca. 15 %) større enn det innsamlerne rapporterer (NORSUS 2026).
* Usikkerheten i om tollkoden fanger produktet (klassifisering av 6309 og 6310, nettovekt mot vekt med emballasje, HS-revisjoner, lavverdisendinger uten HS) er ikke med. Den er strukturell (T6) eller må inn som en egen systematisk faktor.

**T3. Ankerpunktene i samme serie er uavhengige.**
* `residual_core` 2009/2018/2022/2025 (±40/30/30/30 %) trekkes uavhengig, selv om tre av dem bygger på den samme metoden (Mepex-plukkanalyser oppskalert av NORSUS). En metodefeil som er felles for alle ankerpunktene, er ikke med. Kalibreringspunkt: gjenvinningsstasjonene ga 6,1 kt i 2018 (3 analyser) og 15,2 kt i 2022.
* **Dette avgjør usikkerheten i lageret.** Lageret er summen av restleddet over tid. Systematiske feil i kasseringene hoper seg opp lineært, mens uavhengige feil delvis kansellerer hverandre. Intervallet på ±52 % for lageret i 2025 er derfor trolig for smalt for nivået og for bredt for trenden.

**T4. Mange kilder har ingen usikkerhet eller ingen begrunnelse.**
* Uten usikkerhet: hs_mapping (fordeling av HS-koder på produkter), fibre_composition og hs_main_fibre (D19), formparameteren i levetidene og folketallet (det siste er greit).
* `uncertainty_source` er tom for `online_direct_*` (VOEC) og `residual_core`, og er «assumption» for `landfill_share_residual`, som kommer fra SSB.
* De fleste grensene er runde tall (10, 30, 50 %) uten en regel for hvordan de er valgt.

**T5. Skjøter mellom kilder har ingen egen usikkerhet.** Eksempler i modellen:
* VOEC fra 2023 (null i 2019, lineært mellom).
* Privatimport holdt på 2004-nivå før 2004.
* Deponiandel fra SSB-avfallsregnskapet (1990–1998) → 05281 → 10513.
* Eksportandeler for innsamling fra 2018 brukt bakover (D17).
* Produktandeler i norsk produksjon mellom varetall 1989 og Prodcom 2008 (19 år med interpolasjon).

**T6. Strukturelle valg ligger utenfor MC-en.** Eksempler: D8 (lageret i husholdningene som restledd), D31 (innsamling fra eksport i stedet for innsamlernes tall), gjeneksport, at institusjonsandelen tas av tilførselen, VOEC brutto (D38), innsvinging fra 1950 (D2), Weibull med form 2 og lineær interpolasjon. Noen av disse er trolig større enn parameterusikkerheten.

**T7. Ingen bidragsanalyse og ingen stabile trekk.** Med én felles RNG-strøm endres alle trekk når en parameter legges til. Uten en bidragsanalyse vet vi ikke hva som driver ±52 % i lageret, ±115 % i lagerendringen eller ±25 % i restavfallet.

**T8. Konvergens og innsvinging er ikke testet.** N = 1000 er ikke sjekket mot et annet frø eller større N, og innsvingingen fra 1950 er ikke testet (D2).

**T9. Død kode i parametertabellene.** Radene `10513`, `05281` og `trend interpolation` i `dataset_uncertainties.csv` og `laundry_release_rate`, `wwtp_retention` og `lowvalue_undercoverage_CL` står som `todo` og brukes ikke i koden.

## 4. Arbeidspakker

Rekkefølgen er valgt slik at diagnosen kommer før verdiene endres. Numrene viser til fase A i PLAN.

| AP | Innhold | Endrer resultatene? | Omfang |
|---|---|---|---|
| **A0** Trekk og diagnose (A6, A7) | Én RNG-strøm per element (som `item_rng` i N). Sporet kjøring og elastisitetsbasert bidragsanalyse (som `uncertainty_contributions.py`) for hovedstørrelsene: lageret og lagerendringen i husholdningene, innsamlingsgraden, det som settes på markedet (grunnlaget for produsentansvaret), restavfall og eksport av brukte tekstiler. Konvergenstest med to frø og N = 2000. Rydde T9 | Nei (bare andre tilfeldige trekk) | Middels |
| **A1** Tolkning av grensene (A1) | 95 %-intervall overalt, fordelingsregelen fra N, kolonnen `bounds` (`minmax` for litteraturspenn). Rette T1 i `sampling.py` | Ja: bredere bånd der PERT brukes i dag | Lite i koden, middels i tabellene |
| **A2** Lett pedigree (A2) | Ny kolonne `source_type` (1 registrert eller tellet, 2 utvalgsundersøkelse, 3 modellbasert statistikk, 4 ekspertanslag eller antakelse) og en kort begrunnelse per rad. Grensene settes etter type og sjekkes mot kalibreringspunktene (tabell under) | Ja | Middels |
| **A3** Systematisk og årlig del (A3) | `annual_draw` per datasett som i N. 08801 deles i import, eksport og brukte tekstiler, og trekkes årlig. Klassifiseringsfeilen (T2) blir en egen systematisk faktor. Ankerserier som deler metode, får en felles metodefaktor i tillegg til de uavhengige trekkene (T3) | Ja: mer realistisk lager og trend | Middels |
| **A4** Skjøter og utfylte år (A4) | Egne skjøtefaktorer for T5. Nivåene i D30 vurderes på nytt mot N sin tabell `fill_uncertainties` | Ja | Lite til middels |
| **A5** Struktur (A5) | Følsomhetskjøringer for T6 med et flagg i `main_mc.py` (`--variant`), og en tabell som viser effekten på hovedstørrelsene | Nei (egne kjøringer) | Middels |

### Utkast til kildetyper og kalibreringspunkter

| Kilde | Type | Grenser i dag | Kalibreringspunkt |
|---|---|---|---|
| SSB 08801, import og eksport | 1, men med usikker klassifisering | ±5 % min/maks | Bruttoimporten ligger ca. 2 kt (ca. 2 %) fra NORSUS. Eksporten av brukte tekstiler er 15 % over innsamlernes tall |
| VOEC via NORSUS | 1 (registrert), men nytt og brutto | ±50 % | Hoppet 3,8 → 14,0 kt i 2024–2025 (registrering eller forbruk) |
| Mepex-plukkanalyser (`residual_core`) | 2, få analyser | ±30 % | 2018 mot 2022 for gjenvinningsstasjonene: 6,1 mot 15,2 kt |
| Laitala 2012 (`residual_core` 2009) | 3 (oppskalert fra Oslo) | ±40 % | – |
| Grensehandel (SSB 05678/14221) | 2 | ±10 % | – |
| Totalkalkylen ull | 1 + anslag | ±5 % | Ull i FAOSTAT mot andre kilder: +7–34 % (N-prosjektet) |
| Industristatistikk og Prodcom | 2, dekker bare store enheter | −10/+50 % | SNL håndstrikkegarn ca. 1 kt mot 0,6–1,0 kt |
| Innsamlernes egne tall | 2–3 | ±20–100 % | – |
| Institusjonsandel 12 % (Danmark) | 4 | 0,04–0,15 | Nedre grense 3–4 % fra Eurostat TEC (D36) |
| Levetider | 4 (forslag fra litteraturen) | PERT, middelverdi | Fase C kalibrerer mot garderobedata |

## 5. Beslutninger du må ta

1. **Fordelingsregelen fra N** (95 %, PERT ut, normal/lognormal/triangulær etter hvordan grensene er gitt)? *Anbefalt: ja*, slik at tabellene leses likt i begge prosjektene. Unntak: parametre av type 4 (ekspertanslag uten data) får flat fordeling innenfor spennet, slik at vi ikke later som vi vet hvor modusen ligger ([Weijenberg m.fl. 2026](2026-11-02_Weijenberg_robust_tiltaksvurdering.md)).
2. **Årlige trekk for 08801**, delt i import, eksport og brukte tekstiler, og en egen systematisk faktor for klassifisering? *Anbefalt: ja.* Uten en systematisk del blir lageret for sikkert, fordi årlige feil i importen kansellerer hverandre over 37 år.
3. **Felles metodefaktor for ankerserier** som bygger på samme metode (Mepex-plukkanalysene, innsamlernes tall)? *Anbefalt: ja*, med omtrent halvparten av variansen i den felles faktoren som utgangspunkt.
4. **Rekkefølge:** A0 først (ingen endring i resultatene), deretter A1–A4 i én runde med én ny N = 1000-kjøring? *Anbefalt: ja.* Fase B (D37, D38) kan implementeres parallelt, men bør bruke den nye fordelingsregelen.
