import os
import sqlite3
from time import time
from kink import inject, di

# from SpaceInvader.dto import GameOverDTO, GamePlayDTO, HighScoreDTO, LastGameIdDTO, ScoreBoardDTO, UserProfileDataDTO, UsernameCheckerDTO
from SpaceInvader.dto import GameOverDTO, GamePlayDTO, HighScoreDTO, LastGameIdDTO, PlayerEmailDTO, ScoreBoardDTO, UserProfileDataDTO, UsernameCheckerDTO

@inject
class GameRepository:
    def __init__(self,db_name,dbinit):
        self.db_name = "SpaceInvader\\resource\\"+db_name
        # self.db_name = r"https://github.com/noelmandak/Tugas-Kampus/blob/0c783afe451c886e31b141f1ea022d49bd387ecf/gamerepository.db"
        self.conn = None
        self.c = None
        self.setup_database(dbinit)

    def setup_database(self,dbinit):
        print(dbinit)
        if dbinit == "True":
            self.clear_database()
        if dbinit == "demo":
            self.db_name =  "SpaceInvader\\resource\\gamerepository_demo.db" 
        database_exist,message = self.database_exist_check(self.db_name)
        self.conn = sqlite3.connect(self.db_name)
        self.c = self.conn.cursor()
        if not database_exist:
            self.setup_table()

    def database_exist_check(self,db_name):
        try:
            f = open(db_name,"r")
            contents = f.read()
            f.close()
            if len(contents) == 0:
                return False,"File Kosong"
        except UnicodeDecodeError:
            return True,"Database sudah ada"
        except:
            f = open(db_name,"w+")
            f.close()
            return False,"file unexist\ncreating new database file..."

    def clear_database(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def setup_table(self):
        create_user_table = """
        CREATE TABLE user(
            username TEXT(10) PRIMARY KEY,
                 age INTEGER,
               email TEXT
        );"""
        create_game_table = """
          CREATE TABLE game_play_history(
               id_game INTEGER PRIMARY KEY,
              username TEXT,
                 score INTEGER,
              accuracy NUMBER,
           enemy_kiled INTEGER,
           bullet_lost INTEGER,
            time_start DATETIME,
              duration INTEGER,
                 level INTEGER
        );"""
        self.c.execute(create_user_table)
        self.c.execute(create_game_table)
        self.conn.commit()

    def register_new_user(self,username,age,email):
        insert_user = """
        INSERT INTO user 
        VALUES (?, ?, ?);
        """
        self.c.execute(insert_user, (username,age,email))
        self.conn.commit()

    def record_new_game(self,id_game,username,score,accuracy,enemy_killed,bullet_lost,time_start,duration,level):
        record_game = """
        INSERT INTO game_play_history
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        self.c.execute(record_game, (id_game,username,score,accuracy,enemy_killed,bullet_lost,time_start,duration,level))
        self.conn.commit()
    
    def check_username_exist(self,username):
        checker_username = """
        SELECT *
          FROM user
         WHERE username = ?;
        """
        self.c.execute(checker_username,(username,))
        rows = self.c.fetchall()
        if rows == []:
            return UsernameCheckerDTO(False)
        return UsernameCheckerDTO(True)

    def get_user_data(self,username):
        user_data = """
        SELECT *
          FROM user
         WHERE username = ?;"""
        self.c.execute(user_data,(username,))
        rows = self.c.fetchall()[0]
        return UserProfileDataDTO(rows[0],rows[1],rows[2])

    def get_last_game_id(self):
        last_game_id = """
        SELECT id_game
          FROM game_play_history
         ORDER BY id_game DESC
         LIMIT 1"""
        self.c.execute(last_game_id)
        rows = self.c.fetchall()
        if rows == []:
            return LastGameIdDTO(0)
        return LastGameIdDTO(rows[0][0])

    def get_last_game_report(self):
        last_game_id = """
        SELECT *
          FROM game_play_history
         ORDER BY id_game DESC
         LIMIT 1"""
        self.c.execute(last_game_id)
        rows = self.c.fetchall()[0]
        username = rows[1]
        score = rows[2]
        highscore = self.get_user_high_score(username).highscore
        duration = rows[7]
        enemy_kiled = rows[4]
        bullet_lost = rows[5]
        accuracy = rows[3]
        level = rows[8]
        return GameOverDTO(score,highscore,duration,enemy_kiled,bullet_lost,accuracy,level)

    def get_user_high_score(self,username):
        user_play_history = """
        CREATE VIEW user_play_history AS
        SELECT *
          FROM game_play_history
         WHERE username = "?";"""
        
        high_score = """
        SELECT score
         FROM user_play_history
        ORDER BY score DESC
        LIMIT 1;
        """

        drop_view = """DROP VIEW user_play_history;"""

        # self.c.execute(drop_view)
        self.c.execute(user_play_history.replace("?",username))
        self.c.execute(high_score)
        rows = self.c.fetchall()
        self.c.execute(drop_view)

        if rows == []:
            return HighScoreDTO(0)
        return HighScoreDTO(rows[0][0])

    def get_scoreboard_data(self):
        scoreboard = """
          SELECT username, MAX(score)
            FROM game_play_history
        GROUP BY username
        ORDER BY MAX(score) DESC
        """
        self.c.execute(scoreboard)
        rows = self.c.fetchall()
        username_list = []
        highscore_list = []
        for username, highscore in rows:
            username_list.append(username)
            highscore_list.append(highscore)
        return ScoreBoardDTO(username_list,highscore_list)

    def get_user_score_history(self,username):
        score_history = """
        SELECT score
         FROM game_play_history
        WHERE username = '?';"""
        self.c.execute(score_history.replace("?",username))
        rows = self.c.fetchall()
        score_list = []
        for i in rows:
            score_list.append(i[0])
        return score_list

    def get_user_accuracy_history(self,username):
        accuracy_history = """
        SELECT accuracy
         FROM game_play_history
        WHERE username = '?';"""
        self.c.execute(accuracy_history.replace("?",username))
        rows = self.c.fetchall()
        accuracy_list = []
        for i in rows:
            accuracy_list.append(i[0])
        return accuracy_list

    def get_user_enemy_killed_history(self,username):
        enemy_killed_history = """
        SELECT enemy_kiled
         FROM game_play_history
        WHERE username = '?';"""
        self.c.execute(enemy_killed_history.replace("?",username))
        rows = self.c.fetchall()
        enemy_killed_list = []
        for i in rows:
            enemy_killed_list.append(i[0])
        return enemy_killed_list

    def get_user_duration_history(self,username):
        duration_history = """
        SELECT duration
         FROM game_play_history
        WHERE username = '?';"""
        self.c.execute(duration_history.replace("?",username))
        rows = self.c.fetchall()
        duration_list = []
        for i in rows:
            duration_list.append(i[0])
        return duration_list

    def get_first_rank_username_and_email(self):
        first_rank_username_email = """
            SELECT game_play_history.username, user.email
              FROM game_play_history
        INNER JOIN user on game_play_history.username = user.username
          ORDER BY game_play_history.score DESC
             LIMIT 1"""
        self.c.execute(first_rank_username_email)
        rows = self.c.fetchall()
        firsrank_username = None
        firsrank_email = None
        for username,email in rows:
            firsrank_username = username
            firsrank_email = email
        return PlayerEmailDTO(firsrank_username,firsrank_email)
        