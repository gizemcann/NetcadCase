
import ezdxf
import psycopg2

# PostgreSQL bağlantısı
conn = psycopg2.connect(
    dbname="eczane",
    user="postgres",
    password="123456",
    host="localhost",
    port= 5432
)
cursor = conn.cursor()

# DXF dosyasını açma
dxf_file = 'C:/Users/user/Desktop/CaseStudy/CaseStudy/Maden Sınırları/maden_sinirlari.dxf'
doc = ezdxf.readfile(dxf_file)

# DXF data insertion into PostgreSQL
for entity in doc.modelspace().query('*'):
    layer = entity.dxf.layer
    paperspace = entity.dxf.paperspace
    linetype = entity.dxf.linetype
    entityhandle = entity.dxf.handle

    if entity.dxftype() == 'TEXT':
        text = entity.dxf.text
    elif entity.dxftype() == 'MTEXT':
        text = entity.plain_text()
    elif entity.dxftype() == 'ATTRIB':
        text = entity.dxf.text
    else:
        text = None  # Default to None if entity type doesn't have text

    # PostgreSQL insertion query
    insert_query = """
    INSERT INTO dfx_table (layer, paperspace, linetype, entityhandle, text)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (layer, paperspace, linetype, entityhandle, text)

    cursor.execute(insert_query, values)

# Finalize the process
conn.commit()
cursor.close()
conn.close()






