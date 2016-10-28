"""
Main client class.

Sends requests to server and handles move making.
"""

from urllib2 import Request, urlopen  # TODO: students actually use python3 lmao rip
import json
import time
from movegen import *


BASEURL = "http://memetrash.co.uk/codeyork/"
GET, POST = 0, 1


def make_request(url, method, body={}):
    """
    Make a request to a URL, of either GET or POST nature.

    Args:
        url (str): URL to request.
        method (int): GET or POST.
        body (dict): Body of POST request.

    Request:
        tuple(int, dict): Response code and JSON dictionary returned.
            If an error, JSON dictionary is empty.
    """
    if req not in [GET, POST]:
        raise ValueError("Must have get or post request")
    body_data = json.dumps(body)
    req = Request(url) if method==GET else Request(url, body_data)
    req.add_header('Content-Type', 'application/json')
    try:
        respose = urlopen(req)
        return (200, json.loads(response.read()))
    except urllib2.HTTPError as e:
        if e.code == 404:
            raise e     # don't catch these
        return (e.code, {})


class Client(object):

    def __init__(self, move_gen):
        self.game_id = 0
        self.player_id = 0
        self.movegen = move_gen

    def req_newgame(self):
        return make_request(BASEURL + "game", POST)

    def req_join(self):
        return make_request(BASEURL + str(self.game_id) + "/join", POST)

    def req_start(self):
        return make_request(BASEURL + str(self.game_id) + "/start", POST)

    def req_gamestate(self):
        return make_request(BASEURL + str(self.game_id) + "/state", GET)

    def req_move(self, move):
        move['player'] = str(self.player_id)
        return make_request(BASEURL + str(self.game_id) + "/move", POST, move)

    def run(self):
        """
        Run a single game session on the client.
        """
        if self.enter_game():
            self.play_game()

    def enter_game(self):
        """
        Take the player's decision to create / join a game, and initiate the game.
        """
        if raw_input("Start a new game? (y/n) ") == 'y':
            code, response = self.req_newgame()
            self.game_id, self.player_id = response['data']['game'], response['data']['player']
            print("A game has been created with ID = " + str(self.game_id))
            return True
        else:
            self.game_id = int(raw_input("Give a game id (from whoever started the game): "))
            code, response = self.req_join()
            if code == 403:
                print("No game with ID " + str(self.game_id) + " exists.")
                return False
            self.player_id = response['data']['player']
            start_code, start_resp = self.req_startgame()  # player joining starts game
            return True

    def play_game(self):
        """
        Once a game has been started, poll the game for state and send moves if required.
        """
        game_finished = False
        while not game_finished:
            time.sleep(3)
            code, resp = self.req_gamestate()
            if code == 200:
                if resp['data']['finished']:
                    game_finished = True
                    if resp['data']['winner'] == self.player_id:
                        print("You won!")
                    else:
                        print("You lost. Oh well.")
                elif resp['data']['player'] == self.player_id:
                    move = self.movegen.make_move(resp)
                    move_code, move_resp = self.req_move(move)

