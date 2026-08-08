import cv2
import numpy as np
from pathlib import Path
from src.vision.read_skew import (
    read_sudoku,
    find_board,
    four_point_transform,
    recog_by_warped,
    order_points,
)
from src.config import DEBUG

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# 入力画像のパスを指定
image_path = r"D:\sudoku\data\sudoku-picture\sudoku-skew\sudoku_2.png"

# デバッグディレクトリを作成
Path("debug_output").mkdir(exist_ok=True)

# 元の画像を読み込み
img = cv2.imread(str(image_path))
if img is None:
    print(f"画像が読み込めません: {image_path}")
    exit()

print("Step 1: 入力画像を保存")
cv2.imwrite("debug_output/01_input_image.png", img)

print("Step 2: 盤面を検出")
board_cnt = find_board(img)
if board_cnt is None:
    print("盤面が見つかりませんでした")
    exit()

# 盤面の枠を描画した画像
display = img.copy()
cv2.drawContours(display, [board_cnt], -1, (0, 255, 0), 3)
cv2.imwrite("debug_output/02_board_detected.png", display)

print("Step 3: 透視変換を実施")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
warped = four_point_transform(gray, board_cnt.reshape(4, 2))
cv2.imwrite("debug_output/03_perspective_transformed.png", warped)

print("Step 4: 二値化")
_, warped_binary = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite("debug_output/04_binary_image.png", warped_binary)

print("Step 5: OCR認識")
sudoku = recog_by_warped(warped_binary)

print("認識された盤面:")
for row in sudoku:
    print(row)

# セル画像を保存
H, W = warped_binary.shape
cell_h = H // 9
cell_w = W // 9

for r in range(9):
    for c in range(9):
        y_start = r * cell_h
        x_start = c * cell_w
        cell = warped_binary[y_start : y_start + cell_h, x_start : x_start + cell_w]
        cv2.imwrite(f"debug_output/05_cell_{r:02d}_{c:02d}.png", cell)

print("Step 6: OCR結果を画像に重ねて保存")

# 透視変換後画像をカラー化して、上に文字を描画する
overlay = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)

# グリッド線を描画
for i in range(10):
    x = i * cell_w
    y = i * cell_h

    # 3マスごとの太線
    thickness = 3 if i % 3 == 0 else 1

    cv2.line(overlay, (x, 0), (x, H), (0, 0, 255), thickness)
    cv2.line(overlay, (0, y), (W, y), (0, 0, 255), thickness)

# OCR結果を各セル中央に描画
for r in range(9):
    for c in range(9):
        value = sudoku[r][c]

        # 0, ".", "", None は空白扱い
        if value in [0, "0", ".", "", None]:
            continue

        text = str(value)

        x_center = c * cell_w + cell_w // 2
        y_center = r * cell_h + cell_h // 2

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.2
        thickness = 3

        # 文字サイズを取得して中央揃え
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size

        x = x_center - text_w // 2
        y = y_center + text_h // 2

        # 見やすくするため白縁取り → 青文字
        cv2.putText(
            overlay,
            text,
            (x, y),
            font,
            font_scale,
            (255, 255, 255),
            thickness + 3,
            cv2.LINE_AA,
        )
        cv2.putText(
            overlay,
            text,
            (x, y),
            font,
            font_scale,
            (255, 0, 0),
            thickness,
            cv2.LINE_AA,
        )

cv2.imwrite("debug_output/06_ocr_overlay.png", overlay)

print("\nすべての画像が debug_output/ に保存されました。")
print("OCR結果の重ね合わせ画像: debug_output/06_ocr_overlay.png")

 