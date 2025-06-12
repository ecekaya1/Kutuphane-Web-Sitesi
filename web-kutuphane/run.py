from app import app, socketio

if __name__ == '__main__':
    print("Kütüphane Uygulaması başlatılıyor...")
    print("Uygulama http://localhost:8080 adresinde çalışıyor.")
    socketio.run(app, debug=False, host='0.0.0.0', port=8080) 