Titolo:Progetto di Metodi computazionali per la fisica per la simulazione di sciami elettromagnetici.
Autore: Simone Cingolani
Data: Marzo/Aprile/Maggio 2025

Il progetto si compone di tre script Python: funzioni_e_classi.py, simulazioni1.py, main.py.
Per eseguire il programma è necessario scaricare e porre in una medesima directory i 3 script.
Prima di eseguire il file main.py assisucarsi di avere installato pyfiglet (oltre alle librerie numpy, matplotlib,argparse,math). Se così non dovesse essere, è possibile usare in serie i seguenti comandi da terminale (per maggiorni informazioni consultare: https://installati.one/install-python3-pyfiglet-ubuntu-20-04/):
-sudo apt-get update
-sudo apt-get -y install python3-pyfiglet

Eseguendo il programma con il comando python3 main.py l'utente sarà messo davanti ad una scelta:
  -rispondendo di sì potrà inserire manualmente i valori caratteristici del materiale, l'energia della particella ed il passo di avanzamento della simulazione: verranno restituiti il numero di particelle ad ogni passo, l'energia persa per ionizzazione ad ogni passo e l'energia totale persa per ionizzazione. Inoltre l'utente potrà visualizzare i risultati intermedi per lo sviluppo dello sciame usando il comando -s oppure --stampa dopo python3 main.py. Analogamente sarà possibile visualizzare un grafico dell'andamento del singolo sciame simulato in funzione della profondità usando il comando -g0 oppure --grafici0.
  -rispondendo di no l'utente sarà posto dinnanzi alla scelta del materiale da studiare. Una volta scelto il materiale, l'utente potra scegliere il valore del passo di avanzamento e i valori di energia iniziale da studiare. All'utente sarà inoltre chiesto quanti sciami vuole simulare per ogni valore di energia iniziale.
  Nel caso l'utente non abbia espresso interesse nel visualizzare alcun grafico sulla schermata comparirà la scritta "Non avendo selezionato nulla non verrà mostrato alcun grafico".
  Se l'utente (come è ragionevole che sia) è interessato ad uno o tutti i grafici che descrivono gli sciami elettromagnetici nel materiale scelto potrà usare i seguenti comandi (da scrivere dopo python3 main.py da barra di comando):
   -per visualizzare il grafico relativo all'evoluzione del numero di particelle nello sciame in funzione della profondità (ed un istogramma della distribuzione di dati ad una fissata profondità) è possibile usare il comando -g0 (oppure --grafici0).
   -per visualizzare il grafico relativo allo studio dello sviluppo longitudinale dello sciame in funzione dell'energia (e relativo istogramma di come si distribuiscono i dati per un fissato valore di energia) che riporta il valore medio della profondità (in cm) a cui si ha il massimo dello sciame è possibile sfruttare il comando -g1 (oppure --grafici1).
   -per visualizzare il grafico relativo allo studio dell'energia persa per ionizzazione in funzione dell'energia (e relativo istogramma di come si distribuiscono i dati per un fissato valore di energia) è possibile sfruttare il comando -g2 (oppure --grafici2).

In questi casi all'utente verrà chiesto anche: "Si inserisca l'indice dell'energia iniziale degli sciami da studiare", l'utente dovrà rispondere inserendo il numero che identifica l'energia che si ha interesse a studiare (questa sarà l'energia che sarà fissata per la costruzione degli istogrammi e per la rappresentazione dell'evoluzione del numero medio di particelle dello sciame).

Attivando tutte e tre le seguenti possibilità (python3 main.py -g0 -g1 -g2) sarà possibile visualizzare tutti i grafici disponibili.

Analogamente al caso precedente, l'utente potrà visualizzzare le stampe che descrivono l'andamento intermedio dello sciame con il comando -s (--stampa).




BREVEMENTE:
Il primo script (funzioni_e_classi) contiene le funzioni che sono impiegate nel modulo simulazioni1.py e nel modulo main.py oltre al dizionario di materiali che possono essere studiati e le classi Particella ed InsiemeParticelle.
Il secondo script(simulazioni.py) contiene le funzioni impiegate per la simulazione di uno sciame elettromagnetico.
Il terzo script (main.py) contiene le funzioni per l'interfaccia con l'utente (e controllo degli input) e la presentazione dei risultati (se richiesti dall'utente da riga di comando).

TUTTE LE FUNZIONI SONO DOTATE DI DOCSTRING: PER VISUALIZZARLO SI APRA PYTHON DA TERMINALE E SI IMPORTI LA FUNZIONE DI INTERESSE DAL MODULO, SI SCRIVA HELP(NOME_FUNZIONE) E PER USCIRE SI PREMA q.


