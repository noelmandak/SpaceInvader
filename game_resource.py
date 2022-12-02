from kink.inject import inject
import pygame

# password = czrbpchencqjdeio

@inject
class GameResource:
    def __init__(self):
        pygame.init()
        self.icon = pygame.image.load("SpaceInvader\\resource\\ufo.png")
        self.background = pygame.image.load("SpaceInvader\\resource\\background.png")
        
        self.front0 = pygame.image.load("SpaceInvader\\resource\\chrismas\\front_page0.png")
        self.front1 = pygame.image.load("SpaceInvader\\resource\\chrismas\\front_page1.png")
        self.main_menu = pygame.image.load("SpaceInvader\\resource\\chrismas\\main_menu.png")
        self.new_player = pygame.image.load("SpaceInvader\\resource\\chrismas\\new_player.png")
        self.new_player_exist = pygame.image.load("SpaceInvader\\resource\\chrismas\\new_player_exist.png")
        self.new_player_empty_warning = pygame.image.load("SpaceInvader\\resource\\chrismas\\new_player_empty_warning.png")
        self.registered_player = pygame.image.load("SpaceInvader\\resource\\chrismas\\registered_player.png")
        self.registered_player_not_exist = pygame.image.load("SpaceInvader\\resource\\chrismas\\registered_player_not_exist.png")
        self.score_board = pygame.image.load("SpaceInvader\\resource\\chrismas\\score_board.png")
        self.start_page = pygame.image.load("SpaceInvader\\resource\\chrismas\\start_page.png")
        self.quit_game = pygame.image.load("SpaceInvader\\resource\\chrismas\\quit.png")
        self.player_analyst = pygame.image.load("SpaceInvader\\resource\\chrismas\\player_analyst.png")
        # self.in_game_bg1 = pygame.image.load("SpaceInvader\\resource\\chrismas\\in_game_bg1.png")
        # self.pause_game = pygame.image.load("SpaceInvader\\resource\\chrismas\\game_pause.png")
        # self.game_over = pygame.image.load("SpaceInvader\\resource\\chrismas\\game_over.png")
        
        # self.front0 = pygame.image.load("SpaceInvader\\resource\\front_page0.png")
        # self.front1 = pygame.image.load("SpaceInvader\\resource\\front_page1.png")
        # self.main_menu = pygame.image.load("SpaceInvader\\resource\\main_menu.png")
        # self.new_player = pygame.image.load("SpaceInvader\\resource\\new_player.png")
        # self.new_player_exist = pygame.image.load("SpaceInvader\\resource\\new_player_exist.png")
        # self.new_player_empty_warning = pygame.image.load("SpaceInvader\\resource\\new_player_empty_warning.png")
        # self.registered_player = pygame.image.load("SpaceInvader\\resource\\registered_player.png")
        # self.registered_player_not_exist = pygame.image.load("SpaceInvader\\resource\\registered_player_not_exist.png")
        # self.score_board = pygame.image.load("SpaceInvader\\resource\\score_board.png")
        # self.start_page = pygame.image.load("SpaceInvader\\resource\\start_page.png")
        # self.quit_game = pygame.image.load("SpaceInvader\\resource\\quit.png")
        # self.player_analyst = pygame.image.load("SpaceInvader\\resource\\player_analyst.png")
        self.in_game_bg1 = pygame.image.load("SpaceInvader\\resource\\in_game_bg1.png")
        self.pause_game = pygame.image.load("SpaceInvader\\resource\\game_pause.png")
        self.game_over = pygame.image.load("SpaceInvader\\resource\\game_over.png")

        self.music_bg1 = "SpaceInvader\\resource\\bg_music1.mp3"
        self.music_bg2 = "SpaceInvader\\resource\\bg_music2.mp3"
        self.music_bg3 = "SpaceInvader\\resource\\bg_music3.mp3"
        
        self.explosion_sound = pygame.mixer.Sound("SpaceInvader\\resource\\explosion.wav")
        self.button_click_sound = pygame.mixer.Sound("SpaceInvader\\resource\\button1.mp3")
        # self.button_click_sound.set_volume(0.0)
        self.button_warning_sound = pygame.mixer.Sound("SpaceInvader\\resource\\button_warning.mp3")
        self.game_over_sound = pygame.mixer.Sound("SpaceInvader\\resource\\gameover_sound.mp3")
        self.level_up_sound = pygame.mixer.Sound("SpaceInvader\\resource\\level_up.mp3")
        self.input_font = pygame.font.SysFont('High Tower Text', 60)
        self.display_font = pygame.font.SysFont('Eras Bold ITC', 38)
        self.analyst_title_font = pygame.font.Font("SpaceInvader\\resource\\Zico Inline.ttf", 35)
        self.matplotlib_sans = pygame.font.Font("SpaceInvader\\resource\\matplotlib_sans.ttf", 13)
