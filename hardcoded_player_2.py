import requests
import json
import math

# Yarışmadan veri aldığınız adres 
get_url = 'http://localhost:3000'

# Yarışmaya veri gönderdiğiniz adres
post_url = 'http://localhost:4000'

# Verilerin JSON tipinde olduğu belirten iki satır
get_headers = {'Content-Type': 'application/json'}
post_headers = {'Content-Type': 'application/json'}

# Tankın gitmesini istediğimiz lokasyonlar (x,y) listesi
positions2go = [[110, 370],[320,370],[320,620],[680,620],[850,320]]

# Rakip tankın pozisyonunu ekleyeceğiz
# Ateş etmek için lazım olacak
position2attack = [0,0]

# Oyun boyunca sürekli yapmasını istediklerimiz
while True:
    # Ateş etmenin açık kalmadığına emin ol
    f, m, r = 0, 0, 0

    # Oyundan veriyi çek 
    data = requests.get(get_url, headers=get_headers)
    # Veriyi JSON'dan kullanılabilir hale getir
    jsonData = json.loads(data.text)

    # Veriyi değişkenlere ata
    current_x = float(jsonData["tankA"]["x"])
    current_y = float(jsonData["tankA"]["y"])
    current_r = float(jsonData["tankA"]["r"])

    # Lokasyonlar listesi dolu oldukça bunları yap
    if len(positions2go) > 0:
        # Denerken görmek için veriyi yazdır (gidilecek lokasyon, uzaklık x ve y)
        print(positions2go[0], abs(positions2go[0][0] - current_x), abs(positions2go[0][1] - current_y))
        
        # Eğer lokasyona 30 pixelden uzaktaysak bunu yap
        if abs(positions2go[0][0] - current_x) > 30 or abs(positions2go[0][1] - current_y) > 30:
            # atan matematik fonksiyonuyla dönmen gereken açıyı bul
            wanted_r_rad = math.atan2((positions2go[0][1] - current_y),(positions2go[0][0] - current_x))
            # PI ve -PI arasında bulduğun açıyı dereceye çevir.
            wanted_r = -((wanted_r_rad * 180) / math.pi)
            # Yeterince doğru açıdaysan dön
            if abs(current_r - wanted_r) <= 30:
                m, r = 1, 0
            # Açıya 30 dereceden fazla yaklaşana kadar dön
            else:
                m, r = 0, 1
        # Listedeki lokasyona varınca bunu yap
        else:
            # varılan lokasyonu listeden çıkart
            positions2go.pop(0)    
    else:
        # Lokasyonlar listesi boşalınca bunu yap
        position2attack[0] = float(jsonData["tankB"]["x"])
        position2attack[1] = float(jsonData["tankB"]["y"])
        # atan matematik fonksiyonuyla dönmen gereken açıyı bul
        wanted_r_rad = math.atan2((position2attack[1] - current_y),(position2attack[0] - current_x))
        # PI ve -PI arasında bulduğun açıyı dereceye çevir.
        wanted_r = -((wanted_r_rad * 180) / math.pi)
        # Açıya 30 dereceden fazla yaklaşana kadar dön.
        if abs(current_r - wanted_r) <= 30:
            f = 1
        # Doğru açıdasın ateş et
        else:
            m, r = 0, 1
    
    # Veriyi göndermek için hazırla
    data = {"m": m, "r":r, "f":f}
    # JSON formatına dönüştür
    data = json.dumps(data)
    # Gönder
    response = requests.post(post_url, data=data, headers=post_headers)
