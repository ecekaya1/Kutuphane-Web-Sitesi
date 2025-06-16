# Kütüphane Uygulaması

Modern bir kütüphane uygulaması. Kitap değerlendirme ve canlı sohbet özellikleri ile kitapseverler için geliştirilmiştir.

## Özellikler

- Kitap listeleme ve detaylı görüntüleme
- Kitap değerlendirme ve yorum sistemi (1-5 arası puanlama)
- Canlı sohbet özelliği ile kitapseverler arası iletişim
- Kullanıcı hesap yönetimi (kayıt, giriş, çıkış)
- Kitap arama fonksiyonu

## Kurulum

### Gereksinimler

- Python 3.8+
- Flask ve diğer gerekli paketler

### Adımlar

1. Depoyu klonlayın:
```
git clone <repo-url>
cd web-kutuphane
```

2. Sanal ortam oluşturun ve etkinleştirin:
```
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Gerekli paketleri yükleyin:
```
pip install -r requirements.txt
```

4. Çevre değişkenlerini ayarlayın:
```
# .env dosyası oluşturun
SECRET_KEY=gizli-anahtar-buraya
```

5. Uygulamayı çalıştırın:
```
python app.py
```

6. Tarayıcınızda `http://localhost:5000` adresine gidin.

## Veritabanı

Uygulama SQLite veritabanı kullanmaktadır. İlk çalıştırmada otomatik olarak oluşturulur.

## Kullanım

1. Kayıt olun veya giriş yapın
2. Kitapları inceleyin ve değerlendirin
3. Diğer kitapseverlerle sohbet edin

## Teknolojiler

- **Backend:** Flask, SQLAlchemy, Flask-SocketIO
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Veritabanı:** SQLite
- **Gerçek Zamanlı İletişim:** Socket.IO

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: açıklama'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Pull Request oluşturun
