import networkx as nx
import folium
import numpy as np
import os

def elenca_file_graphml():
    """
    Elenca tutti i file .graphml nella directory corrente e permette all'utente di sceglierne uno.
    """
    files = [f for f in os.listdir('.') if f.endswith('.graphml')]
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    scelta = int(input("Scegli il file da caricare (numero): ")) - 1
    return files[scelta]

def carica_grafo_da_graphml(file_path):
    return nx.read_graphml(file_path)

def mostra_numero_nodi(G):
    print(f"Il grafo ha {len(G.nodes())} nodi.")

def seleziona_nodi(nodi):
    selezione = input("Scegli un nodo o un intervallo di nodi (es. 5 o 1-10): ")
    nodi_selezionati = []
    try:
        if '-' in selezione:
            start, end = map(int, selezione.split('-'))
            nodi_selezionati = nodi[start-1:end]
        else:
            indice = int(selezione) - 1
            nodi_selezionati = [nodi[indice]] if 0 <= indice < len(nodi) else []
    except ValueError:
        print("Formato non valido.")
    return nodi_selezionati

def calcola_soglie_centralita(centralita_di_grado):
    valori = list(centralita_di_grado.values())
    quartili = np.percentile(valori, [25, 50, 75])
    return {
        'basso': quartili[0],
        'medio': quartili[1],
        'alto': quartili[2]
    }

def interpreta_centralita(centralita, soglie):
    """
    Interpreta la centralità di grado di un nodo rispetto alle soglie calcolate e fornisce un feedback
    sulla sua rilevanza all'interno della rete, insieme a una breve spiegazione.
    """
    if centralita >= soglie['alto']:
        feedback = "Molto rilevante"
        spiegazione = ("Questo nodo ha una centralità di grado significativamente alta, indicando che "
                       "è uno dei nodi più connessi e centrali nella rete. È probabilmente un punto critico "
                       "per il flusso di informazioni o traffico all'interno della rete.")
    elif centralita >= soglie['medio']:
        feedback = "Rilevante"
        spiegazione = ("Questo nodo ha una centralità di grado moderatamente alta, indicando che "
                       "gioca un ruolo importante nella rete, collegando diverse parti o facilitando "
                       "il flusso all'interno della rete.")
    elif centralita >= soglie['basso']:
        feedback = "Poco rilevante"
        spiegazione = ("Questo nodo ha una centralità di grado bassa, indicando che, sebbene possa "
                       "collegarsi a più nodi, non è centrale per la maggior parte dei percorsi nella rete.")
    else:
        feedback = "Marginale"
        spiegazione = ("Questo nodo ha una centralità di grado molto bassa, indicando che è poco connesso "
                       "e probabilmente si trova ai margini della rete o in una posizione periferica.")
    
    return feedback, spiegazione

def visualizza_nodi_su_mappa(G, nodi_selezionati, centralita_di_grado, soglie):
    mappa = folium.Map(location=[41.9028, 12.4964], zoom_start=6)
    for nodo in nodi_selezionati:
        attributi = G.nodes[nodo]
        feedback = interpreta_centralita(centralita_di_grado[nodo], soglie)
        folium.Marker(
            [float(attributi['y']), float(attributi['x'])],
            popup=f"Nodo: {nodo}\nCentralità di grado: {centralita_di_grado[nodo]}\nImportanza: {feedback}\nStreet count: {attributi.get('street_count', 'N/A')}",
        ).add_to(mappa)
    for nodo in nodi_selezionati:
        mappa.save(f'nodo_{nodo}.html')
        break

def calcola_centralita_di_grado_e_attributi(G, nodi_selezionati):
    centralita_di_grado = nx.degree_centrality(G)
    soglie = calcola_soglie_centralita(centralita_di_grado)
    for nodo in nodi_selezionati:
        feedback, spiegazione = interpreta_centralita(centralita_di_grado[nodo], soglie)
        print(f"\nNodo {nodo}:")
        print(f"Centralità di grado: {centralita_di_grado[nodo]} - {feedback}")
        print(spiegazione)
        attributi = G.nodes[nodo]
        for attributo, valore in attributi.items():
            print(f"  {attributo}: {valore}")
    mappa = visualizza_nodi_su_mappa(G, nodi_selezionati, centralita_di_grado, soglie)

if __name__ == "__main__":
    nome_file_graphml = elenca_file_graphml()
    if nome_file_graphml:
        G = carica_grafo_da_graphml(nome_file_graphml)
        mostra_numero_nodi(G)
        nodi = list(G.nodes())
        nodi_selezionati = seleziona_nodi(nodi)
        if nodi_selezionati:
            calcola_centralita_di_grado_e_attributi(G, nodi_selezionati)
        else:
            print("Nessun nodo selezionato per il calcolo.")
    else:
        print("Operazione annullata o nessun file .graphml disponibile.")