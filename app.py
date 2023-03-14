from flask import Flask, request, render_template, redirect, send_file
from flask_apscheduler import APScheduler
from apscheduler.triggers.interval import IntervalTrigger
from twitterAPI import TwitterAPI
from datetime import date, datetime, timedelta
import TweetChess
import Fantacitorio
import json
import soccerAPI

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

#costanti
INDEX = "index.html"
ERRORE = "errore.html"
RISULTATI = "risultati.html"
CHESS = "chess.html"
FANTACITORIO = "fantacitorio.html"
EREDITA = "eredita.html"
PLAY = "play.html"
SOCCER = "soccer.html"
MATCH = "match.html"
USERTEAM = "userteam.html"

@app.route("/", methods=["GET", "POST"])

#chiamo il file html con l'interfaccia
def homepage():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   if(request.method == "GET"):
      #sto chiamando per la prima volta l'app, carico solo la homepage
      return render_template(INDEX)
   if(request.method == "POST"):
      #sto facendo una ricerca
      #filtri
      filtro = request.form["filtro"]
      query = request.form["query"]
      if filtro == "location":
         lat = request.form["latitudine"]
         lon = request.form["longitudine"]
         rad = request.form["area"]
         filtri = {filtro: [lon, lat, rad]}
      else:
         filtri = {filtro: query}

      #opzioni
      opzioni = {}
      opzioni["lingua"] = request.form["lang"]
      opzioni["max_tweets"] = request.form["max_tweets"]

      #opzioni-data (aggiungo l'ora)
      opzioni["data_inizio"] = request.form["data_inizio"]+"T00:00:00+01:00"
      data_oggi = str(date.today())
      
      if(request.form["data_fine"] == data_oggi):
         now = datetime.now()
         now = now - timedelta(seconds=15)
         query_time = now.strftime("%H:%M:%S")
         opzioni["data_fine"] = request.form["data_fine"]+"T"+query_time+"+01:00"
      else:
         opzioni["data_fine"] = request.form["data_fine"]+"T23:59:59+01:00"

      try:
         result, freq = TAPI.get_tweets(filtri, opzioni)
      except Exception as e:
         return render_template(ERRORE, errore=str(e))
      
      #frequency list

      #ottenuto il json carichiamo la pagina dove mostriamo i risultati
      return render_template(INDEX, query=query, filtro=filtro, results=result, frequency_list=freq,
                             b_risultati=True, b_nuvola=True, b_statistiche=True, b_timeline=True)

   #se e' stata usata una funzione http non gestita dall'app
   return render_template(ERRORE, errore="funzione http non supportata")

@app.route("/chess", methods=["GET", "POST"])

def chess():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   if(request.method == "GET"):
      #sto chiamando per la prima volta l'app, carico solo la homepage di chess
      return render_template(CHESS)
   if(request.method == "POST"):
      #opzioni
      opzioni = {}
      opzioni["username"] = request.form["username"]
      opzioni["move_time"] = request.form["move_time"]
      
      tweetstartgame, game = TweetChess.update_games_list(opzioni, progress=False)
      if(tweetstartgame == False):
         return render_template(ERRORE, errore="username non valido/l'utente non ha twittato")

      if(scheduler.get_job(opzioni["username"]) == None):
         scheduler.add_job(
            func=timer_func,
            args=[opzioni],
            trigger=IntervalTrigger(hours=game["move_time"]),
            id=opzioni["username"],
            name="timer per mosse scacchi",
            replace_existing=False
         )
         
      return render_template(PLAY, game=game)

   return render_template(ERRORE)

@app.route("/fantacitorio", methods=["GET", "POST"])

def fantacitorio():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()

   #classifica
   classifica = Fantacitorio.recupera_punteggi()

   # carosello
   filtri = {}
   filtri["hashtag"] = "fantacitorio"
   opzioni = {}
   opzioni["image"] = True
   opzioni["max_tweets"] = 50
   lista_tweet_team, _ = TAPI.get_tweets(filtri, opzioni)
   lista_tweet_team = json.loads(lista_tweet_team)

   if(request.method == "POST"):
      # cerca squadra utente
      filtri = {}
      filtri["hashtag"] = "fantacitorio"
      filtri["username"] = request.form["query"]
      opzioni = {}
      opzioni["image"] = True
      lista_tweet, _ = TAPI.get_tweets(filtri, opzioni)
      lista_tweet = json.loads(lista_tweet)
      if(lista_tweet.get("data", None) != None):
         user_team = lista_tweet["data"][0]
      else:
         user_team = {
               "username": "",
               "attachments": {"media": {"url": "https://pbs.twimg.com/media/FmnKqgJXEAYnAFo.png"}}
               }
      return render_template(FANTACITORIO, results=lista_tweet_team, classifica=classifica, user_team = user_team, nome = user_team["username"], b_userteam=True)
   return render_template(FANTACITORIO, results=lista_tweet_team, classifica=classifica)

@app.route("/eredita", methods=["GET", "POST"])
def eredita():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   opzioni = {}
   if(request.method == "GET"):
      inizio = date.today()
      inizio = inizio - timedelta(days=inizio.weekday())
      fine = inizio + timedelta(days=6)
      opzioni["data_inizio"] = inizio.strftime("%Y-%m-%d")+"T00:00:00+01:00"
      opzioni["data_fine"] = fine.strftime("%Y-%m-%d")+"T00:00:00+01:00"
   if(request.method == "POST"):
      opzioni["data_inizio"] = request.form["data_inizio"]+"T00:00:00+01:00"
      opzioni["data_fine"] = request.form["data_fine"]+"T00:00:00+01:00"
   res = TAPI.eredita(opzioni)
   return render_template(EREDITA, response=res)

@app.route("/soccer", methods=["GET", "POST"])

def soccer():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   if(request.method == "GET"):
      #sto chiamando per la prima volta l'app, carico solo la lista di partite
      response = soccerAPI.soccer(test=False)
      response = json.loads(response)
      response["response"].reverse()
      return render_template(SOCCER, partite=json.dumps(response))
   if(request.method == "POST"):
      id_ = {"id": request.form["id"]}
      response = json.loads(soccerAPI.match(id_, test=False))
      filtri = {}
      opzioni = {}
      home_team = response["response"][0]["teams"]["home"]["name"]
      away_team = response["response"][0]["teams"]["away"]["name"]
      if(home_team == "AS Roma"): home_team = "Roma"
      if(home_team == "AC Milan"): home_team = "Milan"
      if(away_team == "AS Roma"): away_team = "Roma"
      if(away_team == "AC Milan"): away_team = "Milan"
      filtri["hashtag"] = home_team+away_team
      opzioni["max_tweets"] = 500
      opzioni["primo_tempo_inizio"] = response["response"][0]["fixture"]["periods"]["first"]
      #opzion["primo_tempo_fine"] = 
      opzioni["secondo_tempo_inizio"] = response["response"][0]["fixture"]["periods"]["second"]
      opzioni["secondo_tempo_fine"] = opzioni["secondo_tempo_inizio"]+(50*60)#45+5 per ora, dopo sistemo
      response2 = TAPI.get_match_tweets(filtri, opzioni)
      return render_template(MATCH, dettagli=json.dumps(response), twitter=response2)
      
   return render_template(ERRORE)

@app.route("/robots.txt", methods=["GET", "POST"])
def robots():
   return send_file("./robots.txt")

#general functions
def timer_func(opzioni):
   valid_board , game = TweetChess.update_games_list(opzioni, progress=True)
   if (not game["playing"]) or (not valid_board):
      scheduler.remove_job(opzioni["username"])
     
def run_app():
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   app.run(host="0.0.0.0")

if __name__ == '__main__':
   #inizializzo globale l'istanza della classe che si occupa delle chiamate alle api per poterla usare in tutto il codice
   if "TAPI" not in globals():
      global TAPI
      TAPI = TwitterAPI()
   #TweetChess.init()
   app.run(host="0.0.0.0")