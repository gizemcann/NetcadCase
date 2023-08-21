from sqlalchemy import create_engine, text
from geoalchemy2 import Geometry
import geopandas as gpd

user = "postgres"
password = "123456"
host = "localhost"
port = 5432
database = "eczane"

conn = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(conn)

#Read shapefile using GeoPandas
shapefile_path = 'C:/Users/user/Desktop/CaseStudy/CaseStudy/İlçeler/ilceler_ankara_3857.shp'
gdf = gpd.read_file(shapefile_path)

#Define the geometry column types using Geometry from geoalchemy2
geometry_type = Geometry(geometry_type='GEOMETRY')

#Drop the geometry column temporarily
gdf_no_geom = gdf.drop(columns=['geometry'])

#Import the DataFrame without geometry to the database
gdf_no_geom.to_sql(name="boundary", con=engine, schema="public", if_exists="replace", index=False)

#Add the geometry column with the correct type using GeoAlchemy2

with engine.connect() as connection:
    connection.execute(text(f"ALTER TABLE public.boundary ADD COLUMN geometry {geometry_type};"))
    connection.execute(text(f"UPDATE geometry_columns SET srid=3857 WHERE f_table_name='boundary' AND f_geometry_column='geometry';"))
    for index, row in gdf.iterrows():
        connection.execute(text(f"UPDATE public.boundary SET geometry = ST_GeomFromText(:geom, 3857) WHERE index = :index;"), geom=row['geometry'].w)

print("succes")