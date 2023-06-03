import ujson

import player
import npc


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


def get_account_dict(identification_number: int) -> dict:
    return get_dict_from_json("players_data_base.json")[f"{identification_number}"]


def create_exist_player(identification_number: int) -> player.Player:
    account = get_account_dict(identification_number)
    return player.Player(account["name"], account["login"], account["identification_number"], account["location"],
                         account["damage"], account["health_points"], account["mana"], account["money"],
                         account["experience"], account["enemies"])


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
                                                                 100, 0, 0, {}).json()
    with open("players_data_base.json", "w") as file:
        file.write(ujson.dumps(player_data_base, indent=2))


def get_players_events(identification_number: int) -> list:
    return get_dict_from_json("locations.json")[get_account_dict(identification_number)["location"]]["events"]


def get_player_info(identification_number: int) -> str:
    return create_exist_player(identification_number).info()


def is_enemy_dead(enemy: dict) -> bool:
    return enemy["health_points"] <= 0


def beat_the_enemy(account: player.Player, enemy_name: str) -> player.Player:
    if not (enemy_name in account.enemies.keys()):
        enemy_stats = get_dict_from_json("npc_stats.json")[enemy_name]
        enemy = npc.Enemy(enemy_name, account.identification_number, enemy_stats["damage"],
                          enemy_stats["health_points"], enemy_stats["experience"])
        account.enemies[enemy_name] = enemy.json()
    account.enemies[enemy_name]["health_points"] -= account.damage
    if is_enemy_dead(account.enemies[enemy_name]):
        account.experience += account.enemies[enemy_name]["experience"]
        del account.enemies[enemy_name]
        return account
    account.health_points -= account.enemies[enemy_name]["damage"]
    return account


def check_event(account: player.Player, events: dict, event: str) -> player.Player:
    if "location" in events[event].keys():
        account.location = events[event]["location"]
    if events[event]["type"] == "battle":
        account = beat_the_enemy(account, events[event]["enemy"])
    return account


def do_event(identification_number: int, event: str) -> str:
    events = get_dict_from_json("events.json")
    if not (event in events.keys()):
        return "Unknown action"
    account = create_exist_player(identification_number)
    update_player_data_base(check_event(account, events, event))
    return events[event]["description"]
