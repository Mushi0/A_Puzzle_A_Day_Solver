# A Puzzle A Day Solver

## dependencies: 

- Python version: `3.8`

- For the optimisation model solved with [`CPLEX`](./main_optimisation_CPLEX.py), I used [*IBM CPLEX*](https://www.ibm.com/products/ilog-cplex-optimization-studio) solver version `22.11`. It is a commercial solver, but you can get an academic lisence for free [here](https://www.ibm.com/academic/). 

- For the model solved using [`HiGHS`](main_optimisation_HiGHS.py), I used the Python API of the fastest open source optimisation solver [*HiGHS*](https://highs.dev/). The version of *highspy* is `1.12.0`. 

## Optimisation Method

`main_optimisation_CPLEX.py` and `main_optimisation_HiGHS.py` are the scripts for the optimisation method solved with the two solvers. They take a date as input, and output one solution for the specific date. While running the programme, input the date in the format DD-MM. The solution will be printed out on the terminal. An example is as follow: 

```
Piece 0 at position 1
Piece 1 at position 92
Piece 2 at position 41
Piece 3 at position 39
Piece 4 at position 110
Piece 5 at position 15
Piece 6 at position 19
Piece 7 at position 45

=============Solution=============
6 0 0 0 7 7
6 0 0 0 7 M
6 6 D 7 7 4 4
6 3 3 3 1 1 4
2 3 3 5 5 1 4
2 5 5 5 1 1 4
2 2 2
```

## Brute Force Method

`main_brute_force.py` is the brute force script for getting the solution for every day in a year (including 29th Feb). It reads the file `Pieces.txt` as an input and saves all the feasible solutions in a `result.txt` file at the same directory. An example of the solutions is as follows: 

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