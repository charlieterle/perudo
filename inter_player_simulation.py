# Charles Dieterle
# Perudo simulator (no human players)
# Plots data about dudo success, relative to dice count ratios between players
# See rules.txt for an English language explanation of the rules

import perudo
from matplotlib import pyplot as plt
import numpy as np
from math import sqrt

def simulator(player_count, num_trials, num_intervals,
                            offensive_cup_sizes, defensive_cup_sizes):
    """
    Plot statistics on dudo calls based on multiple simulated games of Perudo

    Arguments:
        -- player_count (int) - number of players
        -- num_trials (int) - number of games to be simulated
        -- num_intervals (int) - # of intervals on the horizontal axis of plots
        -- offensive_cup_sizes (list of ints) - list of cup sizes to be counted during data collection. For example, passing [1, 2] will only count dudo calls when the offensive player has one or two dice in their cup at the time of calling dudo.
        -- defensive_cup_sizes (list of ints) - same as offensive_cup_sizes, but for the defensive player

    Note: Horizontal axis of plot is a ratio of dice counts, offensive/defensive
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
    correct, incorrect = 0, 0  # counts how many dudo calls were correct

    for i in range(num_intervals):
        predicted.append([])
        actual.append([])

    # run the simulations
    for i in range(num_trials):
        my_game = perudo.Game(player_count)
        defensive_player = None

        while my_game.players_left() > 1:
            betting_player = my_game.current_player
            offensive_cup_len = len(my_game.players[betting_player].cup)
            if defensive_player != None:
                defensive_cup_len = len(my_game.players[defensive_player].cup)

            # This will mutate the state of my_game, including current_player
            safest_move = my_game.make_safest_move()

            # when dudo is called, add data to the predicted/actual lists
            if my_game.current_bet == None:
                ratio = offensive_cup_len / defensive_cup_len

                if offensive_cup_len not in offensive_cup_sizes:
                    continue

                if defensive_cup_len not in defensive_cup_sizes:
                    continue

                bucket = get_bucket(ratio)

                # If dudo was successful, append 1 to appropriate buckets,
                # else append 0
                if betting_player != my_game.current_player or my_game.players[defensive_player].cup == []:
                    actual[bucket].append(1)
                    correct += 1
                else:
                    actual[bucket].append(0)
                    incorrect += 1

                # note: safest_move is the calculated
                # probability of a dudo call succeeding
                predicted[bucket].append(safest_move)

                defensive_player = None

            # in this case, dudo wasn't called, so just go to the next turn
            else:
                defensive_player = betting_player

    for i in range(num_intervals):
        bucket_size = len(actual[i])
        if bucket_size != 0:  # take average of all data points in the bucket
            predicted[i] = sum(predicted[i]) / bucket_size
            actual[i] = sum(actual[i]) / bucket_size

        
        if predicted[i] != []:
            # uncomment following code to print statistics for each bucket
            """
            print(f"Interval number {i} statistics:\n")
            print(f"Predicted success: {predicted[i]:.2f}\n"
                f"Actual success: {actual[i]:.2f}")
            print(f"Sample size: {bucket_size}\n\n")
            """
            # comment out following line if above code is in use
            pass
        else:
            predicted[i], actual[i] = None, None

    # create array of values to act as x-axis markers
    interval_markers = []
    r = min_ratio + step / 2
    for i in range(num_intervals):
        # only plot ratios for which there is actually data
        if predicted[i] != None:
            interval_markers.append(r)
        r += step

    # remove all empty buckets
    while True:
        try:
            predicted.remove(None)
            actual.remove(None)
        except ValueError:
            break

    # plot all collected data
    plt.plot(interval_markers, predicted, "go", label="Predicted dudo success rate")
    plt.plot(interval_markers, actual, "mo", label="Actual dudo success rate")
    plt.axis([min_ratio - .1, max_ratio + .1, -.1, 1.1])
    plt.ylabel("Dudo Success Rate")
    plt.xlabel("Dice Count Ratio between players on a dudo call (Offensive Player:Defensive Player)")
    plt.title("Avg. dudo success rates by dice count ratios between\n" +
            f"the two active players ({num_trials} simulated games)\n" +
            "Dudo dial is a linear value (.09 * dice_ratio - .29)")

    # make linear regression line for the actual dudo success rates
    coef = np.polyfit(interval_markers, actual, 1)
    linreg_func = np.poly1d(coef)
    plt.plot(interval_markers, linreg_func(interval_markers), "--b", label = f"Regression Slope = {coef[0]:.4f}, Intercept = {coef[1]:.3f}")

    # calculate error between predicted and actual dudo rates
    sq_error = 0
    for i in range(len(predicted)):
        sq_error += ((predicted[i] - actual[i]) * 100) ** 2
    print(f"Standard deviation of probability prediction = {sqrt(sq_error / len(predicted)):.2f}")

    # print overall dudo success rate & similar stats 
    print(f"Overall success rate = {(correct * 100 / (correct + incorrect)):.2f}")
    print(f"({correct} correct dudo calls out of {correct + incorrect})")

    # show plot
    plt.legend(loc = "best")
    plt.show()


# simulator(player_count, num_trials, num_intervals,
#           offensive_cup_sizes, defensive_cup_sizes)
simulator(6, 1000, 100, [2, 3, 4, 5], [1, 2, 3, 4, 5])
