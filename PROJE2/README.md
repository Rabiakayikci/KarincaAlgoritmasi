# 📋 PROJE TESLİM BİLGİLERİ

**Adınız:** Rabia
**Soyadınız:** KAYIKCI
**Okul Numaranız:** 2312721047
**GitHub Repo Bağlantısı:**
# 🧬 Genetik Algoritma ile bir amaç fonksiyonunun verilen kısıtlara göre optimizasyonu

Bu projede, SDÜ Kampüsünde belirlenen 10 durak kullanılarak en kısa sürede tur hesaplamaları karınca algoritması kullanılarak yapılacaktır.

---

## 📌 KLASÖRLER

 core, data, visual, figure ve .streamlit klasörleri oluşturulmuştur.
---

## 📁 Dosya Yapısı

| Dosya Adı               | Açıklama                                                                                                                              |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `coordinates.py`       | Durak kordinatlarını içerir (googleMapsten gerçek kordinatlar)                                                                         |
| `main.py`              | Algoritmanın çalıştırıldığı ana dosyadır.                                                                                              |
| `README.md`            | Bu açıklama dosyasıdır.                                                                                                                |
| `haversine.py`         | GoogleMaps bağlantısında sıkıntı olursa hata çıkmaması için kordinatlar arasındaki uzaklığı kuş uçuşu hesaplar.                        |
| `matrix_utils.py`      | Duraklar arasındaki mesafeleri hesaplar ve en kısa yolu bulmak için sayısal matrisler hazırlar.                                        |
| `ant_algorithm.py`     | Karıncaların koku ve mesafe bilgisini kullanarak kampüs içinde en kısa yolu bulmak için yaptıkları akıllı simülasyonu yöneten dosyadır.|
| `plotting.py`          | Grafiğe döker.                                                                                                                         |
| `secrets.toml`         | GoogleMaps API anahtarını herkesin görmemesi için özel oluşturulmuş dosyadır.                                                          |
| `rota.png`             | Eğitim grafiğini gösterir.                                                                                                             |
| `convergence.png`      | Çıktı dosyasıdır.                                                                                                                      |

## 📦 Fonksiyon Açıklamaları

### `def haversine(koordinat1, koordinat2)`
Dünya'nın yuvarlak olduğunu hesaba katarak, iki GPS noktası arasındaki "kuş uçuşu" mesafeyi hesaplar.

---

### `def mesafe_matrisi_olustur(koordinatlar, api_key=None)`
Bu fonksiyon, verilen durak listesini ve isteğe bağlı API anahtarını alarak, algoritmanın kullanacağı mesafe matrisini oluşturur. 
İlk adımda, durak sayısı boyutunda ve içi sıfırlarla dolu boş bir kare matris hazırlanır.

Fonksiyon, API anahtarının varlığına göre hareket eder. Eğer geçerli bir Google Maps API anahtarı varsa, servisin "tek seferde maksimum istek" sınırına takılmamak için duraklar 5'erli paketlere bölünür. 
Bu paketler sırasıyla API'ye gönderilir ve duraklar arasındaki gerçek sürüş mesafelerine bakar. Google'dan dönen yanıtlar metre cinsinden olduğu için, bu değerler kilometreye çevrilerek matrise yerleştirilir. 
Eğer Google belirli iki nokta arasında rota bulamazsa, o hücre için otomatik olarak Haversine formülü devreye girer ve kuş uçuşu mesafe hesaplanır.

Eğer API anahtarı hiç tanımlanmamışsa veya API sorgusu sırasında genel bir bağlantı hatası oluşursa, fonksiyon hatayı yakalar ve otomatik olarak yedek moda geçer. 
Bu durumda, matrisin tamamı Haversine formülü kullanılarak kuş uçuşu mesafelerle doldurulur. Fonksiyonun sonunda, Karınca Kolonisi Algoritması'nın kullanıma hazır, dolu bir mesafe matrisi elde edilir.


---

### `def haversine_distance(coord1, coord2)`
Google Maps API'ye ulaşılamadığı veya API'nin rota bulamadığı durumlarda devreye girer ve iki nokta arasındaki mesafeyi kuş uçuşu olarak hesaplar.

Fonksiyon çalışmaya başladığında önce kendisine gönderilen koordinatların formatını kontrol eder, gelen verinin içinde durak ismi varsa onu ayıklar ve sadece koordinat sayılarını (c1 ve c2) alır.

Koordinatlar temizlendikten sonra geopy kütüphanesinin geodesic fonksiyonu devreye girer. 
Bu fonksiyon, Dünya'nın tam düz olmadığını ve kavisli yapısını hesaba katarak iki nokta arasındaki en gerçekçi kuş uçuşu mesafeyi ölçer. 
Sonuç olarak hesaplanan mesafeyi bize Kilometre cinsinden döndürür. Böylece Google Maps çalışmasa bile algoritma durmaz, bu fonksiyon sayesinde yaklaşık mesafelerle çalışmaya devam eder.


---

### `def hesapla_cekicilik(mesafe)`
Karınca seçeceği yolu yolun uzunluğuna göre kara verir. Eğer yol kısa ise bu yol karıncaya daha çekici gelir.
Bu fonksiyonda yapmak istediğimiz ise tam olarak budur.
bir önceki fonksiyondan elde ettiğimiz mesafeleri bu fonksiyona sokarak tercih edeceği en kısa en çekici mesafe tepsit edilir.

---

### `def olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta)`
Karınca şuan nerede, nereye gidebilir, gideceği yerin çekiciliği ve kokusu, koku mu önemli yoksa mesafe mi bu bilgiler parametre olarak alınır.
(burada alpha kokuyu, beta ise mesafeye verilen önemi vurgular.)
Sonra her bir durağın değeri şu şekilde hesaplanır:
durağın kokusu ile alpha, durağın mesafesi ile beta çarpılır ve toplanarak bir değer elde edilir.Sonra bu değerler olasiliklar listesine atılır.
Yüzde hesaplamak içinde bu değerler soplanarak ilerlenir.

Sonra bu elde ettiğimiz olasılıkları toplamı 1 olacak şekilde olasılık değerlerine çeviriyoruz.(rulet)
her bir değer toplama bölünür.(0'a bölme hatası çıkmaması için bir koruma var.eğer toplam 0 ise 1 e böler.)
---

### `def rulet_tekerlegi_secimi(olasilik_dict)`
rastgele bir olasılık değeri seçilir.sırasıyla gelen olasıkları toplayarak belirlenen rastgele değer bu aralıkta mı diye bakar.
eğer bu aralıkta ise o aralık değerini ifade eden durak geri döndürülür.
Eğer seçilen rastgele olasılık değeri herhagi bir aralığa denk gelmezse olasiliklar listesindeki en son durak geri döndürülür.

---

### `def karinca_gezi(baslangic, mesafe, feromon, cekicilik, alpha=1, beta=2)`

Başlangıç noktası belirlenir. Yol uzunluğumuz toplam mesafeden az olduğu sürece yani yol tamamlanana kadar döngü oluşturur.
Yol içerisinde bu zamana kadar gezdiği bütün duraklar tutulur. Ve yeni bir durağa giderken önce en son hangi duraktaydı diye bakılır.
Sonra bütün durakların bulunduğu kümeden şimdiki zamana kadar gidilen durakların tutulduğu listeyi çıkartır.(Hangi duraklara gidilmediğini görmek için.)
Karınca bulunduğu yere göre olasılıkları hesaplar hangisine gitsem acaba diye. En son olarakta aralıklandırma yaparak seçtiği random bir değer ile yeni durağını seçer.
Bu seçilen durak şimdiye kadar gittiği duraklar listesine eklenir.
Seçilen durak ile şuan olunan durak arasındaki mesafeyi toplam mesafeye ekler.
En son gideceği durakta durmaması ve en başta bulunduğu durağa geri dönmesi gerek bu yüzden tüm tutulan kordinatlarda ki son durak tekrar eklenir
o son durak ile şuan olunan durak arasındaki mesafe de hesaplanılarak toplam mesafeye eklenir.
---

### `def feromon_guncelle(feromon, yollar, buharlasma_orani=0.5, Q=1.0)`
Koku karmaşası olmaması için bazı kokuların silinmesi gerek.
Bizim yaptığımız fonksiyonda yollardaki kokuların yarısı silinir.
Karıncaların gittikleri yollardaki kokular azaltıldıktan sonra tekrardan yeni kokular dökülür.
Yolu duraklara göre parçalar sonra Q sabitini gittiği yoldaki mesafelere bölerek katki değeri hesaplanır.
Kısa olan mesafeye daha çok koku bırakır.Kokuyu da çift yönlü bırakır.


---

### `def run_aco(mesafe, karinca_sayisi=5, iterasyon_sayisi=20, alpha=1, beta=2,
            buharlasma_orani=0.5, feromon_katkisi=1)`
Mesafe matrisi gibi ama içi 1lerle dolu olan bir kare matris oluşturulur ve hepsi 0.1 ile çarpılır.(Yolların hepsine eşit ve az olacak şekilde koku bulunması için yapılır.)
Sonra çekicilik hesaplanır. Henüz yol belirleme yapılmadığı için en kısa mesafe sonsuz olarak ayarlanır.
İterasyon sayısı kadar döngü başlatılır.Karıncalar gezmeye gönderilir. Gezdikleri yollar ve uzunluklar listeye eklenir.
en kısa mesafe belirlenir.feromonlar güncellenir.
En son olarak o iterasyonun en iyileri döndürülür.




---

### `def yol_gorsellestir(yol, koordinatlar, kaydet=False, dosya_yolu=None)`
Rotayı görselleştirir.


---

### `def plot_convergence(best_distances, kaydet=False, dosya_yolu=None)`
Karıncaların akıllanıp akıllanmadığını, yol mesafesinin kısalıp kısalmadığını görmemiz için görselleştirir.

---

### `def yol_gorsellestir_folium(yol, koordinatlar)`
Bu fonksiyon, algoritmanın hesapladığı en iyi rotayı görselleştirmek için folium kütüphanesini kullanarak interaktif bir harita oluşturur.  


