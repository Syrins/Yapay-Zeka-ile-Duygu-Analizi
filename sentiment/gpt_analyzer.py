from api.api_client import APIClient

def call_gpt(prompt, max_tokens=9999):
    client = APIClient()
    data = {
        "model": "gpt-3.5-turbo",
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = client.send_request(data)
    try:
        output = response["choices"][0]["message"]["content"]
    except Exception as e:
        output = "Analiz yapılamadı: " + str(e)
    return (output)

def gpt_sentence_analysis(text):
    prompt = (
        "Lütfen aşağıdaki metni cümle bazında çok detaylı analiz edin. "
        "Her cümlenin analizinde şunları belirtin:\n\n"
        "### Cümle {n} Analizi\n"
        "- **Cümle:** Cümlenin tam metni\n"
        "- **Polarity:** Pozitif ya da negatif duygu değeri\n"
        "- **Subjectivity:** Nesnellik/öznelik oranı\n"
        "- **Ton, Nüans ve İfade:** Cümlenin duygusal alt tonu, nüansları, ironik veya sarkastik ifadeler\n"
        "- **Önemli Kelimeler:** Duyguyu etkileyen anahtar kelimeler ve bunların etkileri\n"
        "- **Açıklama:** Sözdizimi, anlatım tarzı, metnin genel bağlamıyla ilişkisi ve duygusal çözümlemesi\n\n"
        "Metin:\n" + text
    )
    return call_gpt(prompt, max_tokens=9999)

def gpt_general_analysis(text):
    prompt = (
        "Lütfen aşağıdaki metin için kapsamlı bir genel analiz yapın. Aşağıdaki unsurları içersin:\n"
        "- Toplam cümle sayısı\n"
        "- En sık kullanılan kelimeler ve frekansları\n"
        "- Anahtar kelimeler (noun phrases) ve metnin ana temaları\n"
        "- Metnin genel duygu durumu, anlatımın akıcılığı, yazının yapısı\n"
        "- Yazarın dil zenginliği, ifadenin netliği ve metinle ilgili öneriler\n\n"
        "Metin:\n" + text
    )
    return call_gpt(prompt, max_tokens=9999)

def gpt_personality_analysis(text):
    prompt = (
        "Lütfen aşağıdaki metne dayanarak yazarın kişilik özelliklerini çok detaylı analiz edin. "
        "Aşağıdaki başlıkları kullanarak analiz yapın:\n\n"
        "### Kişilik Analizi\n"
        "- **Duygusal Durum:** Yüksek duygusallık, sakinlik veya çalkantı gibi\n"
        "- **İletişim Tarzı:** İçe dönüklük/dışa dönüklük, açıklık veya çekingenlik\n"
        "- **Analitik Düşünme:** Eleştirel ve analitik yaklaşım düzeyi\n"
        "- **Yaratıcılık ve Özgünlük:** Metnin özgünlüğü, yaratıcı anlatım ve metafor kullanımı\n"
        "- **Big Five Özellikleri:** (Örneğin, açıklık, sorumluluk, dışa dönüklük, uyumluluk, duygusal denge)\n"
        "- **Güçlü Yönler:** Belirgin olumlu kişilik özellikleri\n"
        "- **Zayıf Yönler:** Geliştirilmesi gereken alanlar\n"
        "- **Motivasyonlar ve Hedefler:** Yaşam öncelikleri, tutkular ve hedefler\n"
        "- **Gelişim Önerileri:** Kişisel gelişim için somut öneriler\n\n"
        "Metin:\n" + text
    )
    return call_gpt(prompt, max_tokens=9999)

def gpt_character_analysis(text):
    prompt = (
        "Lütfen aşağıdaki metin üzerinden karakter analizini çok detaylı yapın. Aşağıdaki başlıkları kullanın:\n\n"
        "### Karakter Analizi\n"
        "- **Yazım Stili ve Üslup:** Metnin anlatım biçimi, kullanılan dilin özellikleri, cümle yapıları\n"
        "- **Anlatımın Canlılığı:** Akıcılık, duygu yoğunluğu, betimleme zenginliği\n"
        "- **Kişisel İfade ve Özgünlük:** Yazarın kendini ifade etme biçimi, özgünlüğü, metafor ve benzetme kullanımı\n"
        "- **Dilin Etkileyiciliği:** Okuyucuyu etkileme gücü, dilin melodisi ve ritmi\n\n"
        "Metin:\n" + text
    )
    return call_gpt(prompt, max_tokens=9999)

def gpt_detailed_analysis(text):
    sentence_analysis = gpt_sentence_analysis(text)
    general_analysis = gpt_general_analysis(text)
    personality_analysis = gpt_personality_analysis(text)
    character_analysis = gpt_character_analysis(text)
    
    combined_result = (
        "## Detaylı Cümle Analizi\n" + sentence_analysis + "\n\n" +
        "## Genel Analiz\n" + general_analysis + "\n\n" +
        "## Kişilik Analizi\n" + personality_analysis + "\n\n" +
        "## Karakter Analizi\n" + character_analysis
    )
    return combined_result
