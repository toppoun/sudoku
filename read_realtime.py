import cv2
import numpy as np
from copy import deepcopy

from read_skew import order_points, find_board,  four_point_transform, recog_by_warped
from backtrack import solve_console



def draw_ar(frame, board_cnt, sudoku, initial_place):
    rect = order_points(board_cnt.reshape(4, 2))

    size = 450  # four_point_transform 側と合わせる
    dst = np.array([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]], dtype="float32")

    M_inv = cv2.getPerspectiveTransform(dst, rect)

    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                continue

            xw = (c + 0.5) * size / 9
            yw = (r + 0.5) * size / 9

            src = np.array([[[xw, yw]]], dtype="float32")
            dst_pt = cv2.perspectiveTransform(src, M_inv)[0][0]

            x, y = int(dst_pt[0]), int(dst_pt[1])

            if(initial_place[r][c] != 0):
                color = (0, 0, 255)
            else:
                color = (0, 0, 0)
            cv2.putText(frame, str(sudoku[r][c]), (x - 20, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)


def draw_grid(frame, rect):
    tl, tr, br, bl = rect

    for i in range(1, 9):
        a = i / 9

        p1 = (tl * (1 - a) + bl * a).astype(int)
        p2 = (tr * (1 - a) + br * a).astype(int)
        cv2.line(frame, tuple(p1), tuple(p2), (0, 255, 0), 1)

        p3 = (tl * (1 - a) + tr * a).astype(int)
        p4 = (bl * (1 - a) + br * a).astype(int)
        cv2.line(frame, tuple(p3), tuple(p4), (0, 255, 0), 1)



recognize = False          # space 押下フラグ
last_sudoku = None         # 認識結果（固定）
last_board_cnt = None      # 追尾用（毎フレーム更新）


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("カメラが開かない")



while True:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()

    board_cnt = find_board(frame)

    if board_cnt is not None:
        cv2.drawContours(display, [board_cnt], -1, (0, 255, 0), 3)
        rect = order_points(board_cnt.reshape(4, 2))
        draw_grid(display, rect)

        # space が押された瞬間
        if recognize:
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                warped = four_point_transform(gray, board_cnt.reshape(4, 2))
                _, warped = cv2.threshold(warped, 0, 255, cv2.THRESH_OTSU)

                last_sudoku = recog_by_warped(warped)
                initial_place = deepcopy(last_sudoku)
                last_board_cnt = board_cnt.copy()

            except Exception:
                pass

            recognize = False

    # 追尾描画
    if last_sudoku is not None and board_cnt is not None:
        draw_ar(display, board_cnt, last_sudoku, initial_place)

    cv2.imshow("frame", display)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):
        recognize = True
    if key == ord("s"):
        solve_console(last_sudoku)
    if key == ord("c"):
        last_sudoku = None
    if key == ord('q'):
        break




cap.release()
cv2.destroyAllWindows()
