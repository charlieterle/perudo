# Charles Dieterle
# Perudo simulator (no human players)
# See rules.txt for an English language explanation of the rules

import perudo
from matplotlib import pyplot as plt

def simulator(player_count, num_trials, num_intervals):
    """
    Plot statistics on dudo calls based on multiple simulated games of Perudo

    Arguments:
        player_count (int) - number of players
        num_trials (int) - number of games to be simulated
        num_intervals (int) - determines how many intervals to include on the
            horizontal axis of the plots.

    Note: All plots will have a horizontal axis related to the players'
    individual dice counts and the game's total dice count
    """

    my_game = perudo.Game(player_count)
    dice_per_player = perudo.DICE_PER_PLAYER

    # this is the min possible ratio of one's own dice to total dice in play.
    min_ratio = 1 / (dice_per_player * (player_count - 1) + 1)

    # this is the max possible ratio of one's own dice to total dice in play.
    max_ratio = dice_per_player/(dice_per_player + 1)

    ratio_diff = max_ratio - min_ratio
    step = ratio_diff / num_intervals

    # The data will be divided according to player's dice to total dice ratios.
    # Therefore, it's necessary to convert the ratios into bucket numbers to
    # populate the lists of data.
    def get_bucket(ratio):
        """
        Get the appropriate bucket number from a given ratio

        If the ratio is min_ratio, the bucket is 0, and if it is max_ratio,
        the bucket is num_intervals - 1. The range of each bucket is step, which
        was declared above.
        """
        if ratio = max_ratio:
            return num_intervals - 1
        else:
            return int((ratio - min_ratio) / step)

    # The lists below will each have num_intervals lists (buckets), into which
    # the predicted rates of dudo and actual dudo outcomes will be placed,
    # based on the ratio of dice in the player's cup to the total number of
    # dice in play.
    previous_predicted, previous_actual = [], []
    current_predicted, current_actual = [], []

    for i in range(num_intervals):
        previous_predicted.append([])
        previous_actual.append([])
        current_predicted.append([])
        current_actual.append([])

    # start the simulation
    for i in range(num_trials):
        previous_player = None
        while my_game.players_left() > 1:
            current_player = my_game.current_player
            current_cup_len = len(my_game.players[betting_player].cup)
            if previous_player != None:
                previous_cup_len = len(my_game.players[previous_player].cup)

            safest_move = my_game.make_safest_move()

            # when dudo is called, add data to the lists declared above
            if my_game.current_bet == None:
                total_dice_count = my_game.dice_count
                previous_ratio = previous_cup_len / total_dice_count
                current_ratio = current_cup_len / total_dice_count

                previous_bucket = get_bucket(previous_ratio)
                current_bucket = get_bucket(current_ratio)
                #   TODO FROM HERE
                if betting_player != my_game.current_player or  \
                                    my_game.players[previous_player].cup == []:
                    append somehting 1
                else:
                    append somethi 0
                dice_counts.append(my_game.dice_count)
                betting_cups.append(betting_cup_len)
                previous_cups.append(previous_cup_len)
                probs.append(safest_move) # note: safest_move is the calculated
                                        # probability of a dudo call succeeding

                previous_player = None

            # in this case, dudo wasn't called, so just go to the next turn
            else:
                previous_player = betting_player

    betting_ratios


    for i in range(len(dudos)):





# change the arguments below to desired player count and number of games
simulator(6, 100, 50)


# basic usage of pyplot
"""
plt.plot(x, y, "bo", label = "Observed temperature")
plt.plot(x, estY, "r-",
         label = "Modeled temperature, " + "r^2 = " + str(r_squared(y, estY)))
plt.ylabel("High Temperature")
plt.xlabel("Year")
plt.title("Regression model and observed data of high temps \n" +
          "in Boston on date Jan 10 from 1961 to 2005")
plt.legend(loc = "best")
plt.show()
"""
