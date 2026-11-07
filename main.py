import random 
import datetime

# Functions

# generate two random numbers based on the difficulty level
def generate_numbers(difficulty):
    
    if difficulty == "1":
        num_1 = random.randint(2,9)
        num_2 = random.randint(2,9)
    else:
        num_1 = random.randint(10,20)
        num_2 = random.randint(10,20)
    
    return num_1, num_2


# check if the user answer is correct
def check_answer(user_answer, correct_answer):
    if user_answer == correct_answer:
        return True
    else:
        return False

# calculate the correct answer based on the operation
def calculate_answer(num_1, num_2, operation):
    if operation == "+":
        return num_1 + num_2
    else:
        return num_1 * num_2


# main code

def main():
    results = []

    # variables
    results = []

    print("\nWelcome to the math quiz! made by MiMi\n\n")
    crt_counter = 0


    # ask if the user wants to answer addition or multiplication questions
    operation = input("Do you want to do addition or multiplication questions? \n1: addition; \n2: multiplication\n\n")
    while operation != "1" and operation != "2":
        print("\nInvalid input. Please enter 1 or 2.\n")
        operation = input("Do you want to do addition or multiplication questions? \n1: addition; \n2: multiplication\n\n")
    if operation == "1":
        operation = "+"
    else:
        operation = "x"


    # ask the user how hard the questions will be, 1 for easy, 2 for medium.
    difficulty = input("\nHow hard do you want the questions to be? \n1: easy; \n2: medium\n\n")
    while difficulty != "1" and difficulty != "2":
        print("\nInvalid input. Please enter 1 or 2.\n")
        difficulty = input("\nHow hard do you want the questions to be? \n1: easy; \n2: medium\n\n")
    if difficulty == "1":
        print("\nYou chose easy questions. The numbers will be between 2 and 9.\n")
    else:
        print("\nYou chose medium questions. The numbers will be between 10 and 20.\n")


    # Ask the user how many questions they want to answer
    while True:
        
        try:
            num_questions = int(input("\nHow many questions do you want to answer? \n\n"))
            if num_questions > 0:
                break    
            else:
                print("\nInvalid input. Please enter a positive number.\n")    
        except ValueError:
            print("\nInvalid input. Please enter a integer.\n")


    # timer starts
    start_time = datetime.datetime.now()


    # Loop through the number of questions and ask the user to answer each one
    for _ in range(num_questions):
        # generate numbers based on difficulty
        num_1, num_2 = generate_numbers(difficulty)
        questions = f"{num_1} {operation} {num_2}"

        # user input for what is the answer
        while True:
            
            try:
                user_answer = int(input(f"\nWhat's {num_1} {operation} {num_2}? \n\n"))
                break
            except ValueError:
                print("\nInvalid input. Please enter an integer.\n")
        
        
        # find the correct answer
        correct_answer = calculate_answer(num_1, num_2, operation)
        result = {
        "question": questions,
        "user_answer": user_answer,
        "correct_answer": correct_answer
        }
        results.append(result)

        
        # check if the user answer is correct
        if check_answer(user_answer, correct_answer):
            print("\nCorrect!\n")
            crt_counter += 1
        else:
            print(f"\nIncorrect! The correct answer is {correct_answer}.\n")


    # Print results and round up the percentage of correct answers to the nearest whole number
    end_time = datetime.datetime.now()
    print(f"\nYou got {crt_counter} out of {num_questions} questions correct. Thats {int(crt_counter/num_questions*100 + 0.5)}% correct.")


    # Print the time taken and round up to the nearest centisecond
    print(f"Time taken:{int((end_time - start_time).total_seconds() * 100 + 0.5) / 100} seconds.\n")

    # print the questions and answers 
    print(f"{'No.':^5}{'Question':^10}{'Your answer':^15}{'Correct answer':^15}")

    for i in range(len(results)):
        print(f"{i+1:^5}{results[i]['question']:^10}{results[i]['user_answer']:^15}{results[i]['correct_answer']:^15}")


if __name__ == "__main__":
    main()