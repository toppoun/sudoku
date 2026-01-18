import time
from tkinter import *
from PIL import ImageGrab
from pathlib import Path

from src.utils import *
from src.config import *

"""
テキストデータの盤面をtkinterで描画しそれを保存する。
手元に試したい数独のテキストデータがある場合はこれを使うと簡単にできる。
"""


def save_canvas_png(canvas, filename="sudoku.png"):
    canvas.update()

    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    img = ImageGrab.grab(bbox=(x+10, y+10, x + w-10, y + h-10))
    img.save(filename)

    print("saved:", filename)



for i in range(3):
    if i == 50 or i == 51:
        continue
    canvas.delete("all")

    sudoku = import_sudoku_text(TEXT_PATH / f"sudoku-data{i}.txt")
    draw(sudoku,"HG創英角ポップ体")

    tk.update()
    time.sleep(0.2)

    filename = Path("sudoku-picture-arial") / f"sudoku-data{i}.png"
    save_canvas_png(canvas, filename)



# sudoku = import_sudoku_text("all1")
# print(sudoku)
# draw(sudoku)
# tk.destroy()
tk.mainloop()