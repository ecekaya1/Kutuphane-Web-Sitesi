import os
import json
import random
from datetime import datetime

class KitapSohbetBotu:
    """Kitap önerileri ve sorular için yapay zeka destekli sohbet botu."""
    
    def __init__(self):
        """Bot başlatılıyor."""
        self.kitap_bilgileri = self._kitap_bilgilerini_yukle()
        self.yazarlar = self._yazarlari_yukle()
        self.turler = [
            "Roman", "Bilim Kurgu", "Fantastik", "Tarih", "Biyografi", 
            "Şiir", "Polisiye", "Macera", "Felsefe", "Psikoloji",
            "Romantik", "Korku", "Yapay Zeka Destekli Bot"
        ]
        
        # Önceden tanımlanmış cevaplar
        self.selamlama_cevaplari = [
            "Merhaba! Size kitaplar hakkında nasıl yardımcı olabilirim?",
            "Selam! Hangi tür kitaplar ilginizi çekiyor?",
            "Merhaba, kitap dünyasına hoş geldiniz! Size nasıl yardımcı olabilirim?"
        ]
        
        self.kitap_onerileri = {
            "Roman": ["Suç ve Ceza", "Sefiller", "Anna Karenina", "Bülbülü Öldürmek"],
            "Bilim Kurgu": ["1984", "Dune", "Neuromancer", "Vakıf"],
            "Fantastik": ["Yüzüklerin Efendisi", "Harry Potter", "Taht Oyunları", "Witcher"],
            "Tarih": ["Sapiens", "Tüfek, Mikrop ve Çelik", "İmparatorlukların Yükselişi ve Çöküşü"],
            "Biyografi": ["Steve Jobs", "Elon Musk", "Benjamin Franklin", "Einstein"],
            "Şiir": ["Şairin Romanı", "Sevda Sözleri", "Bütün Şiirleri", "Otuz Beş Yaş"],
            "Polisiye": ["Sherlock Holmes", "Köpeklerin Sessizliği", "Ve Sonra Hiç Kimse Kalmadı"],
            "Macera": ["Define Adası", "Robinson Crusoe", "Moby Dick", "Jules Verne'in Eserleri"],
            "Felsefe": ["Böyle Buyurdu Zerdüşt", "Devlet", "Varlık ve Zaman", "Etik"],
            "Psikoloji": ["Bilinçaltının Gücü", "İnsanın Anlam Arayışı", "Duygusal Zeka"],
            "Romantik": ["Aşk ve Gurur", "Jane Eyre", "Romeo ve Juliet", "Rüzgar Gibi Geçti"],
            "Korku": ["Dracula", "Frankenstein", "Kara Kule", "O (Stephen King)"],
            "Yapay Zeka Destekli Bot": []
        }
        
        self.kisilik_tipi_kitap_onerileri = {
            "Lider": ["Savaş Sanatı", "Liderlik 101", "Cesur Yeni Dünya"],
            "Yaratıcı": ["Yaratıcı Beyin", "Büyük Sıçrama", "Hayal Gücünün Gücü"],
            "Analitik": ["Düşün ve Zengin Ol", "Sapiens", "Zekanın Yeni Sınırları"],
            "Duygusal": ["Küçük Prens", "Simyacı", "Duygusal Zeka"]
        }
    
    def _kitap_bilgilerini_yukle(self):
        """Kitap bilgilerini yükle."""
        try:
            from app import Kitap
            from app import db
            
            kitaplar = {}
            with db.app.app_context():
                for kitap in Kitap.query.all():
                    kitaplar[kitap.id] = {
                        'baslik': kitap.baslik,
                        'yazar': kitap.yazar,
                        'kategori': kitap.kategori or "Bilinmiyor",
                        'aciklama': kitap.aciklama or "Açıklama bulunmuyor"
                    }
            return kitaplar
        except Exception as e:
            print(f"Kitap bilgileri yüklenirken hata: {e}")
            return {}
    
    def _yazarlari_yukle(self):
        """Yazarları yükle."""
        try:
            yazarlar = set()
            for kitap in self.kitap_bilgileri.values():
                yazarlar.add(kitap['yazar'])
            return list(yazarlar)
        except Exception as e:
            print(f"Yazarlar yüklenirken hata: {e}")
            return ["Fyodor Dostoyevski", "George Orwell", "J.K. Rowling", "Franz Kafka", 
                    "Victor Hugo", "Paulo Coelho", "Antoine de Saint-Exupéry"]
    
    def mesaja_cevap_ver(self, mesaj):
        """Kullanıcı mesajına cevap ver."""
        mesaj = mesaj.lower()
        
        # Kişilik testi aktifse ve cevap geliyorsa
        if hasattr(self, 'test_sorulari') and hasattr(self, 'test_soru_index'):
            if mesaj.strip() in ["evet", "hayır"]:
                return self.kisilik_testi_cevapla(mesaj)
        
        # Selamlama kontrolü
        if any(kelime in mesaj for kelime in ["merhaba", "selam", "sa", "hi", "hello"]):
            return random.choice(self.selamlama_cevaplari)
        
        # Kitap önerisi isteği
        if "öner" in mesaj or "tavsiye" in mesaj:
            return self._kitap_onerisi_ver(mesaj)
        
        # Yazar hakkında bilgi isteği
        if "yazar" in mesaj:
            return self._yazar_bilgisi_ver(mesaj)
        
        # Tür hakkında bilgi isteği
        if "tür" in mesaj or "kategori" in mesaj:
            return self._tur_bilgisi_ver(mesaj)
        
        # Genel kitap sorusu
        if "kitap" in mesaj or "roman" in mesaj or "okuma" in mesaj:
            return self._genel_kitap_bilgisi_ver(mesaj)
        
        # Kişilik testi isteği
        if "kişilik testi" in mesaj or "test" in mesaj:
            return self._kisilik_testi_baslat()
        
        # Genel cevap
        return self._genel_cevap_ver()
    
    def _kitap_onerisi_ver(self, mesaj):
        """Kitap önerisi ver."""
        # Çoklu tür desteği
        secilen_turler = []
        for tur in self.turler:
            if tur.lower() in mesaj:
                secilen_turler.append(tur)
        if len(secilen_turler) > 1:
            cevaplar = []
            for tur in secilen_turler:
                if tur in self.kitap_onerileri:
                    oneriler = self.kitap_onerileri[tur]
                    cevaplar.append(f"{tur} türünde: {', '.join(random.sample(oneriler, min(3, len(oneriler))))}")
            if cevaplar:
                return " | ".join(cevaplar)
        elif len(secilen_turler) == 1:
            tur = secilen_turler[0]
            if tur in self.kitap_onerileri:
                oneriler = self.kitap_onerileri[tur]
                return f"{tur} türünde şu kitapları önerebilirim: {', '.join(random.sample(oneriler, min(3, len(oneriler))))}."
        
        # Yazar bazlı öneri
        for yazar in self.yazarlar:
            if yazar.lower() in mesaj:
                # Yazarın kitaplarını bul
                yazar_kitaplari = [kitap['baslik'] for kitap in self.kitap_bilgileri.values() 
                                  if kitap['yazar'].lower() == yazar.lower()]
                if yazar_kitaplari:
                    return f"{yazar}'dan şu kitapları önerebilirim: {', '.join(yazar_kitaplari)}."
        
        # Genel öneri
        rastgele_tur = random.choice(self.turler)
        oneriler = self.kitap_onerileri[rastgele_tur]
        return f"Size {rastgele_tur} türünde birkaç kitap önerebilirim: {', '.join(random.sample(oneriler, min(3, len(oneriler))))}."
    
    def _yazar_bilgisi_ver(self, mesaj):
        """Yazar hakkında bilgi ver."""
        for yazar in self.yazarlar:
            if yazar.lower() in mesaj:
                # Yazarın kitaplarını bul
                yazar_kitaplari = [kitap['baslik'] for kitap in self.kitap_bilgileri.values() 
                                  if kitap['yazar'].lower() == yazar.lower()]
                if yazar_kitaplari:
                    return f"{yazar}, {len(yazar_kitaplari)} kitabı veritabanımızda bulunan bir yazar. Eserleri: {', '.join(yazar_kitaplari)}."
                else:
                    return f"{yazar} hakkında detaylı bilgi bulunmamaktadır."
        
        return f"Kütüphanemizde şu yazarlar bulunmaktadır: {', '.join(random.sample(self.yazarlar, min(5, len(self.yazarlar))))}."
    
    def _tur_bilgisi_ver(self, mesaj):
        """Tür hakkında bilgi ver."""
        for tur in self.turler:
            if tur.lower() in mesaj:
                if tur in self.kitap_onerileri:
                    return f"{tur} türünde popüler kitaplar: {', '.join(self.kitap_onerileri[tur][:3])}."
        
        return f"Kütüphanemizde şu türler bulunmaktadır: {', '.join(self.turler)}."
    
    def _genel_kitap_bilgisi_ver(self, mesaj):
        """Genel kitap bilgisi ver."""
        # Kitap adı arama
        for kitap_id, kitap in self.kitap_bilgileri.items():
            if kitap['baslik'].lower() in mesaj:
                return f"{kitap['baslik']} - {kitap['yazar']} tarafından yazılmış {kitap['kategori']} türünde bir kitap. {kitap['aciklama']}"
        
        # Genel kitap bilgisi
        return "Kitaplar, bilgi ve hayal gücünün sınırlarını genişleten en değerli kaynaklardır. Size özel bir kitap önerisi ister misiniz?"
    
    def _kisilik_testi_baslat(self):
        sorular = [
            ("Bir grup içinde genellikle liderlik rolünü üstlenir misiniz?", "Lider"),
            ("Sanatsal veya yaratıcı aktivitelerden hoşlanır mısınız?", "Yaratıcı"),
            ("Verilere ve mantığa dayalı kararlar almayı sever misiniz?", "Analitik"),
            ("Duygularınızı ve başkalarının duygularını kolayca anlayabilir misiniz?", "Duygusal")
        ]
        self.test_sorulari = sorular
        self.test_soru_index = 0
        self.test_skorlar = {"Lider": 0, "Yaratıcı": 0, "Analitik": 0, "Duygusal": 0}
        return f"Kişilik testi başlıyor! {sorular[0][0]} (Evet/Hayır)"
    
    def kisilik_testi_cevapla(self, cevap):
        if not hasattr(self, 'test_sorulari') or not hasattr(self, 'test_soru_index'):
            return "Lütfen önce kişilik testini başlatın."
        if cevap.strip().lower() == "evet":
            tip = self.test_sorulari[self.test_soru_index][1]
            self.test_skorlar[tip] += 1
        self.test_soru_index += 1
        if self.test_soru_index < len(self.test_sorulari):
            soru = self.test_sorulari[self.test_soru_index][0]
            return f"{soru} (Evet/Hayır)"
        else:
            en_yuksek = max(self.test_skorlar, key=self.test_skorlar.get)
            oneriler = self.kisilik_tipi_kitap_onerileri[en_yuksek]
            # Testi sıfırla
            del self.test_sorulari
            del self.test_soru_index
            del self.test_skorlar
            return f"Kişilik tipiniz: {en_yuksek}. Size şu kitapları öneriyorum: {', '.join(oneriler)}."
    
    def _genel_cevap_ver(self):
        """Genel cevap ver."""
        genel_cevaplar = [
            "Nasıl yardımcı olabilirim? Kitap önerisi, yazar bilgisi veya belirli bir tür hakkında bilgi isteyebilirsiniz.",
            "Kitaplar hakkında soru sormaktan çekinmeyin. Size yardımcı olmaktan memnuniyet duyarım.",
            "Hangi tür kitaplar ilginizi çekiyor? Size öneriler sunabilirim.",
            "Belirli bir yazar veya kitap türü hakkında bilgi almak ister misiniz?",
            "Okuma listenize eklemek için yeni kitaplar arıyorsanız, size önerilerde bulunabilirim."
        ]
        return random.choice(genel_cevaplar)

# Bot örneği oluştur
kitap_botu = KitapSohbetBotu() 