from app import app, db
from app import Kullanici, Kitap, Yorum
from werkzeug.security import generate_password_hash
from datetime import datetime, date
import random

# Örnek kitap verileri
kitaplar = [
    {
        "baslik": "Suç ve Ceza",
        "yazar": "Fyodor Dostoyevski",
        "yayinci": "İş Bankası Kültür Yayınları",
        "yayin_tarihi": date(2020, 1, 15),
        "isbn": "9789754370447",
        "aciklama": "Suç ve Ceza, Rus yazar Fyodor Dostoyevski tarafından yazılan psikolojik bir romandır. İlk olarak 1866 yılında Rus Habercisi adlı dergide tefrika edilmiştir. Kitap, Saint Petersburg'da yaşayan fakir bir öğrenci olan Rodion Romanoviç Raskolnikov'un işlediği çifte cinayet ve bunun psikolojik etkileri üzerine odaklanır.",
        "kategori": "Roman",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000058245-1.jpg"
    },
    {
        "baslik": "1984",
        "yazar": "George Orwell",
        "yayinci": "Can Yayınları",
        "yayin_tarihi": date(2019, 5, 10),
        "isbn": "9789750719387",
        "aciklama": "1984, George Orwell tarafından kaleme alınmış olan distopik bir politik kurgu romanıdır. Romanın hikâyesi distopik bir dünyada geçer. Distopya, ütopyanın tam tersi olarak, korku ve baskının hâkim olduğu bir dünya düzenini anlatır.",
        "kategori": "Bilim Kurgu",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000064038-1.jpg"
    },
    {
        "baslik": "Küçük Prens",
        "yazar": "Antoine de Saint-Exupéry",
        "yayinci": "Can Yayınları",
        "yayin_tarihi": date(2018, 3, 20),
        "isbn": "9789750713798",
        "aciklama": "Küçük Prens, Fransız yazar ve pilot Antoine de Saint-Exupéry tarafından yazılmış ve çizilmiş bir çocuk kitabıdır. İlk olarak 1943 yılında yayımlanmıştır. Kitap, çölde düşen bir pilotun küçük bir prensi karşılamasını anlatır.",
        "kategori": "Çocuk",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000061346-1.jpg"
    },
    {
        "baslik": "Simyacı",
        "yazar": "Paulo Coelho",
        "yayinci": "Can Yayınları",
        "yayin_tarihi": date(2017, 7, 5),
        "isbn": "9789750726439",
        "aciklama": "Simyacı, Brezilyalı yazar Paulo Coelho'nun 1988 yılında yayımlanan alegorik bir romanıdır. Roman, Santiago adlı genç bir çobanın İspanya'dan Mısır'a uzanan yolculuğunu ve bu yolculukta kendi kişisel macerasını keşfetmesini anlatır.",
        "kategori": "Roman",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000064550-1.jpg"
    },
    {
        "baslik": "Dönüşüm",
        "yazar": "Franz Kafka",
        "yayinci": "İş Bankası Kültür Yayınları",
        "yayin_tarihi": date(2016, 10, 12),
        "isbn": "9789754583250",
        "aciklama": "Dönüşüm, Franz Kafka tarafından 1915 yılında yazılan bir novella'dır. Hikâye, kendisini bir sabah dev bir böceğe dönüşmüş olarak bulan Gregor Samsa'nın durumunu anlatır.",
        "kategori": "Roman",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000105409-1.jpg"
    },
    {
        "baslik": "Sefiller",
        "yazar": "Victor Hugo",
        "yayinci": "İş Bankası Kültür Yayınları",
        "yayin_tarihi": date(2015, 2, 25),
        "isbn": "9789754589016",
        "aciklama": "Sefiller, Victor Hugo tarafından 1862 yılında yazılan bir romandır. Kitap, 19. yüzyıl Fransa'sında geçer ve adaletsizlik, yoksulluk ve sevgi gibi temaları işler.",
        "kategori": "Roman",
        "resim_url": "https://i.dr.com.tr/cache/600x600-0/originals/0000000711546-1.jpg"
    }
]

# Örnek kullanıcı verileri
kullanicilar = [
    {
        "kullanici_adi": "admin",
        "email": "admin@kutuphane.com",
        "parola": "admin123"
    },
    {
        "kullanici_adi": "ahmet",
        "email": "ahmet@example.com",
        "parola": "ahmet123"
    },
    {
        "kullanici_adi": "ayse",
        "email": "ayse@example.com",
        "parola": "ayse123"
    }
]

# Örnek yorumlar
yorumlar = [
    "Harika bir kitap! Kesinlikle tavsiye ederim.",
    "Çok etkileyici bir hikaye, bir solukta okudum.",
    "Yazarın en iyi eserlerinden biri.",
    "Karakterler çok iyi işlenmiş, hikaye akıcı.",
    "Biraz sıkıcı buldum ama yine de değer.",
    "Beklentilerimi karşılamadı.",
    "Klasik bir başyapıt, herkesin okuması gerekir.",
    "Düşündürücü ve etkileyici bir kitap.",
    "Daha önce hiç bu kadar sürükleyici bir kitap okumamıştım."
]

def ekle_ornek_veri():
    with app.app_context():
        # Veritabanını temizle
        db.drop_all()
        db.create_all()
        
        print("Örnek kullanıcılar ekleniyor...")
        for kullanici_veri in kullanicilar:
            kullanici = Kullanici(
                kullanici_adi=kullanici_veri["kullanici_adi"],
                email=kullanici_veri["email"],
                parola_hash=generate_password_hash(kullanici_veri["parola"], method='pbkdf2:sha256')
            )
            db.session.add(kullanici)
        
        db.session.commit()
        
        print("Örnek kitaplar ekleniyor...")
        for kitap_veri in kitaplar:
            kitap = Kitap(**kitap_veri)
            db.session.add(kitap)
        
        db.session.commit()
        
        print("Örnek yorumlar ekleniyor...")
        # Her kitaba rastgele yorumlar ekle
        tum_kullanicilar = Kullanici.query.all()
        tum_kitaplar = Kitap.query.all()
        
        for kitap in tum_kitaplar:
            # Her kitaba 2-5 arası yorum ekle
            yorum_sayisi = random.randint(2, 5)
            for _ in range(yorum_sayisi):
                kullanici = random.choice(tum_kullanicilar)
                puan = random.randint(1, 5)
                yorum_metni = random.choice(yorumlar)
                
                yorum = Yorum(
                    icerik=yorum_metni,
                    puan=puan,
                    kullanici_id=kullanici.id,
                    kitap_id=kitap.id
                )
                db.session.add(yorum)
        
        db.session.commit()
        
        print("Örnek veriler başarıyla eklendi!")

if __name__ == "__main__":
    ekle_ornek_veri() 