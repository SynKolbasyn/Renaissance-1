class Player:
    def __init__(self, name: str, login: str, identification_number: int):
        self.name = name
        self.login = login
        self.identification_number = identification_number
        self.location = "Forest"
        self.damage = 1
        self.health_points = 100
        self.mana = 100
        self.money = 0

    def info(self) -> str:
        return f"Name: {self.name}\n" \
               f"ID: {self.identification_number}\n" \
               f"Damage: {self.damage}\n" \
               f"Health points: {self.health_points}\n" \
               f"Mana: {self.mana}\n" \
               f"Money: {self.money}"

    def json(self) -> dict:
        return {"name": self.name,
                "login": self.login,
                "identification_number": self.identification_number,
                "location": self.location,
                "damage": self.damage,
                "health_points": self.health_points,
                "mana": self.mana,
                "money": self.money}
