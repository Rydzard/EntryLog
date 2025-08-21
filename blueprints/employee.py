from flask import request ,jsonify, session, Blueprint

from blueprints.db import connect_to_database
from psycopg2 import sql

import pandas as pd
from datetime import datetime

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/api/render_employee', methods=['GET'])
def render_employee():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401
        
        
        input_value = request.args.get('search_input')
        
        if not input_value:
            return jsonify({"status": "error", "message": "Chýbajúci vstup."}), 400

        conn = connect_to_database()
        cur = conn.cursor()

        if input_value.isdigit():
            cur.execute(
                "SELECT meno, cip, pracovisko FROM zamestnanci WHERE cip = %s",
                (input_value,)
            )
        else:
            cur.execute(
                "SELECT meno, cip, pracovisko FROM zamestnanci WHERE meno LIKE %s",
                (f"{input_value}",)
            )

        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            return jsonify({"status": "error", "message": "Zamestnanec nebol nájdený"}), 404

        meno, cip, pracovisko = result

        # Volanie funkcie, ktorá vygeneruje tabuľku kľúčov pre daného zamestnanca
        html_table_keys = render_keys(meno)

        employee_data = {
            "name": meno,
            "chip": int(cip),
            "department": pracovisko,
            "keys_table": html_table_keys
        }

        return jsonify(employee_data), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


def render_keys(name):
    try:
        conn = connect_to_database()
        cur = conn.cursor()

        # Získaj kľúče priradené zamestnancovi podľa mena
        cur.execute("SELECT kluc, preco, cas, vydal FROM kluce WHERE meno = %s", (name,))
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        if not rows:
            return "<p>Žiadne kľúče neboli nájdené.</p>"

        # Vytvor Pandas DataFrame a odstráň stĺpec 'name'
        df = pd.DataFrame(rows, columns=colnames)
        if 'name' in df.columns:
            df = df.drop(columns=['name'])

                # Konverzia na DataFrame pre HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč","Prečo", "Čas", "Vydal"])
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")
        return html_table

    except Exception as e:
        return f"<p>Chyba pri načítaní kľúčov: {str(e)}</p>"


@employee_bp.route('/api/add_key', methods=['POST'])
def add_key():
    try:
       
        data = request.get_json()
        name = data.get('name')
        key = data.get('key')
        date = data.get('date_id')
        why = data.get('why_id')
        

        if 'vratnik' in session:
            # session obsahuje kľúč 'vratnik'
            vratnik = session['vratnik']
        else:
            # session neobsahuje 'vratnik'
            return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"})
        
        conn = connect_to_database()
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
            "INSERT INTO Kluce (Kluc, Meno, Preco, Cas, vydal) VALUES (%s, %s, %s, %s, %s)",
            (key, name, why, date,vratnik)
        )

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Údaje boli úspešne uložené."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400



def get_name_by_chip(chip):
    conn = connect_to_database()
    cur = conn.cursor()
    
    cur.execute("SELECT meno FROM Zamestnanci WHERE cip = %s", (chip,))
    result = cur.fetchone()  # Získa prvý riadok výsledku

    cur.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None


@employee_bp.route('/api/return_keys', methods=['POST'])
def return_keys():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        data = request.get_json()

        name = data.get('name_return')
        key = str(data.get('key_return')).strip()

        chip = str(data.get('chip_return')).strip()

        if not name or name.strip() == "":
            name = get_name_by_chip(chip)

        conn = connect_to_database()
        cur = conn.cursor()

        # Skontroluj, či záznam existuje
        cur.execute("""SELECT * FROM Kluce WHERE Meno = %s AND Kluc = %s""", (name, key))
        match = cur.fetchone()

        if not match:
            cur.close()
            conn.close()
            return jsonify({"status": "error","message": f"Kľúč '{key}' nie je priradený zamestnancovi '{name}'."}), 400

        # Odstrániť záznam
        cur.execute("""DELETE FROM Kluce WHERE Meno = %s AND Kluc = %s""", (name, key))

        conn.commit()

        add_history_keys(name,key,session['vratnik'])

        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Kľúč bol úspešne vrátený."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400



@employee_bp.route('/api/load_keys_database', methods=['GET'])
def load_keys_database():
    try:

        conn = connect_to_database()
        cur = conn.cursor()

        # Načítaj všetky údaje z tabuľky Kluce
        cur.execute("SELECT Kluc, Meno, Preco, Cas, vydal FROM Kluce")
        rows = cur.fetchall()

        # Konverzia na DataFrame pre HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Prečo", "Kedy", "Vydal"])
        df[""] = ""
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        cur.close()
        conn.close()

        return html_table, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@employee_bp.route('/api/search_key', methods=['GET'])
def search_key():
    try:
        key = request.args.get('key_number')

        conn = connect_to_database()
        cur = conn.cursor()

        # Vyhľadaj kľúč v databáze
        cur.execute("SELECT Kluc, Meno, Preco,Cas, vydal FROM Kluce WHERE Kluc = %s",(key,))
        rows = cur.fetchall()

        # Premena na HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Prečo", "Kedy","Vydal"])
        df[""] = ""
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        cur.close()
        conn.close()

        return html_table, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    
@employee_bp.route('/api/load_history_keys', methods=['GET'])
def load_history_keys():
    try:
        print("Voslo do historie klucov funkcii")
        conn = connect_to_database()
        cur = conn.cursor()

        # Načítaj všetky údaje z tabuľky Kluce
        cur.execute("SELECT Kluc, Meno, Cas, Vydal FROM historia_kluce ORDER BY Cas DESC")
        rows = cur.fetchall()

        # Konverzia na DataFrame pre HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Kedy", "Vydal"])
        html_table = df.to_html(escape=True, index=False, table_id="table_of_history")

        cur.close()
        conn.close()

        return html_table, 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

def add_history_keys(name,key,vratnik):
    try:
        conn = connect_to_database()
        cur = conn.cursor()

        print(name , key, vratnik)

         # Načítaj všetky údaje z tabuľky Kluce
        cur.execute("SELECT Kluc, Meno, Cas, Vydal FROM Kluce")

        result = cur.fetchone()

        if result is None:
            print("Hosť s daným klucom nebol nájdený v databáze.")
            return

        time_for_return = datetime.now()
        formatted_time = time_for_return.strftime("%d.%m.%Y %H:%M:%S")

        cur.execute(
            "INSERT INTO historia_kluce (Kluc, Meno, Cas, Vydal) VALUES (%s, %s, %s, %s)",
            (key, name, formatted_time, vratnik)
        )
        conn.commit()

        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@employee_bp.route('/api/search_employee_on_history', methods=['POST'])
def search_employee_on_history():
    try:

        if 'vratnik' not in session:
            return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401
        
        data = request.get_json()
        search_key_id = data.get('search_key_id')
        

        if not search_key_id:
            return jsonify({"status": "error", "message": "Chýba identifikátor"}), 400

        # chip_to_delete nech je rovno string, nech je to číslo alebo text
        conn = connect_to_database()
        cur = conn.cursor()

        # 1. Zmaž hosťa podľa čipu alebo textu
        cur.execute("SELECT kluc, meno, cas, vydal FROM historia_kluce WHERE kluc = %s",(search_key_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=["Klúč","Meno", "Kedy", "Vydal"])
        html_table = df.to_html(escape=True, index=False, table_id="table_of_history")

        return html_table, 200
    except Exception as e:
        return str(e), 500