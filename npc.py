import random
import ujson


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


class NPC:
    def __init__(self, name):
        self.name = name


class Enemy:
    def __init__(self, name: str, owner_id: int, damage: int, health_points: int, experience: int):
        self.name = name
        self.owner_id = owner_id
        self.damage = damage
        self.health_points = health_points
        self.experience = experience

    def json(self) -> dict:
        return {
            "name": self.name,
            "owner": self.owner_id,
            "damage": self.damage,
            "health_points": self.health_points,
            "experience": self.experience
        }

    def is_enemy_dead(self) -> bool:
        return self.health_points <= 0

    def get_enemy_drop(self) -> dict:
        return get_dict_from_json("items.json")[random.choice(get_dict_from_json("npc_stats.json")[self.name]["drop"])]
