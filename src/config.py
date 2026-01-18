from pathlib import Path

TEXT_PATH = Path("data/sudoku-data")
PICT_PATH_TIMES = Path("data/sudoku-picture/sudoku-picture-times")
PICT_PATH_HELVETICA = Path("data/sudoku-picture/sudoku-picture-helvetica")
PICT_PATH_COURIER = Path("data/sudoku-picture/sudoku-picture-courier")

#歪んだ画像(写真は通し番号0-10がTimes,11-20がHelvetica,21-30がCourier)
SKEW_PATH = Path("data/sudoku-picture/sudoku-skew")

#画像処理の確認用 /debug に全体の画像と切り取った画像を保存する
DEBUG = False