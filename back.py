from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        # Získame údaje z požiadavky
        data = request.get_json()

        # Získanie údajov zo JSON objektu
        name = data.get('name')
        who = data.get('who')
        date = data.get('date')
        why = data.get('why')

        # Tu môžeš spracovať údaje, napríklad ich uložiť do databázy alebo ich logovať
        print(f"Name: {name}, Who: {who}, Date: {date}, Why: {why}")

        # Odpoveď, ktorá sa pošle na front-end
        return jsonify({"status": "success", "message": "Data received successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
