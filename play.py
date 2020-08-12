# Charles Dieterle
# Single player command-line game of Perudo vs. computers
# See rules.txt for an English language explanation of the rules

import perudo
from time import sleep

def main():

    # get the total dice count and the number of dice in the player's cup
    while True:
        try:
            player_count = int(input("How many computer players do you " \
                                    "want to play against?\n"))
        except ValueError:
            print("You must enter a numeric value.")
            continue
        if player_count < 1:
            print("You must enter positive integers only.")
            continue
        break

    # start a game
    my_game = perudo.Game(player_count + 1)

    # assign human player to the highest player number
    human = player_count

    # loop that begins every round of play
    while True:
        print(f"Round {my_game.round}, start!")
        sleep(1)
        print(f"Your cup: {my_game.players[human]}")
        sleep(3)

        # get first bet if human is first
        if my_game.current_player == human:
            print("You are the first to bet this round.")
            bet_num, bet_total = get_human_bet(my_game)
            while True:
                confirm_bet = input(f"You input a bet of Die Number: {bet_num}"\
                                    f" and Quantity: {bet_total}.\n"\
                                    "Is this correct? "
                                    "Enter 'y' for yes, 'n' for no.\n")

                if confirm_bet not in ["y", "n", "Y", "N"]:
                    print("You must enter either 'y' or 'n'")
                    continue

                # get bet from human again if they want to re-input
                if confirm_bet in ['n', 'N']:
                    print("Please re-enter your bet.")
                    bet_num, bet_total = get_human_bet(my_game)
                    continue

                else:
                    CHECK IF BET IS LEGAL
                    break

            # TODO


        # get first bet if human is not first
        else:
            print(f"First to bet is player {my_game.current_player + 1}.")
        while
        if my_game.current_player == human:


def get_human_bet(game):
    """
    Get a bet from a human player.

    Argument:
        game - perudo.Game object

    Return two ints, the bet num and the bet total
    """
    while True:
        try:
            bet_num = int(input("Enter the die value of your bet:\n"))
        except ValueError:
            print("You must enter a number.")
            continue
        if bet_num < 1 or bet_num > perudo.DIE_SIDES:
            print("The die value must be greater than 0 and less than "\
                    f"or equal to {perudo.DIE_SIDES}.")
            continue
        break
    while True:
        try:
            bet_total = int(input("Enter the quantity of your bet:\n"))
        except ValueError:
            print("You must enter a number.")
            continue
        if bet_total < 1 or bet_total > my_game.dice_count:
            print("The quantity must be greater than 0 and less than "\
                    f"or equal to {my_game.dice_count}.")
            continue
        break
    return bet_num, bet_total

def check_bet(game, bet):
    """
    Check if a bet is legal in a game.

    Arguments:
        game - perudo.Game object
        bet - perudo.Bet object

    Return True if legal, False if illegal
    """
