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

# 🔧 Nastavenie
V súbore je možnosť zadať IP adresu podľa vlastnej potreby:
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

## Nastavenie fetchov

Fetch slúži na posielanie a prijímanie sprav pomocou REST API. Ale tie spravy sa posielajú na konkrétne IP adresu, ktorá je v súbore app.py v main.
Preto je potrebné ešte prepísať IP adresy vo fetchoch na kompunikaciu. Poprípade aj port ak sa menilo v main. Fetche sa nachádzaju iba v JS suboroch.

## Pripojenie na databázu

V súbore db.py sa nachádza funkica ktorá slúži na pripájanie na databázu. Ak sa budú prenastavovať údaje pre databázu v docker-compose.yaml,či je to meno, heslo, host , tak je potrebné prepísať údaje aj vo funkcii v db.py.


## Nastavenie origin v app.py

Nakoniec je potrebné zmeniť IP adresu aj pre origin v súbore app.py v module CORE, ktorý slúži na počúvanie požiadaviek od zadanej adresy.

```bash
CORS(app, supports_credentials=True, origins=["https://123.456.78.90:5001"])
```

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
Po spustení app.py alebo app.exe sa zobrati cmd terminál aj s https adresou.

Príklad:
```bash
https://123.456.78.90:5001/
```

