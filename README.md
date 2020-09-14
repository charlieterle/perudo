# Perudo

Implementation of the dice game Perudo (AKA Liar's Dice), along with a game simulator and other files.

How to play:

1. Read rules.txt for an explanation of the game rules

2. After downloading play.py and perudo.py (into the same directory), run play.py in a terminal window using Python 3

Other files:

  - move_probability.py: computes and prints the probability of success of all possible moves on a given turn of Perudo. You can use this file while playing Perudo (either with computers or humans.) Each time your turn comes up, run the file with Python 3 in a terminal window. Make sure perudo.py is in the same directory.
  
  - simulation.py: simulates multiple games of Perudo using all computer players, and prints statistics from the simulations.
  
  - dice_ratio_simulation.py: creates two plots that display the average calculated and average actual success rates of dudo calls. The first plot shows the relationship between dudo success and the dice ratio between the defensive (previous) player and the entire game. The second plot uses the ratio between the offensive (current) player) and the entire game.
  
  - inter_player_simulation.py: creates a plot that displays the average calculated and average actual success rates of dudo calls. The plot shows the relationship between dudo success and the dice ratio between the offensive (current) player and the defensive (previous) player.
  
I am planning to include an option to play with "calza" rules at a later date. See rules.txt for an explanation of calza.

# Dudo Dial

  - the dudo_dial feature is currently implemented to aid computer players in calculating the correct probability of dudo calls succeeding, but it doesn't work well in all situations. Most notably, it does not currently take into account that the previous player's bet was made with the previous player's cup of dice in mind, and therefore is likely to reflect which dice the previous player has. Therefore, I am currently studying how the probabilities can be tweaked so that the computer players make smarter moves. I will post graphs with data on this topic soon.
