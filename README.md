-Generale
Per buildare il progetto (su linux) basta eseguire il file build_linux.sh
Contiene i comandi docker che vedi sotto.
(potrebbe essere necessario modificare i permessi del file con chmod +x build_linux.sh)

-Docker

Per far funzionare Flask e Docker insieme ho dovuto fare il downgrade a python3.9, non dovrebbe dare grossi problemi di retrocompatibilita' ma se possibile installate quella versione per evitare probelmi.

Per aggiungere dipendenze inserire il nome del package (scaricato da pip3) al file requirements.txt (IMPORTANTE: chi scrive il codice con dipendenze si assicura di aggiornare il file prima di pushare).
Se avete dipendenze scaricate da altre fonti (apt, apt-get, snap, ecc) fatemelo sapere.

Per accedere all'app una volta lanciata l'immagine si puo' usare l'inidirizzo di localhost o 0.0.0.0:8000 (dall'interno) o <ip>:5000 (dall'esterno, se lanciata sul server di dipartimento o in remoto)
(e' possibile che quando deployeremo sul server dovremo cambiare le porte per firewall e cose varie).

Comandi essenziali:
#builda l'immagine docker dopo aver modificato il codice e prima di lanciarla (o se non hai mai lanciato questa release)
docker build -t team4/twitterutils .
#lancia l'immagine docker accessibile da 127.0.0.1 su porta 8000
docker run -p 8000:5000 team4/twitterutils