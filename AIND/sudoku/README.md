# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

Assignment is in this [repository](https://github.com/udacity/aind-sudoku).

# Question 1 (Naked Twins)

Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins problem is in a situation that both boxes have the same 2-digit values in the same unit, while other boxes in the same unit contain one or two of these digits. The goal is to simplify other boxes in the same unit.  This can be achieved by 2 steps:

1. in each unit of 9 boxes, select the boxes that has value length of 2
2. in the same unit, determine which boxes are twins and use the twins to elminate the digits in the same unit 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In diagonal sudoku, two more units are added into the unit list. Basically, there are 2 steps:

1. `reduce_puzzle`  function is composed of iterative loop of `eliminate`,`only_choice`, and `naked_twins`, which reduce the solved digits,  solve the single digits if possible and reduce the twin digits, respectively. 
2. use a "depth-first" function `search` to do a recursion, so every possible solution is transversed until every box is solved.

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
installed the client tool: `pip install udacity-pa`.  

run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  

This process will create a zipfile to submit to the Udacity reviews system.

