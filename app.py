from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('app.html')

if __name__ == "__main__":
    app.run(ssl_context=('certifikat/192.168.51.41+1.pem', 'certifikat/192.168.51.41+1-key.pem'), port=5001, host='192.168.51.41')
