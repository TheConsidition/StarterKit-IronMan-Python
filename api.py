import requests
import time


class API:
    _base_api_path = "http://theconsidition.se/considition/ironman/"
    _api_key = ""
    _max_players = 1
    _map = "standardmap"
    _number_of_elevations = 10
    _number_of_waterstreams = 10
    _number_of_powerups = 10

    def __init__(self, apiKey, maxPlayers, map, numberOfElevations, numberOfWaterstreams, numberOfPowerups):
        self._api_key = apiKey
        self._max_players = maxPlayers
        self._map = map
        self._number_of_elevations = numberOfElevations
        self._number_of_waterstreams = numberOfWaterstreams
        self._number_of_powerups = numberOfPowerups

    # Gets the gamestate for a given game_id.
    # Returns: The gamestate as JSON
    def get_game(self, game_id):
        print("Getting game: " + game_id)
        r = requests.get(self._base_api_path + "games/" + game_id + '/' + self._api_key)
        response = r.json()
        if not response["success"]:
            print(response["message"])
        else:
            return response

    # Creates a new game, with a specified number of max players,
    # waterstreams, elevations, and powerups.
    # Returns: The game_id of the new game
    def init_game(self):
        r = requests.post(self._base_api_path + "games",
                          json={"ApiKey": self._api_key, "MaxPlayers": self._max_players, "Map": self._map,
                                "NumberOfStreams": self._number_of_waterstreams,
                                "NumberOfElevations": self._number_of_elevations,
                                "NumberOfPowerups": self._number_of_powerups})
        response = r.json()
        if not response["success"]:
            print(response["message"])
        else:
            game_id = response["gameId"]
            print("Created new game: " + game_id)
            return game_id

    # Joins a game
    # Returns: The gamestate after the new player has been inserted
    def join_game(self, game_id):
        r = requests.post(self._base_api_path + "games/" + game_id + "/join", json={"ApiKey": self._api_key})
        response = r.json()
        if not response["success"]:
            print(response["message"])
        else:
            print("Joined game: " + response["gameState"]["gameId"])
            return response

    # Readies up for a game
    # Returns: The gamestate after the player has readied up
    def ready_up(self, game_id):
        print("Readying up!")
        r = requests.post(self._base_api_path + "games/" + game_id + "/ready", json={"ApiKey": self._api_key})
        response = r.json()
        if not response["success"]:
            print(response["message"])
        else:
            return response

    # Creates, joins, and readies up for a game
    # Returns: The ID of the started game
    def initiate_one_player_game(self):
        game_id = self.init_game()
        joined_response = self.join_game(game_id)
        readied_response = self.ready_up(game_id)
        return readied_response["gameState"]["gameId"]

    # Continously try to ready up for a game
    # To be used when joining games with more than one player
    # Returns: The gamestate after all of the players have successfully readied up
    def try_ready_for_game(self, game_id):
        print('Readying up!');
        readied_response = self.ready_up(game_id)
        while readied_response is None:
            print("Trying to ready up")
            time.sleep(2)
            readied_response = self.ready_up(game_id)
        return readied_response

    # Makes a move in a given direction with a given speed
    # Returns: The updated gamestate
    def make_move(self, game_id, direction, speed):
        print("Attempting to makeMove with speed: " + speed + " and direction: " + direction)
        r = requests.post(self._base_api_path + "games/" + game_id + "/action/move",
                          json={"ApiKey": self._api_key, "Type": "move", "Speed": speed, "Direction": direction})
        response = r.json()
        if not response["success"]:
            print(response["message"])
            while not response["success"]:
                response = self.get_game(game_id)
            return response
        else:
            return response

    # Takes a step in a given direction
    # Returns: The updated gamestate
    def step(self, game_id, direction):
        print("Attempting to step in direction: " + direction)
        r = requests.post(self._base_api_path + "games/" + game_id + "/action/step",
                          json={"ApiKey": self._api_key, "Direction": direction})
        if r is not None:
            response = r.json()
            if not response["success"]:
                print(response["message"])
                while not response["success"]:
                    response = self.get_game(game_id)
                return response
            else:
                return response

    # Rests for 1 turn
    # Returns: The updated gamestate
    def rest(self, game_id):
        print("Attempting to rest!")
        r = requests.post(self._base_api_path + "games/" + game_id + "/action/rest", json={"ApiKey": self._api_key})
        response = r.json()
        if not response["success"]:
            print(response["message"])
            while not response["success"]:
                response = self.get_game(game_id)
            return response
        else:
            return response

    # Uses a chosen powerup
    def use_powerup(self, game_id, powerup_name):
        print("Attempting to use powerup: " + powerup_name)
        r = requests.post(self._base_api_path + "games/" + game_id + "/action/usepowerup",
                          json={"ApiKey": self._api_key, "Name": powerup_name})
        response = r.json()
        if not response["success"]:
            print(response["message"])
            while not response["success"]:
                response = self.get_game(game_id)
            return response
        else:
            return response

    # Drops a chosen powerup
    def drop_powerup(self, game_id, powerup_name):
        print("Attempting to drop powerup: " + powerup_name)
        r = requests.post(self._base_api_path + "games/" + game_id + "/action/droppowerup",
                          json={"ApiKey": self._api_key, "Name": powerup_name})
        response = r.json()
        if not response["success"]:
            print(response["message"])
            while not response["success"]:
                response = self.get_game(game_id)
            return response
        else:
            return response

    # Ends previous active games
    def end_previous_games_if_any(self):
        print("Attempting to end previous games if any.")
        r = requests.delete(self._base_api_path + "games", json={"ApiKey": self._api_key})
        response = r.json()
        if not response["success"]:
            print(response["message"])