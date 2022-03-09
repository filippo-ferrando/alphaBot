# alphaBot :rocket:

### Progetto scolastico sugli alphabot di [Alladio Michele](https://github.com/MicheleAlladioAKAMich) e [Ferrando Filippo](https://github.com/filippo-ferrando)
Il robot funziona tramite un webserver flask e un database (lato server) contenente le istruzioni per fare determinati movimenti, gli utenti presentie i log di tutti i login e le operazioni eseguite

![](https://github.com/filippo-ferrando/alphaBot/blob/main/foto.jpg)

## Client-Server

<img src="https://github.com/filippo-ferrando/alphaBot/blob/main/schema.png" height="350">

#### Utilizzando le librerie base dell'alphabot siamo in primo luogo riusciti a farlo muovere mandando tramite il client istruzioni come avanti, indietro, ecc. e il tempo per il quale questo doveva muoversi.
#### Nella seconda versione di questo programma utilizziamo un databse con sia i movimenti base che movenze più complesse e invece di mandare tutta l'istruzione tramite il client, mandiamo solamente l'id dell'istruzione nel DB.
#### Nella terza versione, il controllo avviene tramite una webapp con una semplice pagina di login

## Database
Il Database comprende 4 tabelle
 - HISTORY --> contiene i log delle operazioni eseguite
 - LOG_UTENTI --> contiene i log degli utenti che si loggano sulla webapp
 - Movimenti --> contiene i movimenti semplici e complessi del robot
 - USERS --> contiene gli utenti registrati
