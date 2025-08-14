from flask import Flask, request ,jsonify, make_response, session
from blueprints.db import connect_to_database
from flask_cors import CORS
from datetime import timedelta
from blueprints.guests import guests_bp
from blueprints.employee import employee_bp

from werkzeug.security import check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # musí byť nastavený, inak session nebude fungovať
app.permanent_session_lifetime = timedelta(days=1)

# Toto zabezpečí, že cookie pre session bude fungovať len cez HTTPS
app.config['SESSION_COOKIE_SECURE'] = True  

# Odporúčané ďalšie bezpečnostné nastavenia
app.config['SESSION_COOKIE_HTTPONLY'] = True  # aby cookie nebolo dostupné JS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'



app.register_blueprint(guests_bp)
app.register_blueprint(employee_bp)

CORS(app, supports_credentials=True)

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


if __name__ == "__main__":
    app.run(ssl_context=('certifikat/localhost+2.pem', 'certifikat/localhost+2-key.pem'), port=5000, host='127.0.0.1')
