# AI Chatbot Arayüzü - aisuite kütüphanesi

Bu proje, **Sakarya Üniversitesi Yapay Zeka Topluluğu** tarafından düzenlenen **"Chatbot Workshop: Design Your Own AI Assistant"** başlıklı bir atölye kapsamında oluşturulmuştur.

### Bu Proje Nedir?
Bu proje, kullanıcıların farklı yapay zeka modellerini tek bir arayüzde kolayca kullanabilmelerini sağlar. Gelişmiş özelliklerle zenginleştirilmiş bu arayüz, sohbet geçmişini saklama, maliyet hesaplama ve PDF dosyalarını işleme gibi işlevler sunar. Ayrıca, hem çevrimdışı hem de API tabanlı modelleri destekleyerek esneklik sağlar.

---

## **Temel Özellikler**

1. **Model Esnekliği:**
   - Aynı sohbet oturumu içinde farklı yapay zeka modelleri arasında geçiş yapabilir, çeşitli sohbet deneyimleri ve karşılaştırmalar gerçekleştirebilirsiniz.

2. **Sohbet Geçmişi Yönetimi:**
   - Önceki sohbetlerinizi kaydedebilir ve kolayca yeniden ziyaret ederek devam edebilirsiniz.

3. **Markdown Desteği:**
   - Yanıtlar, bağlantılar, kod parçacıkları ve listeler gibi zengin metin öğelerini içerecek şekilde Markdown formatında görüntülenir.

4. **Maliyet Hesaplama:**
   - Farklı yapay zeka API'lerinin fiyatlandırma modellerine göre sohbet maliyetini hesaplar, kullanıcıların harcamalarını yönetmelerine yardımcı olur.

5. **Ollama Entegrasyonu:**
   - Aynı sohbet oturumu içinde hem çevrimdışı hem de API tabanlı modelleri kullanarak performans, gizlilik ve maliyet açısından esneklik sağlar.

6. **Kesintisiz Sohbet için Sohbet Kırpma:**
   - Model sınırlarını aşmamak için eski konuşmaları otomatik olarak kırparak sürekli ve kesintisiz sohbet imkanı sunar.

7. **PDF Yükleme Desteği (Yalnızca Metin):**
   - Metin tabanlı PDF dosyalarını yükleyerek içeriklerini doğrudan sohbet arayüzü üzerinden etkileşimli bir şekilde kullanabilirsiniz. Özellikle özet çıkarma, belirli bilgileri sorgulama veya belgedeki içerik hakkında sorular sormak için idealdir.

---

## **Kurulum Talimatları (Windows)**

### **Adım 1: Gerekli Kütüphaneleri Yükleyin**

1. Depoyu klonlayın:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Gerekli Python kütüphanelerini yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

---

### **Adım 2: Modelleri Yapılandırın**

1. Proje dizinindeki `model_config.json` dosyasını açın.

2. API anahtarlarınızı ve model ayrıntılarınızı güncelleyin. Örnek yapı:
   ```json
   {
       "models": [
           {
               "name": "OpenAI GPT-4o",
               "api_key": "API Anahtarınızı Buraya Girin",
               "id": "openai:gpt-4o",
               "local": false
           },
           {
               "name": "Ollama Llama3.2 3B",
               "api_key": "None",
               "id": "ollama:llama3.2:3b",
               "local": true
           }
       ]
   }
   ```

3. Dikkat edilmesi gerekenler:
   - `"API Anahtarınızı Buraya Girin"` alanını uygun API anahtarları ile değiştirin.
   - çevrimdışı modeller (`"local": true`) API anahtarı gerektirmez.

---

### **Adım 3: Fiyatlandırmayı Yapılandırın (İsteğe Bağlı)**

1. Her modelin maliyetini güncellemek için `pricing_config.json` dosyasını açın:
   ```json
   {
       "openai:gpt-4o": {
           "prompt_tokens": 2.50,
           "completion_tokens": 10.00
       }
   }
   ```

2. Notlar:
   - Fiyatlandırma, **1.000 token başına USD** cinsindendir.
   - çevrimdışı modeller (`local: true`) için fiyatlandırma yapılmaz, çünkü bu modeller donanımınızda çalışır ve ek maliyet oluşturmaz.

---

### **Adım 4: Çevrimdışı Modeller için Kurulum**

1. **Ollama**'yı [resmi web sitesi](https://ollama.com) üzerinden indirin ve yükleyin.

2. Kurulumdan sonra, gerekli çevrimdışı modelleri indirmek için şu komutu kullanın:
   ```bash
   ollama pull <model_id>
   ```
   - `<model_id>` alanını kullanmak istediğiniz modelin kimliğiyle değiştirin (ör. `llama3.2:3b`).

3. Model indirildikten sonra, `model_config.json` dosyasını şu şekilde güncelleyin:
   - **Sağlayıcı:** `ollama` olarak ayarlayın.
   - **Model ID:** İndirilen modelin kimliği.

---

### **Adım 5: Uygulamayı Çalıştırın**

1. Sohbet arayüzünü başlatmak için şu komutu çalıştırın:
   ```bash
   python app.py
   ```

2. Tarayıcınızı açın ve terminalde görüntülenen URL'ye gidin (varsayılan: `http://127.0.0.1:5000/`).

---

### **Adım 6: Ek Özellik - PDF Yükleme**

1. PDF yükleme özelliğini kullanmak için dosyaların aşağıdaki gibi olduğundan emin olun:
   - **Metin tabanlı PDF'ler** (tarama veya görüntü tabanlı PDF'ler desteklenmez).

2. PDF dosyasını yüklemek için sohbet arayüzündeki **Yükle** düğmesine tıklayın. Yüklenen dosyanın metin içeriği, etkileşim için kullanılabilir hale gelecektir.

---

## **İleride Eklenecek Özellikler**

1. **Retrieval-Augmented Generation (RAG):**
   - Harici kaynaklardan veya yüklenen belgelerden ilgili verileri entegre ederek sohbet yanıtlarını geliştirin.

2. **Görüntü Desteği:**
   - Sohbet botunun görüntü girdilerini analiz etme, açıklama yapma veya verileri çıkarma gibi işlemleri desteklemesini sağlayın.

3. **Arayüz Üzerinden Model Ekleme:**
   - Yeni modellerin sistem yapılandırma dosyasını manuel olarak değiştirmeden doğrudan arayüzden eklenmesini sağlayın.

4. **Web Kazıma ile API Fiyatlarını Ayarlama:**
   - Resmi sağlayıcı web sitelerinden fiyatlandırma bilgilerini kazıyarak API fiyatlandırma yapılandırmalarını otomatik olarak güncelleyin.

5. **Arayüzden Maksimum Token Boyutu Ayarı:**
   - Konuşma maksimum token boyutunu doğrudan arayüz üzerinden yapılandırma imkanı sunarak bağlam uzunluğu ve performans üzerinde daha iyi kontrol sağlayın.

---
