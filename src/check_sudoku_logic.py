import tkinter.simpledialog as simpledialog
import time

from src.utils import *
from src.solver.sudoku_logic import *
from src.solver.backtrack import solve_console

"""
テキストファイルから数独を読み込んでsudoku_logicで実装されているロジックによって数独を解く。

現在の状況(参考)
----------結果----------
正解：52個[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 49, 52, 53, 54, 56, 57, 59, 60]
未回答(空欄が残っている状態(ロジックが足りないことを意味する))：7個[17, 24, 29, 45, 48, 55, 58]
不正解(答えが間違っている(ロジックが誤っていることを意味する))：0個[]

全てを解くのに使ったロジック。簡単(計算量の少ない)ものを優先して使うため、下に行くほど使われる回数が少ない。
obvious_singleは確定したマスを埋める唯一の関数のためこの数が埋めたマスの数を示す。
----------回数----------
obvious_singles：809回
obvious_pair：106回
obvious_triple：41回
hidden_singles：33回
hidden_pair：7回
hidden_triple：1回
pointing_pair：9回
pointing_triple：1回
x_wing：8回
y_wing：0回
sword_fish：0回
-----------------------
実行時間：0.14792513847351074s
"""

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



def solve_by_human(data):
    sudoku_row = import_sudoku_text(TEXT_PATH / f"sudoku-data{data}.txt")
    memo = create_memo(sudoku_row)

    changed = True
    while changed:
        changed = False
        for name, func in logic_functions:
            if(func(sudoku_row, memo)):
                changed = True
                statistics[name] += 1
                break
    # solve_console(sudoku_row)

    draw(sudoku_row,"Times New Roman")

    # print(sudoku_row)
    if(check_comp(sudoku_row)):
        if(sudoku_row == answer[int(data)]):
            return True
        else:
            return False
    else:
        if(is_ilegal(sudoku_row)):
            return False
        else:
            return None

def all():
    start = time.time()
    global statistics
    legal = {}
    ilegal = {}
    yet = {}
    statistics = {i: 0 for i,_ in logic_functions}

    for i in range(61):     
        if i == 50 or i == 51:
            continue
        sudoku_row = import_sudoku_text(TEXT_PATH / f"sudoku-data{i}.txt")
        res = solve_by_human(i)
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
    print("----------回数----------")
    for k,v in statistics.items():
        print(f"{k}：{v}回")
    
    print("-----------------------")
    end = time.time()
    time_diff = end - start
    print(f"実行時間：{time_diff} s")



all()


while True:
    in_ = simpledialog.askstring("ダイアログ","コマンドを入力")
    try:
        solve_by_human(in_)
        print(in_)
    except:
        break

#(24,29,45)(48,58)