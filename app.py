from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

if __name__ == "__main__":
    app.run(ssl_context=('certifikat/localhost+2.pem', 'certifikat/localhost+2-key.pem'), port=5001, host='127.0.0.1')
