import npc
import ujson


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


class Player:
    def __init__(self, name: str, login: str, identification_number: int, location: str, damage: int,
                 health_points: int, mana: int, money: int, experience: int, enemies: dict):
        self.name = name
        self.login = login
        self.identification_number = identification_number
        self.location = location
        self.damage = damage
        self.health_points = health_points
        self.mana = mana
        self.money = money
        self.experience = experience
        self.enemies = enemies

    def info(self) -> str:
        return f"Name: {self.name}\n" \
               f"ID: {self.identification_number}\n" \
               f"Location: {self.location}\n" \
               f"Damage: {self.damage}\n" \
               f"Health points: {self.health_points}\n" \
               f"Mana: {self.mana}\n" \
               f"Money: {self.money}\n" \
               f"Experience: {self.experience}"

    def json(self) -> dict:
        return {
            "name": self.name,
            "login": self.login,
            "identification_number": self.identification_number,
            "location": self.location,
            "damage": self.damage,
            "health_points": self.health_points,
            "mana": self.mana,
            "money": self.money,
            "experience": self.experience,
            "enemies": self.enemies
        }

    def update_player_data_base(self):
        player_data_base = get_dict_from_json("players_data_base.json")
        player_data_base[f"{self.identification_number}"] = self.json()
        with open("players_data_base.json", "w") as file:
            file.write(ujson.dumps(player_data_base, indent=2))

    def change_location(self, location: str):
        self.location = location

    def beat_the_enemy(self, enemy_name: str) -> str:
        if not (enemy_name in self.enemies.keys()):
            enemy_stats = get_dict_from_json("npc_stats.json")[enemy_name]
            enemy = npc.Enemy(enemy_name, self.identification_number, enemy_stats["damage"],
                              enemy_stats["health_points"], enemy_stats["experience"])
            self.enemies[enemy_name] = enemy.json()
        enemy = npc.Enemy(enemy_name, self.identification_number, self.enemies[enemy_name]["damage"],
                          self.enemies[enemy_name]["health_points"], self.enemies[enemy_name]["experience"])
        enemy.health_points -= self.damage
        if enemy.is_enemy_dead():
            self.experience += enemy.experience
            del self.enemies[enemy_name]
            return f"You kill {enemy_name}"
        self.health_points -= enemy.damage
        self.enemies[enemy_name] = enemy.json()
        return f"{enemy_name} got {self.damage} damage from you. " \
               f"{enemy_name} has {enemy.health_points} health points.\n" \
               f"You got {enemy.damage} damage from {enemy_name}. " \
               f"You have {self.health_points} health points"
