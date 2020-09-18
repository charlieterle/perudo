# Charles Dieterle
# Perudo simulator (no human players)
# Plots data about dudo success, relative to dice count ratios between players
# See rules.txt for an English language explanation of the rules

import perudo
from matplotlib import pyplot as plt
import numpy as np

def simulator(player_count, num_trials, num_intervals,
                            offensive_cup_sizes, defensive_cup_sizes):
    """
    Plot statistics on dudo calls based on multiple simulated games of Perudo

    Arguments:
        player_count (int) - number of players
        num_trials (int) - number of games to be simulated
        num_intervals (int) - determines how many intervals to include on the
            horizontal axis of the plots.
        offensive_cup_sizes (list of ints) - list of cup sizes that you want to be
            counted during data collection. For example, passing [1, 2] will
            only count dudo calls when the offensive player has one or
            two dice in their cup at the time of calling dudo.
        defensive_cup_sizes (list of ints) - same as offensive_cup_sizes, but for
            the defensive player

    Note: Plots will have a horizontal axis related to ratio of dice counts
        between players
    """

    dice_per_player = perudo.DICE_PER_PLAYER

    # this is the min possible ratio of one player's dice to another's
    min_ratio = 1 / dice_per_player
    max_ratio = dice_per_player

    ratio_diff = max_ratio - min_ratio
    step = ratio_diff / num_intervals

    # The data will be grouped on the x axis by ratios of dice counts.
    # Therefore, it's necessary to convert the ratios into integer bucket
    # numbers that represent ranges of ratios. These buckets will be used as
    # index numbers for lists that gather the data.
    def get_bucket(ratio):
        """
        Get the appropriate bucket number from a given ratio

        If the ratio is min_ratio, the bucket is 0, and if it is max_ratio,
        the bucket is num_intervals - 1. The range of each bucket is
        the value of the variable step, which is ratio_diff / num_intervals
        """
        if ratio == max_ratio:
            return num_intervals - 1
        else:
            return int((ratio - min_ratio) / step)

    # The lists below will each have num_intervals empty-list elements, into
    # which the predicted rates of dudo and actual dudo outcomes will be placed
    # based on the ratio of dice counts between players
    predicted, actual = [], []

    for i in range(num_intervals):
        predicted.append([])
        actual.append([])

    # start the simulation
    for i in range(num_trials):
        my_game = perudo.Game(player_count)
        defensive_player = None

        # Use the dice_count code on the following line to manipulate how
        # large the game is when data is collected (i.e. total dice count)
        while my_game.players_left() > 1:
            betting_player = my_game.current_player
            offensive_cup_len = len(my_game.players[betting_player].cup)
            if defensive_player != None:
                defensive_cup_len = len(my_game.players[defensive_player].cup)

            # This will mutate the state of my_game, including current_player
            safest_move = my_game.make_safest_move()

            # when dudo is called, add data to the lists declared above
            if my_game.current_bet == None:
                ratio = offensive_cup_len / defensive_cup_len

                if offensive_cup_len not in offensive_cup_sizes:
                    continue

                if defensive_cup_len not in defensive_cup_sizes:
                    continue

                bucket = get_bucket(ratio)

                # If dudo was successful, append 1 to appropriate buckets,
                # else append 0
                if betting_player != my_game.current_player or  \
                                    my_game.players[defensive_player].cup == []:
                    actual[bucket].append(1)
                else:
                    actual[bucket].append(0)

                # note: safest_move is the calculated
                # probability of a dudo call succeeding
                predicted[bucket].append(safest_move)

                defensive_player = None

            # in this case, dudo wasn't called, so just go to the next turn
            else:
                defensive_player = betting_player

    for i in range(num_intervals):
        bucket_size = len(actual[i])
        if bucket_size != 0:
            predicted[i] = sum(predicted[i]) / bucket_size
            actual[i] = sum(actual[i]) / bucket_size

        if predicted[i] != []:
            print(f"Interval number {i} statistics:\n")
            print(f"Predicted success: {predicted[i]:.2f}\n"
                f"Actual success: {actual[i]:.2f}")
            print(f"Sample size: {bucket_size}\n\n")
        else:
            predicted[i], actual[i] = None, None

    # create array of values to act as x-axis markers
    interval_markers = []
    r = min_ratio + step / 2
    for i in range(num_intervals):
        interval_markers.append(r)
        r += step

    # make linear regression line for the actual dudo success rates
    # coef = np.polyfit(interval_markers, actual, 1)
    # linreg_func = np.poly1d(coef)
    # plt.plot(interval_markers, linreg_func(interval_markers), "--b")

    # plot all collected data and linear regression line
    plt.plot(interval_markers, predicted, "go",  \
        label = "Predicted success rate")
    plt.plot(interval_markers, actual, "mo",  \
        label = "Actual success rate")
    plt.axis([min_ratio - .1, max_ratio + .1, -.1, 1.1])
    plt.ylabel("Dudo Success Rate")
    plt.xlabel("Dice Count Ratio between players (Offensive Player:Defensive Player)")
    plt.title("Dudo success rates grouped by dice count\n" +
            "ratios between the two players involved\n" +
            "(All Dice counts except Offensive Player w/ 1 die)")
    plt.legend(loc = "best")
    plt.show()


# simulator(player_count, num_trials, num_intervals,
#           offensive_cup_sizes, defensive_cup_sizes)
# NOTE due to the linear regression line, this function may not work with
# values of num_intervals that are greater than 5. I will work to fix this ASAP
simulator(6, 300, 100, [2, 3, 4, 5], [1, 2, 3, 4, 5])
