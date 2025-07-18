# IMET_project

# Flask + PostgreSQL Webová Aplikácia

Tento projekt je jednoduchá webová aplikácia postavená na [Flask](https://flask.palletsprojects.com/) frameworku pre backend a PostgreSQL databáze spustenej cez [Docker Compose](https://docs.docker.com/compose/). Frontend je riešený pomocou HTML stránok, ktoré komunikujú s backendovým API.

---

## 💡 Funkcionalita

- Flask backend poskytuje REST API
- PostgreSQL databáza beží v kontajneri (Docker)
- Možnosť ľubovoľného HTML frontendu
- Jednoduché spustenie pomocou Docker Compose

---

## 🧩 Technológie

- Python 3.8+
- Flask
- PostgreSQL
- Docker & Docker Compose
- HTML (ľubovoľné HTML súbory ako frontend)

---

## 🚀 Spustenie projektu

### 1. Spusti kontajnery s databázou:

Uisti sa, že máš nainštalovaný Docker a potom v koreňovom adresári projektu spusť:

```bash
docker compose up -d
```

### 2.Spusti Flask backend:
Uisti sa, že máš nainštalované závislosti (pozri nižšie). Potom spusti aplikáciu:

```bash
python main.py
```
Týmto sa spustí backendové REST API, ktoré používa databázu PostgreSQL z Docker kontajnera.

### 3. Otvor HTML stránku:

Po spustení backendu môžeš v prehliadači otvoriť ľubovoľný HTML súbor, napríklad:

```bash
 templates\index.html
```