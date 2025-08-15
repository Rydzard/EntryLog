from flask import request ,jsonify, session, Blueprint

from blueprints.db import connect_to_database
from psycopg2 import sql

import pandas as pd
from datetime import datetime

guests_bp = Blueprint('guests', __name__)

@guests_bp.route('/api/add_guest', methods=['POST'])
def add_guest():
    try:
        data = request.get_json(force=True)
        
        name = data['name']
        who = data['who']
        date = data['formattedDate']
        why = data['why']
        currentTime = data['currentTime'] 
        chip_number = data['chip']

        if 'vratnik' in session:
            # session obsahuje kľúč 'vratnik'
            vratnik = session['vratnik']
        else:
            # session neobsahuje 'vratnik'
            return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()
        
        cur.execute("SELECT 1 FROM Zamestnanci WHERE Meno = %s", (who,))
        if not cur.fetchone():
            return jsonify({"status": "error", "message": f"Meno '{who}' neexistuje v databáze zamestnancov."}), 400
        
        cur.execute("SELECT 1 FROM hostia WHERE cip = %s", (chip_number,))
        exists = cur.fetchone()

        if chip_number.isnumeric() and exists:
            return jsonify({"status": "error", "message": f"Čip '{chip_number}' už bol niekomu pridelený."}), 400


        insert_query = sql.SQL('''
            INSERT INTO Hostia ("meno", "zamestnanec", "prichod", "odchod", "preco", "cip", "vydal")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''')
        
        cur.execute(insert_query, (name, who, currentTime, date, why, chip_number,vratnik))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "message": "Guest added successfully"}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@guests_bp.route('/api/load_guests', methods=['GET'])
def load_guests():

    
    conn = connect_to_database("mydatabase","myuser","mypassword")
    try:
        df = pd.read_sql('SELECT id, meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM hostia;', conn)
        df[""] = ""
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        conn.close()

@guests_bp.route('/api/load_history', methods=['GET'])
def load_history():

    conn = None
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        # predpokladám, že tabulka História sa volá "historia" (malé písmená, podľa bežnej praxe)
        df = pd.read_sql('SELECT meno, cas, cip, vydal FROM historia;', conn)
        html_table = df.to_html(escape=True, index=False, table_id="table_of_history")
        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        if conn:
            conn.close()

def add_history(chip_number):
    cur = None
    try:
        if 'vratnik' in session:
            vratnik = session['vratnik']
        else:
            return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401


        print("Voslo do funkcie a aj preslo prvu podmienku")

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()
        cur.execute("SELECT meno FROM hostia WHERE cip = %s", (chip_number,))
        result = cur.fetchone()

        if result is None:
            print("Hosť s daným čipom nebol nájdený v databáze.")
            return

        guest_name = result[0]
        time_for_return = datetime.now()
        formatted_time = time_for_return.strftime("%d.%m.%Y %H:%M:%S")

        cur.execute(
            "INSERT INTO historia (meno, cas, cip, vydal) VALUES (%s, %s, %s, %s)",
            (guest_name, formatted_time, chip_number, vratnik)
        )
        conn.commit()




    except Exception as e:
        print(f"Chyba pri ukladaní histórie: {e}")
        raise

    finally:
        if cur:
            cur.close()


@guests_bp.route('/api/search_guests', methods=['GET'])
def search_guests():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        input_string = request.args.get('search_input')

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        cur.execute(
            "SELECT meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM Hostia WHERE meno ILIKE %s",
            (input_string + '%',)
        )
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500

@guests_bp.route('/api/delete_guests', methods=['POST'])
def delete_guests():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        data = request.get_json()
        chip_to_delete = data.get('delete_input')

        if not chip_to_delete or chip_to_delete.strip() == "":
            return jsonify({"status": "error", "message": "Chýba identifikátor"}), 400

        # chip_to_delete nech je rovno string, nech je to číslo alebo text
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # 1. Zmaž hosťa podľa čipu alebo textu
        cur.execute("DELETE FROM Hostia WHERE Cip = %s", (chip_to_delete,))
        add_history(chip_to_delete)

        # 2. Ulož zmenu
        conn.commit()

        # 3. Načítaj aktualizovaný zoznam hostí
        cur.execute("SELECT meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM Hostia")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500

@guests_bp.route('/api/delete_guests_by_id', methods=['POST'])
def delete_guests_by_id():
    try:
        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        data = request.get_json()
        guest_to_delete = data.get('delete_id')
        chip_to_delete = data.get('delete_chip')

        if not guest_to_delete or guest_to_delete.strip() == "":
            return jsonify({"status": "error", "message": "Chýba identifikátor"}), 400

        # chip_to_delete nech je rovno string, nech je to číslo alebo text
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # 1. Zmaž hosťa podľa čipu alebo textu
        cur.execute("DELETE FROM Hostia WHERE id = %s", (guest_to_delete,))

        #pridat do historie ex navstevnika
        add_history(chip_to_delete)
        # 2. Ulož zmenu
        conn.commit()

        # 3. Načítaj aktualizovaný zoznam hostí
        cur.execute("SELECT meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM Hostia")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=True, index=False, table_id="table_of_guests")

        return html_table, 200
    except Exception as e:
        return str(e), 500