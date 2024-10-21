# GQL_Admissions - Deníček

__Tomáš Kyseľ,__ 
__Jakub Vágner,__ 
__Lukáš Zdražílek,__ 
________________________________________________________________________

<div style="display: flex;">
  <img src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi.qkme.me%2FDT1.jpg&f=1&nofb=1&ipt=29524da4934a16ecce3113def5671ffa17ed0ca2f03b1ec6272343a198b6d0cb&ipo=images" style="width: 30%">
  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FDcXYPtOVAAAoOKa.jpg&f=1&nofb=1&ipt=0fc47f721244bc99d0a6437e702c8b96f4e700beec4126987c92975e234f23e9&ipo=images" style="width: 30%">
</div>

Pracujeme s UG (user), GRANTING a DOCUMENTS

- Otevření, uzavření přihlášky
- Více programů studia
- Stejná user struktura
- Autentizace neřešit (generace login, hesla, nebo přes soc. sítě)
- 1 uložení přihlášky, 2. odeslání přihlášky (lze vzít zpět do konce přihlašování)
- UG má state transition, state machine, vygenerovat (podaná, odeslaná, vzatá zpět)
- Vymazat nebo archivovat minulé přihlášky?
- Více zkoušek = relace 1 ku N, přihláška má testy, tabulka testů cizí klíč, ke které přihlášce se vztahuje, disciplíny cizí klíč na test
- Přihláška = propojení studenta a programu, program = předměty, předměty = disciplíny
- Jednotná entita disciplíny pro všechny
- Fakulty sdílí testy (nechat být)
- Přidat percentil umístění
- Peníze neřešit
- Práva ke čtení userů budou řešeny přes skupiny
- User bude mít stavovou entitu (Přihlašuje se / Student)

- Dle evolution vytvoření struktur databází

### Rozvržení databáze
<img src="database_structure.png" alt="Nefunguje">


## Aktuální úkoly

- [x] Fork hrbolek/gql_events jako template pro naše Admissions a nasdílet

- [x] Udělat hrubý náčrt databázové struktury

- [] Seznámení se se stylem tvoření reálné databázové struktury (gql_events/src/DBDefinitions.py)

- [] Vytvoření reálné databázové struktury s parametry pro gql_admissions

________________________________________________________________________

## Harmonogram skupinové práce pro Admissions část IS

__7.10.2024__ vybraná témata, publikované repositories

__11.10.2024__ analýza kódu 5_SQLalchemy 

__7.11.2024__ 1. projektový den, doložení kompletních descriptions (gql modely)

__9.12.2024__ 2. projektový den, doložení funkcionality (crud)

__29.1.2025__ 3. projektový den, doložení testů
