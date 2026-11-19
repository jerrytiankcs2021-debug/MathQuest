import random

def generate_numbers(difficulty):
    if difficulty == "1":
        num_1 = round(random.uniform(2, 9), 1)
        num_2 = round(random.uniform(2, 9), 1)

    elif difficulty == "2":
        num_1 = round(random.uniform(2, 9), 1)
        num_2 = round(random.uniform(11, 19), 1)

    return num_1, num_2
