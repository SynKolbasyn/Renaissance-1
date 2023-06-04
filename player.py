import npc
import ujson


def get_dict_from_json(file_name: str) -> dict:
    with open(file_name, "r") as file:
        return ujson.load(file)


class Player:
    def __init__(self, name: str, login: str, identification_number: int, location: str, damage: int,
                 health_points: int, mana: int, money: int, experience: int, enemies: dict, inventory: list):
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
        self.inventory = inventory

    def info(self) -> str:
        return f"Name: {self.name}\n" \
               f"ID: {self.identification_number}\n" \
               f"Location: {self.location}\n" \
               f"Damage: {self.damage}\n" \
               f"Health points: {self.health_points}\n" \
               f"Mana: {self.mana}\n" \
               f"Money: {self.money}\n" \
               f"Experience: {self.experience}"

    def inventory_info(self) -> str:
        if not self.inventory:
            return "You haven't got anything"
        info = ""
        for i, e in enumerate(self.inventory):
            info += f"{i + 1}. Name: {e['name']}; Price: {e['price']}; " \
                    f"HP regeneration: {e['hp_regeneration']}\n"
        return info[:-1]

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
            "enemies": self.enemies,
            "inventory": self.inventory
        }

    def is_dead(self) -> bool:
        return self.health_points <= 0

    def update_player_data_base(self):
        player_data_base = self.json()
        with open(f"players_data_base/{self.identification_number}.json", "w") as file:
            file.write(ujson.dumps(player_data_base, indent=2))

    def change_location(self, location: str):
        self.location = location
        self.update_player_data_base()

    def beat_the_enemy(self, enemy_name: str) -> str:
        if not (enemy_name in self.enemies.keys()):
            enemy_stats = get_dict_from_json("npc_stats.json")[enemy_name]
            tmp_enemy = npc.Enemy(enemy_name, self.identification_number, enemy_stats["damage"],
                                  enemy_stats["health_points"], enemy_stats["experience"])
            self.enemies[enemy_name] = tmp_enemy.json()
        enemies = {}
        for i in self.enemies:
            enemies[i] = npc.Enemy(i, self.identification_number, self.enemies[i]["damage"],
                                   self.enemies[i]["health_points"], self.enemies[i]["experience"])
        enemies[enemy_name].health_points -= self.damage
        if enemies[enemy_name].is_enemy_dead():
            self.experience += enemies[enemy_name].experience
            del self.enemies[enemy_name]
            self.inventory.append(enemies[enemy_name].get_enemy_drop())
            self.update_player_data_base()
            return f"You kill {enemy_name}"
        answer = f"{enemy_name} got {self.damage} damage from you. " \
                 f"{enemy_name} has {enemies[enemy_name].health_points} health points.\n"
        for i in enemies:
            self.health_points -= enemies[i].damage
            answer += f"You got {enemies[i].damage} damage from {i}. " \
                      f"You have {self.health_points} health points\n"
        if self.is_dead():
            with open(f"players_data_base/{self.identification_number}.json", "w") as file:
                file.write(ujson.dumps({"name": self.name, "login": self.login,
                                        "identification_number": self.identification_number,
                                        "location": "Forest", "damage": 1, "health_points": 100, "mana": 100,
                                        "money": 0, "experience": 0, "enemies": {}, "inventory": []
                                        }, indent=2))
            return "You dead"
        for i in enemies:
            self.enemies[i] = enemies[i].json()
        self.update_player_data_base()
        return answer
