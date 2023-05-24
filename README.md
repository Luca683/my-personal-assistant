# My Personal Assistant

Tale progetto consiste nella realizzazione di un assistente vocale in grado di eseguire i seguendi comandi:

- Restituire data di oggi, ora attuale e giorno della settimana.
- Modificare il volume del proprio computer (Funzionante solo su Linux).
- Raccontare una barzelletta.
- Mostrare le prestazioni del sistema (Percentuale batteria, utilizzo CPU e RAM).
- Gioco testa o croce.
# Installazione
Assicuriamoci di avere installato la versione di Python 3.10.9.

Per utilizzare My Personal Assistant, è importante prima di tutto installare le dipendenze necessarie, utilizzando il seguente comando sul terminale:

```shell
pip install -r requirements_dev.txt
```

Se esegui il programma da **Linux**, sarà necessario aggiungere le seguenti dipendenze da terminale:

```shell
sudo apt install portaudio19-dev pulseaudio espeak
```

Se esegui il programma da **MacOS**, sarà necessario aggiungere le seguenti dipendenze da terminale:
```shell
brew install pulseaudio espeak
```
Note: con Mac OS 

Esegui poi il programma utilizzando il seguente comando (all'interno della cartella src):
```shell
python my_assistant.py
```

# Guida all'uso
Una volta avviato il programma, il nostro assistente ascolterà le nostre richieste, possiamo dunque cominciare a chiedere qualcosa (a voce), alcuni esempi:

- Che ore sono?
- Testa o croce?
- Dammi le prestazioni della batteria.
- Metti il volume a 50.
- Abbassa il volume di 10.
- Dimmi una barzelletta

Per interrompere l'assistente basterà dire "Stop", così il programma terminerà la sua esecuzione.
# Partecipanti al progetto
- [Luca683](https://github.com/Luca683)
- [oromis34](https://github.com/oromis34)
- [Spongix12](https://github.com/Spongix12)

