from kink import inject
from SpaceInvader.dto import CollisionCheckerDTO, PlayerEmailDTO

from SpaceInvader.game_repository import GameRepository
from SpaceInvader.observerpattern import FirstRankMessange, NoteNewScoreSubject

@inject
class GameService:
    def __init__(self, game_repository : GameRepository,note_new_score_subject_ : NoteNewScoreSubject):
        self.repository = game_repository
        self.note_new_score_subject = note_new_score_subject_ 

        first_rank = self.firstrank_email()
        self.note_new_score_subject.first_rank_setup(first_rank.username,first_rank.email)

    def register_new_user(self,username,age,email):
        username_checker = self.repository.check_username_exist(username)
        if username_checker.exist:
            return False
        self.repository.register_new_user(username,age,email)
        return True

    def login_game(self,username):
        username_checker = self.repository.check_username_exist(username)
        return username_checker.exist

    def user_score_history(self,username):
        return self.repository.get_user_score_history(username)

    def user_accuracy_history(self,username):
        return self.repository.get_user_accuracy_history(username)

    def user_enemy_killed_history(self,username):
        return self.repository.get_user_enemy_killed_history(username)

    def user_duration_history(self,username):
        return self.repository.get_user_duration_history(username)
    
    def game_over_handle(self,username,score,time_start,duration,enemy_killed,bullet_lost,level):
        game_id = self.repository.get_last_game_id().game_id + 1
        if bullet_lost != 0:
            accuracy = round((enemy_killed/bullet_lost)*100,2)
        else:
            accuracy = 0
        time_start = int(time_start)
        duration = int(duration)
        self.repository.record_new_game(game_id,username,score,accuracy,enemy_killed,bullet_lost,time_start,duration,level)
        
        first_rank = self.firstrank_email()
        msg = FirstRankMessange(first_rank.username,first_rank.email)
        self.note_new_score_subject.notify_update(msg)


    def last_game_id(self):
        return self.repository.get_last_game_id()

    def last_game_report(self):
        return self.repository.get_last_game_report()

    def highscoreboard(self):
        return self.repository.get_scoreboard_data()

    def collision_checker(self,alien_pos_x,alien_pos_y,bullet_pos_x,bullet_pos_y):
        distance = ((alien_pos_x-bullet_pos_x)**2 + (alien_pos_y-bullet_pos_y)**2)**0.5
        if distance < 32:
            return CollisionCheckerDTO(True)
        return CollisionCheckerDTO(False)
        

    def firstrank_email(self) -> PlayerEmailDTO: 
        return self.repository.get_first_rank_username_and_email()
        
                    