import pygame
from pygame import mixer
from kink import inject, di
from SpaceInvader.game_resource import GameResource
from SpaceInvader.game_service import GameService
import sys
import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab

@inject
class GameGui:
    def __init__(self,game_service:GameService, game_resource:GameResource):
        pygame.init()
        self.service = game_service
        self.resource = game_resource
        self.clock = pygame.time.Clock()
        self.screen = self.setting_window()
        self.username = None
        self.space_ship = SpaceShip()
        self.enemies = Enemies(10,self.service)
        self.bullet = Bullet()
        self.music_code = 1
        pygame.mixer.music.load(self.resource.music_bg1)
        pygame.mixer.music.play(-1)
        # pygame.mixer.music.set_volume(0.0)

    def rounded_rect_button_click(self,x_pos,y_pos,x_mause,y_mause):
        r = 56
        r_2 = 3136
        l1 = (x_mause-(x_pos+r))**2 + (y_mause-(y_pos+r))**2 <= r_2
        l2 = (x_mause-(x_pos+r+231))**2 + (y_mause-(y_pos+r))**2 <= r_2
        k = x_pos+56 <= x_mause <= x_pos+56+231 and y_pos <= y_mause <= y_pos+112
        return any([l1,l2,k])

    def rounded_rect_text_input_click(self,x_pos,y_pos,x_mause,y_mause):
        r = 59/2
        r_2 = r**2
        l1 = (x_mause-(x_pos+r))**2 + (y_mause-(y_pos+r))**2 <= r_2
        l2 = (x_mause-(x_pos+r+330))**2 + (y_mause-(y_pos+r))**2 <= r_2
        k = x_pos+29 <= x_mause <= x_pos+29+333 and y_pos <= y_mause <= y_pos+59
        return any([l1,l2,k])

    def start_button_click(self,x_pos,y_pos,x_mause,y_mause):
        r = 66
        r_2 = r**2
        l1 = (x_mause-(x_pos+r))**2 + (y_mause-(y_pos+r))**2 <= r_2
        l2 = (x_mause-(x_pos+r+283))**2 + (y_mause-(y_pos+r))**2 <= r_2
        k = x_pos+62 <= x_mause <= x_pos+62+291 and y_pos <= y_mause <= y_pos+132
        return any([l1,l2,k])

    def analyst_button_click(self,x_pos,y_pos,x_mause,y_mause):
        r = 75.5
        r_2 = r**2
        l1 = (x_mause-(x_pos+r))**2 + (y_mause-(y_pos+r))**2 <= r_2
        l2 = (x_mause-(x_pos+r+161))**2 + (y_mause-(y_pos+r))**2 <= r_2
        k = x_pos+38 <= x_mause <= x_pos+38+162 and y_pos <= y_mause <= y_pos+75
        return any([l1,l2,k])
    
    def rect_analyst_button_click(self,x_pos,y_pos,x_mouse,y_mause):
        return x_pos <= x_mouse <= x_pos+224 and y_pos <= y_mause <= y_pos+38

    def round_button_click(self,x_pos,y_pos,x_mause,y_mause,r=39):
        r_2 = r**2
        l = (x_mause-(x_pos+r))**2 + (y_mause-(y_pos+r))**2 <= r_2
        return l

    def setting_window(self):
        screen = pygame.display.set_mode((800,600),pygame.FULLSCREEN)
        icon = self.resource.icon
        pygame.display.set_caption("Space Invader")
        pygame.display.set_icon(icon)
        return screen

    def front_page(self):
        running = True
        bg0 = self.resource.front0
        bg1 = self.resource.front1
        bip = 0
        while running:
            self.clock.tick(2)
            bip+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

            if bip%2 == 0:  
                self.screen.blit(bg0,(0,0))
            else:
                self.screen.blit(bg1,(0,0))
            pygame.display.update()
        self.resource.button_click_sound.play()

    #code = 0
    def main_menu(self):
        running = True
        bg = self.resource.main_menu
        outcode = -1
        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        running = False
                        outcode = 1
                    if event.key == pygame.K_2:
                        running = False
                        outcode = 2
                    if event.key == pygame.K_3:
                        running = False
                        outcode = 3
                    if event.key == pygame.K_q:
                        running = False
                        outcode = -1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.rounded_rect_button_click(46,277,x,y): #new player
                        running = False
                        outcode = 1
                        self.resource.button_click_sound.play()
                    if self.rounded_rect_button_click(410,277,x,y): #registered player
                        running = False
                        outcode = 2
                        self.resource.button_click_sound.play()
                    if self.rounded_rect_button_click(228,429,x,y): #score board
                        running = False
                        outcode = 3
                        self.resource.button_click_sound.play()
                    if self.round_button_click(683,483,x,y): #close button
                        running = False
                        outcode = -1
                        self.resource.button_click_sound.play()
                    
            self.screen.blit(bg,(0,0))
            pygame.display.update()
        
        if outcode == 1:
            self.new_player()
        elif outcode == 2:
            self.registered_player()
        elif outcode == 3:
            self.score_board(0)
        elif outcode == -1:
            self.quit_game()
                    
    #code = 1
    def new_player(self):
        running = True
        bg = self.resource.new_player
        outcode = -1
        text_boxs = ['','','']
        text_boxs_state = [False,False,False]
        base_font = pygame.font.SysFont('High Tower Text', 60)
        bip = 0
        while running:
            bip = (bip + 1) % 4 
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if any(text_boxs_state):
                        i = text_boxs_state.index(True)
                        if event.key == pygame.K_BACKSPACE:
                            text_boxs[i] = text_boxs[i][:-1]
                        elif event.key == 13:
                            if i == 0:
                                text_boxs_state = [False,True,False]
                            elif i == 1:
                                text_boxs_state = [False,False,True]
                            else:
                                
                                if any([i == "" for i in text_boxs]):
                                    bg = self.resource.new_player_empty_warning
                                    self.resource.button_warning_sound.play() # you must fill all  field 
                        
                                    continue
                                register_success = self.service.register_new_user(text_boxs[0],text_boxs[1],text_boxs[2])
                                if register_success:
                                    self.username = text_boxs[0]
                                    running = False
                                    outcode = 4
                                    self.resource.button_click_sound.play() #register success
                                else:
                                    bg = self.resource.new_player_exist
                                    self.resource.button_warning_sound.play() #register failed

                        elif event.key in (92,39):
                            pass
                        else:
                            if i == 1:
                                if event.unicode.isdigit():
                                    text_boxs[i] += event.unicode
                            else:
                                text_boxs[i] += event.unicode.lower().replace(" ","")
                            if i != 2:

                                text_boxs[i] = text_boxs[i][:10]

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(60,483,x,y): #back
                        running = False
                        outcode = 0
                        self.resource.button_click_sound.play()
                    if self.round_button_click(662,483,x,y):                        
                        if any([i == "" for i in text_boxs]):
                            bg = self.resource.new_player_empty_warning
                            self.resource.button_warning_sound.play() #you must fill all  field
                            continue
                        register_success = self.service.register_new_user(text_boxs[0],text_boxs[1],text_boxs[2])
                        if register_success:
                            self.username = text_boxs[0]
                            running = False
                            outcode = 4
                            self.resource.button_click_sound.play() #register success
                        else:
                            bg = self.resource.new_player_exist
                            self.resource.button_warning_sound.play() #register failed

                    if self.rounded_rect_text_input_click(202,261,x,y): #text box 1 clicked
                        text_boxs_state = [True,False,False]
                    elif self.rounded_rect_text_input_click(202,360,x,y): #text box 2 clicked
                        text_boxs_state = [False,True,False]
                    elif self.rounded_rect_text_input_click(202,463,x,y): #text box 3 clicked
                        text_boxs_state = [False,False,True]
                    else: #text box inactive
                        text_boxs_state = [False,False,False]

            self.screen.blit(bg,(0,0))
            if bip < 2:
                if text_boxs_state[0]:
                    pygame.draw.line(self.screen, (97,67,121), (231,316), (567,316), width=2)
                if text_boxs_state[1]:
                    pygame.draw.line(self.screen, (97,67,121), (231,415), (567,415), width=2)
                if text_boxs_state[2]:
                    pygame.draw.line(self.screen, (97,67,121), (231,518), (567,518), width=2)
            k = 30
            if len(text_boxs[2]) >= 10:
                c = "~"
            else:
                c = " "
            text_surface1 = base_font.render(text_boxs[0],True,(99,68,161))
            text_rect1 = text_surface1.get_rect(center=(400,262+k))
            self.screen.blit(text_surface1,text_rect1)
            text_surface2 = base_font.render(text_boxs[1],True,(99,68,161))
            text_rect2 = text_surface2.get_rect(center=(400,361+k))
            self.screen.blit(text_surface2,text_rect2)
            text_surface3 = base_font.render(c+text_boxs[2][-9:],True,(99,68,161))
            text_rect3 = text_surface3.get_rect(center=(400,464+k))
            self.screen.blit(text_surface3,text_rect3)
            pygame.display.update()

        if outcode == 0:
            self.main_menu()
        elif outcode == 4:
            self.start_page()

    #code = 2
    def registered_player(self):   
        running = True
        bg = self.resource.registered_player
        outcode = -1
        base_font = pygame.font.SysFont('High Tower Text', 60)
        user_name = ''
        text_box_state = False
        bip = 0
        while running:
            bip = (bip + 1) % 4
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if text_box_state:
                        if event.key == pygame.K_BACKSPACE:
                            user_name = user_name[:-1]
                        elif event.key == 13:
                            loggin_success = self.service.login_game(user_name)
                            if loggin_success:
                                running = False
                                outcode = 4
                                self.username = user_name.lower()
                                self.resource.button_click_sound.play() #login sucsess
                            else:
                                bg = self.resource.registered_player_not_exist
                                self.resource.button_warning_sound.play() #login failed
                        elif event.key in (92,39):
                            pass
                        else:
                            user_name += event.unicode.replace(" ","")
                            user_name = user_name[:10]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(60,483,x,y): #back
                        running = False
                        outcode = 0
                        self.resource.button_click_sound.play()
                    if self.round_button_click(662,483,x,y):#next

                        loggin_success = self.service.login_game(user_name)
                        if loggin_success:
                            running = False
                            outcode = 4
                            self.username = user_name.lower()
                            self.resource.button_click_sound.play() #login sucess
                        else:
                            bg = self.resource.registered_player_not_exist
                            self.resource.button_warning_sound.play() #login failed

                    if self.rounded_rect_text_input_click(202,345,x,y): #text_box click
                        text_box_state = True
                    else:
                        text_box_state = False

            user_name_show = user_name.center(12).lower()
            self.screen.blit(bg,(0,0))
            if bip < 2:
                if text_box_state:
                    pygame.draw.line(self.screen, (97,67,121), (231,399), (567,399), width=2)
            text_surface = base_font.render(user_name_show,True,(99,68,161))
            text_rect = text_surface.get_rect(center=(400,375))
            self.screen.blit(text_surface,text_rect)
            pygame.display.update()

        if outcode == 0:
            self.main_menu()
        elif outcode == 4:
            self.start_page()

    #code = 3
    def score_board(self,page):
        running = True
        bg = self.resource.score_board
        outcode = -1
        highscore_table = self.service.highscoreboard()
        username_collumn = highscore_table.username_list
        highscore_collumn = highscore_table.highscore_list
        num_name = len(username_collumn)
        if (num_name/13) > 1:
            username_collumn = username_collumn[page*13:(page+1)*13]
            highscore_collumn = highscore_collumn[page*13:(page+1)*13]
        
        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        outcode = 0
                        running = False
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(60,483,x,y): #back
                        running = False
                        outcode = 0
                        self.resource.button_click_sound.play()
                    if page > 0: #can go to previous 
                        if self.round_button_click(662,249,x,y): #up
                            self.resource.button_click_sound.play()
                            running = False
                            outcode = 30
                    if page+1 < (num_name/13):
                        if self.round_button_click(662,343,x,y): #down
                            self.resource.button_click_sound.play()
                            running = False
                            outcode = 31

            self.screen.blit(bg,(0,0))
            for i in range(len(username_collumn)):
                username_label = self.resource.display_font.render(str(i+1+(13*page))+". "+username_collumn[i],True,(255,255,255))
                self.screen.blit(username_label, (195,146+i*30))
                username_label = self.resource.display_font.render(f"{highscore_collumn[i]}",True,(255,255,255))
                text_rect = username_label.get_rect()
                text_rect.right = 625
                text_rect.y = 146+i*30
                self.screen.blit(username_label,text_rect)
            
            
            pygame.display.update()
            
        if outcode == 0:
            self.main_menu()
        elif outcode == 30:
            self.score_board(page-1)
        elif outcode == 31:
            self.score_board(page+1)

    #code = 4
    def start_page(self):
        if self.music_code == 2:
            pygame.mixer.music.load(self.resource.music_bg1)
            pygame.mixer.music.play(-1)
            self.music_code = 1
        running = True
        bg = self.resource.start_page
        base_font = pygame.font.SysFont('High Tower Text', 40)
        outcode = -1

        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        running = False
                        outcode = 0
                    if event.key == pygame.K_p:
                        running = False
                        outcode = 8
                    if event.key == pygame.K_n:
                        running = False
                        outcode = 5
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(60,483,x,y): #back
                        running = False
                        outcode = 0
                        self.resource.button_click_sound.play()
                    if self.start_button_click(192,251,x,y): #start
                        running = False
                        outcode = 5
                        self.resource.button_click_sound.play()
                    if self.analyst_button_click(282,420,x,y): #analist
                        running = False
                        outcode = 8
                        self.resource.button_click_sound.play()

            self.screen.blit(bg,(0,0))
            message = f"Welcome {self.username}!"
            text_surface = base_font.render(message,True,(217,217,217))
            self.screen.blit(text_surface,(315,520))
            pygame.display.update()
            
        if outcode == 0:
            self.main_menu()
        elif outcode == 5:
            self.in_game()
        elif outcode == 8:
            self.player_analyst()
            
    #code = 5
    def in_game(self):
        pygame.mixer.music.load(self.resource.music_bg3)
        pygame.mixer.music.play(-1)
        self.music_code = 2
        running = True
        bg = self.resource.in_game_bg1
        pause_bg = self.resource.pause_game
        is_paused = False
        outcode = -1
        score = 0
        level = 1
        enemy_kiled = 0
        bullet_lost = 0
        level_check_point = 100
        number_font = self.resource.input_font
        self.enemies.spawn_random_all_enemies()
        time_start = time.time()
        while running:
            self.clock.tick(20+5*level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.space_ship.go_left()
                    if event.key == pygame.K_RIGHT:
                        self.space_ship.go_right()

                    if event.key == pygame.K_SPACE:
                        self.bullet.fire_bullet(self.space_ship.x_pos)

                    if event.key == pygame.K_b:
                        running = False
                        outcode = 4
                    if event.key == pygame.K_b:
                        running = False
                        outcode = 4
                    if event.key == pygame.K_p:
                        is_paused = not is_paused
                    if event.key == pygame.K_n:
                        running = False
                        outcode = 7

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.space_ship.stay()        
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(735,14,x,y,r=23.5):
                        is_paused = not is_paused
                        self.resource.button_click_sound.play()
                    if is_paused:
                        if self.round_button_click(662,483,x,y): #next
                            running = False
                            outcode = 7
                    
            if is_paused:
                self.space_ship.stay()
                self.enemies.stay()
                self.bullet.stay()
            else:
                self.enemies.continue_move()
                self.bullet.continue_move()
            
            if (score//100)%2 != 0 and score == level_check_point:
                    self.resource.level_up_sound.play()
                    level +=1 
                    level_check_point += 200 
                    if level % 5 == 0: #Setiap levelnya mencapai kelipatan 5 munculin musuh baru
                        # for i in range(level//5): self.enemies.create_new_enemy() #musuh barunya sebanyak kelipatan 5 dari levelnya
                        self.enemies.create_new_enemy()


            if self.enemies.game_over_checker():
                running = False
                outcode = 7
                
            bullet_x, bullet_y = self.bullet.get_position()
            if bullet_y < -10:
                self.bullet.disappear()
                bullet_lost+=1
            hit,enemy_num =self.enemies.enemy_hited_check(bullet_x, bullet_y)
            if hit:
                enemy_kiled+=1
                bullet_lost+=1
                score+=10
                self.resource.explosion_sound.play()
                self.bullet.disappear()
                self.enemies.respawn_enemy(enemy_num)
            self.screen.blit(bg,(0,0))
            self.space_ship.show(self.screen)
            self.enemies.show(self.screen)
            self.bullet.show(self.screen)
            if is_paused:
                self.screen.blit(pause_bg,(0,0))
            self.show_score(str(score))
            self.show_level(str(level))
            pygame.display.update()
            
        if outcode == 4:
            self.start_page()
        elif outcode == 7:
            time_end = time.time()
            duration = time_end-time_start
            self.service.game_over_handle(self.username,score,time_start,duration,enemy_kiled,bullet_lost,level)
            self.game_over()
    
    #code = 7
    def game_over(self):
        running = True
        bg = self.resource.game_over
        outcode = -1
        self.resource.game_over_sound.play()
        game_overdto = self.service.last_game_report()
        score = self.resource.display_font.render(str(game_overdto.score),True,(255,255,255))
        highscore = self.resource.display_font.render(str(game_overdto.highscore),True,(255,255,255))
        time_play = self.resource.display_font.render(str(game_overdto.duration)+" s",True,(255,255,255))
        enemy_kiled = self.resource.display_font.render(str(game_overdto.enemy_killed),True,(255,255,255))
        bullet_lost = self.resource.display_font.render(str(game_overdto.bullet_lost),True,(255,255,255))
        accuracy = self.resource.display_font.render(str(int(game_overdto.accuracy))+"%",True,(255,255,255))
        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        running = False
                        outcode = 4
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(662,483,x,y): #next
                        running = False
                        outcode = 4
                        self.resource.button_click_sound.play()
            self.screen.blit(bg,(0,0))
            self.show_level(str(game_overdto.level))
            
            self.screen.blit(score,     (299,404))
            self.screen.blit(highscore, (299,454))
            self.screen.blit(time_play, (299,502))
            self.screen.blit(enemy_kiled, (598,404))
            self.screen.blit(bullet_lost, (598,454))
            self.screen.blit(accuracy, (598,502))
            pygame.display.update()
            
        if outcode == 4:
            self.start_page()
    
    #code = 8
    def player_analyst(self):
        running = True
        bg = self.resource.player_analyst
        outcode = -1

        self.screen.blit(bg,(0,0))
        self.show_line_diagram("Score")
        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        outcode = 4
                        running = False
                    
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(60,483,x,y): #back
                        running = False
                        outcode = 4
                        self.resource.button_click_sound.play()
                    if self.rect_analyst_button_click(174,487, x, y):
                        self.show_line_diagram("Score")
                    if self.rect_analyst_button_click(174,530, x, y):
                        self.show_line_diagram("Enemy Killed")
                    if self.rect_analyst_button_click(402,487, x, y):
                        self.show_line_diagram("Accuracy")
                    if self.rect_analyst_button_click(402,530, x, y):
                        self.show_line_diagram("Duration")

            pygame.display.update()
            
        if outcode == 4:
            self.start_page()

    # code -1
    def quit_game(self):
        running = True
        bg = self.resource.quit_game
        outcode = -1

        while running:
            self.clock.tick(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        running = False
                        outcode = -1
                    if event.key == pygame.K_n:
                        running = False
                        outcode = 0
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.round_button_click(200,309,x,y,r=80): #yes
                        running = False
                        self.resource.button_click_sound.play()
                    if self.round_button_click(441,309,x,y,r=80): #no
                        running = False
                        outcode = 0
                        self.resource.button_click_sound.play()

            self.screen.blit(bg,(0,0))
            pygame.display.update()
            
        if outcode == 0:
            self.main_menu()
        time.sleep(0.5)
        
    def show_score(self,score_value):
        score = self.resource.display_font.render(score_value,True,(255,255,255))
        self.screen.blit(score, (119,23))
    
    def show_level(self,level_value):
        score = self.resource.display_font.render(level_value,True,(255,255,255))
        self.screen.blit(score, (436,23))
 
    def play(self):
        self.front_page()
        self.main_menu()

    def show_line_diagram(self,title):
        if title == "Score":
            data = self.service.user_score_history(self.username)
        if title == "Accuracy":
            data = self.service.user_accuracy_history(self.username)
        if title == "Enemy Killed":
            data = self.service.user_enemy_killed_history(self.username)
        if title == "Duration":
            title += " (s)"
            data = self.service.user_duration_history(self.username)

        
        pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(174, 144, 449, 333))
        pygame.display.flip()
        game = range(1,len(data)+1)
        my_dpi = 92
        fig = pylab.figure(figsize=(449/my_dpi, 320/my_dpi),dpi=my_dpi)
        ax = fig.gca()
        ax.plot(game,data,'o--b')
        ax.set_ylabel(title.lower())
        ax.yaxis.set_label_position("right")
        # ax.yaxis.tick_right()
        # ax.xaxis.xticks(game)
        ax.grid()

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (174,144))
        text_surface = self.resource.analyst_title_font.render(title,True,(90,57,155))
        text_rect = text_surface.get_rect(center=(400,160))
        self.screen.blit(text_surface,text_rect)
        text_surface = self.resource.matplotlib_sans.render("game play",True,(0,0,0))
        text_rect = text_surface.get_rect(center=(400,460))
        self.screen.blit(text_surface,text_rect)
        pygame.display.flip()


class SpaceShip:
    def __init__(self) -> None:
        self.ship_img = pygame.image.load("SpaceInvader\\resource\\spaceship.png")
        self.x_pos = 370
        self.y_pos = 480
        self.x_change = 0
        self.move_dist = 5

    def go_right(self):
        self.x_change = self.move_dist

    def go_left(self):
        self.x_change = -self.move_dist

    def stay(self):
        self.x_change = 0

    def show(self,screen):
        if 0 <= self.x_pos + self.x_change <= 739:
                self.x_pos += self.x_change     

        screen.blit(self.ship_img,(self.x_pos,self.y_pos))

class Alien:
    def __init__(self,x_spawn,y_spawn):
        self.alive = True
        self.alien_img = pygame.image.load("SpaceInvader\\resource\\alien1.png")
        # headlist = [pygame.image.load("SpaceInvader\\resource\\bryan_head.png"),
        #             pygame.image.load("SpaceInvader\\resource\\victor_head.png"),
        #             pygame.image.load("SpaceInvader\\resource\\stef_head.png"),
        #             pygame.image.load("SpaceInvader\\resource\\udey_head.png")]
        # self.alien_img = headlist[random.randint(0,3)]
        self.x_pos = x_spawn
        self.y_pos = y_spawn
        self.move_x_dist = 5
        self.move_y_dist = 40
        self.move_pattern = random.randint(0,1)
        self.is_stay = False

    def killed(self):
        self.alive = False

    def move(self):
        if self.move_pattern == 0: #kekiri
            if 0 <= self.x_pos - self.move_x_dist:
                self.x_pos -= self.move_x_dist
            else:
                self.move_pattern = 1
                self.y_pos += self.move_y_dist

        else: #kekanan
            if self.x_pos + self.move_x_dist <= 739:
                self.x_pos += self.move_x_dist
            else:
                self.move_pattern = 0
                self.y_pos += self.move_y_dist

    def respawn(self,x_spawn,y_spawn):
        self.x_pos = x_spawn
        self.y_pos = y_spawn
        self.alive = True

    def stay(self):
        self.is_stay = True
    
    def continue_move(self):
        self.is_stay = False

    def show(self,screen):
        if self.alive:
            if not self.is_stay:
                self.move()
            
            screen.blit(self.alien_img,(self.x_pos,self.y_pos))

class Enemies:
    def __init__(self,num_enemy_,service_):
        self.service = service_
        self.num_enemy = num_enemy_
        self.x_spawn = []
        self.y_spawn = []
        self.aliens = []
        self.spawn_random_all_enemies()

    def spawn_random_all_enemies(self):
        self.x_spawn = random.sample(range(1,739),self.num_enemy)
        self.y_spawn = random.sample(range(50,300),self.num_enemy)
        self.aliens = [Alien(self.x_spawn[i],self.y_spawn[i]) for i in range(self.num_enemy)]

    def create_new_enemy(self):
        x_spawn = random.randint(1,738)
        y_spawn = random.randint(50,299)
        new_alien = Alien(x_spawn,y_spawn)
        self.num_enemy+=1
        self.aliens.append(new_alien)

    def game_over_checker(self):
        y_over = 428
        for alien in self.aliens:
            if alien.y_pos >= y_over:
                return True
        return False

    def stay(self):
        for alien in self.aliens:
            alien.stay()

    def continue_move(self):
        for alien in self.aliens:
            alien.continue_move()        

    def show(self,screen):
        for alien in self.aliens:
            alien.show(screen)

    def respawn_enemy(self,enemy_num):
        x_spawn = random.randint(1,738)
        y_spawn = random.randint(50,299)
        self.aliens[enemy_num].respawn(x_spawn,y_spawn)

    def enemy_hited_check(self,bullet_pos_x,bullet_pos_y):
        for i in range(self.num_enemy):
            alien = self.aliens[i]
            alien_pos_x = alien.x_pos+32
            alien_pos_y = alien.y_pos+32
            collision_checker = self.service.collision_checker(alien_pos_x,alien_pos_y,bullet_pos_x,bullet_pos_y)
            if collision_checker.is_collision:
                kiled_alien = self.aliens[i].killed()
                return True,i
            
        return False,-1

class Bullet:
    def __init__(self):
        self.state = 'ready'
        self.bullet_img = pygame.image.load("SpaceInvader\\resource\\bullet.png")
        self.is_stay = True
        self.x_pos = 0
        self.y_pos = 480
        self.y_change = 10
        self.fire_sound = mixer.Sound("SpaceInvader\\resource\\laser.wav")

    def fire_bullet(self,x):
        if self.state == 'ready':
            self.x_pos = x+16
            self.state = 'fire'
            self.fire_sound.play()
    
    def get_position(self):
        if self.state == 'fire':
            return(self.x_pos+16,self.y_pos)
        return (0,0)

    def disappear(self):
        self.state = 'ready'
        self.y_pos = 480
    
    def stay(self):
        self.is_stay = True
    
    def continue_move(self):
        self.is_stay = False
    
    def move(self):
        if self.state == 'fire':
            self.y_pos -= self.y_change

    def show(self,screen):
        if not self.is_stay:
            self.move()
        if self.state == 'fire':
            screen.blit(self.bullet_img,(self.x_pos,self.y_pos))

    
