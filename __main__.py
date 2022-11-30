import argparse
from kink import inject, di
from SpaceInvader.game_gui import GameGui


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-db_init")
    db_init = parser.parse_args().db_init
    di["dbinit"] = db_init
    di["db_name"] = "gamerepository.db"
    game = GameGui()
    game.play()