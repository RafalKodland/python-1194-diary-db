class Gracz():
    name = "Player 1"
    level = 15
    hp = 100
    is_logged = False

    def attack(self):
        print(f"{self.name} atakuje przeciwnika")
    
    def take_damage(self, amount):
        hp -= amount
        if hp < 0:
            print(f"{self.name} umarł")