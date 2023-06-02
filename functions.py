import ujson

import player


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
