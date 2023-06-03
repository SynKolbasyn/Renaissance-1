import ujson
import os

import player


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


def get_account_dict(identification_number: int) -> dict:
    return get_dict_from_json(f"players_data_base/{identification_number}.json")


def is_account_exist(identification_number: int) -> bool:
    return f"{identification_number}.json" in os.listdir("players_data_base/")


def create_new_account(name: str, login: str, identification_number: int):
    player_data_base = player.Player(name, login, identification_number, "Forest", 1, 100, 100, 0, 0, {}).json()
    with open(f"players_data_base/{identification_number}.json", "w") as file:
        file.write(ujson.dumps(player_data_base, indent=2))


def create_exist_player(identification_number: int) -> player.Player:
    account = get_account_dict(identification_number)
    return player.Player(account["name"], account["login"], account["identification_number"], account["location"],
                         account["damage"], account["health_points"], account["mana"], account["money"],
                         account["experience"], account["enemies"])


def except_not_exist_account(identification_number: int, name: str, login: str):
    if not is_account_exist(identification_number):
        create_new_account(name, login, identification_number)


def get_players_events(identification_number: int) -> list:
    return get_dict_from_json("locations.json")[get_account_dict(identification_number)["location"]]["events"]


def get_player_info(identification_number: int) -> str:
    return create_exist_player(identification_number).info()


def check_event(identification_number: int, events: dict, event: str) -> str:
    account = create_exist_player(identification_number)
    if "location" in events[event].keys():
        account.change_location(events[event]["location"])
    answer = ""
    if events[event]["type"] == "battle":
        answer = account.beat_the_enemy(events[event]["enemy"])
    return answer


def do_event(identification_number: int, event: str) -> str:
    events = get_dict_from_json("events.json")
    if not (event in events.keys()):
        return "Unknown action"
    answer = events[event]["description"] + "\n"
    answer += check_event(identification_number, events, event)
    return answer
