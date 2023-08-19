import os, subprocess

# Choose your PostgreSQL version here
os.environ['PATH'] += 'C:/Program Files/PostgreSQL/15/bin'
# http://www.postgresql.org/docs/current/static/libpq-envars.html
os.environ['PGHOST'] = 'localhost'
os.environ['PGPORT'] = '5432'
os.environ['PGUSER'] = 'postgres'
os.environ['PGPASSWORD'] = '123456'
os.environ['PGDATABASE'] = 'eczane'

base_dir = 'C:/Users/user/Desktop/CaseStudy/CaseStudy/İlçeler/ilceler_ankara_3857.shp'
full_dir = os.walk(base_dir)
shapefile_list = []
for source, dirs, files in full_dir:
    for file_ in files:
        if file_[-3:] == 'shp':
            shapefile_path = os.path.join(base_dir, file_)
            shapefile_list.append(shapefile_path)
for shape_path in shapefile_list:
    cmds = 'shp2pgsql "' + shape_path + '" new_shp_table | psql '
    subprocess.call(cmds, shell=True)