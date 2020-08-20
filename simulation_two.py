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
        dudo_list - list of 3-tuples of the form (dudo, dice_count, cup_size) where:
            - dudo is a bool representing the success of that particular dudo call
                (True is success, False is failure)
            - dice_count is the total number of dice in play in the game
            - cup_size is the number of dice in the previous player's cup

    """

    my_game = perudo.Game(player_count)
    dudo_list = []

    # start the simulation
    previous_player = None
    while my_game.players_left() > 1:
        betting_player = my_game.current_player
        safest_move = my_game.make_safest_move()

        # add a data point to dudo_list
        if my_game.current_bet == None:
            if betting_player != my_game.current_player or  \
                                my_game.players[previous_player].cup == []:
                dudo_list.append((True, my_game.dice_count,  \
                                len(my_game.players[previous_player].cup)))
            else:
                dudo_list.append((False, my_game.dice_count,  \
                                len(my_game.players[previous_player].cup)))
            previous_player = None
        else:
            previous_player = betting_player

    return dudo_list

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

    dudo_actual = []
    dudo_calculations = []
    bet_numbers = []

    for i in range(num_trials):
        dudo_fraction, dudo_calculated, bet_num = single_game(player_count)
        dudo_actual.append(dudo_fraction)
        dudo_calculations.append(dudo_calculated)
        bet_numbers.append(bet_num)

    

# change the arguments below to desired player count and number of games
simulator(6, 100)


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
