# Crossword-Backtracking
Solution for Assignment 3 (Word Puzzle) in CS 480 at ODU.
Implements recursive backtracking to find arrangements of words
adhering to the constraints inherent in the shape of crossword
puzzles.
## Usage
The main driver is the main function in src/crossword.design.py.

Just execute that file with python, e.g.
(from the root directory): `python src/crossword.design.py`
### Args/Options
There are a total of seven (7) optional arguments:  
`--puzzle [PUZZLE]`
  where [PUZZLE] is the path to a text file containing a list
  of variables that together specify the puzzle's structure
  
`--words [WORDS]`
  where [WORDS] is the path to a text file containing a list
  of word candidates for assignment to variables
  
`--heuristic [HEURISTIC]`
  where [HEURISTIC] is either mrv, degree, mrv+degree, or
  first_unassigned. Determines the heuristic used to 
  choose the next unassigned variable during backtracking
  
`--disable_forward_check`
  disables forward checking, so that the backtracking algorithm
  will no longer try to avoid dead ends
  
`--sort_domains`
  enables domain sorting based on letter frequency analysis from:
  www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
  in an attempt to favor candidates that minimally diminish
  the domains of mutually constrained variables
  
`--hide_stats`
  hides additional stats normally displayed underneath the solution
  
`--randomize`
  randomizes domain order for each variable (warning: causes wildly
  varying runtimes)

The default execution (when no additional args are supplied) is equivalent to:
`python src/crossword_design.py --puzzle resources/puzzles/heart.txt --words resources/words/words.txt --heuristic mrv`

## File Structure
Three (3) puzzles are supplied in resources/puzzles, namely mini.txt, 
