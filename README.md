# Yapay Zeka ile Duygu Analizi

Bu proje, metin girdileri üzerinden duygu, kişilik ve karakter analizi yapabilen gelişmiş bir uygulamadır. Uygulama, doğal dil işleme (NLP) kütüphaneleri (TextBlob, langdetect) ve OpenAI GPT-3.5-turbo API'si kullanarak metinleri dört farklı bölümde detaylı şekilde analiz eder:

- **Cümle Bazlı Analiz:** Her cümlenin duygu ölçümleri, ton, önemli kelimeler ve açıklamaları.
- **Genel Analiz:** Metnin genel yapısı, kullanılan kelimeler, anahtar temalar ve öneriler.
- **Kişilik Analizi:** Yazarın kişilik özellikleri, iletişim tarzı, analitik düşünme, yaratıcılık ve gelişim önerileri.
- **Karakter Analizi:** Yazım stili, anlatımın canlılığı, üslup ve kişisel ifade biçimi.

Uygulama, PyQt5 tabanlı modern bir GUI sunar. Kullanıcılar, metin girişi veya dosya yükleme yapabilir, analiz işlemlerini başlatabilir, sonuçları farklı sekmelerde görüntüleyebilir ve sonuçları dışa aktarabilir. Ayarlar menüsü aracılığıyla API URL’si, model seçimi, duygu eşik değerleri ve tema (Modern Dark/Modern Light) gibi seçenekler yapılandırılabilir.

---

## Özellikler

- **Detaylı Analiz:**  
  - **Cümle Bazlı Analiz:** Her cümlenin duygusal tonu, öznel/nesnel oranı, ton, önemli kelimeler ve detaylı açıklamaları.
  - **Genel Analiz:** Metnin genel istatistikleri, en sık kullanılan kelimeler, anahtar kelimeler ve genel duygu durumu.
  - **Kişilik Analizi:** Yazarın kişilik özellikleri, iletişim tarzı, analitik düşünme, yaratıcılık, güçlü/zayıf yönler, motivasyonlar ve gelişim önerileri.
  - **Karakter Analizi:** Yazım stili, üslup, anlatımın canlılığı, kişisel ifade ve özgünlük.
- **Gelişmiş GUI:**  
  - Modern Dark ve Modern Light temaları.
  - Ayrı sekmelerde detaylı analiz sonuçları (Temel, Cümle, Genel, Kişilik, Karakter).
  - Dosya yükleme, temizleme ve dışa aktarma özellikleri.
- **Arka Plan İşlemleri:**  
  - Uzun süren analiz işlemleri için QThread kullanılarak UI donmaları önlenir.
- **Ayarlar Yönetimi:**  
  - API URL, model seçimi, duygu eşik değerleri ve tema tercihi gibi ayarlar "settings.json" dosyasında kalıcı olarak saklanır.

---

## Klasör Yapısı

```
sentiment_analysis/
├── api/
│   └── api_client.py         # API istekleri için istemci
├── config/
│   └── config.py             # API anahtarları ve URL ayarları
├── gui/
│   ├── main_window.py        # Ana pencere ve GUI arayüzü
│   └── settings_window.py    # Ayarlar penceresi
├── sentiment/
│   ├── analyzer.py           # Temel analiz (TextBlob, langdetect)
│   └── gpt_analyzer.py       # GPT analizi (cümle, genel, kişilik, karakter)
└── settings.json             # Kullanıcı ayarlarının saklandığı dosya
```

---

## Kurulum

### Gereksinimler

- Python 3.7 veya üstü
- [PyQt5](https://pypi.org/project/PyQt5/)
- [requests](https://pypi.org/project/requests/)
- [TextBlob](https://pypi.org/project/textblob/)
- [langdetect](https://pypi.org/project/langdetect/)
- [markdown](https://pypi.org/project/Markdown/)

### Bağımlılıkları Yükleme

Terminal veya komut istemcisinde aşağıdaki komutu çalıştırın:

```bash
pip install PyQt5 requests textblob langdetect markdown
```

TextBlob için gerekli dil verilerini yüklemek için:

```bash
python -m textblob.download_corpora
```

---

## API Anahtarları ve Konfigürasyon

`config/config.py` dosyasında API anahtarlarınızı ve API URL'nizi yapılandırın. Örneğin:

```python
API_KEYS = [
    "YOUR_API_KEY_1",
    "YOUR_API_KEY_2",
    "YOUR_API_KEY_3"
]

API_URL = "https://your-api-url/v1/chat/completions"
```

---

## Kullanım

Uygulamayı çalıştırmak için, proje dizininde terminalden:

```bash
python main.py
```

### Uygulama Arayüzü

- **Metin Girişi:** Sol panelde metin girişi yapın veya dosya yükleyin.
- **Analiz İşlemi:** "Analizi Başlat" butonuna tıklayarak temel ve GPT analizi başlatılır. Analiz işlemleri arka planda çalışır, UI donmaz.
- **Sekmeler:** Sağ panelde, analiz sonuçları aşağıdaki sekmelerde görüntülenir:
  - **Temel Analiz:** TextBlob ve langdetect kullanılarak hesaplanan istatistikler ve duygu ölçümleri.
  - **Cümle Analizi:** Her cümlenin detaylı duygu analizi.
  - **Genel Analiz:** Metnin genel yapısı, kullanılan kelimeler ve öneriler.
  - **Kişilik Analizi:** Yazarın kişilik özellikleri, iletişim tarzı, analitik düşünme, vb.
  - **Karakter Analizi:** Yazım stili, üslup ve anlatımın detaylı değerlendirmesi.
- **Ayarlar:** Menüden "Ayarları Düzenle" seçeneğini kullanarak API ayarları, model seçimi, duygu eşik değerleri ve tema tercihini (Modern Dark / Modern Light) yapılandırabilirsiniz.
- **Dışa Aktarım:** Analiz sonuçlarını metin dosyası olarak dışa aktarabilirsiniz.

---

## Geliştirme ve Özelleştirme

- **Analiz Prompt'ları:** `sentiment/gpt_analyzer.py` dosyasında yer alan prompt'lar, daha detaylı analizler almanız için özelleştirilebilir.
- **Tema ve Arayüz:** `gui/main_window.py` dosyasında Modern Dark ve Modern Light temaları tanımlanmıştır. İhtiyacınıza göre stil ayarlarını güncelleyebilirsiniz.
- **Ek Özellikler:** Kullanıcı deneyimini artırmak için ek özellikler (grafik gösterimi, daha fazla ayar seçeneği vb.) entegre edilebilir.

---

## Katkıda Bulunma

Proje ile ilgili geliştirme önerileriniz veya hatalarınız varsa, lütfen bir [issue](https://github.com/your-repo/issues) açın veya pull request gönderin.

---

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakınız.

---
