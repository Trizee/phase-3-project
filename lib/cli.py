import re 
import inquirer
from game import game

all_players = []

def main_menu():
    main_menu = [
    inquirer.List('option',
                    message="Options",
                    choices=['Play','View High Scores','View Players','Update Players','Exit'],
                ),
    ]
    main_menu_answers = inquirer.prompt(main_menu)
    main_menu_answers_key = main_menu_answers['option']
    if main_menu_answers_key == 'Play':
        play_menu()
    elif main_menu_answers_key == 'View Players':
        view_players()
    elif main_menu_answers_key == 'Update Players':
        update_players()
    
def play_menu():
    play_menu = [
        inquirer.List('new',
            message="Are you a new or returning player?",
            choices=['New','Exisiting'],
        ),
    ]
    play_menu_answer = inquirer.prompt(play_menu)
    play_menu_answer_key = play_menu_answer['new']
    if play_menu_answer_key == 'New':
        create_new_player()
    if play_menu_answer_key == 'Exisiting':
        returning_player()

# Children for the play menu
def create_new_player():
    question = [
        inquirer.Text('name', message='Enter Your Name'),
    ]
    answers = inquirer.prompt(question)
    print(answers['name'])
    all_players.append(answers['name'])
    game()
    main_menu()

def view_players():
    print(all_players)

def returning_player():
    question = [
        inquirer.List('update',
                    message="Select an Exsisting Player",
                    choices=[player for player in all_players],
        ),
    ]
    answer = inquirer.prompt(question)
    answer_key = answer['update']
    print(answer_key)
    game()
    main_menu()

def update_players():
    question = [
        inquirer.List('update',
                    message="Select a Player to Update",
                    choices=[player for player in all_players],
        ),
    ]
    answer = inquirer.prompt(question)
    answer_key = answer['update']
    print(answer_key)
    main_menu()

main_menu()