# Charles Dieterle
# Perudo simulator (no human players)
# See rules.txt for an English language explanation of the rules

import perudo

def single_game(player_count):
    """
    Simulate a single game of Perudo

    Arguments:
        player_count (int) - number of players

    Return the following statistics:
        - Fraction of dudo calls that were correct (i.e., the bet was wrong)
        - Avg calculated probability of dudo success
        - Avg number of bets per round
    """

    my_game = perudo.Game(player_count)
    successful_dudos = 0
    dudo_prob_sum = 0
    total_bets = 0
    rounds = 0

    # need to keep track of previous player to get accurate dudo measurement
    previous_player = None

    while my_game.players_left() > 1:
        betting_player = my_game.current_player
        safest_move = my_game.make_safest_move()

        if type(safest_move) == float:
            dudo_prob_sum += safest_move
            rounds += 1
            if betting_player != my_game.current_player and  \
            my_game.players[previous_player].cup != []:
                successful_dudos += 1
            previous_player = None

        else:
            total_bets += 1
            previous_player = betting_player

    return successful_dudos / rounds, dudo_prob_sum / rounds, total_bets / rounds

def simulator(player_count, num_trials):
    """
    Simulate multiple games of Perudo

    Arguments:
        player_count (int) - number of players in the game
        num_trials (int) - number of games simulated

    Print the following statistics:
        - Actual success rate of dudo calls
        - Calculated success rate of dudo calls
        - Avg number of bets per round of play
    """

    dudo_actual = []
    dudo_calculations = []
    bet_numbers = []

    for i in range(num_trials):
        dudo_fraction, dudo_calculated, bet_num = single_game(player_count)
        dudo_actual.append(dudo_fraction)
        dudo_calculations.append(dudo_calculated)
        bet_numbers.append(bet_num)

    print(f"Actual dudo success rate: {sum(dudo_actual) / num_trials}\n" \
        f"Calculated dudo success rate: {sum(dudo_calculations) / num_trials}\n" \
        f"Avg number of bets per round: {sum(bet_numbers) / num_trials}")

# change the arguments below to desired player count and number of games
simulator(6, 1000)