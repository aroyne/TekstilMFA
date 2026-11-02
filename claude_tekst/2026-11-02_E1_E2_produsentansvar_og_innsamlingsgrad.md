# E1 og E2: grunnlaget for produsentansvaret og innsamlingsgraden, 1988–2025

*Notat 2026-11-02. Beregnet per MC-iterasjon (N = 1000) i [calculations/indicators.py](../calculations/indicators.py), slik at korrelasjonen mellom flytene bevares. Resultatene står i `output_files/MC_indicators.csv`.*

## E1: Grunnlaget for produsentansvaret

**Omfang:** vedlegg 1 i forskriftsforslaget (Miljødirektoratet, høring 2026/4671, fra 1.1.2027): kap. 61 og 62, 6301–6304 (unntatt elektriske tepper), 6309, 6401–6405, 4203 og 6504–6505.
* Dyner og puter (9404), som modellen regner som hjemmetekstiler, er utenfor omfanget.
* Klær av lær (4203) og hatter (6504–6505) finnes ikke i modellens handelsdata og mangler. De er små.
* Utenlandske nettbutikker som selger direkte til norske sluttbrukere, er produsenter. Direkte netthandel (VOEC) er derfor med.

**To varianter:**
* *Brutto* = import i omfanget + norsk produksjon (med samme andel i omfanget som importen) + direkte netthandel + import av brukte klær (6309).
* *Netto* = brutto − eksport i omfanget (gjeneksport) − returer fra direkte netthandel.

| År | Brutto, kt (95 %) | Netto, kt (95 %) |
|---|---|---|
| 1990 | 63 (59–67) | 60 (56–65) |
| 2000 | 86 (80–92) | 83 (77–89) |
| 2010 | 113 (105–122) | 110 (102–118) |
| 2018 | 101 (94–109) | 98 (91–105) |
| 2022 | 108 (101–116) | 102 (95–110) |
| 2023 | 93 (86–100) | 86 (79–93) |
| 2024 | 96 (90–103) | 90 (83–97) |
| 2025 | 104 (95–113) | 95 (87–103) |

* Usikkerheten er ±7–9 %. Den kommer mest fra handelsstatistikken (årlig feil og klassifisering) og VOEC.
* Forskjellen mellom brutto og netto er 3–9 kt per år, og den vokser med gjeneksport og returer. Hvilken variant forskriften faktisk bruker, avhenger av hvordan gjeneksport og returer håndteres i rapporteringen.
* Hoppet fra 2024 til 2025 (+8 kt brutto) kommer nesten bare fra VOEC (3,8 → 14,0 kt). Det kan være registrering like mye som forbruk.

## E2: Innsamlingsgraden

Innsamlet separat fra husholdningene ÷ alt husholdningene kasserer (innsamlet + brukbart og utslitt i restavfall og grovavfall), CL+HT+FW og garn:

| År | Innsamlingsgrad (95 %) |
|---|---|
| 1990 | 2 % (1–4) |
| 2000 | 15 % (10–24) |
| 2010 | 31 % (24–42) |
| 2015 | 43 % (37–50) |
| 2018 | 50 % (42–58) |
| 2020 | 45 % (38–53) |
| 2022 | 40 % (34–50) |
| 2025 | 45 % (38–55) |

* Fallet fra 2018 til 2022 kommer av at restavfallet øker fra 38 til 49 kt mellom kartleggingene, mens innsamlingen er omtrent den samme. Det kan være en metodeforskjell mellom kartleggingene (flere plukkanalyser i 2022), ikke en reell nedgang.
* Kravet om separat innsamling fra 2025 kan ennå ikke etterkontrolleres. 2025-tallet er bare ett år, og intervallet (38–55 %) er bredt. Det krever kartlegginger i 2026–2028.
* Innsamlingsgraden er målt mot det husholdningene kasserer ifølge statistikken, ikke mot det som settes på markedet. Mot grunnlaget for produsentansvaret (brutto) er innsamlingen 35 % i 2025.
