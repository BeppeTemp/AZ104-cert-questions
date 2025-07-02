import random
import typer

from rich import print
from datetime import datetime

from utils import *

def main():
    current_time = datetime.now()
    timestamp = int(current_time.timestamp())
    random.seed(timestamp)
    
    questions = extract_questions()
    
    for x in range(1, random.randint(2,10)):
        random.shuffle(questions)
    
    wrong_quests, wrong_quests_number = extract_wrong_quests(questions)
    random.shuffle(wrong_quests)
    
    quiz_len = int(input("Lunghezza del quiz: ") or 57)
    if wrong_quests_number > 0: 
        print("N.B. " + str(wrong_quests_number) + " domande verranno risottoposte 😉.\n")
    
    if (quiz_len - wrong_quests_number) < 0:
        quiz_len = wrong_quests_number
    else:
        quiz_len = quiz_len
        
    extracted_quests = questions[slice(quiz_len - wrong_quests_number)] + wrong_quests
    for x in range(1, random.randint(2,10)):
        random.shuffle(extracted_quests)
    quiz_len = len(extracted_quests)
    
    clean_wrong_quests()
    correct_answers = []
    wrong_answers = []

    with open("data/question_to_recheck.txt", "a") as quest_to_recheck:
        with open("question_to_review.txt", "a") as quest_to_review:
            quest_to_review.write("Quiz date: " + str(current_time) + "\n")

            for i in range(0, int(quiz_len)):
                print("Domanda: " + str(i + 1)+"/"+str(quiz_len))

                print_question(extracted_quests[i])
                answer = input("Risposta: ")

                if (answer.upper() == extracted_quests[i].correct_answer.upper()):
                    print("[bold green]Corretto !!![/bold green]")
                    correct_answers.append(extracted_quests[i].id)
                else:
                    print("[bold red]Errato !!![/bold red]")
                    wrong_answers.append(extracted_quests[i].id)
                    print()
                    print_correct_answer(extracted_quests[i])
                    print()
                    comments = input("Commento: ")
                    quest_to_review.write("Topic " + str(extracted_quests[i].topic) + " - Id " + str(extracted_quests[i].id) + ": " + comments + "\n")
                    quest_to_recheck.write("Topic " + str(extracted_quests[i].topic) + " - Id " + str(extracted_quests[i].id) + "\n")

                print()
                input("Premi invio per continuare...")
                print()

            quest_to_review.write("\n")

    print_result(current_time, quiz_len, correct_answers, wrong_answers)

if __name__ == "__main__":
    typer.run(main)