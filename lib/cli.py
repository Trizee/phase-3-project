import re 
import inquirer

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
        main_menu()
