## 概要
本プロジェクトは数独を解くプログラムであり、 
- バックトラックによる機械的な解法
- 人間が用いる解法ロジックによる解法
- カメラ入力による盤面認識を用いた解法
の3つを実装した。  
  
## 実行方法
sudoku/ で以下のコマンドで実行お願いします。  
- python -m src.backtrack_solver # バックトラックによる機械的な解法
- python -m src.human_solver      # 人間が用いる解法ロジックによる解法
- python -m src.camera_solver     # カメラ入力による盤面認識を用いた解法


※ pytesseract を使用するため，別途 Tesseract OCR のインストールが必要  