# GQL_Admissions - Deníček

__Tomáš Kyseľ,__ 
__Jakub Vágner,__ 
__Lukáš Zdražílek,__ 
________________________________________________________________________

<div style="display: flex;">
  <img src="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fi.qkme.me%2FDT1.jpg&f=1&nofb=1&ipt=29524da4934a16ecce3113def5671ffa17ed0ca2f03b1ec6272343a198b6d0cb&ipo=images" style="width: 30%">
  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpbs.twimg.com%2Fmedia%2FDcXYPtOVAAAoOKa.jpg&f=1&nofb=1&ipt=0fc47f721244bc99d0a6437e702c8b96f4e700beec4126987c92975e234f23e9&ipo=images" style="width: 30%">
</div>


## Progress of work
- [x]  15.11. Dokončeny READ operace na GQL modelech, chybí Link
- [x]  19.11. Dokončeny CREATE operace na GQL modelech


## Aktuální úkoly

- [x] Fork hrbolek/gql_events jako template pro naše Admissions a nasdílet

- [x] Udělat hrubý náčrt databázové struktury

- [x] Seznámení se se stylem tvoření reálné databázové struktury (gql_events/src/DBDefinitions.py)

- [x] Vytvořit modely tabulek 

- [x] Zprovoznit reálné vytvoření tabulek

- [x] Dokončit READ operace na GQL modelech

- [x] Dokončit CREATE operace na GQL modelech

- [x] Dokončit UPDATE operace na GQL modelech

- [x] Dokončit DELETE operace na GQL modelech

- [x] Dokončit Disciplíny

- [x] Dokončit Payments

- [x] Dokončit Testy

- [x] Odstraněno Many to many, testy 95%

- [x] Publish docker image 


________________________________________________________________________

## Harmonogram skupinové práce pro Admissions část IS

__7.10.2024__ vybraná témata, publikované repositories

__11.10.2024__ analýza kódu 5_SQLalchemy 

__20.10.2024__ vytvoření modelů tabulek v DBDefinitions

__30.10.2024__ konzultace ohledně tvorby tabulek

__31.10.2024__ zprovoznění tvorby tabulek v postgres/data

__1.11.2024__ práce na GraphResolver a GraphPermissions

__4.11.2024__ práce na finální struktuře tabulek v databázi + přidání užitečného kódu z hrbolek/gql_admissions

__6.11.2024__ dokončení finální struktuře tabulek v databázi

__7.11.2024__ 1. projektový den, doložení kompletních descriptions (gql modely)

__8.11.2024__ opravy chyb po projektovém dni

__13.11.2024__ vytvoření DBFeeder a Dataloaders

__15.11.2024__ práce na GQL modelech

__16.11.2024__ dokončení GQL modelů, úprava DBDefinitions

__18.11.2024__ práce na CREATE, vytvoření prvních mutací

__19.11.2024__ vytvořen CREATE

__22.11.2024__ vytvořen UPDATE

__24.11.2024__ vytvoření nových funkcí pro CREATE, UPDATE a DELETE

__25.11.2024__ implementace a testy nových CREATE a UPDATE funkcí

__26.11.2024__ práce na Disciplínách a linku

__27.11.2024__ práce na SECRET datatypu, UUUID, implementace nových UPDATE a DELETE funkcí

__2.12.2024__ implementace a testy nových DELETE funkcí

__9.12.2024__ 2. projektový den, doložení funkcionality (crud)

__14.12.2024__ Prvotní úplné testy - 75 %

__18.12.2024__ Konzultace ohledně errorů v testech

__6.1.2025__ Testy po konzultaci a fixu některých errorů - 85 %

__10.1.2025__ Předělání Base a ostatních GQL modelů dle nových požadavků

__11.1.2025__ Testy po předělání GQL - 92 %

__14.1.2025__ Práce na Payments CRUD

__15.1.2025__ Fix UUID test erroru

__16.1.2025__ Práce na PaymentInfo CRUD

__20.1.2025__ Fix query test HEX erroru  

__21.1.2025__ Rebase (nový main)

__22.1.2025__ Fix všech errorů testů - 93 %

__23.1.2025__ Práce na Payments a PaymentsInfo testech

__24.1.2025__ Práce na many to many - EDIT many to many odstraněno

__27.1.2025__ Finální revize - vše v pořádku

__28.1.2025__ Publish docker image

__29.1.2025__ 3. projektový den, doložení testů
