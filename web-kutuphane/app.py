from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from werkzeug.urls import url_parse

# Çevre değişkenlerini yükle
load_dotenv()

# Flask uygulamasını oluştur
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'kutuphane-gizli-anahtar-2023')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kutuphane.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 7 günlük oturum süresi

# Önbellek yapılandırması
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 dakika

# Veritabanı, Önbellek ve Socket.IO oluştur
db = SQLAlchemy(app)
cache = Cache(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Kullanıcı giriş yöneticisi
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris'
login_manager.login_message = 'Bu sayfayı görüntülemek için lütfen giriş yapın.'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

# Yapay zeka botu
try:
        from ai_bot import kitap_botu
except ImportError:
    kitap_botu = None

# Veritabanı modelleri
class Kullanici(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kullanici_adi = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    parola_hash = db.Column(db.String(200), nullable=False)
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    yorumlar = db.relationship('Yorum', backref='kullanici', lazy=True)
    mesajlar = db.relationship('Mesaj', backref='kullanici', lazy=True)

class Kitap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    yazar = db.Column(db.String(100), nullable=False)
    yayinci = db.Column(db.String(100))
    yayin_tarihi = db.Column(db.Date)
    isbn = db.Column(db.String(13))
    aciklama = db.Column(db.Text)
    kategori = db.Column(db.String(50))
    resim_url = db.Column(db.String(200))
    yorumlar = db.relationship('Yorum', backref='kitap', lazy=True)

class Yorum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icerik = db.Column(db.Text, nullable=False)
    puan = db.Column(db.Integer, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    kitap_id = db.Column(db.Integer, db.ForeignKey('kitap.id'), nullable=False)

class Mesaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    kullanici_id = db.Column(db.Integer, db.ForeignKey('kullanici.id'), nullable=False)
    oda = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    user = Kullanici.query.get(int(user_id))
    print(f"Kullanıcı yükleniyor: ID={user_id}, Bulundu={'Evet' if user else 'Hayır'}")
    return user

# Ana sayfa
@app.route('/')
@cache.cached(timeout=60)  # 60 saniye önbellek
def ana_sayfa():
    kitaplar = Kitap.query.order_by(Kitap.id.desc()).limit(10).all()
    return render_template('ana_sayfa.html', kitaplar=kitaplar)

# Kitap detay sayfası
@app.route('/kitap/<int:kitap_id>')
@cache.cached(timeout=30)  # 30 saniye önbellek
def kitap_detay(kitap_id):
    kitap = Kitap.query.get_or_404(kitap_id)
    yorumlar = Yorum.query.filter_by(kitap_id=kitap_id).order_by(Yorum.tarih.desc()).all()
    return render_template('kitap_detay.html', kitap=kitap, yorumlar=yorumlar)

# Yorum ekleme
@app.route('/kitap/<int:kitap_id>/yorum', methods=['POST'])
@login_required
def yorum_ekle(kitap_id):
    kitap = Kitap.query.get_or_404(kitap_id)
    icerik = request.form.get('icerik')
    puan = int(request.form.get('puan'))
    
    if puan < 1 or puan > 5:
        flash('Puan 1-5 arasında olmalıdır.')
        return redirect(url_for('kitap_detay', kitap_id=kitap_id))
    
    yeni_yorum = Yorum(
        icerik=icerik,
        puan=puan,
        kullanici_id=current_user.id,
        kitap_id=kitap_id
    )
    
    db.session.add(yeni_yorum)
    db.session.commit()
    # Önbelleği temizle
    cache.delete_memoized(kitap_detay, kitap_id)
    flash('Yorumunuz başarıyla eklendi.')
    return redirect(url_for('kitap_detay', kitap_id=kitap_id))

# Kayıt sayfası
@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        email = request.form.get('email')
        parola = request.form.get('parola')
        parola_tekrar = request.form.get('parola_tekrar')
        
        kullanici_kontrol = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        email_kontrol = Kullanici.query.filter_by(email=email).first()
        
        if kullanici_kontrol:
            flash('Bu kullanıcı adı zaten kullanılıyor.')
            return redirect(url_for('kayit'))
        
        if email_kontrol:
            flash('Bu e-posta adresi zaten kullanılıyor.')
            return redirect(url_for('kayit'))
        
        if parola != parola_tekrar:
            flash('Parolalar eşleşmiyor.')
            return redirect(url_for('kayit'))
        
        yeni_kullanici = Kullanici(
            kullanici_adi=kullanici_adi,
            email=email,
            parola_hash=generate_password_hash(parola, method='pbkdf2:sha256')
        )
        
        db.session.add(yeni_kullanici)
        db.session.commit()
        
        flash('Kaydınız başarıyla oluşturuldu. Şimdi giriş yapabilirsiniz.')
        return redirect(url_for('giris'))
    
    return render_template('kayit.html')

# Giriş sayfası
@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        kullanici_adi = request.form.get('kullanici_adi')
        parola = request.form.get('parola')
        
        kullanici = Kullanici.query.filter_by(kullanici_adi=kullanici_adi).first()
        
        if not kullanici or not check_password_hash(kullanici.parola_hash, parola):
            flash('Kullanıcı adı veya parola hatalı.')
            return redirect(url_for('giris'))
        
        login_user(kullanici, remember=True)
        next_page = request.args.get('next')
        
        # Kullanıcı girişini logla
        print(f"Kullanıcı giriş yaptı: {kullanici.kullanici_adi}, ID: {kullanici.id}")
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('ana_sayfa')
            
        return redirect(next_page)
    
    return render_template('giris.html')

# Çıkış
@app.route('/cikis')
@login_required
def cikis():
    logout_user()
    flash('Başarıyla çıkış yapıldı.')
    return redirect(url_for('ana_sayfa'))

# Sohbet sayfası
@app.route('/sohbet')
@login_required
def sohbet():
    kitaplar = Kitap.query.all()
    return render_template('sohbet.html', kitaplar=kitaplar)

# Socket.IO olayları
@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        join_room('genel')
        emit('status', {'msg': f'{current_user.kullanici_adi} sohbete katıldı.'}, room='genel')

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        leave_room('genel')
        # Tüm kitap odalarından da çıkış yap
        kitaplar = Kitap.query.all()
        for kitap in kitaplar:
            leave_room(f'kitap_{kitap.id}')
        emit('status', {'msg': f'{current_user.kullanici_adi} sohbetten ayrıldı.'}, room='genel')

@socketio.on('mesaj')
def handle_mesaj(data):
    if current_user.is_authenticated:
        oda = data.get('oda', 'genel')
        mesaj_icerik = data['msg']
        
        # Eğer mesaj AI bota yönelikse
        if mesaj_icerik.startswith('@bot') and kitap_botu:
            bot_mesaji = kitap_botu.mesaja_cevap_ver(mesaj_icerik[4:].strip())
            
            # Bot mesajını kaydet
            bot_mesaj = Mesaj(
                icerik=bot_mesaji,
                kullanici_id=1,  # Admin kullanıcısı (bot için)
                oda=oda
            )
            db.session.add(bot_mesaj)
            db.session.commit()
            
            # Bot mesajını gönder
            emit('mesaj', {
                'msg': bot_mesaji,
                'kullanici': 'KitapBot 🤖',
                'tarih': bot_mesaj.tarih.strftime('%H:%M:%S'),
                'is_bot': True
            }, room=oda)
            return
        
        # Normal kullanıcı mesajı
        mesaj = Mesaj(
            icerik=mesaj_icerik,
            kullanici_id=current_user.id,
            oda=oda
        )
        db.session.add(mesaj)
        db.session.commit()
        
        emit('mesaj', {
            'msg': mesaj_icerik,
            'kullanici': current_user.kullanici_adi,
            'tarih': mesaj.tarih.strftime('%H:%M:%S'),
            'is_bot': False
        }, room=oda)

@socketio.on('join_kitap_odasi')
def handle_join_kitap_odasi(data):
    if current_user.is_authenticated:
        kitap_id = data.get('kitap_id')
        if kitap_id:
            kitap = Kitap.query.get(kitap_id)
            if kitap:
                oda = f'kitap_{kitap_id}'
                join_room(oda)
                emit('status', {
                    'msg': f'{current_user.kullanici_adi} "{kitap.baslik}" kitabı hakkındaki sohbete katıldı.',
                    'kitap_adi': kitap.baslik
                }, room=oda)
                
                # Son mesajları gönder
                son_mesajlar = Mesaj.query.filter_by(oda=oda).order_by(Mesaj.tarih.desc()).limit(10).all()
                for mesaj in reversed(son_mesajlar):
                    kullanici = Kullanici.query.get(mesaj.kullanici_id)
                    emit('mesaj', {
                        'msg': mesaj.icerik,
                        'kullanici': kullanici.kullanici_adi,
                        'tarih': mesaj.tarih.strftime('%H:%M:%S')
                    }, room=request.sid)  # Sadece katılan kullanıcıya gönder

@socketio.on('leave_kitap_odasi')
def handle_leave_kitap_odasi(data):
    if current_user.is_authenticated:
        kitap_id = data.get('kitap_id')
        if kitap_id:
            kitap = Kitap.query.get(kitap_id)
            if kitap:
                oda = f'kitap_{kitap_id}'
                leave_room(oda)
                emit('status', {
                    'msg': f'{current_user.kullanici_adi} "{kitap.baslik}" kitabı hakkındaki sohbetten ayrıldı.',
                    'kitap_adi': kitap.baslik
                }, room=oda)

# Arama işlevi
@app.route('/arama')
def arama():
    sorgu = request.args.get('q', '')
    if sorgu:
        kitaplar = Kitap.query.filter(
            (Kitap.baslik.contains(sorgu)) | 
            (Kitap.yazar.contains(sorgu)) |
            (Kitap.aciklama.contains(sorgu))
        ).all()
    else:
        kitaplar = []
    
    return render_template('arama_sonuclari.html', kitaplar=kitaplar, sorgu=sorgu)

# AI Bot API
@app.route('/api/bot/cevap', methods=['POST'])
@login_required
def bot_cevap():
    if not kitap_botu:
        return jsonify({'error': 'Bot yüklenemedi'}), 500
    
    data = request.get_json()
    if not data or 'mesaj' not in data:
        return jsonify({'error': 'Geçersiz istek'}), 400
    
    cevap = kitap_botu.mesaja_cevap_ver(data['mesaj'])
    return jsonify({'cevap': cevap})

# AI Bot sayfası
@app.route('/bot')
@login_required
def bot_sayfasi():
    return render_template('bot.html')

# Veritabanı oluşturma
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=False) 