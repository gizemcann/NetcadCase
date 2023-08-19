import requests
import psycopg2
from json.decoder import JSONDecodeError

# PostgreSQL veritabanı bağlantısı
conn = psycopg2.connect(
    database="eczane",
    user="postgres",
    password="123456",
    host="localhost",
    port= 5432
)
cur = conn.cursor()

# API URL
api_url = "https://collectapi.com/tr/api/health/nobetci-eczane-api?il=Ankara&ilce=Çankaya"

try:
    # API isteği gönderme
    response = requests.get(api_url)
    response.raise_for_status()  # Hata durumunda istisna fırlatır

    try:
        data = response.json()
        pharmacies = data.get("result")

        for pharmacy in pharmacies:
            name = pharmacy.get("name")
            address = pharmacy.get("address")
            phone = pharmacy.get("phone")

            # PostgreSQL'a veri ekleme
            cur.execute(
                "INSERT INTO pharmacies (name, address, phone) VALUES (%s, %s, %s)",
                (name, address, phone)
            )
            conn.commit()

        print("Veriler başarıyla PostgreSQL veritabanına aktarıldı.")

    except JSONDecodeError:
        print("API yanıtı JSON olarak çözümlenemedi.")

except requests.exceptions.RequestException as e:
    print("API isteği sırasında bir hata oluştu:", e)

# Bağlantıyı kapat
cur.close()
conn.close()




