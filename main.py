from core.calculations import calculate_answer, check_answer
from topics import decimals, whole_numbers


def generate_numbers(difficulty, number_type):
    if number_type == "Whole Numbers":
        return whole_numbers.generate_numbers(difficulty)
    if number_type == "Decimals":
        return decimals.generate_numbers(difficulty)
    raise ValueError("Unknown number type")
