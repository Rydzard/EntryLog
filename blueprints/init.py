from .db import connect_to_database

def init_db():
    conn = connect_to_database()
    cur = conn.cursor()

    # historia
    cur.execute("""
        CREATE TABLE IF NOT EXISTS historia (
            id SERIAL PRIMARY KEY,
            meno VARCHAR(50) NOT NULL,
            cas VARCHAR(50) NOT NULL,
            cip TEXT,
            vydal TEXT NOT NULL
        )
    """)

    # historia_kluce
    cur.execute("""
        CREATE TABLE IF NOT EXISTS historia_kluce (
            id SERIAL PRIMARY KEY,
            meno VARCHAR(50) NOT NULL,
            cas VARCHAR(50) NOT NULL,
            kluc TEXT NOT NULL,
            vydal TEXT NOT NULL
        )
    """)

    # hostia
    cur.execute("""
        CREATE TABLE IF NOT EXISTS hostia (
            id SERIAL PRIMARY KEY,
            meno VARCHAR(50) NOT NULL,
            zamestnanec VARCHAR(50) NOT NULL,
            prichod VARCHAR(50) NOT NULL,
            preco VARCHAR(50) NOT NULL,
            cip TEXT,
            vydal TEXT NOT NULL
        )
    """)

    # kluce
    cur.execute("""
        CREATE TABLE IF NOT EXISTS kluce (
            id SERIAL PRIMARY KEY,
            kluc REAL NOT NULL,
            meno VARCHAR(50) NOT NULL,
            preco VARCHAR(50) NOT NULL,
            cas VARCHAR(50) NOT NULL,
            vydal TEXT NOT NULL
        )
    """)

    # vratnici
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vratnici (
            name_surname CHAR(30) NOT NULL,
            chip TEXT NOT NULL
        )
    """)

    # zamestnanci
    cur.execute("""
        CREATE TABLE IF NOT EXISTS zamestnanci (
            id SERIAL PRIMARY KEY,
            meno VARCHAR(50) NOT NULL,
            pracovisko VARCHAR(50) NOT NULL,
            cip INTEGER NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Všetky tabuľky boli vytvorené (ak neexistovali).")