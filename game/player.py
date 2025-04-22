from faker import Faker
import uuid

fake = Faker()

class Player:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = fake.first_name()
        self.score = 0

    def increment_score(self):
        self.score += 1

    def __repr(self):
        return f"{self.name} (Score: {self.score})"