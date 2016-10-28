"""
Main client class.

Sends requests to server and handles move making.
"""

import urllib2


BASEURL = "http://memetrash.co.uk/codeyork/"
GET, POST = 0, 1


def make_request(url, method=GET):
    if req not in [GET, POST]:
        raise ValueError("Must have get or post request")
    stub_data = urllib2.urlencode({})
    req = Request(url) if method==GET else Request(url, stub_data)
    return urllib2.urlopen(req)


class Client(object):

    def __init__(self):
        self.game_id = 0

    @staticmethod
    def req_newgame():
        return make_request(BASEURL + "game", POST)

    @staticmethod
    def req_join(game_id):
        return make_request(BASEURL + str(game_id) + "/join", POST)

    @staticmethod
    def req_start(game_id):
        return make_request(BASEURL + str(game_id) + "/start", POST)

    @staticmethod
    def req_gamestate(game_id):
        return make_request(BASEURL + str(game_id) + "/state", GET)

    @staticmethod
    def req_move(game_id, player_id):
        return make_request(BASEURL + str(game_id) + "/move/" + str(player_id), POST)

    def run(self):
        """
        Run a single game session on the client.
        """
        if self.start_game():
            self.play_game()

    def start_game(self):
        """
        Take the player's decision to start / join a game, and initiate the game.
        """
        pass

    def play_game(self):
        """
        Once a game has been started, poll the game for state and send moves if required.
        """
        pass

