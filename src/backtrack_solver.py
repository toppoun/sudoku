from src.solver.backtrack import solve_console
from src.utils import *

"""
バックトラックで数独をとく。
"""

sudoku_num = 0
sudoku = import_sudoku_text(TEXT_PATH / f"sudoku-data{sudoku_num}.txt")
res = solve_console(sudoku)
draw(sudoku, "Times New Roman")
tk.mainloop()