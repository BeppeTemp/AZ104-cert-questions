import json
import datetime
import random
from typing import Tuple

from rich import print
from datetime import datetime

from rich.table import Table
from rich.console import Console


class Answer:
    def __init__(self, letter, text):
        self.letter = letter
        self.text = text


class Question:
    def __init__(self):
        #self.topic = None
        self.id = None
        self.text = None
        self.answers = []
        self.correct_answer = None
        self.comment = None
        self.image = None

    def add_answer(self, letter, text):
        self.answers.append(Answer(letter, text))


def print_question(question: Question):
    console = Console()
    
    current_time = datetime.now()
    timestamp = int(current_time.timestamp())
    random.seed(timestamp)

    #table = Table(f'#{str(question.id)} {str(question.topic)}' , question.text)
    table = Table(f'#{str(question.id)}' , question.text)
    random.shuffle(question.answers)
    for answer in question.answers:
        table.add_row(answer.letter, answer.text)

    if (question.image != None):
        table.add_row("Image link", question.image)
        
    console.print(table)


def print_correct_answer(question: Question):
    print(f'Risposta corretta: {question.correct_answer}')
    print(f'Commento: {question.comment}')

def extract_wrong_quests(questions: list[Question]) -> Tuple[list[Question], int]:
    wrong_quests = []
    with open('data/question_to_recheck.txt', 'r') as file:
        for id in [int(line.strip()) for line in file]:
            for quest in questions:
                if quest.id == id:
                    wrong_quests.append(quest)
    
    return wrong_quests, len(wrong_quests)

def clean_wrong_quests():
    with open('data/question_to_recheck.txt', 'w') as file:
        file.write('')

def extract_questions() -> list[Question]:
    with open("data/pca_questions.json", 'r') as json_file:
        questions_data = json.load(json_file)

    questions = []

    for question_data in questions_data:
        question = Question()
        #question.topic = question_data['topic']
        question.id = question_data['id']
        question.text = question_data['text']
        question.correct_answer = question_data['correct_answer']
        question.comment = question_data['comment']
        question.image = question_data['image']

        for answer_data in question_data['answers']:
            question.add_answer(answer_data['letter'], answer_data['text'])

        questions.append(question)

    return questions


def print_result(current_time, quiz_lenght, correct_answer: list[Question], wrong_answer: list[Question]):
    print("---------------------------------------------")
    print(f"Quiz lenght: {quiz_lenght}")
    print(f"Date: {current_time}")
    print(f"Correct answers: {correct_answer}")
    print(f"Wrong answers: {wrong_answer}")
    print()

    percentage = len(correct_answer) / int(quiz_lenght) * 100

    if percentage > 70:
        print(f"[bold green]Test Passed !!![/bold green] ({percentage})")
    else:
        print(f"[bold red]Test Failed !!![/bold red] ({percentage})")

    print("---------------------------------------------")