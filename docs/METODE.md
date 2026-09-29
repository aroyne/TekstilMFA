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

Rekkefølgen i beregningen følger varestrømmen: RW/MA → DI → US → CO/WM → EN. Hver prosess har høyst én *balanseflyt*, og den regnes ut som restledd. Alle andre flyter kommer fra data, parametre eller lagermodellen. Balansene sjekkes i hver MC-iterasjon. En negativ balanseflyt betyr at dataene ikke er konsistente, og skal gi en tydelig feil. Den skal ikke klippes til null i det stille. Ubalanse mellom kasseringer fra lagermodellen og uavhengig avfallsstatistikk vises som diagnostikk (beslutning D8).

## 3. Dynamisk lagermodell (US.HH, US.IC, WM.LF)

Implementert i [calculations/stock_model.py](../calculations/stock_model.py) og testet i [tests/test_stock_model.py](../tests/test_stock_model.py).

* Innstrømsdrevet: I(t) er summen av innstrømmene til lageret, altså salg til husholdninger, privatimport og kjøp av brukt.
* Levetid: Weibull (standard) eller lognormal per produktgruppe. Parametrene er middellevetid og form ([parameters/lifetimes.csv](../parameters/lifetimes.csv)).
* Diskret konvensjon: S(a) er andelen av en årgang som fortsatt er i lageret a år etter at den kom inn. Da blir lager(t) − lager(t−1) = I(t) − O(t) eksakt.
* Innsvinging: Innstrømmen før 1988 er ukjent. Den settes til 1988-nivået (eller en trend) i et antall innsvingingsår, og valget testes i en følsomhetsanalyse (D2).
* Kontroller: Lager per innbygger sammenlignes med garderobestudier (SIFO/OsloMet). Utstrømmen sammenlignes med avfall pluss innsamling (NORSUS 2023, plukkanalyser).
* Produkter som behandles som emballasje (sekker, SA) får levetiden `immediate`: alt kasseres samme år, og det bygges ikke opp lager (D13).
* Kjøp av brukt (CO.RE → US.HH) går inn som en ny årgang, med samme eller kortere restlevetid (egen parameter).

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
* **Kjent fallgruve fra N-budsjettet:** Når en flyt bytter datakilde ved en årsgrense, må periodene ikke overlappe. Overlappende år gir doble rader per iterasjon og forskyver fordelingen.

## 6. Handelsdata (SSB 08801)

* HS8-koder med suffikset `_<år>` (koden er gyldig fra det året). Kodene mappes til produktgruppe via **lengste prefiks** i [parameters/hs_mapping.csv](../parameters/hs_mapping.csv), på 2- eller 4-sifret nivå. Det tåler omlegginger av HS8-koder bedre enn en fullstendig 8-sifret liste.
* `amount` = nettovekt i kg. `supp_quantity` = stykk (S) eller par (P). `value_nok` = verdi.
* Stykk og verdi brukes til kontroll: kg per plagg over tid, og NOK/kg for å regne om privatimport fra kroner til masse.
* Første kontroll (2022): Import minus eksport for CL+HT+FW er ≈ 94,7 kt, mot 105,9 kt satt på markedet ifølge NORSUS (2023). Differansen (≈ 11 kt) er av den størrelsen vi venter for privatimport, direkte netthandel og norsk produksjon.

## 7. Mikrofibre (WM.WW, EN)

Massemessig er dette små flyter, men de er viktige for miljøet. Frigjøringen modelleres som lageret i bruk × frigjøringsrate per år, deretter fordelt med renseanleggets tilbakeholdelse (andel primær- og sekundærrensing i Norge, SSB) og slambruk. Egen prioritet (P2), og flytene skal kunne vises separat i resultatene.

## Referanser (metode)

* Brunner, P. H. & Rechberger, H. (2016). *Handbook of Material Flow Analysis*, 2nd ed. CRC Press.
* Laner, D., Rechberger, H. & Astrup, T. (2014). Systematic evaluation of uncertainty in material flow analysis. *J. Ind. Ecol.* 18(6).
* Laner, D., Feketitsch, J., Rechberger, H. & Fellner, J. (2016). A novel approach to characterize data uncertainty in MFA and its application to plastics flows in Austria. *J. Ind. Ecol.* 20(5).
* Müller, E., Hilty, L. M., Widmer, R., Schluep, M. & Faulstich, M. (2014). Modeling metal stocks and flows: a review of dynamic material flow analysis methods. *Environ. Sci. Technol.* 48(4).
* Bornhöft, N. A. et al. (2016). A dynamic probabilistic material flow modeling method. *Environ. Model. Softw.* 76. (i Termo-tekstil-litteraturen)
* «A high-resolution dynamic probabilistic material flow analysis of seven plastic polymers; A case study of Norway» (i Termo-tekstil-litteraturen): nærmeste metodiske sammenligning for Norge.
* Pauliuk, S. & Heeren, N. (2020). ODYM – An open software framework for studying dynamic material systems. *J. Ind. Ecol.* 24(3). (Alternativ til egen lagermodell. Vi velger egen implementasjon for å holde koden konsistent med NitrogenBudsjett.)

*Bibliografiske detaljer skal verifiseres og legges i `library.bib` før de brukes på nettsidene.*
