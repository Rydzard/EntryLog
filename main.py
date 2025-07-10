from flask import Flask, request ,jsonify

import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

path_to_database_guests = "datas/guests.csv"
path_to_database_employee = "datas/employee.csv"

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
        date = data.get('date')
        why = data.get('why')
        
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

if __name__ == "__main__":
    app.run(debug=True)