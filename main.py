import tkinter.simpledialog as simpledialog
import time

from utils import *
from sudoku_logic import *

#---------- option ----------#


#----------------------------#

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
    ("sword_fish", sword_fish)
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

    draw(sudoku_row)

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