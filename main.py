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

pysqldf = lambda q: sqldf(q, globals())

def join_database(filepath):
    return pd.read_csv(filepath)

@app.route('/add_guest', methods=['POST'])
def add_guest():
    try:

        print("Tu voslo")
        # Získame údaje z požiadavky
        data = request.get_json()

        # Získanie údajov zo JSON objektu
        name = data.get('name')
        who = data.get('who')
        date = data.get('formattedDate')
        why = data.get('why')
        currentTime = data.get('currentTime')
        chip_number = data.get('chip')
        print(int(chip_number))
        print(currentTime)

        database_guests = join_database(path_to_database_guests)

        print("Tu sa vypisal datum")
        print(date)
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
    database_guests["Možnosti"] = '<button onclick="showOptions()" class="moreButton">...</button>'
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
    updated_history = pd.concat([database_history, new_entry], ignore_index=True)

    # Uloží aktualizovanú históriu
    updated_history.to_csv(path_to_database_history, mode='w', header=True, index=False)

    print("Záznam pridaný do histórie:")
    print(new_entry)


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
    #globals()['data_guests'] = data_guests

    delete_guest = data_guests[data_guests['Čip'] != int(input_string)]

    delete_guest.to_csv(path_to_database_guests, mode='w', header=True, index=False)
    # query = f'DELETE FROM data_guests WHERE "Kto prišiel" != \'{input_string}\''
    # print(query)
    # deleted_guest = pysqldf(query)
    html_table = delete_guest.to_html(escape=False, index=False, table_id="table_of_guests")

    add_history(input_string,data_guests,path_to_database_history)

    return html_table,200

if __name__ == "__main__":
    app.run(debug=True)