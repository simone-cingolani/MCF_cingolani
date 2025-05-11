import numpy as np
import matplotlib.pyplot as plt
import argparse
import pyfiglet


#FUNZIONI PER LA RICHIESTA VALORI IN INPUT


def richiesta_input_positivo(messaggio):

    """
    Chiede un valore positivo all'utente e verifica che sia valido. Il valore deve essere un numero maggiore di zero.
    Parametri
    -----------
       messaggio (string): messaggio che l'utente visualizza.
        
    
    Restituisce
    -----------
       valore_input (float)  il valore inserito dall'utente come float(una volta superati i controlli)
    """


  
    while True:
      valore_input=(input(messaggio))                                 #chiedo valore e sostituisco eventuali virgole con punti
      valore_input = valore_input.replace(',', '.')

      if valore_input.replace('.','1',1).isdigit():   #questa strategia mio permette di controllare che l'input sia effettivamente una cifra (a meno del punto decimale)
        valore_input = float(valore_input)
        if valore_input>0:
          return valore_input
      else:
          print("Non è stato inserito un numero valido.")



def richiesta_input_0_1(messaggio):

    """
    Chiede un valore compreso tra 0 e 1 all'utente e verifica che l'input sia valido.
    Parametri
    -----------
       messaggio (stringa): messaggio che si vuole far visualizzare all'utente come stringa
        
    
    Restituisce
    -----------
       valore_input (float) ossia il valore inserito dall'utente come float(una volta superati i controlli).
    """


  
  
    while True:
      valore_input=(input(messaggio))
      valore_input = valore_input.replace(',', '.')
      if valore_input.replace(".","1",1).isdigit():
        valore_input = float(valore_input)
        if (valore_input>=0) and (valore_input<=1):
          return valore_input
        else:
          print("Non è stato inserito un valore tra 0 e 1")
      else:
        print("Non è stato inserito un numero valido")





#CREAZIONE DELLE CLASSI
class Particella:
    def __init__(self, tipo, energia):
        self.tipo = tipo
        self.energia = energia

    def aggiorna_energia(self, nuova_energia):
        self.energia = nuova_energia

class InsiemeParticelle:
    def __init__(self):
        self.elettrone = []
        self.positrone = []
        self.fotone = []

    def aggiunta(self, particella):
        if particella.tipo == "elettrone":
            self.elettrone.append(particella)
        elif particella.tipo == "positrone":
            self.positrone.append(particella)
        elif particella.tipo == "fotone":
            self.fotone.append(particella)





#DEFINISCO LA FUNZIONE CHE SFRUTTANDO PARSEAGRUMENT MI MOSTRA I PRINT INTERMEDI (CHE MI FANNO SEGUIRE L'EVOLUZIONE DELLO SCIAME IN LIVE)

def parse_arguments():

    """
    Permette all'utente di passare informazioni al programma dalla linea di comando: scegliere se visualizzare grafici o stampe intermedie.
    Parametri
    -----------
       None
        
    
    Restituisce
    -----------
       parser.parse_args() (Oggetto Namespace che contiene i valori degli argomenti in base alle scelte dell'utente)
    """
  
    parser = argparse.ArgumentParser(description='Simulazione di uno scieme elettromagnetico.',
                                     usage      ='python3 main.py  --opzione')
    parser.add_argument('-s', '--stampa',    action='store_true',                    help="Mostra l'evoluzione dello sciame attraverso controlli intermedi")
    parser.add_argument('-g1', '--grafici1', action='store_true',                    help="Mostra i grafici sullo sviluppo longitudinale dello sciame")
    parser.add_argument('-g2',  '--grafici2', action='store_true',                    help="Mostra i grafici sulla perdita di energia dello sciame")
    parser.add_argument('-g0', '--grafici0', action='store_true',                     help="Mostra i grafici relativi all'evoluzione dello sciame in termini di numero di particelle")
    return  parser.parse_args()




#DEFINIZIONE DIZIONARIO DEI MATERIALI DA STUDIARE
materiali = {
    "lutetium silicon oxide": { "E_c_elettrone": 11.71,  # MeV
                             "E_c_positrone": 11.32,  # MeV
                             "Perdita_ionizz": 9.648, # MeV/cm
                             "xi": 1.143              # cm
                             },
    "roccia standard": {"E_c_elettrone": 49.13, #MeV
                        "E_c_positrone": 47.74, #MeV
                        "Perdita_ionizz": 4.47, #MeV/cm
                        "xi": 10.02             # cm
                         }}




def errorbar_funzione(ax, xdata, ydata, erry, titolo, titolox, titoloy):
    """
    Permette di plottare un grafico con barre d'errore.
    Parametri
    -----------
        ax (oggetto Axes):    oggetto Axes che verrà mostrato
        xdata (array o lista di float): array di dati da visualizzare sulle ascisse
        ydata (array o lista di float): array di dati da visualizzare sulle ordinate
        erry  (array o lista di float): incertezza da associare a ydata
        titolo (stringa): titolo del grafico
        titolox (stringa) : label dell'asse x
        titoloy(stringa)  : label dell'asse y
        
    
    Restituisce
    -----------
         None
    La sua azione è quella di modificare ax
    """
    ax.errorbar(xdata,ydata,yerr=erry,fmt='o',markerfacecolor='gray',markeredgecolor='black',ecolor='black',elinewidth=0.9,capsize=4,label=r'Media $\pm$ Std')
    ax.set_title(titolo, fontsize=16, fontweight='bold')
    ax.set_xlabel(titolox,fontsize=14, fontweight='bold')
    ax.set_ylabel(titoloy, fontsize=14, fontweight='bold')
    ax.grid(True, which='both', alpha=0.5)
    #ax.set_yscale('log')
  
def hist_funzione(ax,datax,titolo,titolox,range_istogramma):
    """
    Permette di plottare un grafico di tipo istogramma.
    Parametri
    -----------
        ax (oggetto Axes):    oggetto Axes che verrà mostrato
        datax (array o lista di float): array di dati di cui studiare la distibuzione
        titolo (stringa): titolo del grafico
        titolox (stringa) : label dell'asse x
        range_istogramma(tuple): range dell'istogramma
        
    
    Restituisce
    -----------
         None
    La sua azione è quella di modificare ax
    """
  #minimo=min(datax)
  #massimo=max(datax)
  #range_istogramma=(minimo-10,massimo+10)

    ax.hist(datax, bins='auto', range=range_istogramma, edgecolor='black',color='dimgray',alpha=0.8)
    ax.set_title(titolo, fontsize=16, fontweight='bold')
    ax.set_xlabel(titolox, fontsize=14, fontweight='bold')
    ax.set_ylabel('Occorrenze', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.5)
    #ax.set_yscale('log')



  
def scelta_tra_due_possibilità(messaggio,possibilità1,p1, possibilità2, p2, messaggio_err):
    """
    Permette di mostrare all'utente un messaggio, ricevere un input e controllare se corrisponda ad una tra due stringhe.
    Parametri
    -----------
        messaggio (stringa): messaggio che si vuole far visualizzare all'utente per ricevere in input una stringa
        possibilità1 (stringa):prima possibilità con cui confrontare l'input
        possibilità2 (stringa):seconda possibilità con cui confrontare l'input
        p1 (stringa): abbreviazione per possibilità1
        p2 (stringa): abbreviazione per possibilità2
        messaggio_err (stringa): messaggio da far visualizzare all'utente in caso di input non compatibile 
        
    
    Restituisce
    -----------
        scelta (stringa)
    """
  
    while True:
      user_input=(input(messaggio))
      if (user_input==possibilità1) or (user_input==possibilità2) or (user_input==p1) or (user_input==p2):
        scelta=user_input
        return scelta
      else:
        print(messaggio_err)


#in "calcolo statistica" prendo una lista anziché un array perché le operazioni di append (con cui ottengo le liste da dare come argomento alla funzione) su liste sono più rapide
def calcolo_statistica(lista):

    """
    Permette il calcolo di media, deviazione standard e deviazione standard della media di una lista.
    Parametri
    -----------
        lista (lista di float): lista di cui si vuole calcolare media, std e stdm
        
    
    Restituisce
    -----------
        (media,std,std_media) (tuple)
        None nel caso in cui la lista è troppo corta
    """
    if len(lista) > 1:       #altrimenti rischio NaN
      lista = np.array(lista)
      media = np.mean(lista)
      #se simulo tot sciami (sono un campione) voglio che questi mi forniscano una stima della variabilità reale---->uso la campionaria (ddof=1)
      std = np.std(lista, ddof=1)
      std_media = std / np.sqrt(len(lista))
      return media, std, std_media
    else:
      return None



def stampa_titolo1():
    """
    Permette di stampare un banner
    """
    titolo = pyfiglet.figlet_format("Benvenuto! \n Simuliamo\nqualche\nsciame!!!")
    print(titolo)
