# Charles Dieterle
# Command-line program to give the probabilities for each possible move
# for a given game state of Perudo.
# See rules.txt for an English language explanation of the rules

import perudo

def main():
    """
    Print the probabilities of potential moves on a single turn of Perudo
    """

    # get the total dice count and the number of dice in the player's cup
    while True:
        try:
            total_dice_count = int(input("How many dice are in play, "\
                            "including yours?\n"))
            your_dice_count = int(input("How many dice are in your own cup?\n"))
        except ValueError:
            print("You must enter a numeric value.")
            continue
        if total_dice_count < 1 or your_dice_count < 1:
            print("You must enter positive integers only.")
            continue
        break

    # get all of the die values in current player's cup
    first_attempt = True
    while True:
        if first_attempt:
            print("Enter the die value of each of your dice, one by one:")
        else:
            print("Please re-enter the value of each die, one by one:")
        cup = []
        for i in range(your_dice_count):
            try:
                die = int(input())
            except ValueError:
                print("You must enter a number.")
                first_attempt = False
                break
            cup.append(die)
        # make sure all die values were entered
        if len(cup) != your_dice_count:
            continue
        # make sure all die values are valid
        if all(val > 0 and val <= perudo.DIE_SIDES for val in cup):
            break
        else:
            print("All die values must be greater than 0 and less than "\
                    f"or equal to {perudo.DIE_SIDES}.")
            first_attempt = False
            continue

    # Determine whether bet exists, and if so, get the quantity and die number
    while True:
        bet_exists = input("Is there a bet in play already? "\
                            "Enter 'y' for yes, 'n' for no.\n")
        if bet_exists not in ["y", "n", "Y", "N"]:
            print("You must enter either 'y' or 'n'")
            continue
        if bet_exists == "n" or bet_exists == "N":
            bet = None
            break
        else:
            # Get info about current bet
            while True:
                try:
                    bet_num = int(input("What is the die value of the "\
                                        "bet in play?\n"))
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
                    bet_total = int(input("What is the dice quantity of the "\
                                            "bet in play?\n"))
                except ValueError:
                    print("You must enter a number.")
                    continue
                if bet_total < 1 or bet_total > total_dice_count:
                    print("The quantity must be greater than 0 and less than "\
                            f"or equal to {total_dice_count}.")
                    continue
                break
            bet = perudo.Bet(bet_num, bet_total)
            # Get dice count of previous player
            while True:
                try:
                    previous_dice_count = int(input("How many dice are in the "\
                                    "previous player's cup?\n"))
                except ValueError:
                    print("You must enter a numeric value.")
                    continue
                if previous_dice_count < 1:
                    print("You must enter positive integers only.")
                    continue
                break
            break

    # Get dice count of next player
    while True:
        try:
            next_dice_count = int(input("How many dice are in the next player's "\
                                    "cup?\n"))
        except ValueError:
            print("You must enter a numeric value.")
            continue
        if next_dice_count < 1:
            print("You must enter positive integers only.")
            continue
        break

    # Determine whether palifico or not
    while True:
        palifico = input("Is it a Palifico round? "\
                            "Enter 'y' for yes, 'n' for no.\n")
        if palifico not in ["y", "n", "Y", "N"]:
            print("You must enter either 'y' or 'n'")
            continue
        if palifico in ["n", "N"]:
            palifico = False
            break
        else:
            palifico = True
            break

    move_list = perudo.get_all_bets(total_dice_count, previous_dice_count,  \
                                    next_dice_count, cup, bet, palifico)

    print("Potential moves and probabilities of success:")

    for bet_prob in move_list:
        prob = bet_prob[1] * 100
        if type(bet_prob[0]) == str:
            print(f"{bet_prob[0]}: {bet_prob[1]}")
        else:
            print(f"Bet of Number {bet_prob[0].num} and",
                  f"Quantity {bet_prob[0].total}: {prob:.1f}%")

if __name__ == "__main__":
    main()
