# perudo

Implementation of the dice game Perudo (AKA Liar's Dice), along with a game simulator and other files.


Please read the .txt files for explanations of the game rules and the probability calculations used in the source code.

As of August 6 2020, the source code files include:

  - perudo.py: gameplay definitions.

  - move_probability.py: computes and prints the probability of success of all possible moves on a given turn of Perudo.

  - simulation.py: simulates multiple games of Perudo using all computer players, and prints statistics from the simulations.

I am planning to include the following updates at a later date:

  - human-playable functionality: a file that will allow the user to play a game of perudo against computers

  - update to dudo_dial: this feature is currently implemented to calculate probability of dudo calls, but it doesn't work well in all situations. see probability.txt for an in-depth explanation

  - add palifico and calza: these gameplay features aren't implemented yet, but are very common. palifico will probably be part of normal gameplay, and calza will most likely be an option. see rules.txt for explanation of these features.
