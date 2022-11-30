
from matplotlib import use


class UserProfileDataDTO:
    def __init__(self, username_, age_, email_):
        self.username = username_
        self.age = age_
        self.email = email_

class GamePlayDTO:
    def __init__(self,id_game_,username_,score_,accuracy_,enemy_killed_,bullet_lost_,time_start_,duration_):
        self.id_game = id_game_
        self.username = username_
        self.score = score_
        self.accuracy = accuracy_
        self.enemy_killed = enemy_killed_
        self.bullet_lost = bullet_lost_
        self.time_start = time_start_
        self.duration = duration_

class GameOverDTO:
    def __init__(self,score_,highscore_,duration_,enemy_killed_,bullet_lost_,accuracy_,level_):
        self.score = score_
        self.highscore = highscore_
        self.duration = duration_
        self.enemy_killed = enemy_killed_
        self.bullet_lost = bullet_lost_
        self.accuracy = accuracy_
        self.level = level_

class UsernameCheckerDTO:
    def __init__(self, exist_):
        self.exist = exist_

class LastGameIdDTO:
    def __init__(self, game_id_):
        self.game_id = game_id_

class HighScoreDTO:
    def __init__(self,highscore_):
        self.highscore = highscore_

class ScoreBoardDTO:
    def __init__(self,username_list_,highscore_list_):
        self.username_list = username_list_
        self.highscore_list = highscore_list_

class CollisionCheckerDTO:
    def __init__(self,is_collision_):
        self.is_collision = is_collision_

class PlayerEmailDTO:
    def __init__(self,username_,email_):
        self.username = username_
        self.email = email_