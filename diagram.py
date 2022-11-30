import matplotlib.pyplot as plt
from kink import inject, di
import numpy as np

from game_repository import GameRepository

di["dbinit"] = "False"
di["db_name"] = "gamerepository.db"
repository = GameRepository()
score_list = np.array(repository.get_user_score_history("jelia"))
print(score_list)
# number of employees of A
game = np.array(range(1,len(score_list)+1))
my_dpi = 92
plt.figure(figsize=(434/my_dpi, 300/my_dpi), dpi=my_dpi)
plt.rc('axes',edgecolor='white')
plt.rcParams.update({'font.size':10})
# plot a line chart
plt.plot(game, score_list, 'o--b')
# set axis titles
plt.xlabel("game",color = "w")
plt.ylabel("score",color = "w")
# set chart title
plt.title("Score Plot",color = "w")
plt.savefig("SpaceInvader\\ScorePlot.png",transparent=True,format="png")
plt.show()