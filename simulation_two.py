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
        while my_game.players_left() > 1 and my_game.dice_count > 3:
            total_dice_count = my_game.dice_count
            betting_player = my_game.current_player
            current_cup_len = len(my_game.players[betting_player].cup)
            if previous_player != None:
                previous_cup_len = len(my_game.players[previous_player].cup)

            # This will mutate the state of my_game, including current_player
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
                    previous_actual[previous_bucket].append(1)
                    current_actual[current_bucket].append(1)
                else:
                    previous_actual[previous_bucket].append(0)
                    current_actual[current_bucket].append(0)

                # note: safest_move is the calculated
                # probability of a dudo call succeeding
                previous_predicted[previous_bucket].append(safest_move)
                current_predicted[current_bucket].append(safest_move)

                previous_player = None

            # in this case, dudo wasn't called, so just go to the next turn
            else:
                previous_player = betting_player

    # REMOVE THIS LINE LATER
    print(f"dudo dial = {perudo.DUDO_DIAL}")

    for i in range(num_intervals):
        previous_bucket_size = len(previous_actual[i])
        if previous_bucket_size != 0:
            previous_predicted[i] = sum(previous_predicted[i]) / previous_bucket_size
            previous_actual[i] = sum(previous_actual[i]) / previous_bucket_size

        current_bucket_size = len(current_actual[i])
        if current_bucket_size != 0:
            current_predicted[i] = sum(current_predicted[i]) / current_bucket_size
            current_actual[i] = sum(current_actual[i]) / current_bucket_size

        print(f"Interval number {i} statistics:\n")

        if previous_predicted[i] != []:
            print(f"Previous player predicted success: {previous_predicted[i]:.2f}\n"
                f"Previous player actual success: {previous_actual[i]:.2f}")
            print(f"sample size: {previous_bucket_size}")
        else:
            previous_predicted[i], previous_actual[i] = 0, 0
        if current_predicted[i] != []:
            print(f"Current player predicted success: {current_predicted[i]:.2f}\n"
                f"Current player actual success: {current_actual[i]:.2f}")
            print(f"sample size: {current_bucket_size}\n")
        else:
            current_predicted[i], current_actual[i] = 0, 0

    # create array of values to act as x-axis markers
    interval_markers = []
    r = min_ratio
    for i in range(num_intervals):
        interval_markers.append(r)
        r += step

    plt.plot(interval_markers, previous_predicted, "bo",  \
        label = "Predicted success rate of dudo with previous player ratio")
    plt.plot(interval_markers, previous_actual, "ro",  \
        label = "Actual success rate of dudo with previous player ratio")
    plt.ylabel("Success Rate")
    plt.xlabel("Lower Bound of Interval")
    plt.title("Predicted success rate vs actual success rate of dudo calls \n" +
            "for a given dice ratio of the previous player")
    plt.legend(loc = "best")
    plt.show()


# simulator(player_count, num_trials, num_intervals)
simulator(6, 5000, 20)
