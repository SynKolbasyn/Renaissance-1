import ujson

import player


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


def get_account_dict(identification_number: int) -> dict:
    return get_dict_from_json("players_data_base.json")[f"{identification_number}"]


def create_exist_player(identification_number: int) -> player.Player:
    account = get_account_dict(identification_number)
    return player.Player(account["name"], account["login"], account["identification_number"], account["location"],
                         account["damage"], account["health_points"], account["mana"], account["money"])


def update_player_data_base(account: player.Player):
    player_data_base = get_dict_from_json("players_data_base.json")
    player_data_base[f"{account.identification_number}"] = account.json()
    with open("players_data_base.json", "w") as file:
        file.write(ujson.dumps(player_data_base, indent=2))


def is_account_exist(identification_number: int) -> bool:
    return f"{identification_number}" in get_dict_from_json("players_data_base.json").keys()


def create_new_account(name: str, login: str, identification_number: int):
    player_data_base = get_dict_from_json("players_data_base.json")
    player_data_base[f"{identification_number}"] = player.Player(name, login, identification_number, "Forest", 1, 100,
                                                                 100, 0).json()
    with open("players_data_base.json", "w") as file:
        file.write(ujson.dumps(player_data_base, indent=2))


def get_players_events(identification_number: int) -> list:
    return get_dict_from_json("locations.json")[get_account_dict(identification_number)["location"]]["events"]


def get_player_info(identification_number: int) -> str:
    return create_exist_player(identification_number).info()


def check_event_type(account: player.Player, events: dict, event: str) -> player.Player:
    if events[event]["type"] == "movement":
        account.location = events[event]["location"]
    return account


def do_event(identification_number: int, event: str) -> str:
    events = get_dict_from_json("events.json")
    if not (event in events.keys()):
        return "Unknown action"
    account = create_exist_player(identification_number)
    update_player_data_base(check_event_type(account, events, event))
    return events[event]["description"]
