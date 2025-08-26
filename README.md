# IMET_project

# Flask + PostgreSQL Webová Aplikácia

Tento projekt je jednoduchá webová aplikácia postavená na [Flask](https://flask.palletsprojects.com/) frameworku pre backend a PostgreSQL databáze spustenej cez [Docker Compose](https://docs.docker.com/compose/). Frontend je riešený pomocou HTML stránok, ktoré komunikujú s backendovým API.

---

## 💡 Funkcionalita

- Flask backend poskytuje REST API  
- PostgreSQL databáza beží v kontajneri (Docker)  
- Možnosť použiť ľubovoľný HTML frontend  
- Jednoduché spustenie pomocou Docker Compose  

---

## 🧩 Technológie

- Python 3.8+  
- Flask  
- PostgreSQL  
- Docker & Docker Compose  
- HTML  
- CSS  
- JS  

---

# 🐘 Databáza PostgreSQL

Pri databáze ako je napríklad PostgreSQL sú 2 možné spôsoby ako spojazdniť.

## 1. možnosť 
### Použitie Dockeru


Ak aplikácia beží na serveri alebo chcete jednoduchú distribúciu, odporúča sa používať Docker s oficiálnym PostgreSQL image.
Docker zabezpečí, že databáza sa spustí rovnakým spôsobom na každom počítači, izolovane a s minimálnymi nastaveniami.

Tak treba prenastaviť údaje aj v docker-compose.yaml súbore ale aj v blueprints/db.py súbore

```bash
DB_HOST = "IP_servera"
DB_PORT = 5432
DB_USER = "meno_uzivatela"
DB_PASSWORD = "heslo"
DB_NAME = "nazov_databazy"
```

Tak isto aj v docker-compose.yaml súbore treba zmeniť port na konkretnu IP adresu servera

```bash
ports:
     - "IP_servera:5432:5432"
```

Podstatné je aby boli rovnaké údaje v dockeri aj v db.py súbore.
Ale treba zabezpečiť aby server povolil komunikovať s počítačom vrátnika.
Ak sa všetko nastavilo správne tak stačí spustiť docker-compose (treba mať spustený aj docker). 


Príklad spustenia databázy cez Docker Compose ktorý sa nachádza v projekte:
```bash
docker compose up -d
```

-d nie je potrebný, pretože slúži len na spustenie kontajnera na pozadí, aby CMD zostalo voľné.

Po úspešnom spustení sa dá dostať do adminera, cez link: 
```bash
http://localhost:8080/
```

Link sa nastavuje v docker-compose.yaml súbore, ale zatiaľ je tam defaultne na lokálnej IP adresne 127.0.0.1:8080. V admineri sa dá sledovať databáza, prenastavovať struktúru databazy, poprípade pridat zamestnanca (da sa aj pomocou importu CSV súboru s údajmi)


## 2. možnosť
### Lokálna inštalácia

Ak aplikácia beží len lokálne (napr. pre vývoj alebo testovanie), je možné nainštalovať [PostgreSQL](https://www.postgresql.org/download) nativne na OS.
Databáza sa spúšťa automaticky pri štarte systému a v tom prípade sa nemusí spúšťať Docker kontajnery.
Ako aj pri Dockeri aj tu sa dá v admineri sledovať databázu, prenastavovať struktúru databazy, poprípade pridat zamestnanca aj cez CSV súbor.

To sa môže stiahnúť aj vratnikovi do počítača, a aplikácia sa automaticky pripojí na tú konkrétnu databázu. Len tiež treba tak nastaviť údaje vo funkcii connect_to_database() v db.py súbore.

# 🔧 Nastavenie
Systém sa dá spustiť aj na inej IP adrese ako je localhost a je možnosť zadať inú IP adresu podľa vlastnej potreby:
```bash
if __name__ == "__main__":
     app.run(ssl_context=('certifikat/certifikat.pem', 'certifikat/certifikat-key.pem'), port=5001, host='123.456.78.90')
```
Je to na konci súboru app.py

## ⚠️ Podstatná vec

## Nastavenie certifikátu

Keďže aplikacia beží na protokole HTTPS (kvôli session ID), je potrebné vytvoriť si vlastný certifikát. Certifikát je platný každé 3 mesiace, ktoré je jednoduché obnoviť pomocou nástroju [Mkcert](https://github.com/FiloSottile/mkcert). Certifikát je potrebý vytvoriť na danú IP adresu, ktorá bude používať aplikácia.

```bash
mkcert "IP adressa" localhost
```

Po vytvorení certifikátu stačí len pridať do ssl_context čo je vyššie v súbore app.py v main.
Preto je potrebné mať platný certifikát aby po spustení nebolo potrebné kliknúť na 'Vstúpiť nebezpečne na stránku', ale hlavne preto že Session ID by sa ani nevytvoril a v tom prípade aplikacia nedovolí sa prilásiť do systému, keďže Sessions sú povolené len pre HTTPS protokol.

Ak sa budú znovu vytvoriť certifikáty, stačí ho uložiť do priečinka 'certifikat' pod rovnakými názvami súborov ako staršie certifikáty, pričom nové súbory budú aktuálne.

## Nastavenie fetchov

Fetch slúži na posielanie a prijímanie sprav pomocou REST API. Ale tie správy sa posielajú na konkrétnu IP adresu, ktorá je v súbore app.py v main.
Preto je potrebné ešte prepísať IP adresy vo fetchoch na kompunikaciu. Poprípade aj port ak sa menilo v main. Ale to nám stačí len prepísať konštantu, ktorá ukladá link url, ktorá sa ukladá do fetchu.

URL konštanta je v súbore static/script/app.js:
```bash
const BASE_URL = "https://localhost:5001/api";
```
Jedine čo treba zmeniť je IP adresa alebo port podľa vlastnej potreby.

## Pripojenie na databázu

V súbore db.py sa nachádza funkica ktorá slúži na pripájanie na databázu. Ak sa budú prenastavovať údaje pre databázu v docker-compose.yaml, či je to meno, heslo, host, tak je potrebné prepísať údaje aj vo funkcii v db.py.


## Nastavenie origin v app.py

Potrebné je zmeniť IP adresu aj pre origin v súbore app.py v module CORE, ktorý slúži na počúvanie požiadaviek od zadanej adresy.

Príklad:
```bash
CORS(app, supports_credentials=True, origins=["https://123.456.78.90:5001"])
```
## pyInstaller a exe subor

Existuje knižnica pyInstaller, ktorá dokáže convertovat Python aplikáciu na jednoduchý .exe súbor. Ak sa menili nejake údaje, tak je potrebné spustiť tento command:

```bash
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --add-data "certifikat;certifikat" --distpath . app.py
```
ktorý vytvorí .exe súbor aj so zmenami, pretože celá aplikácia sa zabalí s aktualnou verziou aplikacie.

# 🚀 Spustenie projektu

### 1. Spustenie kontajnerov s databázou:

Je potrebné uistiť sa, že je nainštalovaný Docker. Následne v koreňovom adresári projektu spustiť:

```bash
docker compose up -d
```

### 2. Spustenie Flask backendu:
Je potrebné nainštalovať všetky závislosti (pozri nižšie). Potom je možné spustiť aplikáciu:

```bash
python app.py
```

alebo spustiť 

```bash
app.exe
```

### 3. Otvorenie web stránky:
Po spustení app.py alebo app.exe sa zobrati cmd terminál aj s HTTPS adresou.

Príklad:
```bash
https://123.456.78.90:5001/
```

