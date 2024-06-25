import osmnx as ox
import os
import hashlib
import shutil
import matplotlib.pyplot as plt
import geopandas as gpd

ox.config(use_cache=True, log_console=True)

regioni_italiane = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia",
    "Toscana", "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"
]

print("Su quale regione vuoi operare?")
for indice, regione in enumerate(regioni_italiane, start=1):
    print(f"{indice}. {regione}")

scelta = int(input("Scegli il numero corrispondente alla regione: ")) - 1
luogo = f"{regioni_italiane[scelta]}, Italia"

def genera_hash_query(query):
    return hashlib.sha1(query.encode('utf-8')).hexdigest()

def rinomina_file_cache(hash_query, nuovo_nome):
    cartella_cache = '.osmnx/cache'
    vecchio_nome_file = os.path.join(cartella_cache, f"{hash_query}.json")
    nuovo_nome_file = os.path.join(cartella_cache, f"{nuovo_nome}.json")
    
    if os.path.exists(vecchio_nome_file):
        shutil.move(vecchio_nome_file, nuovo_nome_file)
        print(f"File rinominato: {nuovo_nome_file}")
    else:
        print("File non trovato nella cache.")

def plot_semplificato(rete, descrizione):
    fig, ax = ox.plot_graph(rete, node_size=0, edge_linewidth=0.5, show=False, close=False)
    plt.axis('off')
    plt.savefig(f"{descrizione}_{luogo.split(',')[0].lower()}_simpl.png", dpi=300)
    plt.close()
    print(f"Plot semplificato salvato come {descrizione}_{luogo.split(',')[0].lower()}_simpl.png")

def scarica_e_salva(luogo, tipo_rete, descrizione):
    query = f"{luogo}_{tipo_rete}"
    hash_query = genera_hash_query(query)
    rete = ox.graph_from_place(luogo, network_type=tipo_rete)
    nome_file = f"{descrizione}_{luogo.split(',')[0].lower()}.graphml"
    ox.save_graphml(rete, filepath=nome_file)
    print(f"Grafo salvato come {nome_file}")
    plot_semplificato(rete, descrizione)
    
    rinomina_file_cache(hash_query, nome_file.replace('.graphml', ''))

scarica_e_salva(luogo, "drive", "rete_stradale")