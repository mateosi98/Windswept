# Windswept

Using SB3 library for DRL to play a simple game that involves uncertainty and risk.

![Screenshot 2023-05-22 at 11 16 27](https://github.com/mateosi98/Windswept/assets/51299251/8e42a7bc-8f4f-4bcc-8db4-b13fa52fe41b)

Each turn, you can place a random number of blocks ~Unif(1,3), with the possibility of creating multiple columns (for reinforcement purposes). After each turn, the wind blows on one of the 10 floors of the space ~Unif(0,9) and knocks down a column of blocks from the corresponding floor upwards. If the wind blows on a floor that has no blocks, nothing falls. This game is interesting because it has two important randomness factors in each game. 
