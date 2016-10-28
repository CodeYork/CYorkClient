"""
Main client class.

Sends requests to server and handles move making.
"""

import urllib2  # TODO: students actually use python3 lmao rip
import json


BASEURL = "http://memetrash.co.uk/codeyork/"
GET, POST = 0, 1


def make_request(url, method):
    """
    Make a request to a URL, of either GET or POST nature.

    Args:
        url (str): URL to request.
        method (int): GET or POST.

    Request:
        tuple(int, dict): Response code and JSON dictionary returned.
            If an error, JSON dictionary is empty.
    """
    if req not in [GET, POST]:
        raise ValueError("Must have get or post request")
    stub_data = urllib2.urlencode({})
    req = Request(url) if method==GET else Request(url, stub_data)
    try:
        respose = urllib2.urlopen(req)
        return (200, json.loads(response.read()))
    except urllib2.HTTPError as e:
        if e.code == 404:
            raise e     # don't catch these
        return (e.code, {})


class Client(object):

    def __init__(self):
        self.game_id = 0
        self.player_id = 0

    def req_newgame():
        return make_request(BASEURL + "game", POST)

    def req_join():
        return make_request(BASEURL + str(self.game_id) + "/join", POST)

    def req_start(game_id):
        return make_request(BASEURL + str(self.game_id) + "/start", POST)

    def req_gamestate(game_id):
        return make_request(BASEURL + str(self.game_id) + "/state", GET)

    def req_move(game_id, player_id):
        return make_request(BASEURL + str(self.game_id) + "/move/" + str(self.player_id), POST)

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
            code, response = req_newgame()
            self.game_id, self.player_id = response['data']['game'], response['data']['player']
            print("A game has been created with ID = " + str(self.game_id))
            return True
        else:
            self.game_id = int(raw_input("Give a game id (from whoever started the game): "))
            code, response = req_join()
            if code == 403:
                print("No game with ID " + str(self.game_id) + " exists.")
                return False
            self.player_id = response['data']['player']
            return True

    def play_game(self):
        """
        Once a game has been started, poll the game for state and send moves if required.
        """
        pass

