# Metode – Tekstil-MFA for Norge

*Levende dokument. Beskriver metoden slik den er og slik den er planlagt. Status per del står i [PLAN.md](PLAN.md).*

## 1. Utgangspunkt og forskjeller fra NitrogenBudsjett

Rammeverket er arvet fra NitrogenBudsjett: pool/subpool/flyt-struktur, flytkoder, én funksjon per flyt, parametertabeller med usikkerhetsgrenser, Monte Carlo med en deterministisk runde 0, oppsummering med median og 95 %-intervall, og dokumentasjon per flyt på GitHub Pages med manuelle tekstblokker. Tre ting er annerledes:

| | NitrogenBudsjett | TekstilMFA |
|---|---|---|
| Struktur | Gitt av INMS-veilederen (Winiwarter et al., 2025) | Egen struktur (se [SYSTEMDEFINISJON.md](SYSTEMDEFINISJON.md)) |
| Rapportering | Offisiell Excel-mal (`Report.xlsx`) | Ingen offisiell mal. Resultatene er CSV og nettside. |
| Lager | Ingen eksplisitte lager; flyter per år | **Lagre i bruk er sentrale.** Dynamisk, innstrømsdrevet lagermodell med levetidsfordelinger. |
| Dimensjoner | Flyt × år | Flyt × produktgruppe × år (fibertype senere) |
| Tilfeldige tall | Global `np.random` | `np.random.Generator` med valgfritt frø (`--seed`), slik at kjøringer kan reproduseres |

## 2. Massebalanse

For hver prosess og hvert år skal følgende gjelde:

  Σ innstrømmer − Σ utstrømmer = lagerendring (0 for prosesser uten lager)

Rekkefølgen i beregningen følger varestrømmen: RW/MA → DI → US → CO/WM → EN. Hver prosess har høyst én *balanseflyt*, og den regnes ut som restledd. Alle andre flyter kommer fra data, parametre eller lagermodellen. Balansene sjekkes i hver MC-iterasjon. En negativ balanseflyt betyr at dataene ikke er konsistente, og skal gi en tydelig feil. Den skal ikke klippes til null i det stille. **Kildehierarki (D8):** Kasseringer og avfallsflyter hentes fra offisielle kilder: først SSB og Miljødirektoratet, deretter rapporter bestilt av myndighetene (NORSUS, Mepex), og deretter aktørenes egne tall (innsamlere). For prosessene med lager i bruk (US.HH, US.IC) er lagerendringen restleddet:

  ΔLager(t) = tilført(t) − kassert(t), der kassert(t) kommer fra avfallsstatistikken

Lagerendringen kan være negativ, i motsetning til en balanseflyt. Lageret i bruk blir den akkumulerte summen fra et startlager (D2). Systematiske feil i avfalls- eller tilførselsdataene hoper seg da opp i lageret. Et urimelig lager (sammenlignet med garderobestudier og lagermodellen) er derfor et diskusjonspunkt i seg selv.

## 3. Dynamisk lagermodell (US.HH, US.IC, WM.LF)

Implementert med flodyms `InflowDrivenDSM` i [calculations/fibre_layer.py](../calculations/fibre_layer.py), foreløpig for CL+HT+FW i US.HH. Der gir modellen sammensetningen av kasseringene i fiberlaget (§ 9). Levetidene står i [parameters/lifetimes.csv](../parameters/lifetimes.csv) (forslag, se litteraturnotatet 2026-10-05 § 5), og middellevetiden trekkes i hver MC-iterasjon. Den parallelle sammenligningen av utstrømmen med avfallsstatistikken er ikke rapportert ennå.

**Rolle (D8):** Lagermodellen er et *parallelt, uavhengig anslag*. Kasseringene i hovedresultatet kommer fra avfallsstatistikken. Lagermodellen gir kasseringer og lager ut fra tilførsel og levetid, og de sammenlignes med hovedresultatet per år og produktgruppe. Forskjellene brukes som diskusjonsgrunnlag: er levetidene riktige, vokser lageret av klær som ikke brukes, er noen avfallsstrømmer underrapportert? Lagermodellen brukes også for mikrofibre (frigjøring ∝ lager i bruk) og for deponilageret (WM.LF).

* Innstrømsdrevet: I(t) er nye varer til husholdningene, altså salg, privatimport og direkte netthandel. Kjøp av brukt (1–2 % av innstrømmen) er foreløpig holdt utenfor.
* Levetid: Weibull (standard) eller lognormal per produktgruppe. Parametrene er middellevetid og form ([parameters/lifetimes.csv](../parameters/lifetimes.csv)).
* Tidskonvensjon (D20): Flytene er summer per kalenderår, og lageret er nivået ved årsslutt. Innstrømmen regnes som om den kom midt i året, så en årgang er 0,5, 1,5, 2,5 … år gammel ved årsslutt. Da blir lager(t) − lager(t−1) = I(t) − O(t) eksakt.
* Innsvinging: Innstrømmen før 1988 er ukjent. Den settes til 1988-nivået (eller en trend) i et antall innsvingingsår, og valget testes i en følsomhetsanalyse (D2).
* Sammenligning: Utstrømmen sammenlignes med kasseringene i avfallsstatistikken. Lageret sammenlignes med det akkumulerte restleddet og med garderobestudier (SIFO/OsloMet).
* Produkter som behandles som emballasje (sekker, SA) får levetiden `immediate`: alt kasseres samme år, og det bygges ikke opp lager (D13).

## 4. Overføringskoeffisienter (TK) som endrer seg over tid

Andeler som varierer over tid, som innsamlingsgrad, eksportandel og deponiandel, legges inn som **ankerpunkter** (år, verdi, usikkerhet) i [parameters/time_dependent_parameters.csv](../parameters/time_dependent_parameters.csv). Mellom ankerpunktene interpoleres det lineært. Før første og etter siste ankerpunkt holdes verdien konstant. Hvert ankerpunkt trekkes i MC. Interpolerte år får i tillegg en egen støyfaktor (`trend interpolation`), slik som i NitrogenBudsjett. Kjente regimeskifter kodes som harde brudd, ikke som glatt interpolasjon, for eksempel forbudet mot å deponere biologisk nedbrytbart avfall fra 2009 og VOEC-ordningen fra 2020.

TK-er ut av samme prosess må summere til 1. Når flere av dem trekkes samtidig, normaliseres de, eller de trekkes med en Dirichlet-fordeling.

## 5. Usikkerhet og Monte Carlo

Oppsettet er det samme som i NitrogenBudsjett:

* Parametre og datasett har `lower_bound`, `upper_bound`, `uncertainty_type` (perc/abs) og `distribution_type` (PERT/lognormal/normal). Trekkingen skjer i [calculations/sampling.py](../calculations/sampling.py).
* Runde 0 er deterministisk. Rundene 1..n trekker alle parametre og én multiplikativ støyfaktor per datasett.
* **Korrelasjon over tid:** Én faktor per datasett og iterasjon betyr at en systematisk feil (for eksempel underrapportering av vekt) er fullt korrelert over alle år. Det er riktig for nivået. Trenden i hver iterasjon blir da kun påvirket av parametre som varierer med tid. Om det trengs, kan det legges til en uavhengig støy per år (tilfeldig feil).
* **Datakvalitet:** Usikkerhetsgrensene settes systematisk. Planen er en pedigree-matrise som oversetter datakvalitet (pålitelighet, fullstendighet, tids-, geografisk og teknologisk relevans) til en variasjonskoeffisient (Laner et al., 2016). Dette erstatter faste ±20 % per kildetype. Poengsummen lagres per datasett og parameter, slik at valget kan etterprøves.
* **Lagermodell i MC:** Levetidsparametrene trekkes per iterasjon, og hele lagermodellen kjøres på nytt per iterasjon. Da forplanter usikkerheten i levetiden seg riktig til både lager og utstrømmer.
* **Resultat:** median, 2,5- og 97,5-persentil og den deterministiske verdien per flyt × produkt × år ([main_mc.py](../main_mc.py)). Rådata kan eksporteres med `--export-raw-mc` til trendanalyser.
* **Følsomhet:** Rangkorrelasjon (Spearman) mellom trukne input og nøkkelresultater (lager 2024, kasseringer, innsamlingsgrad). Det krever at trekkene lagres per iterasjon (planlagt).
* **Konvergens:** Sjekk at median og persentiler er stabile for n = 1000 mot 5000.
* **Kjent fallgruve fra N-budsjettet:** Når en flyt bytter datakilde ved en årsgrense, må periodene ikke overlappe. Ellers telles overlappsårene to ganger, og fordelingen forskyves.

## 6. Handelsdata (SSB 08801)

* HS8-koder med suffikset `_<år>` (koden er gyldig fra det året). Kodene mappes til produktgruppe via **lengste prefiks** i [parameters/hs_mapping.csv](../parameters/hs_mapping.csv), på 2- eller 4-sifret nivå. Det tåler omlegginger av HS8-koder bedre enn en fullstendig 8-sifret liste.
* `amount` = nettovekt i kg. `supp_quantity` = stykk (S) eller par (P). `value_nok` = verdi.
* Stykk og verdi brukes til kontroll: kg per plagg over tid, og NOK/kg for å regne om privatimport fra kroner til masse.
* Første kontroll (2022): Import minus eksport for CL+HT+FW er ≈ 94,7 kt, mot 105,9 kt satt på markedet ifølge NORSUS (2023). Differansen (≈ 11 kt) er av den størrelsen vi venter for privatimport, direkte netthandel og norsk produksjon.

## 7. Mikrofibre (WM.WW, EN)

Massemessig er dette små flyter, men de er viktige for miljøet. Frigjøringen modelleres som lageret i bruk × frigjøringsrate per år, deretter fordelt med renseanleggets tilbakeholdelse (andel primær- og sekundærrensing i Norge, SSB) og slambruk. Egen prioritet (P2), og flytene skal kunne vises separat i resultatene.

## 8. Implementering

* **Rammeverk:** Systemet er bygget i [flodym](https://github.com/pik-piam/flodym) (PIK, MIT-lisens), etterfølgeren til ODYM. `calculations/system.py` bygger systemet én gang fra registeret: prosesser, implementerte flyter med dimensjoner (`dims`) og lagre (`stock_dims`). MC-trekkingen, parametertabellene og ankerpunktene er våre egne. flodym har ikke Monte Carlo.
* **Rekkefølge:** Hver iterasjon setter alle flyter til NaN, og deretter kjører poolene i varestrømmens rekkefølge: `rw → di → co → us → wm` (`main_mc.py`). En pool leser flytene fra poolene før den direkte fra systemet (`mfa.flows[kode].values`). Til slutt lukkes systemet (`close()`). Det sjekker at ingen flyt er NaN eller negativ, beregner lagrene fra flytene og sjekker massebalansen. En flyt som ingen pool setter, gir feil.
* **Resultater** lagres som én array per flyt (iterasjon × år × produkt) og oppsummeres til `output_files/MC_summary.csv`. Raden har flyt, produkt eller produktgruppe, år, median, 2,5- og 97,5-persentil, antall iterasjoner og den deterministiske verdien. Datakilder og metode dokumenteres i koden og på md-siden per flyt, ikke per rad.
* **Handelsdata** summeres per retning, kategori, produkt og år én gang før MC-løkka (`aggregate_trade`). I hver iterasjon brukes bare støyfaktoren. 1 000 iterasjoner tar ca. 6 s.
* **Ankerpunkter:** Andeler og rater ligger i `parameters/time_dependent_parameters.csv`, og observerte mengder fra rapporter i `data_files/anchor_values.csv`. Begge har samme format og trekkes likt: hvert ankerpunkt for seg, med egen fordeling. Mellom ankerpunktene interpoleres det lineært (`calculations/timeseries.py`), og før første og etter siste holdes verdien konstant.
* **Lagerendring** er innstrømmer minus utstrømmer for prosessens lager i flodym. Den rapporteres som en flyt fra prosessen til seg selv (`US.HH-US.HH-Stock change-TOT` osv.).
* **Produktdimensjon:** `p` (produkt) til og med salg og i US.IC, `g` (produktgruppe, der CORE = CL+HT+FW) for innsamling, restavfall og sortering, og ingen produktdimensjon (`ALL`) for avfallsbehandlingen.
* **Kjerneflyter:**
  * **Privatimport (D16):** SSB NOK ÷ (tollverdi per kg × påslag), fordelt på CL og FW etter importert masse.
  * **Direkte netthandel (D7):** ankerpunkter.
  * **Salg (DI.RT-balansen):** import − eksport, fordelt på husholdninger og næringsliv/offentlig etter `institutional_share`. Sekker (SA) går til US.IC.
  * **Innsamling (D17):** eksport av HS 6309+6310 + andelen som beholdes i Norge.
  * **Restavfall (D15):** ankerpunkter.
  * **Deponi og forbrenning (D15):** deponiandel fra SSB.
  * **Eksport av restavfall (D11):** eksportandel fra SSB 13035, 2015–2025.
  * **Lagerendring i US.HH:** restledd (D8).
* Åpne spørsmål og forenklinger: `claude_tekst/2026-09-29_sporsmal_fase2.md`.

## 9. Tekstilform og fiberlag (D18, D19)

**Tekstilform (D18)** er kolonnen `form` i `system/flows.csv` (FIB, FAB, NEW, MIX, USE, WRN, PCW, MFR). Den er en egenskap ved flyten, ikke en dimensjon. Der en blandet flyt har et tall av egen interesse, deles den. Tekstiler i restavfall fra husholdningene er derfor to flyter: brukbare (USE) og utslitte (WRN). Andelen brukbart er ankerpunkter fra plukkanalysene: 27,5 % (2011, snitt av Oslo 2010 og 2011, Laitala m.fl. 2012), 45 % (2022, bare restavfall som hentes hjemme) og 40 % (2025). Den gjelder CORE-gruppen. CA, TA og OM regnes som utslitte.

**Fiberlaget (D19)** ([calculations/fibre_layer.py](../calculations/fibre_layer.py)) er et eget flodym-system med de samme prosessene og flytene og en ekstra dimensjon `m`: SYN, CO, WO, CV, OTH og NT (ikke-tekstil). Det fylles etter at TOT-systemet er lukket, og endrer aldri TOT. Summen over `m` er lik TOT (det sjekkes), og massebalansen sjekkes per materiale.

* **Tilført:** hovedfiberen i HS-koden (`parameters/hs_main_fibre.csv`) gir sammensetningen av registrert import per produkt og år. «Kjemiske fibre» uten nærmere angivelse (MMF) deles med `mmf_synthetic_share` (0,92, Textile Exchange 2024). Koder uten fiber (RES, UNK) fordeles med `parameters/fibre_composition.csv` (PEFCR 2025 for CL og FW, ellers produktets egne koder med oppgitt fiber). Tekstildelen skaleres med 1 − `nontextile_share_<produkt>`. Eksport, salg, privatimport, netthandel og institusjonsavfall får importsammensetningen. Eksport er for det meste gjeneksport (D6).
* **Kassert fra husholdningene:** For CL+HT+FW kommer sammensetningen fra utstrømmen av årgangsmodellen (§ 3). Den gjelder innsamling, restavfall (brukbart og utslitt får samme sammensetning) og alt gjennom CO. CA, TA og OM kasseres samme år og beholder tilførselssammensetningen.
* **Avfallsbehandling:** Flytene ut av WM.RS får blandingen av alt som går inn i WM.RS det året.
* **Forenklinger:** Hovedfiberen regnes som hele tekstildelen. En matrise fra hovedfiber til fiberandeler mangler. Levetidene er like for alle fibre, selv om litteraturen tyder på lengre levetid for syntetiske plagg (Laitala m.fl. 2018; IMPRO 2014). `fibre_composition.csv` har ingen usikkerhet.
* **Resultat:** `output_files/MC_summary_fibre.csv` (flyt × produkt × materiale × år).
* **Validering:** Syntetisk andel av tekstilet i det som kastes er ca. 40 % (2021), 41 % (2022) og 42 % (2025), mot målt 44 % (Syversen 2023, 2021) og 38 % (Mepex via Rubach 2023, 2022). Syntetisk + NT er 51 % i 2025, mot 48,3 % fossilbasert målt (de Sadeleer & Rubach 2026). NT omfatter også lær og naturgummi. Ull blir ca. 5 %, mot 3 % målt.

## Referanser (metode)

* Brunner, P. H. & Rechberger, H. (2016). *Handbook of Material Flow Analysis*, 2nd ed. CRC Press.
* Laner, D., Rechberger, H. & Astrup, T. (2014). Systematic evaluation of uncertainty in material flow analysis. *J. Ind. Ecol.* 18(6).
* Laner, D., Feketitsch, J., Rechberger, H. & Fellner, J. (2016). A novel approach to characterize data uncertainty in MFA and its application to plastics flows in Austria. *J. Ind. Ecol.* 20(5).
* Müller, E., Hilty, L. M., Widmer, R., Schluep, M. & Faulstich, M. (2014). Modeling metal stocks and flows: a review of dynamic material flow analysis methods. *Environ. Sci. Technol.* 48(4).
* Bornhöft, N. A. et al. (2016). A dynamic probabilistic material flow modeling method. *Environ. Model. Softw.* 76. (i Termo-tekstil-litteraturen)
* «A high-resolution dynamic probabilistic material flow analysis of seven plastic polymers; A case study of Norway» (i Termo-tekstil-litteraturen): nærmeste metodiske sammenligning for Norge.
* Pauliuk, S. & Heeren, N. (2020). ODYM – An open software framework for studying dynamic material systems. *J. Ind. Ecol.* 24(3). (Alternativ til egen lagermodell. Vi velger egen implementasjon for å holde koden konsistent med NitrogenBudsjett.)

*Bibliografiske detaljer skal verifiseres og legges i `library.bib` før de brukes på nettsidene.*
