import http.client
import psycopg2
import json

# PostgreSQL veritabanı bağlantısı
conn_postgres = psycopg2.connect(
    database="eczane",
    user="postgres",
    password="123456",
    host="localhost",
    port= 5432
)
cur_postgres = conn_postgres.cursor()

# API bağlantısı
conn_api = http.client.HTTPSConnection("api.collectapi.com")

headers = {
    'content-type': "application/json",
    'authorization': "apikey 4qq5VVSdgJppXDX3ik5ftZ:1BGnPkR5jho5bK3CKplnCS"
}

conn_api.request("GET", "/health/dutyPharmacy?ilce=%C3%87ankaya&il=Ankara", headers=headers)

res = conn_api.getresponse()

data = res.read()

# API'den gelen veriyi JSON olarak çözümle
api_data = json.loads(data.decode("utf-8"))
# Verileri PostgreSQL veritabanına eklemek
for pharmacy in api_data["result"]:
    name = pharmacy.get("name")
    dist = pharmacy.get("dist")
    address = pharmacy.get("address")
    phone = pharmacy.get("phone")
    loc = pharmacy.get("loc")

    # Verinin benzersiz bir özelliği ile kontrol yap
    cur_postgres.execute(
        "SELECT * FROM pharmaciess WHERE name = %s AND address = %s",
        (name, address)
    )
    existing_pharmacy = cur_postgres.fetchone()

    # Veri yoksa eklemeyi yap
    if not existing_pharmacy:
        cur_postgres.execute(
            "INSERT INTO pharmaciess (name, dist, address, phone, loc) VALUES (%s, %s, %s, %s, %s)",
            (name, dist, address, phone, loc)
        )
        conn_postgres.commit()
        print(f"{name} eklendi.")
    else:
        print(f"{name} zaten var, eklenmedi.")

print("Veri aktarım işlemi tamamlandı.")

# Bağlantıları kapat
cur_postgres.close()
conn_postgres.close()

