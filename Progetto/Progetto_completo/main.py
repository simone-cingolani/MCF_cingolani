import numpy as np
import matplotlib.pyplot as plt
import argparse
import funzioni_e_classi as fc
import simulazioni1 as sim
from funzioni_e_classi import materiali
import math





if __name__ == "__main__":
  #Stampo il banner per dare il benvenuto all'utente
  fc.stampa_titolo1()
  #salvo in args le scelte fatte da riga di comando dall'utente 
  args=fc.parse_arguments()
  #chiedo all'utente se è iteressato a simulare uno sciame in un materiale di cui egli conosce i valori caratteristici (prima parte del progetto)
  scelta=fc.scelta_tra_due_possibilità("Vorrebbe simulare un singolo sciame elettromagnetico in un materiale di cui inserirà i dati? (sì(s)/no(n)): ","sì" ,"no" , "s","n", "Cortesemente, rispondere sì(o s) o no(o n).")
  if (scelta=="s") or (scelta=="sì"):             
    
    E_in=fc.richiesta_input_positivo("Inserire il valore dell'energia iniziale della particella (in MeV): ")
    E_c_el=fc.richiesta_input_positivo("Inserire il valore dell'energia critica del materiale (per elettroni)(in MeV): ")
    E_c_pos=fc.richiesta_input_positivo("Inserire il valore dell'energia critica del materiale (per positroni) (in MeV): ")
    Perdita_en=fc.richiesta_input_positivo("Inserire il valore della perdita di energia per ionizzazione in una lunghezza di radiazione del materiale (in MeV): ")
    s=fc.richiesta_input_0_1("Inserire il valore del passo di avanzamento della simulazione, nota bene il passo deve essere compreso tra 0 e 1: ")
    print(f"Eccellente!\nEseguo la simulazione di uno sciame elettromagnetico (con passo di avanzamento pari a {s}) originato da un elettrone con un'energia pari a {E_in}MeV in un materiale caratterizzato da una energia critica per elettroni pari a {E_c_el}MeV e per positroni pari a {E_c_pos}MeV.")

    #simulo lo sciame e salvo i risultati
    risultati=sim.simula_sciame(E_in,s,E_c_el, E_c_pos,Perdita_en, stampa=args.stampa)
    print(f"L'energia totale persa per ionizzazione è pari a: {risultati[0]}MeV")
    print(f"L'energia persa per ionizzazione ad ogni step è: {risultati[1]} MeV")
    print(f"Il numero di particelle ad ogni step è: {risultati[2]}")
    print(f"Il numero di step compiuti è: {len(risultati[3])}")
      

    #se l'utente ne ha interesse può visualizzare un grafico che descrive l'evoluzione dello sciame
    
    if args.grafici0:
      X=fc.richiesta_input_positivo("Inserire il valore della lunghezza di radiazione del materiale (in cm): ")
      print("Eccellente, presento un grafico dell'andamento del numero di particelle in funzione della profondità!")
      conversione=np.array(risultati[3])
      profondità=X*s*conversione
      fig, ax0 = plt.subplots(figsize=(16,8))
      fc.errorbar_funzione(ax0, profondità, risultati[2], None, f"Evoluzione del numero di particelle",f"Profondità (cm)" , f"Numero di particelle")
      plt.show()
  ##############################################################################################################################################################################################################




  #in alternativa, mostro all'utente i risultati per materiali dalle caratteristiche tabulate
  elif (scelta=="n") or (scelta=='no'):
    scelta_materiale=fc.scelta_tra_due_possibilità("Preferisce vedere i risultati relativi alla roccia standard oppure al lutetium silicon oxide? (roccia standard(SR)/lutetium silicon oxide(LSO)): ", "roccia standard", "lutetium silicon oxide","SR","LSO","Purtroppo,ad oggi, abbiamo disponibili solo roccia standard e lutetium silicon oxide.")
    
    if (scelta_materiale=="roccia standard") or (scelta_materiale=="SR"):
      E_c_elettrone=materiali["roccia standard"]["E_c_elettrone"]
      E_c_positrone=materiali["roccia standard"]["E_c_positrone"]
      Perdita_ionizz=materiali["roccia standard"]["Perdita_ionizz"]
      xi=materiali["roccia standard"]["xi"]
    elif (scelta_materiale=="lutetium silicon oxide") or (scelta_materiale=="LSO"):
      E_c_elettrone=materiali["lutetium silicon oxide"]["E_c_elettrone"]
      E_c_positrone=materiali["lutetium silicon oxide"]["E_c_positrone"]
      Perdita_ionizz=materiali["lutetium silicon oxide"]["Perdita_ionizz"]
      xi=materiali["lutetium silicon oxide"]["xi"]


    #l'utente  ha comunque la possibilità di scegliere il passo di avanzamento della simulazione e le energie iniziali dello sciame
      
    val=fc.richiesta_input_0_1("Inserire il valore del passo di avanzamento della simulazione, nota bene il passo deve essere compreso tra 0 e 1: ")
    while True:
      ini=fc.richiesta_input_positivo("Quale intervallo di energie iniziali è interessato a studiare? (numero iniziale) (in MeV): ")
      fin=fc.richiesta_input_positivo("Quale intervallo di energie iniziali è interessato a studiare? (numero finale) (in MeV): ")
      #per poter sondare in maniera uniforme le energie da studiare nell'intervallo di interesse chiedo "gap"
      gap=fc.richiesta_input_positivo("Inserire il valore del passo di avanzamento dell'energia dell'elettrone (in MeV): ")
      #controllo che siano valori opportuni (oltre ad essere positivi)
      if (ini<fin) and gap<(fin-ini):
        break
      else:
        print("Attenzione, gli ultimi 3 input non sono in una relazione sensata tra di loro e/o il passo è nullo")
    E_in = np.arange(ini, fin,gap)  #Energie iniziali



    #in base alle necessità l'utente sceglie quanti sciami simulare
    while True:
      risposta=input(f"Quanti sciami vuole simulare per ogni valore di energia?: ")
      if risposta.isdigit():
        num_simulazioni=int(risposta)
        if num_simulazioni>1:    #0 iterazioni non hanno senso e una sola iterazione si può fare con la prima parte del programma (e qui darebbe problemi nel calcolo della deviazione standard della media)
          break
      else:
        print(f"Attenzione:il valore inserito deve essere intero e maggiore di 1")



    numero_particelle_energie, ion_loss_energie = sim.simulazione_materiali(E_in,val,E_c_elettrone,E_c_positrone,Perdita_ionizz,num_simulazioni,stampa=args.stampa)

    


    ###########################################################################################################################################################################################################


    #INIZIA LO STUDIO GRAFICO DELLO SCIAME

    

    #STUDIO DEL NUMERO DI PARTICELLE IN FUNZIONE DELLA PROFONDITÀ


    
    #se l'utente è interessato allo studio grafico dello sciame può scegliere la prima, seconda, terza... delle energie iniziali da studiare(serve sia per il grafico dell'evoluzione dello sciame che per gli istogrammi relativi ai grafici di studio dello sviluppo longitudinale e di studio dell'energia persa)

    if (args.grafici0==True) or (args.grafici1==True) or (args.grafici2==True):
      while True:
        for indice, i in enumerate(E_in):
          print("Indice ed energia: ",'{:<10} {:02f}'.format(indice,i), "MeV")
        risposta=input(f"Si inserisca l'indice dell'energia iniziale degli sciami da studiare (0 - {len(E_in)-1}): ")
        if risposta.isdigit():
          indice_energia=int(risposta)
          if indice_energia>=0 and indice_energia<=len(E_in)-1:
            break
          else:
            print(f"Attenzione:il valore inserito deve essere compreso tra 0 e {len(E_in)-1}")
        else:
          print(f"Attenzione:il valore inserito deve essere un intero")
    else:
      print("Non avendo selezionato nulla non verrà mostrato alcun grafico")


    if args.grafici0:
    
      #seleziono tutti gli sciami con quell'energia iniziale individuata da indice_energia
      tutti_gli_sciami = numero_particelle_energie[indice_energia]

      #trovo la lunghezza massima tra i num_simulazioni sciami di tutti_gli_sciami (in generale possono avere lunghezza diversa)
      max_len = 0
      for sciame in tutti_gli_sciami:
        lunghezza = len(sciame)
        if lunghezza > max_len:
          max_len = lunghezza


      #ogni sciame di tutti_gli_sciami avrà un certo numero di particelle per ogni step tra 0 e max_len-1
      #mi preparo la lista che conterrà un numero di liste pari a max_len
      #la lista i-esima interna alla lista valori_per_step raccoglierà il numero di particelle dei vari sciami al passo i-esimo
      valori_per_step = []
      for i in range(max_len):
        valori_per_step.append([])  
      #per ogni sciame e per ogni valore i tra 0 e max_len-1 appendo all'i-esima lista di valori_per_step il numero di particelle dello sciame all'i-esimo step
 

      for sciame in tutti_gli_sciami:
        for i in range(max_len):
          if i < len(sciame):
            valore = sciame[i]
          else:
            valore=0                        #il fatto che un certo sciame non arrivi ad una certa profondità è un informazione statisticamente rilevante (allora appendo 0)
          valori_per_step[i].append(valore) #appendo il numero di particelle di quello sciame a quello step 


      #ora ho una lista di dimensioni max_len contenente liste del numero di particelle di tutti gli sciami ad un dato step tra 0 e max_len-1
  
      media_per_step=[]
      std_per_step_media=[]


      for valori in valori_per_step:
        media,_,stdm=fc.calcolo_statistica(valori)
        media_per_step.append(media)
        std_per_step_media.append(stdm)

      #avrei potuto lavorare da subito con array ma l'append su liste è più rapido ed efficiente
      media_per_step=np.array(media_per_step)
      std_per_step_media=np.array(std_per_step_media)
      #considero le profondità da 0cm alla massima raggiunta (alla quale anche lo sciame più lungo ha 0 particelle)
      xdata1 = (np.arange(max_len)) * val * xi
      ydata1 = media_per_step
    
      print("Eccellente, di seguito mostro lo sviluppo dello sciame rispetto alla profondità")
      indice_profondità = math.floor((len(xdata1)-1)/3)      #scelgo di vedere la distribuzione di quello che è un punto spesso vicino al massimo
      dati_istogramma = valori_per_step[indice_profondità]   #studio distribuzione in una lista valori
      minimo=min(dati_istogramma)
      massimo=max(dati_istogramma)
      range_istogramma=(minimo-10,massimo+10)


      fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
      fc.errorbar_funzione(ax1,xdata1, ydata1,std_per_step_media, f'Numero medio di particelle in funzione della profondità \nper un energia iniziale di {E_in[indice_energia]}MeV','Profondità (cm)','Numero di particelle')
      fc.hist_funzione(ax2,dati_istogramma,f'Distribuzione del numero di particelle\n ad una profondità di circa {xdata1[indice_profondità]:.0f}cm', 'Numero di particelle',range_istogramma)
      plt.suptitle("Evoluzione dello sciame", fontsize=20)
      plt.tight_layout()
      plt.show()







    

    
    #STUDIO DELLO SVILUPPO LONGITUDINALE DELLO SCIAME
    
    if args.grafici1:
      print("Eccellente, di seguito mostro i grafici sullo sviluppo longitudinale")
      #creo una lista che dovrà contenere tante sottoliste quanti i valori delle energie iniziali e contenenti le posizioni dei massimi di ogni sciame simulato per un certo valore di energia iniziale
      posizioni_massimi_energie=[]
      for i in numero_particelle_energie: #fissare i significa fissare l'energia_iniziale
        posizioni_massimi_sciami=[]
        for k in i:        #fissare k significa fissare lo sciame di energia i-esima
          mass=-1
          indi=0
          #cerco il massimo ed il rispettivo indice (corrisponde allo step a cui rivelo quel massimo)
          for indice,j in enumerate(k): 
            if j>mass:
              mass = j
              indi=indice
          posizioni_massimi_sciami.append(indi)
        posizioni_massimi_energie.append(posizioni_massimi_sciami)


      #fino a qui sono in unità di lunghezze di radiazione: converto a cm
      posizioni_massimi_energie=np.array(posizioni_massimi_energie)
      posizioni_massimi_energie=posizioni_massimi_energie*val*xi                 #so che tutte le sotto-liste dentro hanno stessa len--->ok!
      

      #faccio media e ds
      posizioni_massimi_energie_media=[]
      posizioni_massimi_energie_std_media=[]


      for i in posizioni_massimi_energie:
        media,_,stdm=fc.calcolo_statistica(i)
        posizioni_massimi_energie_media.append(media)
        posizioni_massimi_energie_std_media.append(stdm)

      
      posizioni_massimi_energie_media=np.array(posizioni_massimi_energie_media)
      posizioni_massimi_energie_std_media=np.array(posizioni_massimi_energie_std_media)
    

      xdata2=E_in
      ydata2=posizioni_massimi_energie_media
      
      
      # GRAFICO ERRORBAR


      # GRAFICO ISTOGRAMMA
      #per l'energia di interesse approfondiamo la distribuzione delle profondità dei massimi
      dati_istogramma = posizioni_massimi_energie[indice_energia]
      minimo=min(dati_istogramma)
      massimo=max(dati_istogramma)
      range_istogramma=(minimo-10,massimo+10)



      fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(16,8))

      fc.errorbar_funzione(ax3,xdata2, ydata2,posizioni_massimi_energie_std_media, "Profondità del massimo dello sciame \n in funzione dell'energia iniziale",'Energia iniziale (MeV)','Profondità (cm)')
      fc.hist_funzione(ax4,dati_istogramma,f'Distribuzione delle profindità a cui si ha il massimo \n per un energia iniziale di {E_in[indice_energia]}MeV', 'Profindità (cm)',range_istogramma)
      plt.suptitle("Sviluppo longitudinale dello sciame", fontsize=20)
      plt.tight_layout()
      plt.show()




      

    #STUDIO DELL'ENERGIA PERSA PER IONIZZAZIONE



    if args.grafici2:
      
      mean_value_energie=[]
      std_value_energie_media=[]

      #for indice, i in enumerate(ion_loss_energie):
      #print(len(ion_loss_energie[indice]))

      
      #qui ho già ion_loss che mi contiene le liste delle energie perse dai vari sciami
      for i in ion_loss_energie:
        media,_,stdm=fc.calcolo_statistica(i)
        mean_value_energie.append(media)
        std_value_energie_media.append(stdm)
      
      mean_value_energie=np.array(mean_value_energie)
      std_value_energie_media=np.array(std_value_energie_media)

      xdata3=E_in
      ydata3=mean_value_energie
      xdata4=E_in
      ydata4=mean_value_energie/E_in  #(anche per questo mi sono assicurato che le energie iniziali non potessero essere 0: rischio NaN)

      #studio dell'energia persa in funzione dell'energia iniziale

      print("Mostro i grafici sulla perdita di energia")
      

      minimo=min(ion_loss_energie[indice_energia])
      massimo=max(ion_loss_energie[indice_energia])
      range_istogramma=(minimo-10,massimo+10)
      
      fig, (ax5, ax6) = plt.subplots(1, 2, figsize=(16, 8))
       
      fc.errorbar_funzione(ax5,xdata3, ydata3,std_value_energie_media, "Energia persa assoluta vs Energia iniziale",'Energia iniziale (MeV)','Energia persa per ionizzazione (MeV)')
      fc.hist_funzione(ax6,ion_loss_energie[indice_energia],f'Distribuzione delle perdite di energia \n per un energia iniziale di {E_in[indice_energia]}MeV', 'Energia persa (MeV)',range_istogramma)
      plt.suptitle("Energia persa per ionizzazione", fontsize=20)
      plt.tight_layout()
      plt.show()
      data_norm = ion_loss_energie[indice_energia] / E_in[indice_energia]
      data_norm=np.array(data_norm)
      minimo=min(data_norm)
      range_istogramma=(minimo-0.01,1)
      fig, (ax7, ax8) = plt.subplots(1, 2, figsize=(16, 8))
       
      fc.errorbar_funzione(ax7,xdata4, ydata4,std_value_energie_media/E_in, "Energia persa normalizzata vs Energia iniziale",'Energia iniziale (MeV)','Energia persa per ionizzazione normalizzata')
      fc.hist_funzione(ax8,data_norm,f'Distribuzione delle perdite di energia \n per un energia iniziale di {E_in[indice_energia]}MeV', 'Energia persa normalizzata',range_istogramma)
      plt.suptitle("Energia persa per ionizzazione", fontsize=20)
      plt.tight_layout()
      plt.show()

       
