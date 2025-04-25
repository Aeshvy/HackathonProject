from faker import Faker
import uuid

fake = Faker()

class Player:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = f"The {fake.color_name()} {fake.word().capitalize()}"
        self.score = 0

    def increment_score(self):
        self.score += 1

    def __repr__(self):
        return f"{self.name} (Score: {self.score})"