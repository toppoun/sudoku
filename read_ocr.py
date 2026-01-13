from pathlib import Path
import cv2
import numpy as np
import pytesseract

from utils import *
from config import *

"""
数独の文字の読み取りにはOCR(Optical Character Recognition：光学文字認識)を用いた。
前処理にはcv2を使った。
"""


# 数独読み取り

def read_sudoku(image_path, i = None):

    img = cv2.imread(image_path)

    # --- グレースケール ---
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 平均化 ---
    gray = cv2.blur(gray, (3, 3), 0)

    # --- 二値化 ---
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    # --- 輪郭検出 ---
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # --- 最大輪郭 = 盤面 ---
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    board = thresh[y:y+h, x:x+w]

    # --- 9×9 分割 ---
    H, W = board.shape
    cell_h = H // 9
    cell_w = W // 9

    sudoku = [[0]*9 for _ in range(9)]

    for r in range(9):
        for c in range(9):
            y_start = r * cell_h
            x_start = c * cell_w
            cell = board[y_start : y_start + cell_h, x_start : x_start + cell_w]

            # --- 余白カット ---
            ch, cw = cell.shape
            margin = int(min(ch, cw) * 0.1)
            cell_inner = cell[
                margin:ch-margin,
                margin:cw-margin
            ]

            # --- 数字を太らせる ---
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            cell_inner = cv2.dilate(cell_inner, kernel, iterations=1)
            cell_inner = cv2.resize(cell_inner, (32, 32))
            cell_inner = cv2.bitwise_not(cell_inner)

            

            if cv2.countNonZero(cell_inner) < 50:
                sudoku[r][c] = 0
                continue

            text = pytesseract.image_to_string(
                cell_inner,
                config="--psm 10 -c tessedit_char_whitelist=123456789"
            )

            text = int(text) if text.strip().isdigit() else 0
            #1,4,7は間違えがちだから細くして画質悪くして特徴を薄める(特に１の上の部分が４に間違えられる)
            if(text in [1,4,7]):
                cell_inner = cv2.bitwise_not(cell_inner)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                cell_inner = cv2.erode(cell_inner, kernel, iterations=2)
                cell_inner = cv2.resize(cell_inner, (24, 24))
                cell_inner = cv2.bitwise_not(cell_inner)
                text = pytesseract.image_to_string(
                    cell_inner,
                    config="--psm 10 -c tessedit_char_whitelist=123456789"
                )

                text = int(text) if text.strip().isdigit() else 0
            sudoku[r][c] = int(text)

            if(DEBUG):
                cv2.imwrite(f"debug/{i}_{r}_{c}.png", cell_inner)


    return sudoku
