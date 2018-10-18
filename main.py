from api import API
import random
import sys

# TODO : Insert your API-key here
_api_key = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
# Specify your API-key number of players per game),
# mapname, and number of waterstreams/elevations/powerups here
_api = API(_api_key, 1, "standardmap", 10, 10, 10)


# A "solution" that takes a step in a random direction every turn
def solution(game_id):
    initial_state = _api.get_game(game_id)
    if initial_state["success"]:
        state = initial_state["gameState"]
        tiles = state["tileInfo"]
        current_player = state["yourPlayer"]
        current_y_pos = current_player["yPos"]
        current_x_pos = current_player["xPos"]
        while not state["gameStatus"] == "done":
            print("Starting turn: " + str(state["turn"]))
            tiles = state["tileInfo"]
            print(str(state["yourPlayer"]))
            current_player = state["yourPlayer"]
            current_y_pos = current_player["yPos"]
            current_x_pos = current_player["xPos"]
            # Take a step in a random direction
            step_direction_array = ["w", "e", "n", "s"]
            random_step = random.randint(0, 3)
            print("Stepped: " + str(step_direction_array[random_step]))
            response = _api.step(game_id, step_direction_array[random_step])
            state = response["gameState"]
        print("Finished!")
    else:
        print(initial_state["message"])


def main():
    game_id = ""
    # If no gameID is specified as parameter to the script,
    # Initiate a game with 1 player on the standard map
    if len(sys.argv) == 1:
        _api.end_previous_games_if_any()  # Can only have 2 active games at once. This will end any previous ones.
        game_id = _api.init_game()
        joined_game = _api.join_game(game_id)
        readied_game = _api.try_ready_for_game(game_id)
        if readied_game is not None:
            print("Joined and readied! Solving...")
            solution(game_id)
    else:
        game_id = sys.argv[1]


main()
