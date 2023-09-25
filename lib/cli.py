import re 
import inquirer
from game import game
from sqlalchemy import (create_engine, desc,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class Players(Base):

    __tablename__ = 'players'

    id =Column(Integer(),primary_key=True)
    _name = Column('name',String())

    def __init__(self,name):
        self.name = name

    @hybrid_property
    def name(self):
        return self._name 
    
    @name.setter
    def name(self,name):
        if isinstance(name,str) and 0 < len(name):
            self._name = name
        else:
            raise ValueError('Not a valid Input')

    def __repr__(self):
        return f'Player: {self.name}'
    
if __name__ == '__main__':
    engine = create_engine('sqlite:///players.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # defining table varibles
    players = session.query(Players).all()
    player_names = session.query(Players.name).all()

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
        new_player = Players(
            name = answers['name']
        )
        if new_player.name in [player[0] for player in player_names]:
            print('Sorry Username is Already in Use')
            create_new_player()
        else:
            session.add(new_player)
            session.commit()
            game()
            main_menu()
        
        

    def view_players():
        print(player for player in players)

    def returning_player():
        question = [
            inquirer.List('update',
                        message="Select an Exsisting Player",
                        choices=[player for player in players],
            ),
        ]
        answer = inquirer.prompt(question)
        answer_key = answer['update']
        game()
        main_menu()

    def update_players():
        question = [
            inquirer.List('update',
                        message="Select a Player to Update",
                        choices=[player for player in players],
            ),
        ]
        answer = inquirer.prompt(question)
        answer_key = answer['update']
        # print(answer_key)
        main_menu()

    main_menu()