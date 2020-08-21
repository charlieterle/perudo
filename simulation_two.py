# Charles Dieterle
# Perudo simulator (no human players)
# See rules.txt for an English language explanation of the rules


import perudo
from matplotlib import pyplot

def single_game(player_count):
    """
    Simulate a single game of Perudo and returns related data

    Arguments:
        player_count (int) - number of players

    Returns:
        dudos - list of bools (True for successful dudo call, False for failure)
        dice_counts - list of ints (total number of dice in play in the game)
        betting_cups - list of ints (num of dice in the betting player's cup)
        previous_cups - list of ints (num of dice in the previous player's cup)
    """

    my_game = perudo.Game(player_count)
    dudos, dice_counts, previous_cups, betting_cups = [], [], [], []

    # start the simulation
    previous_player = None
    while my_game.players_left() > 1:
        betting_player = my_game.current_player
        bet_cup_len = len(my_game.players[betting_player].cup)
        if previous_player != None:
            prev_cup_len = len(my_game.players[previous_player].cup)
        safest_move = my_game.make_safest_move()

        # when dudo is called, add data to the lists declared above
        if my_game.current_bet == None:
            if betting_player != my_game.current_player or  \
                                my_game.players[previous_player].cup == []:
                dudos.append(True)
            else:
                dudos.append(False)

            dice_counts.append(my_game.dice_count)
            betting_cups.append(bet_cup_len)
            previous_cups.append(prev_cup_len)

            previous_player = None

        # in this case, dudo wasn't called, so just continue to the next turn
        else:
            previous_player = betting_player

    return dudos, dice_counts, betting_cups, previous_cups

def simulator(player_count, num_trials):
    """
    Simulate multiple games of Perudo

    Arguments:
        player_count (int) - number of players in the game
        num_trials (int) - number of games simulated

    Return the following statistics:
        - Avg fraction of dudo calls that were correct
        - Avg number of bets per round
        - Avg number of rounds per game
    """

    dudos, dice_counts, previous_cups, betting_cups = [], [], [], []

    for i in range(num_trials):
        one_game = single_game(player_count)
        dudos.extend(one_game[0])
        dice_counts.extend(one_game[1])
        betting_cups.extend(one_game[2])
        previous_cups.extend(one_game[3])

    # this is the minimum ratio of one's own dice to total dice in play.
    # this occurs when the player has 1 die left, and everyone else has 5
    min_ratio = 1 / (perudo.DICE_PER_PLAYER * player_count - 4)

    # this is the maximum ratio of one's own dice to total dice in play.
    # this occurs when the player has 5 dice, and the only remaining opponent
    # has 1 die left
    max_ratio = 5/6



# change the arguments below to desired player count and number of games
simulator(6, 10)


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
