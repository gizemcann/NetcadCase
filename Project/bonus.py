from flask import Flask, render_template
import geopandas as gpd
import folium

app = Flask(__name__)

@app.route('/')
def index():
    # WMS servisi verilerini çek
    wms_url = 'URL_TO_WMS_SERVICE'
    wms_layer = 'LAYER_NAME'
    wms = folium.WmsTileLayer(url=wms_url, layers=wms_layer, format="image/png", transparent=True)
    
    # WFS servisi verilerini çek
    wfs_url = 'URL_TO_WFS_SERVICE'
    wfs_layer = 'LAYER_NAME'
    gdf = gpd.read_file(wfs_url, layer=wfs_layer)
    
    # Harita oluştur
    m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=12)
    
    # WMS ve WFS katmanlarını haritaya ekle
    wms.add_to(m)
    folium.GeoJson(gdf).add_to(m)
    
    return render_template('index.html', map=m._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)
