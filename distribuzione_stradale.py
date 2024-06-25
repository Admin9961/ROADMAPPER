import os
import geopandas as gpd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def massimizza_finestra():
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed') # Testato solo su Windows

def scegli_file_geojson():
    files = [file for file in os.listdir('.') if file.endswith('.geojson')]
    if not files:
        print("Nessun file GeoJSON trovato nella directory corrente.")
        return None
    
    print("File GeoJSON trovati:")
    for indice, file in enumerate(files, start=1):
        print(f"{indice}. {file}")
    
    scelta = int(input("Scegli il numero del file GeoJSON da analizzare: ")) - 1
    return files[scelta]

def analizza_geojson(file_path):
    gdf = gpd.read_file(file_path)
    
    print(f"Numero totale di elementi: {len(gdf)}")
    print(f"Proiezione CRS originale: {gdf.crs}")
    
    gdf = gdf.to_crs(epsg=32633) # Più adatto per analisi in una regione specifica
    print(f"Proiezione CRS trasformata in: {gdf.crs}")
    
    if gdf.geometry.geom_type.unique()[0] == 'LineString':
        gdf['length'] = gdf.geometry.length
        print(f"Lunghezza totale delle strade: {gdf['length'].sum()} metri")
    
    if 'highway' in gdf.columns:
        print(f"Tipi di strada presenti: {gdf['highway'].unique()}")
        plt.figure()
        gdf['highway'].value_counts().plot(kind='bar')
        plt.title('Distribuzione dei Tipi di Strada')
        plt.xlabel('Tipo di Strada')
        plt.ylabel('Frequenza')
        massimizza_finestra()
        plt.show()

    plt.figure()
    gdf.plot()
    plt.title('Mappa della Rete Stradale')
    massimizza_finestra()
    plt.show()

if __name__ == "__main__":
    file_geojson = scegli_file_geojson()
    if file_geojson:
        analizza_geojson(file_geojson)
    else:
        print("Operazione annullata.")