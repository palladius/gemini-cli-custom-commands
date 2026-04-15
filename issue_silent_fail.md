# Bug: Lo script `musicgen-lyria3` fallisce silenziosamente se la cartella di destinazione non esiste

**Descrizione del problema:**
Quando si eseguono gli script della skill `musicgen-lyria3` (ad esempio `musicgen-lyria3-30sec.py` o `musicgen-lyria3-2min.py`) specificando un file di output in una sotto-cartella che non esiste (es. `lyria_music/YYYYMMDD/nome_file.mp3`), lo script non crea il file ma termina comunque con **exit code 0 (successo)**.
Questo causa un problema enorme per i modelli LLM, che credono che la generazione sia andata a buon fine e impazziscono cercando il file "fantasma".

**Causa:**
Manca la cartella genitore e lo script non gestisce correttamente l'eccezione o non fa fallire l'esecuzione in modo visibile.

**Soluzione proposta (da Riccardo):**
Invece di forzare la creazione della cartella (es. con un `mkdir -p` silente) col rischio di creare alberature di cartelle strane o indesiderate, la soluzione migliore è fare un **fallimento corretto e rumoroso**.
Lo script dovrebbe intercettare l'errore di cartella inesistente e fare una `print` o `echo` chiara dell'errore, terminando con un exit code di errore (es. `exit 1`). In questo modo, il modello (come OpenClaw) riceve il feedback corretto ("Cartella non trovata") e può correggere il tiro (ad esempio creando la cartella prima di riprovare).