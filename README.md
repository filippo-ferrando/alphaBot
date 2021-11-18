# alphaBot :rocket:

### Progetto scolastico sugli alphabot di [Alladio Michele](https://github.com/MicheleAlladioAKAMich) e [Ferrando Filippo](https://github.com/filippo-ferrando)
Il robot funziona tramite un sistema client-server TCP e un database (lato server) contenente le istruzioni per fare determinati movimenti.

![](https://github.com/filippo-ferrando/alphaBot/blob/main/foto.jpg)

## Client-Server

<img src="https://github.com/filippo-ferrando/alphaBot/blob/main/schema.png" height="400">

Utilizzando le librerie base dell'alphabot siamo in primo luogo riusciti a farlo muovere mandando tramite il client istruzioni come avanti, indietro, ecc. e il tempo per il quale questo doveva muoversi.
Nella seconda versione di questo programma utilizziamo un databse con sia i movimenti base che movenze più complesse e invece di mandare tutta l'istruzione tramite il client, mandiamo solamente l'id dell'istruzione nel DB.

## Database
Il database da noi utilizzato presenta una struttura mono-tabella molto semplice, le voci presenti sono solo 3:
 - ID --> che ci permette di identificare l'istruzione
 - NOME --> che rende più facile a noi capire su che istruzione stiamo lavorando
 - ISTRUZIONE --> che contiene l'istruzione singola o la serie di istruzioni che il robot dovrà eseguire
