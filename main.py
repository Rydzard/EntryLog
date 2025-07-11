from flask import Flask, request ,jsonify

import pandas as pd
from pandasql import sqldf
from flask_cors import CORS
import keyboard
app = Flask(__name__)
CORS(app)

path_to_database_guests = "datas/guests.csv"
path_to_database_employee = "datas/employee.csv"

pysqldf = lambda q: sqldf(q, globals())

def join_database(filepath):
    return pd.read_csv(filepath)

def load_card():
    while(True):
        input= keyboard.read_event()
        if(len(input)==6):
            break
    return input

@app.route('/add_guest', methods=['POST'])
def add_guest():
    try:
        # Získame údaje z požiadavky
        data = request.get_json()

        # Získanie údajov zo JSON objektu
        name = data.get('name')
        who = data.get('who')
        date = data.get('date')
        why = data.get('why')
        
        # string = load_card()
        # print(string)

        database_guests = join_database(path_to_database_guests)

        new_guest = pd.DataFrame([{
            'Kto prišiel': name,
            'Ku komu': who,
            'Čas': date,
            'Prečo': why
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

@app.route('/search_guests', methods=['POST'])
def search_guests():
    data = request.json 
    print(data)

    data_guests = join_database(path_to_database_guests)
    input_string = data.get('search_input')

    globals()['data_guests'] = data_guests

    query = f'SELECT * FROM data_guests WHERE "Kto prišiel" LIKE "{input_string}%"'
    vysledok = pysqldf(query)

    vysledok["Možnosti"] = '<button onclick="showOptions()" class="moreButton">...</button>'
    html_table = vysledok.to_html(escape=False, index=False, table_id="table_of_guests")

    print(html_table)

    #data_guests.query("Kto prišiel" == data[0])
    return html_table,200

if __name__ == "__main__":
    app.run(debug=True)