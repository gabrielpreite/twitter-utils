import json
import numpy as np
from twitterAPI import TwitterAPI
import datetime


global TAPI
TAPI = TwitterAPI()


punteggi_file = "PunteggiFantacitorio.json"
politici_file = "politici.json"
help_file = "help_fantacitorio.json"
punteggi_list = {}
politici_list = {}
help_list = {}


def get_nome(politico):
    return politico.get("nome")
def get_cognome(politico):
    return politico.get("cognome")
def get_punti(politico):
    return politico.get("punteggio")
def get_incremento(politico):
    return politico.get("incremento_settimana")
def get_inc_medio(politico):
    return politico.get("incremento_medio")
def get_inc_max(politico):
    return politico.get("incremento_max")
def get_inc_min(politico):
    return politico.get("incremento_min")
def get_pos_media(politico):
    return politico.get("posizione_classifica_media")
def get_pos_old(politico):
    return politico.get("posizione_classifica_old")
def get_pos_now(politico):
    return politico.get("posizione_classifica_new")


#Aggiunge nuovo politico in punteggi_list
def nuovo_politico(nome, cognome, punti):
    with open(punteggi_file, 'r+') as file:
        punteggi_list = json.load(file)
    punti = int(punti)
    politico = {
        "nome" : nome,
        "cognome" : cognome,
        "punteggio" : punti,
        "incremento_settimana" : punti,
        "incremento_medio" : [punti],
        "incremento_max" : punti,
        "incremento_min" : punti,
        "posizione_classifica_media" : [],
        "posizione_classifica_old" : 10000,
        "posizione_classifica_new" : 10000,
        "best": []
    }

    punteggi_list["politico"].append(politico)

    #Save JSON file
    with open(punteggi_file, 'w') as file:
        json.dump(punteggi_list, file, indent = 4)



#Modifica il punteggio relativo al politico
def aggiungi_punteggio(cognome, punti, tweet, data_tweet):
    #Read JSON file
    with open(punteggi_file, 'r+') as file:
        punteggi_list = json.load(file)
    with open(politici_file, 'r+') as file:
        politici_list = json.load(file) 
    with open(help_file, 'r+') as file:
        help_list = json.load(file) 

    #cerca politico in punteggi_list
    found = 0
    for politico in punteggi_list["politico"]:
        if politico["cognome"].lower().find(cognome.lower()) != -1:
            week_ago = datetime.date.today() - datetime.timedelta(days=7)
            if data_tweet>week_ago.strftime("%s"):
                politico["incremento_settimana"] = int(politico["incremento_settimana"]) + int(punti)
            politico["punteggio"] = int(politico["punteggio"]) + int(punti)
            politico["incremento_medio"].append(int(punti))
            if int(punti) < int(politico["incremento_min"]):
                politico["incremento_min"] = int(punti)
            if int(punti) > int(politico["incremento_max"]):
                politico["incremento_max"] = int(punti)
            found += 1

    #cerca politico in politici_list
    if found == 0:
        politico_nome = ""
        politico_cognome = ""
        for politico in politici_list["politico"]:
            if politico["cognome"].lower().find(cognome.lower()) != -1:
                politico_nome = politico["nome"]
                politico_cognome = politico["cognome"]
                found -= 1
        if found == -1:
            nuovo_politico(politico_nome, politico_cognome, punti)
        elif found < -1:
            #ERRORE: EDITA A MANO I PUNTEGGI (POLITICO INESISTENTE IN PUNTEGGI_LIST)
            errore_politici_list = {
                "tweet" : tweet,
                "cognome" : cognome,
            }
            help_list["errore_politici_list"].append(errore_politici_list)
            with open(help_file, 'w') as file:
                json.dump(help_list, file, indent = 4)
            
    
    #Save JSON file
    if found == 1:
        with open(punteggi_file, 'w') as file:
            json.dump(punteggi_list, file, indent = 4)
    elif found > 1:
        #ERRORE: EDITA A MANO I PUNTEGGI (POLITICO ESISTENTE IN PUNTEGGI_LIST)
        errore_punteggi_list = {
                "tweet" : tweet,
                "cognome" : cognome,
            }
        help_list["errore_punteggi_list"].append(errore_punteggi_list)
        with open(help_file, 'w') as file:
            json.dump(help_list, file, indent = 4)


#Unica funzione da chiamare per recuperare o aggiornare i punteggi
def recupera_punteggi():
    with open(help_file) as file:
        help_list = json.load(file)

    anno = datetime.date.today().year
    mese = datetime.date.today().month
    giorno = datetime.date.today().day
    if ((datetime.date.today() - (datetime.date(help_list["last_reset"][0]["year"], help_list["last_reset"][0]["month"], help_list["last_reset"][0]["day"]))).days > 7):
        reset_statistiche()
        help_list["last_reset"][0]["day"] = giorno
        help_list["last_reset"][0]["month"] = mese
        help_list["last_reset"][0]["year"] = anno
    if (not (help_list["data"][0]["day"] == giorno and help_list["data"][0]["month"] == mese and help_list["data"][0]["year"] == anno)):
        with open(politici_file) as file:
            politici_list = json.load(file)
        
        #ricerca tweet per username Fanta_citorio
        filtri = {}
        filtri["username"] = "Fanta_citorio"
        opzioni = {}
        opzioni["max_tweets"] = 10
        opzioni["data_inizio"] = datetime.datetime(help_list["data"][0]["year"], help_list["data"][0]["month"], help_list["data"][0]["day"]).strftime("%Y-%m-%dT%H:%M:%S")+"+01:00"
        help_list["data"][0]["day"] = giorno
        help_list["data"][0]["month"] = mese
        help_list["data"][0]["year"] = anno
        
        with open(help_file, 'w') as file:
            json.dump(help_list, file, indent = 4)
        
        tweet_list, _ = TAPI.get_tweets(filtri, opzioni)
        tweet_list = json.loads(tweet_list)
        #scorro e analizzo punteggi tweets
        if(tweet_list.get("data", None) != None):
            for tweet in tweet_list["data"]:
                tweet_words = tweet["text"].split()
                punteggio = 0
                data_tweet = tweet["created_at"]
                for word in tweet_words:
                    if(word.isnumeric()):
                        punteggio = word
                    if(word.isalpha() and int(punteggio)!=0):
                        for politico in politici_list["politico"]:
                            if(politico["cognome"].lower().find(word.lower()) != -1 and len(word)>2):
                                aggiungi_punteggio(politico["cognome"].lower(), punteggio, tweet_words, data_tweet)
    
    return mostra_classifica()


#Restituisce la classifica dei politici in ordine di punteggio
def mostra_classifica():
    #Read JSON file
    with open(punteggi_file, 'r+') as file:
        punteggi_list = json.load(file)


    #ordina in base al punteggio
    punteggi_list["politico"].sort(key=get_punti, reverse=True)
    i = 1
    best_singlescore = 0
    worst_singlescore = 10000
    best_climber = 0
    best_average = 0
    best_average_classifica = 0
    best_weekly = 0
    for politico in punteggi_list["politico"]:
        politico["best"] = []
        politico["posizione_classifica_new"] = i
        if (politico["incremento_max"] > best_singlescore):
            best_singlescore = politico["incremento_max"]
        if (politico["incremento_min"] < worst_singlescore):
            worst_singlescore = politico["incremento_min"]
        if ((politico["posizione_classifica_old"] - politico["posizione_classifica_new"]) > best_climber):
            best_climber = politico["posizione_classifica_old"] - politico["posizione_classifica_new"]
        if (np.mean(politico["incremento_medio"]) > best_average):
            best_average = np.mean(politico["incremento_medio"])
        if (np.mean(politico["posizione_classifica_media"]) > best_average_classifica):
            best_average_classifica = np.mean(politico["posizione_classifica_media"])
        if (politico["incremento_settimana"] > best_weekly):
            best_weekly = politico["incremento_settimana"]
        i += 1

    for politico in punteggi_list["politico"]:
        if (politico["incremento_max"] == best_singlescore):
            politico["best"].append("best singlescore")
        if (politico["incremento_min"] == worst_singlescore):
            politico["best"].append("worst singlescore")
        if ((politico["posizione_classifica_old"] - politico["posizione_classifica_new"]) == best_climber):
            politico["best"].append("best climber")
        if (np.mean(politico["incremento_medio"]) == best_average):
            politico["best"].append("best average")
        if (np.mean(politico["posizione_classifica_media"]) == best_average_classifica):
            politico["best"].append("best average classifica")
        if (politico["incremento_settimana"] == best_weekly):
            politico["best"].append("best weekly")

    with open(punteggi_file, 'w') as file:
        json.dump(punteggi_list, file, indent = 4)

    return punteggi_list


#Raccoglie i tweet contenenti team registrati al gioco
def recupera_team(user = ""):
    filtri = {}
    filtri["hashtag"] = "fantacitorio"

    if user != "":
        filtri["username"] = user

    opzioni = {}
    opzioni["image"] = True
    opzioni["max_tweets"] = 50

    lista_tweet_team, _ = TAPI.get_tweets(filtri, opzioni)
    lista_tweet_team = json.loads(lista_tweet_team)

    return lista_tweet_team


#Restituisce il tweet dell'utente con il team registrato per il gioco
def recupera_team_utente(user):
    tweet_team_utente = recupera_team(user)

    return tweet_team_utente[0]


#resetta i punteggi settimanali dei punteggi
def reset_statistiche():
    with open(punteggi_file, 'r+') as file:
        punteggi_list = json.load(file)


    punteggi_list["politico"].sort(key=get_punti, reverse=True)
    i = 1
    for politico in punteggi_list["politico"]:
        politico["incremento_settimana"] = 0
        politico["posizione_classifica_old"] = politico["posizione_classifica_new"]
        politico["posizione_classifica_media"].append(i)
        politico["best"] = []
        i += 1


    with open(punteggi_file, 'w') as file:
        json.dump(punteggi_list, file, indent = 4)