# Charles Dieterle
# Single player command-line game of Perudo vs. computers
# See rules.txt for an English language explanation of the rules

import perudo
from time import sleep

def main():

    print("You have started a game of Perudo!\n"\
        "Each player will have five 6-sided dice.\n")
    sleep(1)
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
        print(f"Round {my_game.round}, start!\n")
        sleep(1.5)
        print(f"There are {my_game.dice_count} dice in play, including yours.\n")
        sleep(1.5)
        print(f"You rolled your dice and got: {my_game.players[human].cup}\n")

        if my_game.current_player == human:
            print("You are the first to bet this round.\n")
        else:
            print(f"Player {my_game.current_player + 1} is the first to bet this round.\n")
        sleep(2)

        previous_player = None

        # loop that begins each turn
        while True:
            betting_player = my_game.current_player

            if betting_player == human:
                while True:

                    # get the bet from the human
                    move = get_human_bet(my_game)

                    if type(move) == str:
                        # attempt dudo, loop back to get bet again if invalid
                        if move == "dudo":
                            try:
                                my_game.dudo()
                                break
                            except perudo.MoveError as err:
                                print(f"{err}\n")
                                sleep(2)
                                continue

                        # calza implementation to be added here in the future

                    # attempt the bet, loop back if invalid
                    else:
                        bet_num, bet_total = move[0], move[1]
                        try:
                            my_game.make_bet(bet_num, bet_total)
                            break
                        except perudo.BetError as err:
                            print(err)
                            continue

            # it is not the human's turn, so let a computer bet
            else:
                my_game.make_safest_move()

            # if dudo was called, print the result
            # this block will need significant changes to implement calza
            if my_game.current_bet == None:
                # next_player will start the next round
                next_player = my_game.current_player

                # human player called dudo
                if betting_player == human:

                    # human called dudo and lost, but has dice remaining
                    if next_player == human:
                        print("You called dudo and lost! You lost a die.")

                    # human called dudo and lost their last die, ending the game
                    elif my_game.players[human].cup == []:
                        print("You called dudo and lost!\n"\
                            "You lost your last die. Game Over!")
                        return  # end of game

                    # human called dudo and won
                    else:
                        print("You called dudo and won!")
                        if my_game.players[previous_player].cup == []:
                            print(f"Player {previous_player + 1} lost their last die!\n"\
                                "They were eliminated from the game.\n")
                        else:
                            print(f"Player {previous_player + 1} lost a die.\n")

                    sleep(2)

                # computer player called dudo
                else:
                    # TODO - need to check if previous_player was eliminated first
                    
                    # computer called dudo and lost, but has dice remaining
                    if betting_player == next_player:
                        print(f"Player {betting_player + 1} called dudo and lost!\n"\
                            "They lost one die.\n")

                    # computer called dudo and lost their last die
                    elif my_game.players[betting_player].cup == []:
                        print(f"Player {betting_player + 1} called dudo and lost!\n"\
                            "They lost their last die and were eliminated from the game.\n")

                    # computer player called a dudo and won
                    else:
                        print(f"Player {betting_player + 1} called dudo and won!")

                        # human lost a die but remains in the game
                        if next_player == human:
                            print("You lost a die.\n")

                        # human lost their last die, ending the game
                        elif my_game.players[human].cup == []:
                            print("You lost your last die. Game Over!")
                            return  # end of game

                        # a computer player lost a die but remains in the game
                        elif previous_player == next_player:
                            print(f"Player {previous_player + 1} lost a die.\n")

                        # a computer player lost a die and was eliminated
                        else:
                            print(f"Player {previous_player + 1} lost their last die "\
                                    "and were eliminated from the game.\n")

                    sleep(2)

                # end the current round
                break

            # dudo was not called, so print the bet that was made
            else:
                if betting_player == human:
                    print("You made a bet of:")
                else:
                    print(f"Player {betting_player + 1} made a bet of:")

                print(f"Die Number: {my_game.current_bet.num} and "\
                    f"Quantity: {my_game.current_bet.total}\n")

                # update previous_player for the next turn
                previous_player = betting_player
                sleep(2)

        if my_game.dice_count == len(my_game.players[human].cup):
            print("You are the last player with dice left. Congratulations, you win!")
            return  # end of game


def get_human_bet(game):
    """
    Get a bet from a human player.

    Argument:
        game - perudo.Game object

    Returns either of:
        1. a string indicating dudo or calza
        2. a two-tuple of ints, bet_num and bet_total
    """

    print("It is now your turn!\n")
    sleep(1)

    while True:
        move_type = input("Type 'dudo' to call dudo, or 'bet' to make a bet,\n"\
                    "then hit the Return key.\n")
                    # add calza option once calza is implemented
        move_type = move_type.lower()
        if move_type not in ["bet", "dudo"]:
            print("Your input was invalid. Please try again.")
            continue
        else:
            break

    if move_type == "dudo":
        return "dudo"

    # add case for calza here once calza is implemented

    # the player wants to bet, so get their bet
    else:
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
            if bet_total < 1 or bet_total > game.dice_count:
                print("The quantity must be greater than 0 and less than "\
                        f"or equal to {my_game.dice_count}.")
                continue
            break
        return bet_num, bet_total


if __name__ == "__main__":
    main()
