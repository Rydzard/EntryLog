from flask import Flask, request ,jsonify

import pandas as pd
from pandasql import sqldf
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

path_to_database_guests = "datas/guests.csv"
path_to_database_employee = "datas/employee.csv"
path_to_database_history = "datas/history.csv"
path_to_database_keys = "datas/keys.csv"

pysqldf = lambda q: sqldf(q, globals())

def join_database(filepath):
    return pd.read_csv(filepath)

@app.route('/add_guest', methods=['POST'])
def add_guest():
    try:
        # Získame údaje z požiadavky
        data = request.get_json()

        # Získanie údajov zo JSON objektu
        name = data.get('name')
        who = data.get('who')
        date = data.get('formattedDate')
        why = data.get('why')
        currentTime = data.get('currentTime')
        chip_number = data.get('chip')

        database_guests = join_database(path_to_database_guests)

        new_guest = pd.DataFrame([{
            'Kto prišiel': name,
            'Ku komu': who,
            'Od kedy': currentTime,
            'Do kedy': date,
            'Prečo': why,
            'Čip': chip_number
        }])

        new_data_df = pd.concat([new_guest,database_guests], ignore_index=True)
        new_data_df.to_csv(path_to_database_guests, mode='w', header=True, index=False)

        # Odpoveď, ktorá sa pošle na front-end
        return jsonify({"status": "success", "message": "Data received successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/load_guests', methods=['GET'])
def load_guests():

    database_guests = join_database(path_to_database_guests)
       # Použijeme index riadku ako jedinečný identifikátor pre tlačidlo
    database_guests["Možnosti"] = database_guests.index.to_series().apply(
        lambda idx: f'<button onclick="showOptions({idx})" class="moreButton">...</button>'
    )

    html_table = database_guests.to_html(escape=False, index=False, table_id="table_of_guests")

    return html_table, 200  # vraciaš HTML tabuľku ako text

@app.route('/load_history', methods=['GET'])
def load_history():
    database_guests = join_database(path_to_database_history)
    html_table = database_guests.to_html(escape=False, index=False, table_id="table_of_guests")

    return html_table, 200  # vraciaš HTML tabuľku ako text

def add_history(input_string, data_guests, path_to_database_history):
    # Načíta historickú databázu
    database_history = join_database(path_to_database_history)

    # Nájde hosťa podľa čipu
    delete_guest = data_guests[data_guests['Čip'] == int(input_string)]

    if delete_guest.empty:
        print("Hosť s daným čipom nebol nájdený.")
        return

    # Vytvorí nový záznam o vrátení
    new_entry = pd.DataFrame({
        'Kto vrátil': delete_guest['Kto prišiel'].values,
        'Kedy vrátil': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
        'Čip': [int(input_string)]
    })

    # Pridá nový záznam do histórie
    updated_history = pd.concat([new_entry,database_history], ignore_index=True)

    # Uloží aktualizovanú históriu
    updated_history.to_csv(path_to_database_history, mode='w', header=True, index=False)


@app.route('/search_guests', methods=['POST'])
def search_guests():
    data = request.json 
    data_guests = join_database(path_to_database_guests)
    input_string = data.get('search_input')

    globals()['data_guests'] = data_guests

    query = f'SELECT * FROM data_guests WHERE "Kto prišiel" LIKE "{input_string}%"'
    vysledok = pysqldf(query)

    vysledok["Možnosti"] = '<button onclick="showOptions()" class="moreButton">...</button>'
    html_table = vysledok.to_html(escape=False, index=False, table_id="table_of_guests")

    return html_table,200


@app.route('/delete_guests', methods=['POST'])
def delete_guests():
    data = request.json

    data_guests = join_database(path_to_database_guests)
    input_string = data.get('delete_input')

    delete_guest = data_guests[data_guests['Čip'] != int(input_string)]

    delete_guest.to_csv(path_to_database_guests, mode='w', header=True, index=False)
    html_table = delete_guest.to_html(escape=False, index=False, table_id="table_of_guests")

    add_history(input_string,data_guests,path_to_database_history)

    return html_table,200

@app.route('/render_employee', methods=['POST'])
def render_employee():
    try:
        data = request.get_json()
        input = data.get('input_string')
        
        employee_dataset = join_database(path_to_database_employee)

        if isinstance(input, int):
            employee_dataset = employee_dataset[employee_dataset['Čip'] == input]
        else:
            employee_dataset = employee_dataset[employee_dataset['Meno'] == input]

        html_table_keys = render_keys(employee_dataset.iloc[0]["Meno"])
        
        employee_data = [{
            "name": employee_dataset.iloc[0]["Meno"],
            "chip": int(employee_dataset.iloc[0]["Čip"]),
            "department": employee_dataset.iloc[0]["Pracovisko"],
            "keys_table": html_table_keys
        }]

        return jsonify(employee_data), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
    
def render_keys(info):

    keys_dataset = join_database(path_to_database_keys)
    keys_dataset = keys_dataset[keys_dataset['Meno'] == info]
    del keys_dataset['Meno']
    html_table = keys_dataset.to_html(escape=False, index=False, table_id="table_of_guests")
    return html_table


@app.route('/show_options', methods=['POST'])
def show_options():
    try:
        data = request.json
        id_number = data.get('id')
        
        guests_dataset = join_database(path_to_database_guests)
        guests_name = guests_dataset.iloc[id_number]["Kto prišiel"]

        html_table_keys = render_keys(guests_name)

        guess_data = [{
            "name": guests_dataset.iloc[id_number]["Kto prišiel"],
            "chip": int(guests_dataset.iloc[id_number]["Čip"]),
            "keys_table": html_table_keys
        }]

        return jsonify(guess_data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(port=5000,debug=True)