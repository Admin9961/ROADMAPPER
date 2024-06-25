import osmnx as ox
import geopandas as gpd
import os

def leggi_grafo_da_file(nome_file):
    """
    Legge un grafo da un file GraphML.
    Args:
        nome_file (str): Il percorso del file GraphML da leggere.
    Returns:
        G (networkx.MultiDiGraph): Il grafo letto dal file GraphML.
    """
    G = ox.load_graphml(nome_file)
    print(f"Grafo letto da {nome_file}.")
    return G

def filtra_dati(G, tipi_strada):
    """
    Filtra il grafo per includere solo i tipi di strada specificati.
    Args:
        G (networkx.MultiDiGraph): Il grafo originale.
        tipi_strada (list): Lista dei tipi di strada da mantenere.
    Returns:
        G_filtrato (networkx.MultiDiGraph): Il grafo filtrato.
    """
    edges_filtrati = [(u, v, k) for u, v, k, data in G.edges(keys=True, data=True) if data['highway'] in tipi_strada]
    G_filtrato = G.edge_subgraph(edges_filtrati).copy()
    print(f"Grafo filtrato mantenendo solo i tipi di strada: {tipi_strada}.")
    return G_filtrato

def standardizza_dati(G):
    """
    Standardizza i dati del grafo, convertendolo in un GeoDataFrame e standardizzando il CRS.
    Args:
        G (networkx.MultiDiGraph): Il grafo da standardizzare.
    Returns:
        gdf_edges (geopandas.GeoDataFrame): GeoDataFrame degli archi standardizzato.
    """
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
    gdf_edges.to_crs(epsg=4326, inplace=True) # Qui lasciamo 4326, con l'altro formato si genera un errore di plotting
    print("Dati standardizzati al CRS WGS 84.")
    return gdf_edges

def salva_dati(gdf, nome_file):
    """
    Salva il GeoDataFrame in un file, convertendo i campi di tipo list in stringhe, escludendo la colonna 'geometry'.
    Args:
        gdf (geopandas.GeoDataFrame): Il GeoDataFrame da salvare.
        nome_file (str): Il percorso del file in cui salvare i dati.
    """
    for col in gdf.columns.drop('geometry'):
        if gdf[col].apply(type).eq(list).any():
            gdf[col] = gdf[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

    try:
        gdf.to_file(nome_file, driver='GeoJSON')
        print(f"Dati salvati in {nome_file}.")
    except Exception as e:
        print(f"Errore nel salvare i dati: {e}")

if __name__ == "__main__":
    files_graphml = [file for file in os.listdir('.') if file.endswith('.graphml')]
    print("File .graphml trovati nella directory corrente:")
    for idx, file in enumerate(files_graphml, start=1):
        print(f"{idx}. {file}")
    scelta_idx = int(input("Scegli il numero del file da convertire: ")) - 1
    nome_file_grafo = files_graphml[scelta_idx]
    tipi_strada = ['motorway', 'primary', 'secondary']
    G = leggi_grafo_da_file(nome_file_grafo)
    G_filtrato = filtra_dati(G, tipi_strada)
    gdf_edges = standardizza_dati(G_filtrato)
    nome_file_geojson = input("Inserisci il nome del file .geojson di output (includi l'estensione .geojson): ")
    salva_dati(gdf_edges, nome_file_geojson)