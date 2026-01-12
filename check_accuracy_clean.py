from read_ocr import *

"""フォント選択
PICT_PATH_TIMES: Times New Roman (明朝体っぽい)
PICT_PATH_HELVETICA = Helvetica (ゴシック体っぽい)
PICT_PATH_COURIER = Courier (細い)

3つのフォント全て(59個*3フォント)でテキストデータの盤面と一致した。
他のフォントでは試していないのでこれらのフォント以外はわからない。
"""
PICT_PATH = PICT_PATH_COURIER

failed = {i: 0 for i in range(1,10)}
ac = 0
cnt = 0
for i in range(61):
    if i == 50 or i == 51:
        continue

    sudoku_pic = read_sudoku(PICT_PATH / f"sudoku-data{i}.png", i)
    sudoku_text = import_sudoku_text(TEXT_PATH / f"sudoku-data{i}.txt")

    if(sudoku_pic == sudoku_text):
        ac += 1
    else:
        for l in range(9):
            for c in range(9):
                if(sudoku_pic[l][c] != sudoku_text[l][c]):
                    failed[sudoku_text[l][c]] += 1
                    print(f"missed: {sudoku_pic[l][c]} at{i,l,c} actual: {sudoku_text[l][c]}")
        print(failed)
    cnt += 1
    print(f"{i}: Done... {ac}")
    


# sudoku_pic = read_sudoku(SKEW_PATH / f"sudoku-data{0}.png")
# sudoku_text = import_sudoku_text(TEXT_PATH / f"sudoku-data{1}.txt")
# print(sudoku_pic)
print(f"{ac}/{cnt}")