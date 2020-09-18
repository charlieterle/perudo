# Charles Dieterle
# Perudo simulator (no human players)
# Plots data about dudo success, relative to players' dice counts
# See rules.txt for an English language explanation of the rules

import perudo
from matplotlib import pyplot as plt

def simulator(player_count, num_trials, num_intervals, cup_sizes):
    """
    Plot statistics on dudo calls based on multiple simulated games of Perudo

    Creates two plots:
        1. The predicted success of dudo and the actual success of dudo, grouped
            by the ratio of dice counts between the defensive player and the
            whole table
        2. The same as the other plot, except using the dice count of the
            offensive player

    Arguments:
        player_count (int) - number of players
        num_trials (int) - number of games to be simulated
        num_intervals (int) - determines how many intervals to include on the
            horizontal axis of the plots.
        cup_sizes (list of ints) - list of cup sizes that you want to be counted
            during data collection. For example, passing [1, 2] will only
            count dudo calls when the previous or current player had one or
            two dice in their cup at the time.

    Note: Plots will have a horizontal axis related to ratio between the
        dice count of individual players and the dice count of the entire game
    """

    dice_per_player = perudo.DICE_PER_PLAYER

    # this is the min possible ratio of one's own dice to total dice in play.
    min_ratio = 1 / (dice_per_player * (player_count - 1) + 1)

    # this is the max possible ratio of one's own dice to total dice in play.
    max_ratio = dice_per_player/(dice_per_player + 1)

    ratio_diff = max_ratio - min_ratio
    step = ratio_diff / num_intervals

    # The data will be divided according to player's dice to total dice ratios.
    # Therefore, it's necessary to convert the ratios into integer bucket
    # numbers that represent ranges of ratios.
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
        my_game = perudo.Game(player_count)
        previous_player = None
        while my_game.players_left() > 1:
            total_dice_count = my_game.dice_count
            betting_player = my_game.current_player
            current_cup_len = len(my_game.players[betting_player].cup)
            if previous_player != None:
                previous_cup_len = len(my_game.players[previous_player].cup)

            # This will update the state of my_game, including current_player
            # When a dudo is called, make_safest_move returns a float that
            # represents the calculated probability of success of that call.
            safest_move = my_game.make_safest_move()

            # when dudo is called, add data to the lists declared above
            if my_game.current_bet == None:
                previous_ratio = previous_cup_len / total_dice_count
                current_ratio = current_cup_len / total_dice_count

                previous_bucket = get_bucket(previous_ratio)
                current_bucket = get_bucket(current_ratio)

                # If dudo was successful, append 1 to appropriate buckets,
                # else append 0
                if betting_player != my_game.current_player or  \
                                    my_game.players[previous_player].cup == []:
                    if previous_cup_len in cup_sizes:
                        previous_actual[previous_bucket].append(1)
                        previous_predicted[previous_bucket].append(safest_move)
                    if current_cup_len in cup_sizes:
                        current_actual[current_bucket].append(1)
                        current_predicted[current_bucket].append(safest_move)
                else:
                    if previous_cup_len in cup_sizes:
                        previous_actual[previous_bucket].append(0)
                        previous_predicted[previous_bucket].append(safest_move)
                    if current_cup_len in cup_sizes:
                        current_actual[current_bucket].append(0)
                        current_predicted[current_bucket].append(safest_move)

                previous_player = None

            # in this case, dudo wasn't called, so just go to the next turn
            else:
                previous_player = betting_player

    # Prepare the gathered data to be plotted
    # by taking the average of each sub-list
    for i in range(num_intervals):
        previous_bucket_size = len(previous_actual[i])
        # If the list is empty, there were no dudo calls in that ratio range,
        # and therefore no data.
        if previous_bucket_size != 0:
            previous_predicted[i] = sum(previous_predicted[i]) / previous_bucket_size
            previous_actual[i] = sum(previous_actual[i]) / previous_bucket_size

        current_bucket_size = len(current_actual[i])
        if current_bucket_size != 0:
            current_predicted[i] = sum(current_predicted[i]) / current_bucket_size
            current_actual[i] = sum(current_actual[i]) / current_bucket_size

        if previous_predicted[i] != [] and current_predicted [i] != []:
            print(f"Interval number {i} statistics:\n")

        if previous_predicted[i] != []:
            print(f"Previous player predicted success: {previous_predicted[i]:.2f}\n"
                f"Previous player actual success: {previous_actual[i]:.2f}")
            print(f"sample size: {previous_bucket_size}")
        else:
            # Don't plot the ratios for which there is no data
            previous_predicted[i], previous_actual[i] = None, None
        if current_predicted[i] != []:
            print(f"Current player predicted success: {current_predicted[i]:.2f}\n"
                f"Current player actual success: {current_actual[i]:.2f}")
            print(f"sample size: {current_bucket_size}\n")
        else:
            current_predicted[i], current_actual[i] = None, None

    # create array of values to act as x-axis markers
    interval_markers = []
    r = min_ratio + step / 2
    for i in range(num_intervals):
        interval_markers.append(r)
        r += step

    # First plot - only plot data for previous player's dice ratios
    plt.plot(interval_markers, previous_predicted, "bo",  \
        label = "Avg. Predicted success rate of dudo")
    plt.plot(interval_markers, previous_actual, "ro",  \
        label = "Avg. Actual success rate of dudo")
    plt.axis([min_ratio, max_ratio, -.1, 1.1])
    plt.ylabel("Success Rate")
    plt.xlabel("Approximate Dice Count Ratio of Previous Player to Whole Table")
    plt.title("Success rate of dudo calls with respect to the\n" +
            "dice count ratio of the previous player to the whole table")
    plt.legend(loc = "best")
    plt.show()

    # Second plot - only plot data for current player's dice ratios
    plt.plot(interval_markers, current_predicted, "bo",  \
        label = "Avg. Predicted success rate of dudo")
    plt.plot(interval_markers, current_actual, "ro",  \
        label = "Avg. Actual success rate of dudo")
    plt.axis([min_ratio, max_ratio, -.1, 1.1])
    plt.ylabel("Success Rate")
    plt.xlabel("Approximate Dice Count Ratio of Current Player to Whole Table")
    plt.title("Success rate of dudo calls with respect to the\n" +
            "dice count ratio of the current player to the whole table\n")
    plt.legend(loc = "best")
    plt.show()


# simulator(player_count, num_trials, num_intervals, cup_sizes)
simulator(6, 1000, 200, [1, 2, 3, 4, 5])
