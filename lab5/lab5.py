class Fighter:
    def __init__(self, name, health, damage_per_attack):
        self.name = name
        self.health = health
        self.damage_per_attack = damage_per_attack

    def __del__(self):
        print(f"Object {self.name} deleted.")

    def get_name(self):
        return self.name

    def get_health(self):
        return self.health

    def display(self):
        print(f"Name: {self.name}")
        print(f"Health: {self.health}")
        print(f"Damage: {self.damage_per_attack}")


class Fight:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2

    def start_fight(self):
        winner_name = None


        while True:

            self.fighter2.health -= self.fighter1.damage_per_attack
            if self.fighter2.get_health() <= 0:
                print(f"{self.fighter2.get_name()} has been defeated!")
                winner_name = self.fighter1.get_name()
                break

            self.fighter1.health -= self.fighter2.damage_per_attack
            if self.fighter1.get_health() <= 0:
                print(f"{self.fighter1.get_name()} has been defeated!")
                winner_name = self.fighter2.get_name()
                break

        return winner_name


if __name__ == "__main__":
    fighter_one = Fighter("Conor", 100, 15)
    fighter_two = Fighter("Khabib", 110, 10)

    print("--- Fighter 1 ---")
    fighter_one.display()
    print("--- Fighter 2 ---")
    fighter_two.display()
    print("\n--- Fight Starts ---")

    current_fight = Fight(fighter_one, fighter_two)
    winner_name = current_fight.start_fight()

    print(f"\nThe winner is {winner_name}!")
