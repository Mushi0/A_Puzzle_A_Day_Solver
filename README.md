# A Puzzle A Day Solver

## dependencies: 

- Python version: `3.8`

- For the optimisation model `main_optimisation.py`, I used *IBM CPLEX* solver version `22.11`. It is a commercial solver, but you can get an academic lisence for free [here](https://www.ibm.com/academic/). 

## Optimisation Method

`main_optimisation.py` file is the optimisation method for getting one solution for a specific date. While running the programme, input the date in the format DD-MM. The solution will be printed out on the terminal. 

## Brute Force Method

`main.py` is the brute force script for getting the solution for every day in a year (including 29th Feb). It reads the file `Pieces.txt` as an input and saves all the feasible solutions in a `result.txt` file at the same directory. An example of the solutions is as follows: 

```
Solution 0:
Date: 26/11
0 0 0 1 1 1
0 0 0 1 M 1
2 2 2 3 3 3 6
2 7 7 3 3 6 6
2 7 4 4 4 4 6
7 7 5 5 D 4 6
5 5 5

Solution 1:
Date: 29/11
0 0 0 1 1 1
0 0 0 1 M 1
2 2 2 3 3 3 6
2 7 7 3 3 6 6
2 7 4 4 4 4 6
7 7 5 5 5 4 6
D 5 5
```