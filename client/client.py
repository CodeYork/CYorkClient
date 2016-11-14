"""
Main client class.

Sends requests to server and handles move making.
"""

import sys

if sys.version_info[0] == 2:
    from urllib2 import Request, urlopen, HTTPError
else:
    from urllib.request import Request, urlopen, HTTPError

import json
import time
from client.movegen import *


BASEURL = "https://four.gjcampbell.co.uk/"
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
    if method not in [GET, POST]:
        raise ValueError("Must have get or post request")
    body_data = json.dumps(body).encode('utf-8', 'replace')
    req = Request(url) if method==GET else Request(url, body_data)
    req.add_header('Content-Type', 'application/json')
    try:
        response = urlopen(req)
        data = response.read()
        return (200, json.loads(data.decode('utf-8'), strict=False))
    except HTTPError as e:
        if e.code not in [400, 401, 403]:
            raise e     # don't catch these
        return (e.code, {})


class Client(object):

    def __init__(self, move_gen):
        self.game_id = None
        self.player_id = None
        self.movegen = move_gen

    def req_newgame(self):
        return make_request(BASEURL + "game", POST)

    def req_join(self):
        return make_request(BASEURL + "game/" + str(self.game_id) + "/join", POST)

    def req_start(self):
        return make_request(BASEURL + "game/" + str(self.game_id) + "/start", POST)

    def req_gamestate(self):
        return make_request(BASEURL + "game/" + str(self.game_id), GET)

    def req_move(self, move_col):
        query = "?player=" + str(self.player_id) + "&col=" + str(move_col)
        return make_request(BASEURL + "game/" + str(self.game_id) + "/move" + query, POST)

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
        if input("Start a new game? (y/n) ") == 'y':
            code, response = self.req_newgame()
            self.game_id, self.player_id = response['data']['game'], response['data']['player']
            print("A game has been created with ID = " + str(self.game_id))
            return True
        else:
            self.game_id = input("Give a game id (from whoever started the game): ")
            code, response = self.req_join()
            if code == 403:
                print("The game with ID " + str(self.game_id) + " is already full.")
                return False
            self.player_id = response['data']['player']
            return True

    def transform_gamestate(self, resp):
        """
        Convert game state into 2d array of True's if own pawn, False's otherwise.
        """
        game_state = resp['data']['board']
        for r, row in enumerate(game_state):
            for c, col in enumerate(row):
                if game_state[r][c] is None: continue
                game_state[r][c] = (game_state[r][c] == self.player_id)
        return game_state

    def print_gamestate(self, state):
        print("Current game state (X = you, O = opponent, _ = no token):")
        printable_rows = [" ".join({True: "X", False: "O", None: "_"}[x] for x in row) for row in state]
        print("\n".join(printable_rows))

    def play_game(self):
        """
        Once a game has been started, poll the game for state and send moves if required.
        """
        game_finished = False
        while not game_finished:
            time.sleep(1)
            code, resp = self.req_gamestate()
            if code == 200 and resp['data']['started']:
                if resp['data']['winner'] is not None:
                    game_finished = True
                    board = self.transform_gamestate(resp)
                    self.print_gamestate(board)
                    if resp['data']['winner'] == self.player_id:
                        print("You won!")
                    else:
                        print("You lost. Oh well.")
                elif resp['data']['current'] == self.player_id:
                    try:
                        board = self.transform_gamestate(resp)
                        self.print_gamestate(board)
                        move_col = self.movegen.make_move(board)
                        assert(isinstance(move_col, int))
                        assert(0 <= move_col < len(board[0]))
                        move_code, move_resp = self.req_move(move_col)
                    except BaseException as e:
                        if isinstance(e, KeyboardInterrupt):
                            raise e
                        print(e)

