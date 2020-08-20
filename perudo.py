# Charles Dieterle
# Perudo gameplay definitions
# See rules.txt for an English language explanation of the rules

import random
from math import factorial

# global constants to declare how many sides per die and dice per player
DIE_SIDES = 6
DICE_PER_PLAYER = 5

# Constant to "dial in" the dudo calls so that their predicted success
# rate is close to their actual success rate
# See probability.txt for a complete explanation.
# This feature will be refined in the future
DUDO_DIAL = .22

class Player():
    """
    A single player in a game of Perudo

    Attributes:
        cup - list of ints representing die rolls
    """

    # players get a cup and 5 dice
    def __init__(self):
        self.cup = []
        for i in range(DICE_PER_PLAYER):
            self.cup.append(random.randint(1, DIE_SIDES))

    # lose one die
    def lose_die(self):
        self.cup.pop()

    # re-roll dice at the start of a new round
    def roll_dice(self):
        for i in range(len(self.cup)):
            self.cup[i] = random.randint(1, DIE_SIDES)

    def __str__(self):
        return str(self.cup)


class Bet():
    """
    A bet in a game of Perudo (a die number and a quantity of dice)

    Attributes:
        num - int representing the die number
        total - int representing the quantity of dice with number num
    """

    # creates a bet in a round of Perudo
    def __init__(self, num, total):
        self.num = num
        self.total = total

    def __str__(self):
        return f"Bet of Number: {self.num} and Quantity: {self.total}"


class Game():
    """
    A game of Perudo

    Attributes:
        players - list of player objects
        current_bet - Bet object representing the current betting state
        current_player - int representing the player whose turn it is
        round - int representing which round of the game it is
        dice_count - int representing how many dice are in play
        move_list - list of (Bet object, probability) pairs
                    where probability is a float
        palifico - bool representing whether palifico rules are in play or not
    """

    # start the game with player_count players
    def __init__(self, player_count):
        self.players = []
        for i in range(player_count):
            self.players.append(Player())
        self.current_bet = None
        self.current_player = random.randint(0, player_count - 1)
        self.round = 1
        self.dice_count = player_count * DICE_PER_PLAYER
        self.move_list = get_all_bets(self.dice_count, \
                            self.get_current_player().cup, None)
        self.palifico = False


    # syntactic sugar for getting the current Player object
    def get_current_player(self):
        return self.players[self.current_player]


    # make a bet
    def make_bet(self, num, total):
        # check for non-sensical bets
        if num < 1 or num > DIE_SIDES:
            raise BetError("ILLEGAL BET: Die number must be between "\
                            f"1 and {DIE_SIDES}.")
        if total > self.dice_count:
            raise BetError("ILLEGAL BET: Dice quantity cannot be greater "\
                            "than the total number of dice in play.")
        if self.current_bet:
            if self.palifico and num != self.current_bet.num:
                raise BetError("ILLEGAL BET: Cannot change the die number "\
                                "of a bet in a palifico round.")

        # make sure the bet is valid in the current bet environment
        if self.current_bet != None:
            current_num = self.current_bet.num
            current_total = self.current_bet.total
            if current_num == 1:
                if num == 1 and total <= current_total:
                    raise BetError("ILLEGAL BET: Must raise either the "\
                                    "bet quantity or the die number.")
                if num > 1 and total <= current_total * 2:
                    raise BetError("ILLEGAL BET: If increasing the die value "\
                                    "from 1, the dice quantity must be "\
                                    f"at least {current_total * 2 + 1}.")
            else:
                if num == 1:
                    if current_total % 2 == 1:
                        ones_total = int(current_total / 2) + 1
                    else:
                        ones_total = int(current_total / 2)
                    if total < ones_total:
                        raise BetError("ILLEGAL BET: If decreasing the die "\
                                        "value to 1, the bet quantity "\
                                        f"must be at least {ones_total}.")
                else:
                    if num < current_num:
                        raise BetError("ILLEGAL BET: Cannot bet on a die "\
                                        "number less than the current bet, "\
                                        "except for 1.")
                    elif total <= current_total and num == current_num:
                        raise BetError("ILLEGAL BET: Must raise either the "\
                                        "bet quantity or the die number.")

        # bet is legal, so change the current_bet for the game
        self.current_bet = Bet(num, total)
        self.set_next_player()
        if self.palifico:
            self.move_list = get_all_bets(self.dice_count,
                                        self.get_current_player().cup,
                                        self.current_bet,
                                        palifico=True)
        else:
            self.move_list = get_all_bets(self.dice_count,
                                        self.get_current_player().cup,
                                        self.current_bet)


    # start a new round
    def start_new_round(self):
        for p in self.players:
            p.roll_dice()
        self.current_bet = None
        self.round += 1
        if self.palifico:
            self.move_list = get_all_bets(self.dice_count,
                                        self.get_current_player().cup,
                                        None,
                                        palifico=True)
        else:
            self.move_list = get_all_bets(self.dice_count,
                                        self.get_current_player().cup,
                                        None)


    # move the current_player index to the next player
    def set_next_player(self):
        if self.current_player == len(self.players) - 1:
            self.current_player = 0
        else:
            self.current_player += 1
        # if current_player is out of the game, go to the next player
        if self.get_current_player().cup == []:
            self.set_next_player()


    # move the current_player index to the previous player
    def set_previous_player(self):
        if self.current_player == 0:
            self.current_player = len(self.players) - 1
        else:
            self.current_player -= 1
        # if current_player is out of the game, go to the previous player
        if self.get_current_player().cup == []:
            self.set_previous_player()


    # returns the number of active players
    def players_left(self):
        count = 0
        for player in self.players:
            if player.cup != []:
                count += 1
        return count


    # call dudo, ending the round, or potentially ending the game
    def dudo(self):
        if self.current_bet == None:
            raise MoveError("Cannot call dudo until a player has bet.")

        # get the current bet, compare it to the actual dice totals
        die_number = self.current_bet.num
        guess_total = self.current_bet.total
        actual_total = 0
        for p in self.players:
            for die in p.cup:
                # if palifico round, 1s aren't wildcard
                if self.palifico:
                    if die == die_number:
                        actual_total += 1
                else:
                    if die == die_number or die == 1:
                        actual_total += 1

        # set palifico to False in case a palifico round just ended
        self.palifico = False

        # make previous player the current player if the bet was incorrect
        if guess_total > actual_total:
            self.set_previous_player()

        losers_cup = self.get_current_player().cup

        # remove one die from the player who lost the bet
        losers_cup.pop()
        self.dice_count -= 1

        # set game to palifico mode if the losing player has just one die left
        if len(losers_cup) == 1:
            players_remaining = 0
            for p in self.players:
                if len(p.cup) > 0:
                    players_remaining += 1
            # palifico rounds only occur when more than 2 players remain
            if players_remaining > 2:
                self.palifico = True

        # if the losing player was eliminated, go to the next player
        if losers_cup == []:
            self.set_next_player()

            # if only one player left, end the game
            if len(self.get_current_player().cup) == self.dice_count:
                self.current_bet = None
                return

        self.start_new_round()


    def print_all_moves(self):
        """
        Print the probability of each possible move succeeding

        The possible moves are:
            - dudo
            - bets by changing the number
                -- bet with num += 1 or more
                    (not possible if num == 6; often multiple bets possible)
                -- bet with num = 1 and total = total / 2, rounding up
            - bet by changing the total (adding 1)
            - bet adding to number and total = total * 2 + 1
                (only available if current bet has num == 1)
        """

        print("Potential moves and probabilities of success:")

        for bet_prob in self.move_list:
            prob = bet_prob[1] * 100
            print(f"{bet_prob[0]}: {prob:.1f}%")


    def make_safest_move(self):
        """
        Make the move with highest probability of success

        Note:
            dudo_dial is used to determine dudo's success, but this feature is
            a work in progress. See a full explanation in probability.txt
        """

        highest_prob = 0
        best_move = None
        for move in self.move_list:
            if move[1] >= highest_prob:
                highest_prob = move[1]
                best_move = move[0]

        if best_move == "Dudo":
            self.dudo()

            # The following line is included for the simulation file to gather
            # data about forecasted dudo success vs. actual dudo success
            return highest_prob

        else:
            self.make_bet(best_move.num, best_move.total)


def get_probability(dice_count, player_cup, a_bet, palifico=False):
    """
    Calculate the probability of a single bet succeeding

    Arguments:
        dice_count - int, the total number of dice in play
        player_cup - list of ints, the current dice values a player has
        current_bet - bet object, with attributes num and total

    Named argument:
        palifico - set to True when palifico rules are in play

    returns a float
    """

    die_num = a_bet.num
    hand_total = 0
    for d in player_cup:
        if d == die_num or d == 1:
            hand_total += 1

    # get values n, r, and p for the formula (see probability.txt for details)
    n = dice_count - len(player_cup)
    r = a_bet.total - hand_total
    # if r < 0, then the bet will always succeed
    if r < 1:
        return 1.000
    if die_num == 1 or palifico:
        p = 1 / DIE_SIDES
    else:
        p = 2 / DIE_SIDES

    total_prob = 0
    while r <= n:
        nCr = factorial(n) / (factorial(r) * factorial(n - r))
        total_prob += nCr * (p ** r) * ((1 - p) ** (n - r))
        r += 1

    return total_prob


def get_all_bets(dice_count, cup, bet_state, palifico=False):
    """
    Retrieve all potential new bets and their probabilities

    Arguments:
        dice_count - an int representing the total number of dice in play
        cup - a list of ints representing the current player's cup
        bet_state - a Bet object

    Named argument:
        palifico - set to True when palifico rules are in play

    returns a list of tuples of form (b, prob),
        where b is a Bet object and prob is a float
    """

    move_list = []

    # if it is the first turn, create an initial betting scenario
    if bet_state == None:

        # initialize quantity at a moderately safe level
        quantity = round(dice_count / DIE_SIDES - 1)

        # in case there are very few dice in play, make the minimum quantity 1
        if quantity <= 0:
            quantity = 1

        # get probability of success for a bet where num = 1
        prob = get_probability(dice_count, cup, Bet(1, quantity))
        move_list.append((Bet(1, quantity), prob))

        # bets for all num > 1
        if not palifico:
            quantity = round(2 * dice_count / DIE_SIDES - 1)
        if quantity <= 0:
            quantity = 1
        for num in range(2, DIE_SIDES + 1):
            prob = get_probability(dice_count, cup, Bet(num, quantity))
            move_list.append((Bet(num, quantity), prob))

        return move_list

    # Now it is not the first turn,
    # so get the next bets with bet_state in mind
    die_number = bet_state.num
    quantity = bet_state.total

    # first, probability of success of dudo
    dudo_prob = 1 - DUDO_DIAL - get_probability(dice_count, cup, bet_state)
    move_list.append(("Dudo", dudo_prob))

    # bet of total += 1. Note: if quantity == dice_count (unlikely),
    # then this bet always has a probability of 0, so it will be skipped.
    if quantity != dice_count:
        prob = get_probability(dice_count, cup, Bet(die_number, quantity + 1))
        move_list.append((Bet(die_number, quantity + 1), prob))

    # In palifico rounds, return here to avoid bets that change the die number
    if palifico:
        return move_list

    # if die_number == 1, get probability of success for all bets where
    # num > 1 and total = total * 2 + 1
    if die_number == 1:
        q = quantity * 2 + 1
        for num in range(2, DIE_SIDES + 1):
            prob = get_probability(dice_count, cup, Bet(num, q))
            move_list.append((Bet(num, q), prob))

        return move_list

    # get probability of success when num = 1 and total = total / 2
    if quantity % 2 == 1:
        q = int((quantity + 1) / 2)
    else:
        q = int(quantity / 2)
    prob = get_probability(dice_count, cup, Bet(1, q))
    move_list.append((Bet(1, q), prob))

    # get probability of success for all bets created by adding to num
    if die_number != DIE_SIDES:
        for num in range(die_number + 1, DIE_SIDES + 1):
            prob = get_probability(dice_count, cup, Bet(num, quantity))
            move_list.append((Bet(num, quantity), prob))

    return move_list


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class BetError(Error):
    """Exception raised when an illegal bet is attempted

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=None):
        self.message = message


class MoveError(Error):
    """Exception raised when an illegal move is attempted
        For example, a dudo call on the first turn of a round

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=None):
        self.message = message
