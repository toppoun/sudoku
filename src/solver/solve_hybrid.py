from src.utils import *
from src.solver.sudoku_logic import *
from src.solver.backtrack import solve_console

logic_functions = [
    ("obvious_singles", obvious_singles),
    ("obvious_pair", obvious_pair),
    ("obvious_triple", obvious_triple),
    ("hidden_singles", hidden_singles),
    ("hidden_pair", hidden_pair),
    ("hidden_triple", hidden_triple),
    ("pointing_pair", pointing_pair),
    ("pointing_triple", pointing_triple),
    ("x_wing", x_wing),
    ("y_wing", y_wing),
    ("sword_fish", sword_fish),
]
def solve_by_hybrid(sudoku_row):
    changed = True
    memo = create_memo(sudoku_row)
    while changed:
        changed = False
        for name, func in logic_functions:
            if(func(sudoku_row, memo)):
                changed = True
                break
    solve_console(sudoku_row)