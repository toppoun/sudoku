import time
import tkinter.simpledialog as simpledialog

from src.solver.backtrack import solve_console
from src.utils import *

"""
バックトラックで数独をとく。
"""

def all():
    start = time.time()
    legal = {}
    ilegal = {}
    yet = {}

    for i in range(61):     
        if i == 50 or i == 51:
            continue
        sudoku_row = import_sudoku_text(TEXT_PATH / f"sudoku-data{i}.txt")
        res = solve_console(sudoku_row)
        if(res):
            # print(f"{i} ok")
            legal[i] = (sudoku_row)

        elif(res == False):
            # print(f"{data} 間違い")
            ilegal[i] = (sudoku_row)
        if(res is None):
            # print(f"No.{i} {count_zero(sudoku_row)} Remain")
            yet[i] = (sudoku_row)
    print("----------結果----------")
    print(f"正　解：{len(legal)}個{list(legal.keys())}")
    print(f"不正解：{len(ilegal)}個{list(ilegal.keys())}")
    print(f"未回答：{len(yet)}個{list(yet.keys())}")
    print("-----------------------")
    end = time.time()
    time_diff = end - start
    print(f"実行時間：{time_diff} s")



all()
while True:
    in_ = simpledialog.askstring("ダイアログ","コマンドを入力")
    try:
        sudoku_row = import_sudoku_text(TEXT_PATH / f"sudoku-data{int(in_)}.txt")
        solve_console(sudoku_row)
        draw(sudoku_row,"Times New Roman")
    except:
        break
tk.mainloop()