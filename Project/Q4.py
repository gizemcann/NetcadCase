import openpyxl
import psycopg2

# Excel dosyasını oku
wb = openpyxl.load_workbook('C:/Users/user/Desktop/CaseStudy/CaseStudy/basvuru_noktaları.xlsx')
sheet = wb.active

data = []
for index, row in enumerate(sheet.iter_rows(values_only=True)):
    if index == 0:  # Skip header row
        continue
    data.append(row)

# PostgreSQL veritabanına bağlan
conn = psycopg2.connect(
    dbname="eczane",
    user="postgres",
    password="123456",
    host="localhost",
    port=5432
)
cursor = conn.cursor()

for row in data:
    sql = "INSERT INTO basvuru_noktaları (basvuru_numarasi, kisi_adi, adresi, sehri) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, row)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
cursor.close()
conn.close()

print("Veriler PostgreSQL'e aktarıldı.")
