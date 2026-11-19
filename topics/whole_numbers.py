import random

def generate_numbers(difficulty):
    if difficulty == "1":
        num_1 = random.randint(2, 9)
        num_2 = random.randint(2, 9)

    elif difficulty == "2":
        num_1 = random.randint(1, 9)
        num_2 = random.randint(10, 20)

    return num_1, num_2
