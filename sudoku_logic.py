import itertools
from utils import *

"""
・obvious_singles
・obvious_pair
・obvious_triple
・hidden_singles
・hidden_pair
・hidden_triple
・pointing_pair
・pointing_triple
・x_wing
・y_wing
・sword_fish
の11個のロジックを実装した(2026/1/12(月)現在)
"""

def obvious_singles(sudoku,memo=None) -> bool:
    #メモの長さが1の物があったらそこに数字を確定させる。
    is_changed = False

    if(memo is None):
        memo = create_memo(sudoku)
    
    del_list = {}
    for key,cell in memo.items():
        if(len(cell) == 1):
            sudoku[key[0]][key[1]] = cell[0]
            del_list[key] = cell[0]

    for k,num in del_list.items():
        memo.pop(k)
        d_unit = get_cell_units(k)
        for cell in d_unit:
            if(cell in memo and num in memo[cell]):
                memo[cell].remove(num)
                is_changed = True




    for val in memo.values():
        if(len(val) == 0):
            print("0を検出 obvious single")

    
    return is_changed


def obvious_pair(sudoku,memo=None) -> bool:
    if(memo is None):
        memo = create_memo(sudoku)
    memo_len2 = {k: v for k, v in memo.items() if len(v) == 2}
    units = get_units()
    is_changed = False
    before_len = len(memo)
    

    for unit in units:
        ignore_pos = []
        current_unit = {k: v for k, v in memo_len2.items() if k in unit}
        place_nums = list(current_unit.items())

        for comb in itertools.combinations(place_nums,2):
            combination = set()
            for cell in comb:
                combination.update(cell[1])
            if(len(combination) == 2):
                # print(f"{comb}で{combination}の明らかなダブル")
                for pos in comb:
                    ignore_pos.append(pos[0])
                for d_pos in unit:
                    if(d_pos in memo and d_pos not in ignore_pos):
                        before_len = len(memo[d_pos])
                        for d_num in combination:
                            if d_num in memo[d_pos]:
                                memo[d_pos].remove(d_num)
                        if(len(memo[d_pos]) != before_len):
                            is_changed = True



    # for val in memo.values():
    #     if(len(val) == 0):
    #         print("0を検出,obvious pair")
    
    return is_changed


def obvious_triple(sudoku,memo=None) -> bool:
    if(memo is None):
        memo = create_memo(sudoku)
    memo_len2or3 = {k: v for k, v in memo.items() if len(v) == 2 or len(v) == 3}
    units = get_units()
    is_changed = False
    

    for unit in units:
        
        current_unit = {k: v for k, v in memo_len2or3.items() if k in unit}
        place_nums = list(current_unit.items())

        for comb in itertools.combinations(place_nums,3):
            ignore_pos = []
            combination = set()
            for cell in comb:
                combination.update(cell[1])
            if(len(combination) == 3):

                for pos in comb:
                    ignore_pos.append(pos[0])

                for d_pos in unit:
                    if(d_pos in memo and d_pos not in ignore_pos):
                        before_len = len(memo[d_pos])
                        for d_num in combination:
                            if d_num in memo[d_pos]:
                                memo[d_pos].remove(d_num)
                        if(len(memo[d_pos]) != before_len):
                            is_changed = True

    # for val in memo.values():
    #     if(len(val) == 0):
    #         print("0を検出,obvious triple")

    return is_changed        


def hidden_singles(sudoku,memo=None) -> bool:
    if(memo is None):
        memo = create_memo(sudoku)

    units = get_units()
    is_changed = False
    
    for unit in units:
        current_unit = {k: v for k, v in memo.items() if k in unit}
        current_count = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
        
        for _,cell in current_unit.items():
            for num in cell:
                current_count[num] += 1


        single = [k for k,v in current_count.items() if v == 1]
        
        for d_num in single:
            for pos,lis in current_unit.items():
                if(d_num in lis):
                    memo[pos] = [d_num]
                    is_changed = True
    
 
    # for val in memo.values():
    #     if(len(val) == 0):
    #         print("0を検出 hidden single")

    return is_changed


def hidden_pair(sudoku,memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)
    units = get_units()
    is_changed = False

    #1から9までの数字を含んでいるセルを数える
    for unit in units:
        num_to_cells = {i: [] for i in range(1, 10)}
        for pos in unit:
            if pos in memo:
                for num in memo[pos]:
                    num_to_cells[num].append(pos)

        #そのうち含まれているセルが2つであるものの数字を取りあげる
        candidate_nums = [k for k, v in num_to_cells.items() if len(v) == 2]

        #取り上げられた位置で2つの組み合わせを全パターン試す
        for pair in itertools.combinations(candidate_nums, 2):

            #num1 num2にそれぞれの数字を割り当てる
            num1, num2 = pair

            #その数字を含んでいる位置を出す
            pos_list1 = num_to_cells[num1]
            pos_list2 = num_to_cells[num2]

            #異なる2つの数字が同じセルにあったら隠れたペア確定
            if pos_list1 == pos_list2:
                target_cells = pos_list1
                keep_nums = {num1, num2}
                for pos in target_cells:
                    if pos in memo:
                        before_len = len(memo[pos])
                        memo[pos] = [n for n in memo[pos] if n in keep_nums]
                        if len(memo[pos]) < before_len:
                            is_changed = True


    # for val in memo.values():
    #     if(len(val) == 0):
    #         print("0を検出, hidden pair")
    
    return is_changed


def hidden_triple(sudoku,memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)
    units = get_units()
    is_changed = False

    #1から9までの数字を含んでいるセルを数える
    for unit in units:
        num_to_cells = {i: [] for i in range(1, 10)}
        for pos in unit:
            if pos in memo:
                for num in memo[pos]:
                    num_to_cells[num].append(pos)

        #そのうち含まれているセルが2つまたは3つであるものの数字を取りあげる
        candidate_nums = [k for k, v in num_to_cells.items() if len(v) == 3 or len(v) == 2]

        #取り上げられた位置で3つの組み合わせを全パターン試す
        for pair in itertools.combinations(candidate_nums, 3):

            #num1 num2にそれぞれの数字を割り当てる
            num1, num2, num3 = pair

            #その数字を含んでいる位置を出す
            pos_list1 = num_to_cells[num1]
            pos_list2 = num_to_cells[num2]
            pos_list3 = num_to_cells[num3]


            if len(set(pos_list1) |set(pos_list2) |set(pos_list3)) == 3:

                target_cells = pos_list1
                keep_nums = {num1, num2, num3}

                for pos in target_cells:
                    if pos in memo:
                        before_len = len(memo[pos])
                        memo[pos] = [n for n in memo[pos] if n in keep_nums]
                        if len(memo[pos]) < before_len:
                            is_changed = True



    # for val in memo.values():
    #     if(len(val) == 0):
    #         print("0を検出 hidden triple")

    return is_changed


def pointing_pair(sudoku, memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)

    box_units = get_units("box")
    is_changed = False


    for box_unit in box_units:
        current_box = {k: v for k, v in memo.items() if k in box_unit}

        # ボックス内の各数字の候補位置を集計
        num_positions = {i: [] for i in range(1,10)}
        for pos, nums in current_box.items():
            for n in nums:
                num_positions[n].append(pos)

        for n, poses in num_positions.items():
            if len(poses) != 2:
                continue
            
            # 全て同じ row にあるかチェック
            rows = {p[0] for p in poses}
            cols = {p[1] for p in poses}

            # pointing-row
            if len(rows) == 1:
                row = next(iter(rows))
                # 行の中で、今のボックス以外のセルを探す
                del_targets = [p for p in memo.keys() if p[0] == row and p not in box_unit]
                for p in del_targets:
                    if n in memo[p]:
                        memo[p].remove(n)
                        is_changed = True

            # pointing-col
            if len(cols) == 1:
                col = next(iter(cols))
                del_targets = [p for p in memo.keys() if p[1] == col and p not in box_unit]
                for p in del_targets:
                    if n in memo[p]:
                        memo[p].remove(n)
                        is_changed = True


            # print(current_box_count)



        
 

    return is_changed


def pointing_triple(sudoku,memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)

    box_units = get_units("box")
    is_changed = False

    for box_unit in box_units:
        current_box = {k: v for k, v in memo.items() if k in box_unit}

        # ボックス内の各数字の候補位置を集計
        num_positions = {i: [] for i in range(1,10)}
        for pos, nums in current_box.items():
            for n in nums:
                num_positions[n].append(pos)

        for n, poses in num_positions.items():
            if len(poses) != 3:
                continue
            
            # 全て同じ row にあるかチェック
            rows = {p[0] for p in poses}
            cols = {p[1] for p in poses}

            # pointing-row
            if len(rows) == 1:
                row = next(iter(rows))
                # 行の中で、今のボックス以外のセルを探す
                del_targets = [p for p in memo.keys() if p[0] == row and p not in box_unit]
                for p in del_targets:
                    if n in memo[p]:
                        memo[p].remove(n)
                        is_changed = True

            # pointing-col
            if len(cols) == 1:
                col = next(iter(cols))
                del_targets = [p for p in memo.keys() if p[1] == col and p not in box_unit]
                for p in del_targets:
                    if n in memo[p]:
                        memo[p].remove(n)
                        is_changed = True

    return is_changed


def x_wing(sudoku, memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)

    #まず行ごとに見てって候補がとなる数字のセルが2つの物を探す
    #辞書２重でやばいわかりずらい。
    #{行: {メモの数字: {メモの数字が入る位置} } }
    row_units = get_units("row")
    is_changed = False

    row_len2 = {}
    for row_unit in row_units:
        current_row = {k: v for k,v in memo.items() if k in row_unit}
        num_position = {i: [] for i in range(1,10)}
        for pos, nums in current_row.items():
            for n in nums:
                num_position[n].append(pos)
        len2 = {k: v for k,v in num_position.items() if len(v) == 2}
        row_len2[row_units.index(row_unit)] = len2

    # print(row_len2)
    #行の総組み合わせで回す
    for r1 in range(9):
        for r2 in range(r1+1, 9):
            
            #row_1,row_2は{メモの数字: 位置, メモの数字: 位置, メモの数字: 位置, メモの数字: 位置, メモの数字: 位置}
            row_1 = row_len2[r1]
            row_2 = row_len2[r2]

            #両方に数字があったらその数字を指定してx-wingか確認
            for num in range(1, 10):
                if num in row_1 and num in row_2:
                    rows = {r1, r2}
                    cols = {pos[1] for pos in row_1[num] + row_2[num]} 
                    if(len(cols) == 2):
                        # print(f"{rows}行目を除く{cols}列から{num}を削除")
                        col1,col2 = sorted(cols)
                        for row in range(9):
                            if row not in (r1, r2):
                                for col in (col1, col2):
                                    if (row, col) in memo and num in memo[(row, col)]:
                                        memo[(row, col)].remove(num)
                                        # print("x-wing使用")
                                        is_changed = True     

                    

    col_units = get_units("col")
    col_len2 = {}
    for col_unit in col_units:
        current_col = {k: v for k, v in memo.items() if k in col_unit}
        num_position = {i: [] for i in range(1, 10)}
        for pos, nums in current_col.items():
            for n in nums:
                num_position[n].append(pos)
        len2 = {k: v for k, v in num_position.items() if len(v) == 2}
        col_len2[col_units.index(col_unit)] = len2

    # 列の総組み合わせで回す
    for c1 in range(9):
        for c2 in range(c1 + 1, 9):
            col_1 = col_len2[c1]
            col_2 = col_len2[c2]

            # 両方に数字があったらその数字を指定してx-wingか確認
            for num in range(1, 10):
                if num in col_1 and num in col_2:
                    cols = {c1, c2}
                    rows = {pos[0] for pos in col_1[num] + col_2[num]}
                    if len(rows) == 2:
                        row1, row2 = sorted(rows)
                        # X-Wingが見つかった行の他の列から num を削除
                        for col in range(9):
                            if col not in (c1, c2):
                                for row in (row1, row2):
                                    if (row, col) in memo and num in memo[(row, col)]:
                                        memo[(row, col)].remove(num)
                                        # print("x-wing使用")
                                        is_changed = True
    
        
    return is_changed
    

def y_wing(sudoku, memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)

    #まずpivotを探す
    row_units = get_units("row")
    is_changed = False

    for row_unit in row_units:
        row_len2 = {k: v for k,v in memo.items() if k in row_unit and len(v) == 2}
        if(len(row_len2) == 2):
            cand1 = (list(row_len2.keys()))[0]
            cand2 = (list(row_len2.keys()))[1]
            cand1_col = get_cell_units(cand1,"col")
            cand2_col = get_cell_units(cand2,"col")

            cand1_col_len2 = {k: v for k,v in memo.items() if k in cand1_col and len(v) == 2}
            cand2_col_len2 = {k: v for k,v in memo.items() if k in cand2_col and len(v) == 2}

            if(len(cand1_col_len2) == 2):
                y_win_cand1 = row_len2 | cand1_col_len2
                pivot = {k: v for k,v in y_win_cand1.items() if k == cand1}
                pincer1 = {k: v for k,v in y_win_cand1.items() if k == cand2}
                pincer2 = {k: v for k,v in y_win_cand1.items() if k != cand1 and k!= cand2}

                # print(f"pivot：{pivot}、ピンサー1：{pincer1}、ピンサー2：{pincer2}")
                pivot_vals = set(list(pivot.values())[0])
                p1_vals = set(list(pincer1.values())[0])
                p2_vals = set(list(pincer2.values())[0])

                common_p1 = pivot_vals & p1_vals
                common_p2 = pivot_vals & p2_vals


                if(len(common_p1) == 1 and len(common_p2) == 1):
                    z1 = list(p1_vals - pivot_vals)
                    z2 = list(p2_vals - pivot_vals)

                    if(len(z1) == 1 and len(z2) == 1 and z1[0] == z2[0]):
                        Z = z1[0]

                        # print(f"Y-Wing 発見：Pivot={pivot} P1={pincer1} P2={pincer2} Z={Z}")

                        p1_cells = set(get_cell_units(list(pincer1.keys())[0]))
                        p2_cells = set(get_cell_units(list(pincer2.keys())[0]))

                        target_cells = p1_cells & p2_cells

                        for cell in target_cells:
                            if(cell not in memo):
                                continue

                            if(Z in memo[cell]):
                                memo[cell].remove(Z)
                                print(f"{cell} から {Z} を削除")
                                is_changed = True


            if(len(cand2_col_len2) == 2):
                y_win_cand2 = row_len2 | cand2_col_len2

                pivot = {k: v for k,v in y_win_cand2.items() if k == cand2}
                pincer1 = {k: v for k,v in y_win_cand2.items() if k == cand1}
                pincer2 = {k: v for k,v in y_win_cand2.items() if k != cand1 and k!= cand2}

                pivot_vals = set(list(pivot.values())[0])
                p1_vals = set(list(pincer1.values())[0])
                p2_vals = set(list(pincer2.values())[0])

                common_p1 = pivot_vals & p1_vals
                common_p2 = pivot_vals & p2_vals

                if(len(common_p1) == 1 and len(common_p2) == 1):
                    z1 = list(p1_vals - pivot_vals)
                    z2 = list(p2_vals - pivot_vals)

                    if(len(z1) == 1 and len(z2) == 1 and z1[0] == z2[0]):
                        Z = z1[0]

                        # print(f"Y-Wing 発見(C2側)：Pivot={pivot} P1={pincer1} P2={pincer2} Z={Z}")

                        p1_cells = set(get_cell_units(list(pincer1.keys())[0]))
                        p2_cells = set(get_cell_units(list(pincer2.keys())[0]))

                        target_cells = p1_cells & p2_cells
                        for cell in target_cells:
                            if(cell not in memo):
                                continue

                            if(Z in memo[cell]):
                                memo[cell].remove(Z)
                                print(f"{cell} から {Z} を削除")
                                is_changed = True

    return is_changed


def sword_fish(sudoku,memo=None) -> bool:
    if memo is None:
        memo = create_memo(sudoku)
    row_units = get_units("row")
    is_changed = False

    row_len3 = {}
    for row_unit in row_units:
        current_row = {k: v for k,v in memo.items() if k in row_unit}
        num_position = {i: [] for i in range(1,10)}
        for pos, nums in current_row.items():
            for n in nums:
                num_position[n].append(pos)
        len3 = {k: v for k,v in num_position.items() if len(v) == 3}
        row_len3[row_units.index(row_unit)] = len3

    # print(row_len2)
    #行の総組み合わせで回す
    for r1 in range(9):
        for r2 in range(r1+1, 9):
            for r3 in range(r2 + 1, 9):
                
                #row_1,row_2は{メモの数字: 位置, メモの数字: 位置, メモの数字: 位置, メモの数字: 位置, メモの数字: 位置}
                row_1 = row_len3[r1]
                row_2 = row_len3[r2]
                row_3 = row_len3[r3]

                #両方に数字があったらその数字を指定してx-wingか確認
                for num in range(1, 10):
                    if num in row_1 and num in row_2 and num in row_3:
                        rows = {r1, r2, r3}
                        cols = {pos[1] for pos in row_1[num] + row_2[num] + row_3[num]} 
                        if(len(cols) == 3):
                            # print(f"{rows}行目を除く{cols}列から{num}を削除")
                            col1,col2,col3 = sorted(cols)
                            for row in range(9):
                                if row not in (r1, r2, r3):
                                    for col in (col1, col2, col3):
                                        if (row, col) in memo and num in memo[(row, col)]:
                                            memo[(row, col)].remove(num)
                                            print("swordfish使用")
                                            is_changed = True 

                    

    col_units = get_units("col")
    col_len3 = {}
    for col_unit in col_units:
        current_col = {k: v for k, v in memo.items() if k in col_unit}
        num_position = {i: [] for i in range(1, 10)}
        for pos, nums in current_col.items():
            for n in nums:
                num_position[n].append(pos)
        len3 = {k: v for k, v in num_position.items() if len(v) == 3}
        col_len3[col_units.index(col_unit)] = len3

    # 列の総組み合わせで回す
    for c1 in range(9):
        for c2 in range(c1 + 1, 9):
            for c3 in range(c2 + 1, 9):
                col_1 = col_len3[c1]
                col_2 = col_len3[c2]
                col_3 = col_len3[c3]

                # 両方に数字があったらその数字を指定してx-wingか確認
                for num in range(1, 10):
                    if num in col_1 and num in col_2 and num in col_3:
                        cols = {c1, c2, c3}
                        rows = {pos[0] for pos in col_1[num] + col_2[num] + col_3[num]}
                        if len(rows) == 3:
                            row1, row2, row3 = sorted(rows)
                            # X-Wingが見つかった行の他の列から num を削除
                            for col in range(9):
                                if col not in (c1, c2, c3):
                                    for row in (row1, row2, row3):
                                        if (row, col) in memo and num in memo[(row, col)]:
                                            memo[(row, col)].remove(num)
                                            print("swordfish使用")
                                            is_changed = True  
    
    return is_changed

