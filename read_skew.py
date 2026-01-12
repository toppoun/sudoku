from pathlib import Path
import cv2
import numpy as np
import pytesseract

from config import *
from utils import *


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def order_points(pts):
    """座標を [左上, 右上, 右下, 左下] の順に並べ替える関数"""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    """透視変換を行って画像を正方形に補正する関数"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # 幅と高さを計算（最大値をとる）
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped



def pre_process_image(img):
    """盤面検出用の前処理"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ノイズ除去（強めにかける）

    blur = cv2.medianBlur(gray, 7)
    # 二値化（適応的閾値処理）
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    # 白黒反転（輪郭検出は白を対象にするため）
    thresh = cv2.bitwise_not(thresh)
    return thresh

def find_board(img):
    """画像から数独の盤面（最大の四角形）を見つける"""
    processed = pre_process_image(img)
    contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 面積の大きい順にソート
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    board_cnt = None
    
    for c in contours:
        peri = cv2.arcLength(c, True)
        # 輪郭を近似（頂点数を減らす）
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        # 点が4つ（四角形）であれば、それが盤面である可能性が高い
        if len(approx) == 4:
            board_cnt = approx
            break
            
    return board_cnt

def read_sudoku(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return [[0]*9 for _ in range(9)]


    # 1. 盤面の輪郭を見つける
    board_cnt = find_board(img)
    # print(board_cnt)
    
    
    if board_cnt is None:
        print(f"盤面が見つかりませんでした: {image_path}")
        return [[0]*9 for _ in range(9)]

    # 2. 透視変換（グレー画像に対して行う）
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    warped = four_point_transform(gray, board_cnt.reshape(4, 2))
    _,warped = cv2.threshold(warped, 0, 255, cv2.THRESH_OTSU)



    if(DEBUG):
        cv2.imwrite(f"debug/warped_{i}.png", warped)

    board = warped
    
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
            cell_inner = cv2.bitwise_not(cell_inner)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            cell_inner = cv2.dilate(cell_inner, kernel, iterations=2)
            cell_inner = cv2.resize(cell_inner, (32, 32))
            cell_inner = cv2.bitwise_not(cell_inner)

            if(DEBUG):
                cv2.imwrite(f"debug/{i}_{r}_{c}.png", cell_inner)

            if cv2.countNonZero(cell_inner) < 50:
                sudoku[r][c] = 0
                continue

            text = pytesseract.image_to_string(
                cell_inner,
                config="--psm 10 -c tessedit_char_whitelist=123456789"
            )

            text = text.strip()
            if(text.isdigit()):
                sudoku[r][c] = int(text)
            else:
                sudoku[r][c] = 0


    return sudoku

ac = 0
cnt = 0
failed = {i: 0 for i in range(11)}
for i in range(3):
    if i == 50 or i == 51:
        continue

    sudoku_pic = read_sudoku(SKEW_PATH / f"sudoku-data{i}.png")
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