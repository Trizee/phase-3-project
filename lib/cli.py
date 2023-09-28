import inquirer
from game import game
from sqlalchemy import (create_engine, desc,
    Index, Column, DateTime, Integer, String, ForeignKey,)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (sessionmaker, relationship, backref)
import time

Base = declarative_base()

class Players(Base):

    __tablename__ = 'players'

    id =Column(Integer(),primary_key=True)
    name = Column('name',String())
    description = Column('description',String())
    scores = relationship('Scores', backref=backref('players'), cascade='all, delete-orphan')

    def __repr__(self):
        return f'Player: {self.name}'
    
class Scores(Base):

    __tablename__ = 'scores'

    id = Column(Integer(),primary_key=True)
    player = Column(Integer(),ForeignKey('players.id'))
    score = Column('score', Integer())

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
        time.sleep(1)
        print(r'''
 _____        _                                
/__   \ _ __ (_)  __ _   __ _  _ __ ___    ___ 
  / /\/| '__|| | / _` | / _` || '_ ` _ \  / _ \
 / /   | |   | || (_| || (_| || | | | | ||  __/
 \/    |_|   |_| \__, | \__,_||_| |_| |_| \___|
                 |___/                         
''')
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
            player1 = session.query(Players).filter_by(name = new_player.name).first()
            final_score = game()
            new_score = Scores(
                player= player1.id,
                score= final_score
            )
            print_game_over()
            session.add(new_score)
            session.commit()
            main_menu()
            
    def highscore():
        players = session.query(Players).all()
        all_scores = session.query(Scores).all()
        all_score_scores = [(score.score,score.players.name) for score in all_scores]
        sortedlist = sorted(all_score_scores, key=lambda k: k[0], reverse=True)
        if not players:
                print('Sorry No Exsisting Users')
        else:
            print(f"""

██   ██ ██  ██████  ██   ██     ███████  ██████  ██████  ██████  ███████ ███████ 
██   ██ ██ ██       ██   ██     ██      ██      ██    ██ ██   ██ ██      ██      
███████ ██ ██   ███ ███████     ███████ ██      ██    ██ ██████  █████   ███████ 
██   ██ ██ ██    ██ ██   ██          ██ ██      ██    ██ ██   ██ ██           ██ 
██   ██ ██  ██████  ██   ██     ███████  ██████  ██████  ██   ██ ███████ ███████ 

1) {sortedlist[0][0]} // Set By: {sortedlist[0][1]}
2) {sortedlist[1][0]} // Set By: {sortedlist[1][1]}                                                                                
3) {sortedlist[2][0]} // Set By: {sortedlist[2][1]}                                                                                

                        """)
        main_menu()

    def view_players():
        players = session.query(Players).all()
        all_scores = session.query(Scores).all()
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
            times_played = [score.score for score in all_scores if answer['update'].id == score.player]
            des = answer['update'].description
            print(f'''{answer['update']}
Player Description: {des}
Times Played: {len(times_played)}
Highest Score: {max(times_played)}
 ''')
            main_menu()
            # add methods to see all of number of of games a player played / highest score

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
        final_score = game()
        new_score = Scores(
            player= answer_key.id,
            score= final_score
        )
        session.add(new_score)
        session.commit()
        print_game_over()
        main_menu()

    def update_players():
        players = session.query(Players).all()
        player_names = session.query(Players.name).all()
        question = [
            inquirer.List('update',
                        message="Select a Player to Update",
                        choices=[player for player in players],
            ),
            inquirer.List('criteria',
                          message='What Do You Want To Update',
                          choices=['Name','Description','Nevermind']
            )
        ]
        answer = inquirer.prompt(question)
        answer_player = answer['update']
        answer_criteria = answer['criteria']
        
        if answer_criteria == 'Name':
            questions = [
                inquirer.Text('name', message=f"Old Name: {answer_player.name} /// New Name"),
                ]
            answers_name = inquirer.prompt(questions)
    
            if answers_name['name'] == answer_player.name:
                print('Name Must Be Different')

            elif answers_name['name'] in [player[0] for player in player_names]:
                print('Sorry This Name Is Already In Use')
            else:
                answer_player.name = answers_name['name']
                session.commit()
       
        elif answer_criteria == 'Description':
            questions = [
                inquirer.Text('des', message=f' Old Description: {answer_player.description} /// New Description'),
                ]
            answers_des = inquirer.prompt(questions)
            if answers_des['des'] == answer_player.description:
                print('Description Must Be New')
            else:
                answer_player.description = answers_des['des']
                session.commit()
        
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
            print('Sorry To See You Go')
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

