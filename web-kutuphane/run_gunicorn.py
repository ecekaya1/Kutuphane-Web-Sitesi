import os
import subprocess
import sys

def run_gunicorn():
    """Gunicorn ile uygulamayı çalıştır."""
    print("Kütüphane Uygulaması Gunicorn ile başlatılıyor...")
    
    # Windows'ta doğrudan Gunicorn çalışmayabilir
    if os.name == 'nt':
        print("Windows sistemde socketio ile çalıştırılıyor...")
        from app import app, socketio
        
        # Debug bilgisi
        print("Oturum bilgileri kontrol ediliyor...")
        print(f"SECRET_KEY: {app.config['SECRET_KEY'][:5]}...")
        print(f"SESSION_TYPE: {app.config.get('SESSION_TYPE')}")
        print(f"SESSION_PERMANENT: {app.config.get('SESSION_PERMANENT')}")
        
        socketio.run(app, host='0.0.0.0', port=8080, debug=False)
    else:
        # Linux/Mac için Gunicorn
        cmd = [
            'gunicorn',
            '--worker-class', 'eventlet',
            '--workers', '4',
            '--bind', '0.0.0.0:8080',
            'wsgi:app'
        ]
        subprocess.call(cmd)

if __name__ == '__main__':
    run_gunicorn() 