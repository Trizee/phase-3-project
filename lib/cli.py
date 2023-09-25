import re 
import inquirer
from game import game
from sqlalchemy import (create_engine, desc,
    Index, Column, DateTime, Integer, String, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()

class Players(Base):

    __tablename__ = 'players'

    id =Column(Integer(),primary_key=True)
    name = Column('name',String())
    description = Column('description',String())
    scores = relationship('Scores', backref='players')

    def __init__(self,name,description):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'Player: {self.name}'
    
class Scores(Base):

    __tablename__ = 'scores'

    id = Column(Integer(),primary_key=True)
    player = Column(Integer(),ForeignKey('players.id'))
    score = Column('score', Integer())

    def __init__(self,player,score):
        self.player = player
        self.score = score

    def __repr__(self):
        return f'{self.score}'
    
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
        elif main_menu_answers_key == 'View High Scores':
            highscore()
        
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
            inquirer.Text('des', message='Give a Description'),
        ]
        answers = inquirer.prompt(question)
        new_player = Players(
            name = answers['name'],
            description = answers['des'],
        )
        if new_player.name in [player[0] for player in player_names]:
            print('Sorry Username is Already in Use')
            create_new_player()
        else:
            session.add(new_player)
            session.commit()
            game()
            main_menu()
            
    def highscore():
        print(r"""

                                       ._ o o
                                       \_`-)|_
                                    ,""       \ 
                                  ,"  ## |   ಠ ಠ. 
                                ," ##   ,-\__    `.
                              ,"       /     `--._;)
                            ,"     ## /
                          ,"   ##    /


                    """)
        main_menu()

    def view_players():
        question = [
            inquirer.List('update',
                        message="Select Player to View",
                        choices=[player for player in players],
            ),
        ]
        answer = inquirer.prompt(question)
        print(answer['update'].id)

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
        main_menu()

    main_menu()

