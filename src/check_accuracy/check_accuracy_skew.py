from vision.read_skew import *

"""注意
read_skewをリアルタイムように調整したため静止画の精度が悪い。
"""

ac = 0
cnt = 0
failed = {i: 0 for i in range(11)}
for i in range(31):
    sudoku_pic = recog_by_warped(read_sudoku(SKEW_PATH / f"sudoku_{i}.png", i), i)
    sudoku_text = import_sudoku_text(TEXT_PATH / f"sudoku-data{i}.txt")

    if(sudoku_pic == sudoku_text):
        ac += 1
        print(f"complete {i}")
    else:
        for l in range(9):
            for c in range(9):
                if(sudoku_pic[l][c] != sudoku_text[l][c]):
                    if(sudoku_pic[l][c] not in failed):
                        failed[10] += 1
                    else:
                        failed[sudoku_text[l][c]] += 1
                        print(f"missed: {sudoku_pic[l][c]} at{i,l,c} actual: {sudoku_text[l][c]}")
        
    cnt += 1
    print(f"{i}: Done... {ac}")
    print(failed)
    # print(failed)
    print(sudoku_pic)
    print(sudoku_text)

print(f"{ac}/{cnt}") 