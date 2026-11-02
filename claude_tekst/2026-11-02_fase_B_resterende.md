# Fase B: resterende punkter (forslag)

*Notat 2026-11-02. Besluttet samme dag: (1) de tre flytene er fjernet, (2) ext_tec05 er vurdert og gir ingen ny nedre grense per produkt (se D36), (3) sekkespørsmålet er lagt i [HENVENDELSER.md](../docs/HENVENDELSER.md), (4) fibermatrisen er implementert (D41).*

## 1. Tre planlagte flyter uten data

Alle tre står som `planned` i [system/flows.csv](../system/flows.csv) og har ingen kode.

| Flyt | Situasjon | Forslag |
|---|---|---|
| `US.IC-CO.CO` innsamling fra institusjoner | Ingen data. Det institusjonene leverer til innsamlerne, eksporteres som 6309. Etter D31 er det dermed allerede med i «Separate collection from households», som er eksport minus donerte usolgte varer. NTGs mottak fra institusjoner er egen flyt til WM.RC (D34). | **Fjernes fra registeret.** D31 får en setning om at innsamlingen fra husholdninger kan inneholde noe fra næringslivet. |
| `CO.SO-RW.RW` eksport av sortert | Eksporten av brukte tekstiler (6309 og 6310) er én serie i 08801, og den skiller ikke sortert fra usortert. Det som sorteres i Norge og eksporteres, er derfor med i eksporten fra CO.CO (D31, D32). | **Fjernes.** En egen flyt ville kreve en andel uten kilde og ville bare flytte masse mellom to eksportflyter. |
| `CO.RE-WM.RS` usolgte bruktvarer | Ankerpunktene for ombruk gjelder det som faktisk er solgt. Usolgte varer sorteres om av innsamlerne og havner i eksport eller sorteringsrester (D33). | **Fjernes.** |

Fordel: Registeret viser bare flyter som finnes i modellen, og systemdiagrammet blir enklere. Ulempe: Flytene forsvinner som påminnelser. De kan i stedet stå i PLAN som mulige utvidelser når produsentansvaret gir rapporteringsdata (fra 2027–2028).

## 2. Parameterforslagene og institusjonsandelen per produkt

* Forslagene i avsnitt 5.4 i [litteraturnotatet](2026-10-05_litteraturgjennomgang_oppdatert.md) er implementert, men levetidene står som `proposal`. De kalibreres i fase C. **Forslag:** Punktet flyttes til fase C.
* `institutional_share` er én verdi for alle produkter (12 %, 4–15 %). Eurostat ext_tec05 gir andelen av importen som går direkte til næringsliv og offentlig sektor per HS-kapittel. Nedre grense finnes i dag bare for klær (3–4 %). **Forslag:** Hente ext_tec05 for kap. 63 (hjemmetekstiler og andre konfeksjonerte varer) og 64 (sko), og sette en nedre grense per produkt. Den øvre grensen og den sentrale verdien er fortsatt antakelser.

## 3. Sekker

D13 er besluttet: Sekker går til US.IC og kastes samme år, telles med i tilført masse og holdes utenfor sammenligninger med avfallsstatistikk. Det åpne spørsmålet er om de registreres som plastemballasje eller tekstil i SSBs avfallsstatistikk. Det endrer ikke modellen, bare tolkningen av sammenligningene. **Forslag:** Spørsmålet tas med i henvendelsen til SSB (sammen med 05281 og tekstilregnskapet for 1990–1998), og punktet lukkes i fase B.

## 4. Fiberlaget

* **Matrise fra hovedfiber til fiberandeler.** I dag regnes et plagg der tollkoden sier bomull, som 100 % bomull. Tollreglene klassifiserer etter fiberen som utgjør størst vekt, så blandinger (for eksempel bomull med elastan eller polyester) havner under hovedfiberen. **Forslag:** En enkel matrise der hovedfiberen utgjør en andel *a* (for eksempel 0,85, 0,7–1,0, flat fordeling) og resten fordeles på syntetisk. Kilde for *a* må finnes. Kandidater er PEFCR Apparel & Footwear (sammensetningen til referanseproduktene) og Textile Exchange.
* **Restposter (RES, UNK):** fordeles i dag med `fibre_composition.csv`. Ingen endring er foreslått.
* **Ull:** Modellen gir ca. 5 % ull, mens målinger gir ca. 3 %. Matrisen over vil trekke ull ned, fordi ullplagg ofte er blandinger.

Fiberlaget endrer ikke massene (D19). Det haster derfor mindre enn fase C.

## Spørsmål til deg

1. Skal de tre planlagte flytene fjernes fra registeret?
2. Skal ext_tec05 hentes for kap. 63 og 64, slik at institusjonsandelen får nedre grense per produkt?
3. Skal sekkespørsmålet tas med i SSB-henvendelsen og punktet lukkes?
4. Skal matrisen for fiberandeler vente til etter fase C?
