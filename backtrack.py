import time
start = time.time()

def import_sudoku(num): #テキストファイルから数独データを取得
    with open(f"sudoku-data{num}.txt") as file:
        sudoku_raw = []
        current_line = []
        for line in file:
            new_line=line.rstrip("\n")
            for x in new_line:
                if x == " " or x == ".":
                    x = 0
                    current_line.append(x)
                else:
                    x = int(x)
                    current_line.append(x)
            sudoku_raw.append(current_line)
            current_line=[]
    return sudoku_raw


def find_zero(sudoku): #0の場所の行数と列数を返す
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0:
                return i,j
    
    return -1,-1 #0がなければ(-1,-1)を返す

#print(find_zero(sudoku_raw))

def check(sudoku, i, j, value):
    
    for x in sudoku[i]:
        if x==value:
            return False
    
    for y in range(9):
        if sudoku[y][j] == value:
            return False
    

    box_i = (i // 3) * 3
    box_j = (j // 3) * 3
    for a in range(3):
        for b in range(3):
            if sudoku[box_i + a][box_j + b] == value:
                return False

    return True


def solve_console(sudoku): #バックトラック部分処理
    i, j = find_zero(sudoku)
    if i ==  -1:
        return True
    
    for value in range(1, 10):
        if check(sudoku, i, j, value):
            sudoku[i][j]=value

            if solve_console(sudoku): #次のマスを埋める

                return True
            
        sudoku[i][j] = 0

    
    return False


# print(solve_console(sudoku_raw))
# print(sudoku_raw)

def solve(sudoku): #バックトラック部分処理
    i,j=find_zero(sudoku)
    if i==-1:
        return True #終了条件
    
    for value in range(1,10):
        if check(sudoku,i,j,value):
            sudoku[i][j]=value

            if solve(sudoku): #次のマスを埋める
                # canvas.after(1)

                return True
            
        sudoku[i][j]=0
        # draw(sudoku)
        # tk.update()
        # canvas.after(1)
    
    return 

answer = {}
# for data in range(60):
#     if(data == 51 or data == 50):
#         pass
#     else:
#         sudoku_raw = import_sudoku(data)
#         solve(sudoku_raw)
# answer[46] = sudoku_raw

# print("finish")
# end = time.time()
# time_diff = end - start
# print(time_diff)

#１回計測 127.028987884521