from pathlib import Path
import cv2
import numpy as np
import pytesseract

from config import *
from utils import *

"""
紙に書かれた数独の盤面を読み取るための関数。
綺麗な静止画とは違ってまず盤面を正方形に直してからやる必要がある。
"""


def order_points(pts):
    #座標を [左上, 右上, 右下, 左下] の順に並べ替える
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    #透視変換を行って画像を正方形にする
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
    #盤面検出用の前処理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ノイズ除去（強めにかける）

    blur = cv2.medianBlur(gray, 7)
    # 二値化
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    # 白黒反転（輪郭検出は白を対象にするため）
    thresh = cv2.bitwise_not(thresh)
    return thresh


def is_square_like(pts, tol=0.2):
    #正方形っぽくないやつを除外する
    def dist(a, b):
        return np.linalg.norm(a - b)

    tl, tr, br, bl = pts
    edges = [
        dist(tl, tr),
        dist(tr, br),
        dist(br, bl),
        dist(bl, tl)
    ]

    max_len = max(edges)
    min_len = min(edges)

    # 辺の長さが±20%以内ならOK
    return min_len / max_len > (1 - tol)


def find_board(img):
    area_min = 50000
    #画像から数独の盤面（最大の四角形）を見つける
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
            rect = order_points(approx.reshape(4,2))
            if is_square_like(rect) and cv2.contourArea(rect) > area_min:
                board_cnt = approx
                break
            
    return board_cnt

#数字を真ん中にする
def center_digit(img):
    coords = np.column_stack(np.where(img > 0))
    if len(coords) == 0:
        return img

    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    digit = img[y_min:y_max+1, x_min:x_max+1]

    h, w = img.shape
    dh, dw = digit.shape

    canvas = np.zeros_like(img)

    y0 = (h - dh) // 2
    x0 = (w - dw) // 2

    canvas[y0:y0+dh, x0:x0+dw] = digit
    return canvas

def read_sudoku(image_path, i = None):
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

    #2値化
    



    if(DEBUG):
        cv2.imwrite(f"debug/warped_{i}.png", warped)
    
    return warped

    


def recog_by_warped(warped, i = None):
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
            margin = int(min(ch, cw) * 0.15)
            cell_inner = cell[
                margin:ch-margin,
                margin:cw-margin
            ]

            
            cell_inner = center_digit(cell_inner)

            cell_inner = cv2.adaptiveThreshold(cell_inner, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            cell_inner = cv2.resize(cell_inner, (64, 64))

            cell_inner = cv2.bitwise_not(cell_inner)
            #切り捨てレート設定
            ratio = cv2.countNonZero(cell_inner) / cell_inner.size
            cell_inner = cv2.bitwise_not(cell_inner)
            if ratio < 0.01:
                sudoku[r][c] = 0
                # print(f"No digit detected. {r,c}")
                continue

            text = pytesseract.image_to_string(
                cell_inner,
                config="--psm 10 -c tessedit_char_whitelist=123456789"
            )

            text = int(text) if text.strip().isdigit() else 0
            if(text > 9 or text == 0):
                cell_inner = cv2.bitwise_not(cell_inner)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
                cell_inner_b = cv2.dilate(cell_inner, kernel, iterations=2)
                cell_inner_b = cv2.bitwise_not(cell_inner_b)
                text = pytesseract.image_to_string(
                    cell_inner_b,
                    config="--psm 10 -c tessedit_char_whitelist=123456789")
                
                text = int(text) if text.strip().isdigit() else 0
                if(text > 9 or text == 0):
                    cell_inner_e = cv2.erode(cell_inner, kernel, iterations=2)
                    cell_inner_e = cv2.bitwise_not(cell_inner_e)
                    text = pytesseract.image_to_string(
                        cell_inner_e,
                        config="--psm 10 -c tessedit_char_whitelist=123456789")
                    text = int(text) if text.strip().isdigit() else 0

            if(DEBUG):
                cv2.imwrite(f"debug/{i}_{r}_{c}.png", cell_inner)

            sudoku[r][c] = text


    return sudoku

