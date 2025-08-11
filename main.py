from flask import Flask, request ,jsonify, make_response, render_template, session

from blueprints.db import connect_to_database
from psycopg2 import sql



import pandas as pd
from flask_cors import CORS
from datetime import datetime,timedelta

from werkzeug.security import check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # musí byť nastavený, inak session nebude fungovať
app.permanent_session_lifetime = timedelta(days=1)

CORS(app)

@app.route('/api/add_guest', methods=['POST'])
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
        if cur.fetchone():
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

@app.route('/api/load_guests', methods=['GET'])
def load_guests():
    conn = connect_to_database("mydatabase","myuser","mypassword")
    try:
        df = pd.read_sql('SELECT meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM hostia;', conn)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")
        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        conn.close()

@app.route('/api/load_history', methods=['GET'])
def load_history():
    conn = None
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        # predpokladám, že tabulka História sa volá "historia" (malé písmená, podľa bežnej praxe)
        df = pd.read_sql('SELECT meno, cas, cip, vydal FROM historia;', conn)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_history")
        return html_table, 200
    except Exception as e:
        return str(e), 500
    finally:
        if conn:
            conn.close()

def add_history(chip_number, conn):
    cur = None
    try:
        if 'vratnik' in session:
            vratnik = session['vratnik']
        else:
            return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

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


@app.route('/api/search_guests', methods=['GET'])
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
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500

@app.route('/api/delete_guests', methods=['POST'])
def delete_guests():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401

        data = request.get_json()
        chip_to_delete = data.get('delete_input')

        if(not chip_to_delete.isnumeric()):
            return jsonify({"status": "error", "message": "Neplatný čip."}), 400

        chip_to_delete = int(chip_to_delete)

        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # 1. Zmaž hosťa podľa čipu
        cur.execute("DELETE FROM Hostia WHERE Cip = %s", (chip_to_delete,))

        add_history(chip_to_delete , conn)

        # 2. Ulož zmenu
        conn.commit()

        # 3. Načítaj aktualizovaný zoznam hostí
        cur.execute("SELECT meno, zamestnanec, prichod, odchod, preco, cip, vydal FROM Hostia")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]

        cur.close()
        conn.close()

        df = pd.DataFrame(rows, columns=columns)
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        return html_table, 200

    except Exception as e:
        return str(e), 500

@app.route('/api/render_employee', methods=['GET'])
def render_employee():
    try:

        if 'vratnik' not in session:
                return jsonify({"status": "error", "message": "Nie si prihlásený alebo session vypršala"}), 401
        
        
        input_value = request.args.get('search_input')
        
        if not input_value:
            return jsonify({"status": "error", "message": "Chýbajúci vstup."}), 400

        conn = connect_to_database("mydatabase", "myuser", "mypassword")
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


def render_keys(meno):
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Získaj kľúče priradené zamestnancovi podľa mena
        cur.execute("SELECT kluc, preco, cas, vydal FROM kluce WHERE meno = %s", (meno,))
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


@app.route('/api/add_key', methods=['POST'])
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
    conn = connect_to_database("mydatabase", "myuser", "mypassword")
    cur = conn.cursor()
    
    cur.execute("SELECT meno FROM Zamestnanci WHERE cip = %s", (chip,))
    result = cur.fetchone()  # Získa prvý riadok výsledku

    cur.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None


@app.route('/api/return_keys', methods=['POST'])
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

        conn = connect_to_database("mydatabase","myuser","mypassword")
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
        cur.close()
        conn.close()

        return jsonify({"status": "success", "message": "Kľúč bol úspešne vrátený."}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400



@app.route('/api/load_keys_database', methods=['GET'])
def load_keys_database():
    try:
        conn = connect_to_database("mydatabase","myuser","mypassword")
        cur = conn.cursor()

        # Načítaj všetky údaje z tabuľky Kluce
        cur.execute("SELECT Kluc, Meno, Preco, Cas, vydal FROM Kluce")
        rows = cur.fetchall()

        # Konverzia na DataFrame pre HTML tabuľku
        df = pd.DataFrame(rows, columns=["Klúč", "Meno", "Prečo", "Kedy", "Vydal"])
        html_table = df.to_html(escape=False, index=False, table_id="table_of_guests")

        cur.close()
        conn.close()

        return html_table, 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/search_key', methods=['GET'])
def search_key():
    try:
        key = request.args.get('key_number')

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



@app.route('/api/login', methods=['POST'])
def login():
    try:

        data = request.get_json()
        name = data.get("name_guard")
        chip = data.get("chip")

        if not name or not chip:
            return jsonify({"message": "Zadaj meno aj čip"}), 400

        conn = connect_to_database("mydatabase", "myuser", "mypassword")
        cur = conn.cursor()

        # Hľadáme hash čipu pre dané meno
        cur.execute("SELECT chip FROM vratnici WHERE name_surname = %s", (name,))
        result = cur.fetchone()

        if result is None:
            return jsonify({"message": "Neplatné meno alebo heslo"}), 401
        
        stored_hash = result[0]

        # Overíme zadaný čip proti hashu v databáze
        if check_password_hash(stored_hash, chip):
            session.permanent = True
            session['vratnik'] = name

            resp = make_response(jsonify({"message": "Prešlo", "status": "success"}))
            return resp
        else:
            return jsonify({"message": "Neplatné meno alebo heslo"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/logout')
def logout():
    session.clear()  # vymaže všetky session dáta, teda aj 'user'
    response = make_response(jsonify({"message": "Odhlásený"}), 200)
    response.set_cookie('session', '', expires=0, path='/')
    return response


@app.route('/')
def home():
    return render_template('app.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
