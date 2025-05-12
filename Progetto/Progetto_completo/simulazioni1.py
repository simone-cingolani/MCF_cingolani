import funzioni_e_classi as fc
import numpy as np
import argparse

#definisco m_e*c^2 comeglobal constant
ENERGIA_DI_MASSA=0.511 #MeV


#FUNZIONI DI PROBABILITÀ
def bremsstrahlung(s):
    """
    Funzione di probabilità di emissione di un fotone gamma da parte di e+ ed e-:
    f(x)=1-e^(-x).
    Parametri
    -----------
       s (float): passo di avanzamento della simulazione (tra 0 e 1).
        
    
    Restituisce
    -----------
       f(s)=1-e^(-s) (float) ossia la probabilità di emettere un fotone per bremsstrahlung.
    """
    return 1 - np.exp(-s)


def coppia(s):
  
    """
    Funzione di probabilità di produzione di una coppia di particelle e+ ed e-:
    f(x)=1-e^(-7/9*x).
    Parametri
    -----------
       s (float): passo di avanzamento della simulazione (tra 0 e 1).
        
    
    Restituisce
    -----------
       f(s)=1-e^(-7/9*s) (float) ossia la probabilità di produrre una coppia positrone-elettrone.
    """
    return 1 - np.exp(-7/9 * s)




def gestione_elettroni(sciame_em, val, E_c_elettrone, Perdita_ionizz,nuove_particelle):
    """
    Descrive il comportamento degli elettroni in virtù di quella che è la loro energia, includendo fenomeni di bremsstrahlung e ionizzazione.
    Parametri
    -----------
       sciame_em (Oggetto InsiemeParticelle): è l'insieme di particelle contenente la lista di elettroni sulla copia della quale scorro.
       val (float): passo di avanzamento della simulazione (tra 0 e 1).
       E_c_elettrone (float): energia critica del materiale per gli elettroni.
       Perdita_ionizz (float): l'energia persa per ionizzazione in una lunghezza di radiazione.
       nuove_particelle (lista di oggetti di Particella): lista che raccoglie le particelle originate da una gestione.
        
    
    Restituisce
    -----------
       E_step (float) ossia l'energia persa per ionizzazione e aggiorna sia l'oggetto di InsiemeParticelle che nuove_particelle.
    """

  

    #mi interessa sapere quanta energia perde ognuno degli elettroni nella lista
    E_step=0
    #con list creo una copia su cui scorrere per non creare problemi rimuovendo le particelle
    for e in list(sciame_em.elettrone):

      ################
      #Bremsstrahlung#
      ################
        
      if e.energia > E_c_elettrone:
          x_val = np.random.uniform(0, 1)
          if x_val <= bremsstrahlung(val):
              E = e.energia / 2
              fotone_brem_e = fc.Particella("fotone", E)
              #aggiungo il fotone creato per bremsstrahlung alle nuove particelle (non ancora aggiunto allo sciame_em)
              nuove_particelle.append(fotone_brem_e)
              #in accordo con la conservazione dell'energia, l'elettrone ha metà della sua energia originale
              e.aggiorna_energia(E)
      
      ############## 
      #Ionizzazione#
      ##############
      
      if e.energia > Perdita_ionizz*val:
          energia_persa = Perdita_ionizz*val
          e.aggiorna_energia(e.energia - energia_persa)
          E_step += energia_persa
      else:
          energia_persa = np.random.uniform(0, e.energia)
          sciame_em.elettrone.remove(e)
          E_step += energia_persa
    return E_step



def gestione_fotoni(sciame_em, val,nuove_particelle):
  
    """
    Descrive il comportamento dei fotoni in virtù di quella che è la loro energia, includendo fenomeni di produzione di coppie di ionizzazione.
    Parametri
    -----------
       sciame_em (Oggetto InsiemeParticelle): è l'insieme di particelle contenente la lista di fotoni sulla copia della quale scorro.
       val (float): passo di avanzamento della simulazione (tra 0 e 1).
       nuove_particelle (lista di oggetti Particella): lista che raccoglie le particelle originate dalla gestione.
        
    
    Restituisce
    -----------
       E_step (float) ossia l'energia persa per ionizzazione e aggiorna sia l'oggetto di InsiemeParticelle che nuove_particelle.
    """



    #mi interessa sapere quanta energia viene persa per ionizzazione dai fotoni
    E_step=0
    #l'uso di list mi permette di iterare su una copia (non deep, per poter modificare gli oggetti) della lista di interesse
    for f in list(sciame_em.fotone):
    
      ######################  
      #Produzione di coppie#
      ######################
    
      if f.energia > 2 * ENERGIA_DI_MASSA:
          x_val = np.random.uniform(0, 1)
          if x_val <= coppia(val):
              E = f.energia / 2
              sciame_em.fotone.remove(f)
              #l'operazione precedente sarebbe problematica se stessi iterando su sciame_em.fotone stessa
              nuove_particelle.append(fc.Particella("elettrone", E))
              nuove_particelle.append(fc.Particella("positrone", E))
              #ho aggiunto le due nuove particelle create alla lista delle nuove particelle

      #Ionizzazione

      else:
          energia_persa = np.random.uniform(0, f.energia)
          E_step += energia_persa
          sciame_em.fotone.remove(f)
    return E_step

#POSITRONI:
def gestione_positroni(sciame_em, val, E_c_positrone, Perdita_ionizz,nuove_particelle):
    """
    Descrive il comportamento dei positroni in virtù di quella che è la loro energia, includendo fenomeni di bremsstrahlung e di ionizzazione.
    Parametri
    -----------
       sciame_em (Oggetto InsiemeParticelle): è l'insieme di particelle contenente la lista di positroni sulla copia della quale scorro.
       val (float): passo di avanzamento della simulazione (tra 0 e 1).
       E_c_positrone (float): energia critica del materiale per i positroni.
       Perdita_ionizz (float): l'energia persa per ionizzazione in una lunghezza di radiazione.
       nuove_particelle (lista di oggetti Particella): lista che raccoglie le particelle originate.
    
    Restituisce
    -----------
       E_step (float) ossia l'energia persa per ionizzazione e aggiorna sia l'oggetto di InsiemeParticelle che nuove_particelle.
    """



    #mi interessa la perdita di energia per ionizzazione da tutti i positroni
    E_step=0
    for p in list(sciame_em.positrone):

      ################
      #Bremsstrahlung#
      ################
    
      if p.energia > E_c_positrone:
          x_val = np.random.uniform(0, 1)
          if x_val <= bremsstrahlung(val):
              E = p.energia / 2
              fotone_brem_p = fc.Particella("fotone", E)
              #aggiungo il fotone creato per bremsstrahlung alle nuove particelle
              nuove_particelle.append(fotone_brem_p)
              p.aggiorna_energia(E)

      ##############
      #Ionizzazione#
      ##############

      if p.energia > Perdita_ionizz*val:
          energia_persa = Perdita_ionizz*val
          p.aggiorna_energia(p.energia - energia_persa)
          E_step += energia_persa
      
      else:
          energia_persa = np.random.uniform(0, p.energia)
          sciame_em.positrone.remove(p)
          E_step += energia_persa
    return E_step




#NOTA IMPORTANTE:
#L'energia persa durante l'iterazione i-esima viene salvata in energy_count[i+1],
#se così non fosse associeremmo un'energia persa per ionizzazione in generale diversa da 0 alla profondità di 0cm (fisicamente senza senso).
# Pertanto:
#   - energy_count[0] = 0 corrisponde alla situazione iniziale a 0 cm (prima dell'interazione),
#   - energy_count[n] = perdita energetica avvenuta nel tratto tra (n−1)*val*xi e n*val*xi
#In conclusione l'apparente mismatch che c'è tra energy_count e step non è accidentale ma necessario per
#dare un senso fisico corretto quando si passa da step a profondità in cm.
#Questo vale anche per la creazione di nuove particelle: per cui a 0cm avremmo sempre una particella
#e non il numero di particelle, in generale diverso da 1, che si viene a creare dalla 0_esima iterazione del ciclo(la prima).

#ove xi=lunghezza di rad.




# SIMULAZIONE BASE
def simula_sciame(energia_iniziale, val, E_c_elettrone, E_c_positrone, Perdita_ionizz, stampa=False):

    """
    Simula uno sciame elettromagnetico originato da un elettrone: La simulazione include la gestione dei processi di bremsstrahlung, produzione di coppie e ionizzazione.
    
    Parametri
    -----------
    energia_iniziale (float): energia dell'elettrone che dà origine allo sciame.
    val (float): passo di avanzamento della simulazione (tra 0 e 1).
    E_c_elettrone (float): energia critica del materiale per gli elettroni.
    E_c_positrone (float): energia critica del materiale per i positroni.
    Perdita_ionizz (float): energia persa per ionizzazione in una lunghezza di radiazione.
    stampa (bool): se True, stampa informazioni intermedie.
    
    Restituisce
    -----------
    ion_loss (float): energia totale persa per ionizzazione.
    energy_count (list): energie perse a ogni step.
    count_vector (list): numero di particelle a ogni step (rappresenta l'evoluzione dello sciame).
    step (list): lista degli step.
    """
    #creo un oggetto di InsiemeParticelle
    sciame_em = fc.InsiemeParticelle()
    #inizialmente è popolato unicamente dall'elettrone che da origine allo sciame
    sciame_em.aggiunta(fc.Particella("elettrone", energia_iniziale))

    
    
    ion_loss = 0                #per descrivere la perdita totale di energia
    energy_count = [0]          #per descrivere, ad ogni passo della simulazione, l'energia persa (al passo 0 l'energia persa è nulla: l'elettrone non è entrato ancora)
    count_vector = []           #per descrivere l'evoluzione dello sciame in termini di particelle che lo popolano
    passo = 0                   #per tenere conto dello step corrente
    step = []                   #per salvare i vari step dello sciame
    
    while True:

            
      #salvo il numero di particelle (non verranno conteggiate le particelle create nell'iterazione corrente)---> altrimenti a 0cm potrei avere più particelle oltre all'elettrone originale 
      num_particelle = len(sciame_em.elettrone) + len(sciame_em.positrone) + len(sciame_em.fotone)
      #aggiorno le liste
      count_vector.append(num_particelle)
      step.append(passo)

      

      #se l'utente vuole, viene mostrata la situazione dello step corrente
      #ad esempio, a 0cm (step 0) c'è unicamente l'elettrone e ancora non ha perso energia (è ancora alla soglia del materiale)
      if stampa:
        print(f"Step {passo} - Particelle: {num_particelle}")
        print(f"Elettroni: {len(sciame_em.elettrone)}, Positroni: {len(sciame_em.positrone)}, Fotoni: {len(sciame_em.fotone)}")
        print("----------------------------------------------------------------------------------------------------------------")



      #lo sciame si arresta quando tutte le particelle vengolo rimosse dallo sciame
      if num_particelle == 0:
          break

      #aggiorno il contatore dello step
      passo += 1

      #creo una lista che mi conterrà le particelle originate nello step corrente (che saranno gestite al successivo)
      nuove_particelle=[]
      
      #inizia la gestione delle particelle
      E_step=0
      E_step += gestione_elettroni(sciame_em, val, E_c_elettrone, Perdita_ionizz,nuove_particelle)
      E_step += gestione_positroni(sciame_em, val, E_c_positrone, Perdita_ionizz,nuove_particelle)
      E_step += gestione_fotoni(sciame_em, val,nuove_particelle)

      #questa energia persa (calcolata all'iterazione n sarà da associare alla profondità n+1)---->a 0 cm altrimenti l'eletrone avrebbe già perso energia
      energy_count.append(E_step) 
      ion_loss += E_step

      
      #alle particelle non rimosse dallo sciame em aggiungo le nuove particelle per trovarmele nel computo successivo
      for particella_nuova in nuove_particelle:
          sciame_em.aggiunta(particella_nuova)




    return ion_loss, energy_count, count_vector, step







#SIMULAZIONE AVANZATA

def simulazione_materiali(E_in_list, val, E_c_elettrone, E_c_positrone, Perdita_ionizz, num_simulazioni,stampa=False):

    """
    Permette di simulare diversi sciami elettromagnetici per un certo numero di valori distinti di energia iniziale dello sciame.
    Parametri
    -----------
       E_in_list (lista): lista di valori di energia dell'elettrone che dà origine allo sciame.
       val (float): passo di avanzamento della simulazione (tra 0 e 1).
       E_c_elettrone (float): energia critica del materiale per gli elettroni.
       E_c_positrone (float): energia critica del materiale per i positroni.
       Perdita_ionizz (float): l'energia persa per ionizzazione in una lunghezza di radiazione.
       num_simulazioni (int): è il numero sciami da simulare per uno stesso valore di energia nella lista E_in_list.
       stampa (bool): se True permette di attivare le stampe intermedie per controllare l'andamento dello sciame.
        
    
    Restituisce
    -----------
      - numero_particelle_energie (lista di liste di liste di int), contiene un numero pari a len(E_in_list) di sotto-liste ciascuna con dimensione num_simulazioni e contenente delle sotto-liste che rappresentano ciascuna l'andamento del numero di particelle di un singolo sciame simulato. 
      - ion_loss_energie (lista di liste di float), contiene un numero pari a len(E_in_list) di sotto-liste ciascuna con dimensione num_simulazioni e contenente i valori di energia persa per ionizzazione in tutti gli sciami simulati.
    """

    #creo liste per i risultati finali
    numero_particelle_energie = []
    ion_loss_energie=[]
    #scorro su tutti i valori di energia iniziale nella lista E_in_list
    for energia_iniziale in E_in_list:
        #creo liste che conterranno i risultati di tutti gli sciami simulati per una data energia iniziale
        particelle_iter = []
        ion_loss_iter=[]


        
        if stampa:
            print( '##########################################################################')
            print(f"        Per un'energia iniziale di {energia_iniziale}MeV      ")
            print( '##########################################################################')

            
        #per ognuno di questi valori di energia simulo num_simulazioni sciami em (per poter studiare le fluttuazioni statistiche)
        for i in range(num_simulazioni):
            #uso la funzione simula_sciame ed ignoro i return di poco interesse, che mi costerebbero RAM ed efficienza per salvarli in delle liste
            ion_loss, _, count_vector, _  = simula_sciame(energia_iniziale, val, E_c_elettrone, E_c_positrone, Perdita_ionizz,stampa=stampa)
            #separo le stampe relative a sciami distinti
            if stampa:
                print("                                                    ")
                print("                                                    ")
                print("                                                    ")
                print("                                                    ")
            #inserisco i risultati del singolo sciame in liste
            particelle_iter.append(count_vector)
            ion_loss_iter.append(ion_loss)


            
        #raccolgo i risultati dei num_simulazioni sciami di uguale energia iniziale
        numero_particelle_energie.append(particelle_iter)
        ion_loss_energie.append(ion_loss_iter)

    return numero_particelle_energie, ion_loss_energie
