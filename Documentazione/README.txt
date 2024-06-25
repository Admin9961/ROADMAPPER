Questo programma è composto da quattro script, vanno eseguiti nell'ordine:

1. 'python raccolta_dati.py': questo si occupa di scaricare i dati richiesti da OpenStreetMap. L'utente può selezionare liberamente la regione, e i formati sono salvati in '.graphml' per ulteriori analisi, e anche in '.png' per avere una prima panoramica;
2. 'python graph_to_geojson.py': converte il '.graphml' in geojson usando il formato EPSG=4326. Nel processo il '.graphml' viene semplificato, per facilitare il lavoro su computer meno performanti;
3. 'python distribuzione_stradale.py': qui usiamo il geojson per visualizzare i dati sulla rete stradale con matplotlib;
4. 'python calc_cent_grado.py': questo estrae informazioni su ciascun nodo, lo georeferenzia con folium, e ne calcola la centralità di grado.

Lo scopo dello script, consistente nell'analisi delle reti stradali italiane, può essere usato per studiare la sicurezza della rete o identificare aree con alta accessibilità per lo sviluppo di servizi pubblici.
Comprende un 'Dockerfile' per la virtualizzazione dell'impianto.