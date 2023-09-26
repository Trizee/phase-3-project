import os
import inquirer
from game import game
from sqlalchemy import (create_engine, desc,
    Index, Column, DateTime, Integer, String, ForeignKey,)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (sessionmaker, relationship, )

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
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # # defining table varibles
    # players = session.query(Players).all()
    # player_names = session.query(Players.name).all()

    def main_menu():
        main_menu = [
        inquirer.List('option',
                        message="Options",
                        choices=['Play','View High Scores','View Players','Update Players','Delete a Player','Exit'],
                    ),
        ]
        main_menu_answers = inquirer.prompt(main_menu)
        main_menu_answers_key = main_menu_answers['option']
        if main_menu_answers_key == 'Play':
            player_menu()
        elif main_menu_answers_key == 'View Players':
            view_players()
        elif main_menu_answers_key == 'Update Players':
            update_players()
        elif main_menu_answers_key == 'View High Scores':
            highscore()
        elif main_menu_answers_key == 'Delete a Player':
            delete_player()

    def player_menu():
        players = session.query(Players).all()
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
            if not players:
                print('Sorry No Exsisting Users')
                player_menu()
            else:    
                returning_player()

    # Children for the play menu
    def create_new_player():
        player_names = session.query(Players.name).all()
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
            print_game_over()
            main_menu()
            
    def highscore():
        players = session.query(Players).all()
        if not players:
                print('Sorry No Exsisting Users')
        else:
            print(r"""

██   ██ ██  ██████  ██   ██     ███████  ██████  ██████  ██████  ███████ ███████ 
██   ██ ██ ██       ██   ██     ██      ██      ██    ██ ██   ██ ██      ██      
███████ ██ ██   ███ ███████     ███████ ██      ██    ██ ██████  █████   ███████ 
██   ██ ██ ██    ██ ██   ██          ██ ██      ██    ██ ██   ██ ██           ██ 
██   ██ ██  ██████  ██   ██     ███████  ██████  ██████  ██   ██ ███████ ███████ 
                                                                                 
                                                                                 

                        """)
        main_menu()

    def view_players():
        players = session.query(Players).all()
        if not players:
                print('Sorry No Exsisting Users')
                main_menu()
        else:
            question = [
                inquirer.List('update',
                            message="Select Player to View",
                            choices=[player for player in players],
                ),
            ]
            answer = inquirer.prompt(question)
            print(answer['update'].id)

    def returning_player():
        players = session.query(Players).all()
        question = [
            inquirer.List('update',
                        message="Select an Exsisting Player",
                        choices=[player for player in players],
            ),
        ]
        answer = inquirer.prompt(question)
        answer_key = answer['update']
        game()
        new_score = Scores(
            player= answer_key.id,
            score= 10
        )
        session.add(new_score)
        session.commit()
        print_game_over()
        main_menu()

    def update_players():
        players = session.query(Players).all()
        question = [
            inquirer.List('update',
                        message="Select a Player to Update",
                        choices=[player for player in players],
            ),
        ]
        answer = inquirer.prompt(question)
        answer_key = answer['update']
        main_menu()

    def delete_player():
        players = session.query(Players).all()
        question = [
            inquirer.List('delete',
                        message="Select a Player to Delete",
                        choices=[player for player in players],
            ),
            inquirer.List('confirm',
                          message='Are You Sure Changes Will be Permanent',
                          choices= ['Yes', 'No']
                          )
        ]
        answer = inquirer.prompt(question)
        if answer['confirm'] == 'No':
            print('Phew, Please Play Again!')
        if answer['confirm'] == 'Yes':
            session.delete(answer['delete'])
            session.commit()        
        print(answer)
        main_menu()

    def print_game_over():
        print(f'''
           
  ▄▀  ██   █▀▄▀█ ▄███▄       ████▄     ▄   ▄███▄   █▄▄▄▄ 
▄▀    █ █  █ █ █ █▀   ▀      █   █      █  █▀   ▀  █  ▄▀ 
█ ▀▄  █▄▄█ █ ▄ █ ██▄▄        █   █ █     █ ██▄▄    █▀▀▌  
█   █ █  █ █   █ █▄   ▄▀     ▀████  █    █ █▄   ▄▀ █  █  
 ███     █    █  ▀███▀               █  █  ▀███▀     █   
        █    ▀                        █▐            ▀    
       ▀                              ▐                  
              ''')

    main_menu()

