# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver


## Project Structure
* `solution.py`: Sudoku solver core functions
* `solution_test.py`: Solver test  
* `PySudoku.py` - Solution visualization
* `visualize.py` - Solution visualization

Here's an example of Sudoku being solved

![alt text][image1]

## Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: I first implemented the naked twins elimination for one pass. see function `naked_twins` in `solution.py`.
It iterate through all the units, try to find naked twins, and eliminate the digits from their peers. The constraint propagation is achieved in the `reduce_puzzle` function. In this function, I repeatedly perform `eliminate`, `only_choice`, and `naked_twins` to reduce the search space.

## Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The only difference for diagonal sudoku is in addition to the rows, columns and 3x3 cell, we have a new type of unit: diagonal boxes. I added the two diagonal units to the unitlist and peers list. The rest of solving process is identical to normal sudoku.

[image1]: ./animation_image/animation.gif
