import math

def calculate_answer(num_1, num_2, operation):
    if operation == "+":
        return num_1 + num_2

    elif operation == "-":
        return num_1 - num_2

    elif operation == "x":
        return num_1 * num_2

    elif operation == "/":
        return num_1 / num_2

    else:
        raise ValueError("Unknown operation")

def check_answer(user_answer, correct_answer):
    return math.isclose(
        user_answer,
        correct_answer,
        rel_tol=1e-9,
        abs_tol=1e-9
    )
