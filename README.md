# Perudo

Implementation of the dice game Perudo (AKA Liar's Dice), along with a game simulator and other files.

How to play:

1. Read rules.txt for an explanation of the game rules

2. After downloading play.py and perudo.py (into the same directory), run play.py in a terminal window using Python 3

Files unrelated to gameplay:

  - move_probability.py: computes and prints the probability of success of all possible moves on a given turn of Perudo. You can use this file while playing Perudo (either with computers or humans.) Each time your turn comes up, run the file with Python 3 in a terminal window. Make sure perudo.py is in the same directory.
  
  - simulation.py: simulates multiple games of Perudo using all computer players, and prints statistics from the simulations.
  
  - dice_ratio_simulation.py: creates two plots that display the average calculated and average actual success rates of dudo calls. The first plot shows the relationship between dudo success and the dice ratio between the defensive (previous) player and the entire game. The second plot uses the ratio between the offensive (current) player) and the entire game.
  
  - inter_player_simulation.py: creates a plot that displays the average calculated and average actual success rates of dudo calls. The plot shows the relationship between dudo success and the dice ratio between the offensive (current) player and the defensive (previous) player.
  
I am planning to include an option to play with "calza" rules at a later date. See rules.txt for an explanation of calza.

# Dudo Dial

  The dudo dial feature was originally implemented as a constant adjustment to the estimated probability of success of calling dudo in the game. I implemented this because I noticed that the predicted success rate of dudo calls by computer players was around 60% on average, but in reality those calls only succeeded 40-45% of the time. Without a good understanding of why this was, I pushed out a quick fix by just testing out a bunch of constant values until I found out that got the average predicted success rates close to the average actual success rates.
  
  I knew this was a crude approach at the time, because the computers were not taking into account how many dice their neighboring players had. They were only using the total number of dice in the game to predict the chances of success of a dudo call. So, I created another simulation file (inter_player_simulation.py) to track dudo successes relative to the number of dice in neighboring player's hands. There are many graphs from this file in the simulation_graphs directory that use only certain dice counts for each player, but I found the most informative graphs to be those that used all possible dice counts EXCEPT for dudo calls where the offensive player had just one die left. This exception is due to the fact that the offensive player's dudo calls were 100% successful in these scenarios (see the graph titled inter-offense-1), and I have yet to understand why.
  
  Anyhow, the new simulation file gave me a neat graph that looked like a nice clean line with a slope of about .09, or 9%. This means that if the dice count ratio of offense:defense increases by 1, then the dudo call has a 9% greater chance of succeeding. So, I used that slope to create a dudo dial function that simply takes the current offense:defense dice ratio, which players would know in a real game, and multiplies it by .09 and adds a constant. This new dudo dial actually resulted in the overall winning percentage of dudo calls to drop, BUT the probability predictions were much closer to the actual dudo success rate – the standard deviation of average success rates reduced by about 40%, from .12 to .07.
  
# Next Steps

  There is still more to do to create smarter computer players. I still do not know why the offensive player always wins on their dudo calls if they have just one die. I suspect that I could create a nice dataset from simulated games that could be used to train computer players with some machine learning techniques, but I am not quite capable of that yet. I will look into these points in the future with the aim of creating computer players that always make very smart moves.
