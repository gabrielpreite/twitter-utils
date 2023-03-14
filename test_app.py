import pytest
import time
import json
import chess
from app import app
from TweetChess import update_games_list, end_game
from twitterAPI import TwitterAPI
from soccerAPI import soccer, match

def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200 

def test_chess_route():
    response = app.test_client().get('/chess')
    assert response.status_code == 200 

def test_fantacitorio_route():
    response = app.test_client().get('/fantacitorio')
    assert response.status_code == 200 

def test_eredita_route():
    response = app.test_client().get('/eredita')
    assert response.status_code == 200 

def test_soccer_route():
    response = app.test_client().get('/soccer')
    assert response.status_code == 200 

def test_ricerca():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    data = "query=ciao&filtro=keyword&lang=all&max_tweets=10&data_inizio=2023-01-07&data_fine=2023-01-14&area="
    url = "/"

    response = app.test_client().post(url, data=data, headers=headers)

    assert response.status_code == 200

def test_ricerca_location():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    data = "query=&filtro=location&lang=it&max_tweets=10&data_inizio=2023-01-08&data_fine=2023-01-15&latitudine=44.49381148123335&longitudine=11.340465545654297&area=30"
    url = "/"

    response = app.test_client().post(url, data=data, headers=headers)

    assert response.status_code == 200

def test_soccer_match():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    data = "id=881930"
    url = "/soccer"

    response = app.test_client().post(url, data=data, headers=headers)
    assert response.status_code == 200

def test_chess_player():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    data = "username=gabrielpreite96&move_time=1"
    url = "/chess"

    response = app.test_client().post(url, data=data, headers=headers)
    assert response.status_code == 200

def test_chess_updategamelist():
    opzioni = {"username": "gabrielpreite96", "move_time": 1}
    _, game = update_games_list(opzioni)
    time.sleep(2)
    _, gameupdated = update_games_list(opzioni, True)
    assert game != gameupdated
    time.sleep(2)
    _, game = update_games_list(opzioni, True)
    assert game != gameupdated
    time.sleep(2)

def test_chess_endgame():
    with open("ChessGames.json", "r") as f:
        data = json.load(f)
        for d in data["games"]:
            if d["tweetaccount"] == "gabrielpreite96":
                game = d
    assert end_game(game, chess.Board("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"))["board"] == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_eredita_full():
    TAPI = TwitterAPI()
    opzioni = {"data_inizio" : "2023-01-09T00:00:00+01:00", "data_fine": "2023-01-15T22:59:59+01:00"}
    assert json.loads(TAPI.eredita(opzioni, cache=False))["data_inizio"] == "2023-01-09"

def test_soccer_live():
    assert json.loads(soccer(test=False))["errors"] == []

def test_match_live():
    assert json.loads(match({"id": "881930"},test=False))["errors"] == []

if __name__ == '__main__':
    #GET
    test_index_route()
    time.sleep(1)
    test_chess_route()
    time.sleep(1)
    test_fantacitorio_route()
    time.sleep(1)
    test_eredita_route()
    time.sleep(1)
    test_soccer_route()
    time.sleep(1)

    #POST
    test_ricerca()
    time.sleep(1)
    test_ricerca_location()
    time.sleep(1)
    test_soccer_match()
    time.sleep(1)
    test_chess_player()
    time.sleep(1)

    #FUNCTIONS
    #chess
    test_chess_updategamelist()
    time.sleep(1)
    test_chess_endgame()
    time.sleep(1)
    #cleanup
    with open("reset_chess.json", "r") as f2:
        with open("ChessGames.json", "w") as f:
            json.dump(f2, f)

    #eredita
    test_eredita_full()
    time.sleep(1)

    #soccer
    test_soccer_live()
    test_match_live()