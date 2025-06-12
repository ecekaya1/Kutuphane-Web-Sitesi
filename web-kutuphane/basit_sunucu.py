from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Merhaba! Flask sunucusu çalışıyor."

if __name__ == '__main__':
    print("Basit Flask sunucusu başlatılıyor...")
    print("http://localhost:8080 adresinde çalışıyor")
    app.run(host='0.0.0.0', port=8080, debug=False) 