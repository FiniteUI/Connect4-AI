# Connect4
This is a small personal project to build an AI for the game Connect 4. 

Connect 4 is a solved game, meaning the ideal move can be determined at any point. For a perfect AI and explanation, see here: http://blog.gamesolver.org/
However, I wanted to build my own AI from scratch without taking anything from other sources.

For my AI, I'm utilizing a point based system. At each move, the AI simulates all possibilities for the next N move, and assigns a point value to them.
The point value represents how likely (or unlikely) that move is to result in a win.

Currently, the following parameters are taken into account:
1. If the move is a win
2. If the move is a loss
3. How many streaks of two with an open position next to them there are
4. How many streaks of two with an open position on both sides of them there are
5. How many streaks of three with an open position next to them there are
6. How many streaks of three with an open position on both sides of them there are
7. For 3-6, how many open cells are under the open positions

The AI calculates this for it's own moves as well as the opponent's possible moves, and sums it all up. Each move score is the sum of the ideal move scores for all
possibilities it leads to. The enemy's move score is multiplied by a negative multiplier in this sum. 

The AI works well, its main limitation is how many moves ahead it can look. Due to the amount of possibilites and the implementation, I've settled on using 7 moves ahead.
This results in ~15 seconds to pick a move towards the start of the game, with this number decreasing drastically as options dry up. To look any further ahead, the 
program would need to be sped up significantly. Ideally, the program would look at all possible moves regardless of how far ahead they are, but with this implementation,
that would take much too long.

I would like to keep working on this in the future, to see if I can speed the program up to look a few extra moves ahead, and improve the points system.
I will also be looking at trying to implement the perfect Connect 4 AI mentioned above.

The files contained in this repository are as follows:
Connect4.py - This is my implementation of the game Connect 4 for the AI to play.
TestConnect4.py - This uses the Connect4.py script to run a game of Connect 4 on the console.
AI.py - This is the implementation of the AI itself.
TestAI.py - This creates an instance of the AI and allows the player to play against it on the console.
TestAIAgainstItself.py - This runs two instances of the AI against eachother.

Here is the output of a game played with TestAI.py:
[GameOutput.txt](https://github.com/FiniteUI/Connect4/files/10297855/GameOutput.txt)

