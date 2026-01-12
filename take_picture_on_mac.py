import cv2
from pathlib import Path

# ===============================
# 設定
# ===============================

SAVE_DIR = Path("take-picture")
SAVE_DIR.mkdir(exist_ok=True)

MAX_SHOTS = 60

# ===============================
# カメラ開始
# ===============================

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("カメラが開かない。現実が悪い。")

count = 26

# ===============================
# メインループ
# ===============================

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ---------- 正方形クロップ ----------
    h, w, _ = frame.shape
    side = min(h, w)
    y0 = (h - side) // 2
    x0 = (w - side) // 2
    frame_sq = frame[y0:y0 + side, x0:x0 + side]

    display = frame_sq.copy()

    # ---------- UI表示 ----------
    cv2.putText(
        display,
        f"SPACE: capture   Q: quit   {count}/{MAX_SHOTS}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # ガイド枠（気分）
    cv2.rectangle(
        display,
        (0, 0),
        (side - 1, side - 1),
        (0, 255, 0),
        2
    )

    cv2.imshow("Sudoku Capture (Square)", display)

    key = cv2.waitKey(1) & 0xFF

    # ---------- 撮影 ----------
    if key == ord(' '):
        path = SAVE_DIR / f"sudoku_{count}.png"
        cv2.imwrite(str(path), frame_sq)
        print(f"saved: {path.name}")
        count += 1

        if count >= MAX_SHOTS:
            break

    if key == ord('q'):
        break

# ===============================
# 終了処理
# ===============================

cap.release()
cv2.destroyAllWindows()
