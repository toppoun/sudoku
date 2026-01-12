import os
from PIL import Image
import pillow_heif

# 変換元のフォルダと変換後のフォルダを指定します
input_folder = "sudoku-heic/"
output_folder = "sudoku-skew/"

# 変換元のフォルダ内のHEICファイルを取得します
heic_files = [f for f in os.listdir(input_folder) if f.endswith('.HEIC')]

for heic_file in heic_files:
    # HEICファイルのパスを作成
    heic_path = os.path.join(input_folder, heic_file)
    
    # PNGファイルのパスを作成
    png_file = os.path.splitext(heic_file)[0] + '.png'
    png_path = os.path.join(output_folder, png_file)
    
    # HEICファイルをPNGに変換
    heif_file = pillow_heif.read_heif(heic_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )
    image.save(png_path, 'PNG')
    
    print(f'{heic_file} を {png_file} に変換しました。')

print('変換が完了しました。')
