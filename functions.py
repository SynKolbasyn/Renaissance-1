import ujson

import player


def get_account_dict(identification_number: int) -> dict:
    with open("players_data_base.json", "r") as file:
        player_data_base = ujson.load(file)
    return player_data_base[f"{identification_number}"]


def create_player(identification_number: int) -> player.Player:
    account = get_account_dict(identification_number)
    return player.Player(account["name"], account["login"], account["identification_number"], account["location"],
                         account["damage"], account["health_points"], account["mana"], account["money"])


def is_account_exist(identification_number: int) -> bool:
    with open("players_data_base.json", "r") as file:
        player_data_base = ujson.load(file)
    return f"{identification_number}" in player_data_base.keys()


def create_new_account(name: str, login: str, identification_number: int):
    with open("players_data_base.json", "r") as file:
        player_data_base = ujson.load(file)
    player_data_base[f"{identification_number}"] = player.Player(name, login, identification_number).json()
    with open("players_data_base.json", "w") as file:
        file.write(ujson.dumps(player_data_base, indent=2))


def get_players_events(identification_number: int) -> list:
    with open("locations.json", "r") as file:
        locations = ujson.load(file)
    return locations[get_account_dict(identification_number)["location"]]["events"]


def get_player_info(identification_number: int) -> str:
    return create_player(identification_number).info()
