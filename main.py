from flask import Flask, request ,jsonify
import psycopg2
from psycopg2 import sql

import pandas as pd
from pandasql import sqldf
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)


def connect_to_database(dbname, user, password, host='localhost', port='5432'):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

@app.route('/add_guest', methods=['POST'])
def add_guest():
    try:
        data = request.get_json(force=True)
        
        name = data['name']
        who = data['who']
        date = data['formattedDate']   # očakávam formát 'YYYY-MM-DD'
        why = data['why']
        currentTime = data['currentTime']  # tiež 'YYYY-MM-DD' alebo datetime string podľa DB
        chip_number = data['chip']
        
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()
        
        insert_query = sql.SQL('''
            INSERT INTO Hostia ("meno", "zamestnanec", "prichod", "odchod", "preco", "cip")
            VALUES (%s, %s, %s, %s, %s, %s)
        ''')
        
        cur.execute(insert_query, (name, who, currentTime, date, why, chip_number))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Guest added successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/load_guests', methods=['GET'])
def load_guests():
    conn = connect_to_database("mydatabase","myuser","mypassword")
    try:
        df = pd.read_sql('SELECT * FROM hostia;', conn)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")
        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        conn.close()

@app.route('/load_history', methods=['GET'])
def load_history():
    conn = None
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        # predpokladám, že tabulka História sa volá "historia" (malé písmená, podľa bežnej praxe)
        df = pd.read_sql('SELECT * FROM historia;', conn)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_history")
        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        if conn:
            conn.close()

def add_history(chip_number):
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        cur.execute("SELECT meno FROM hostia WHERE cip = %s", (chip_number,))
        result = cur.fetchone()

        if result is None:
            print("❌ Hosť s daným čipom nebol nájdený v databáze.")
            return

        meno_hosta = result[0]
        cas_vratenia = datetime.now()

        cur.execute(
            "INSERT INTO historia (meno, cas, cip) VALUES (%s, %s, %s)",
            (meno_hosta, cas_vratenia, chip_number)
        )
        conn.commit()
        print("✅ Záznam o vrátení bol úspešne uložený do histórie.")

    except Exception as e:
        print(f"Chyba pri ukladaní histórie: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/search_guests', methods=['POST'])
def search_guests():
    try:
        data = request.get_json()
        input_string = data.get('search_input')

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM Hostia WHERE Meno ILIKE %s",
            (input_string + '%',)
        )
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500



@app.route('/delete_guests', methods=['POST'])
def delete_guests():
    try:
        data = request.get_json()
        chip_to_delete = data.get('delete_input')

        chip_to_delete = int(chip_to_delete)
        
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # 1. Zmaž hosťa podľa čipu
        cur.execute("DELETE FROM Hostia WHERE Cip = %s", (chip_to_delete,))

        add_history(chip_to_delete)

        # 2. Ulož zmenu
        conn.commit()

        # 3. Načítaj aktualizovaný zoznam hostí
        cur.execute("SELECT * FROM Hostia")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500

@app.route('/render_employee', methods=['POST'])
def render_employee():
    try:
        data = request.get_json()
        input_value = data.get('input_string')

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Rozlíšime, či je vstup čip (číslo) alebo meno (text)
        if isinstance(input_value, int) or (isinstance(input_value, str) and input_value.isdigit()):
            cur.execute("SELECT meno, cip, pracovisko FROM zamestnanci WHERE cip = %s", (int(input_value),))
        else:
            cur.execute("SELECT meno, cip, pracovisko FROM zamestnanci WHERE meno = %s", (input_value,))

        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            return jsonify({"status": "error", "message": "Zamestnanec nebol nájdený"}), 404

        meno, cip, pracovisko = result

        # Zavoláme funkciu, ktorá vygeneruje HTML tabuľku kľúčov (napr. podľa mena)
        html_table_keys = render_keys(meno)

        employee_data = [{
            "name": meno,
            "chip": int(cip),
            "department": pracovisko,
            "keys_table": html_table_keys
        }]

        return jsonify(employee_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    
def render_keys(meno):
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Získaj kľúče priradené zamestnancovi podľa mena
        cur.execute("SELECT * FROM kluce WHERE meno = %s", (meno,))
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        if not rows:
            return "<p>Žiadne kľúče neboli nájdené.</p>"

        # Vytvor Pandas DataFrame a odstráň stĺpec 'meno'
        df = pd.DataFrame(rows, columns=colnames)
        if 'meno' in df.columns:
            df = df.drop(columns=['meno'])

        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")
        return html_table

    except Exception as e:
        return f"<p>Chyba pri načítaní kľúčov: {str(e)}</p>"


@app.route('/add_key', methods=['POST'])
def add_key():
    try:
        data = request.get_json()
        name = data.get('name')
        key = data.get('key')
        date = data.get('date_id')
        why = data.get('why_id')

        if not date:
            date = "Nepriradené"
        
        if not why:
            why = "Nepriradené"

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Over, či klúč už existuje
        cur.execute("SELECT 1 FROM Kluce WHERE Kluc = %s", (key,))
        if cur.fetchone():
            return jsonify({"status": "error", "message": "Tento kľúč už je vydaný!"}), 400

        # Over, či meno existuje v tabuľke zamestnancov
        cur.execute("SELECT 1 FROM Zamestnanci WHERE Meno = %s", (name,))
        if not cur.fetchone():
            return jsonify({"status": "error", "message": f"Meno '{name}' neexistuje v databáze zamestnancov."}), 400

        # Vlož nový záznam
        cur.execute(
            "INSERT INTO Kluce (Kluc, Meno, Preco, Cas) VALUES (%s, %s, %s, %s)",
            (key, name, why, date)
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Údaje boli úspešne uložené."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/return_keys', methods=['POST'])
def return_keys():
    try:
        data = request.get_json()

        name = str(data.get('name_return')).strip()
        key = str(data.get('key_return')).strip()

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Skontroluj, či záznam existuje
        cur.execute("""
            SELECT * FROM Kluce
            WHERE Meno = %s AND Kluc = %s
        """, (name, key))
        match = cur.fetchone()

        if not match:
            cur.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": f"Kľúč '{key}' nie je priradený zamestnancovi '{name}'."
            }), 400

        # Odstrániť záznam
        cur.execute("""
            DELETE FROM Kluce
            WHERE Meno = %s AND Kluc = %s
        """, (name, key))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Kľúč bol úspešne vrátený."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/load_keys_database', methods=['GET'])
def load_keys_database():
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Načítaj všetky údaje z tabuľky Kluce
        cur.execute("SELECT Kluc, Meno, Preco, Cas FROM Kluce")
        rows = cur.fetchall()

        # Konverzia na DataFrame pre HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Prečo", "Kedy"])
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        cur.close()
        conn.close()

        return html_table, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/search_key', methods=['POST'])
def search_key():
    try:
        data = request.get_json()
        key = data.get('key_number')

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Vyhľadaj kľúč v databáze
        cur.execute("SELECT Kluc, Meno, Preco, Cas FROM Kluce WHERE Kluc = %s", (int(key),))
        rows = cur.fetchall()

        # Premena na HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Prečo", "Kedy"])
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        cur.close()
        conn.close()

        return html_table, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400



def create_all_tables():
    conn = None
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()
        
        # Vytvorenie tabuľky guests
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Hostia (
            id SERIAL PRIMARY KEY,
            Meno VARCHAR(50) NOT NULL,
            Zamestnanec VARCHAR(50) NOT NULL,
            Prichod VARCHAR(50) NOT NULL,
            Odchod VARCHAR(50) NOT NULL,
            Preco VARCHAR(50) NOT NULL,
            Cip INTEGER NOT NULL
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Zamestnanci (
            id SERIAL PRIMARY KEY,
            Meno VARCHAR(50) NOT NULL,
            Cip INTEGER NOT NULL,
            Pracovisko VARCHAR(50) NOT NULL
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Historia (
            id SERIAL PRIMARY KEY,
            Meno VARCHAR(50) NOT NULL,
            Cas VARCHAR(50) NOT NULL,
            Cip INTEGER NOT NULL
        );
        ''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS Kluce (
            id SERIAL PRIMARY KEY,
            Kluc INTEGER NOT NULL,
            Meno VARCHAR(50) NOT NULL,
            Preco VARCHAR(50) NOT NULL,
            Cas VARCHAR(50) NOT NULL
        );
        ''')

        
        conn.commit()
        cur.close()
        print("Všetky tabuľky boli úspešne vytvorené alebo už existujú.")
    except Exception as e:
        print(f"Chyba pri vytváraní tabuliek: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_all_tables()
    app.run(port=5000,debug=True)