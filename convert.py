import argparse
import glob
import os
from PIL import Image

# ========================================================================== #
#  関数名: check_args
# -------------------------------------------------------------------------- #
#  説明: コマンドライン引数の受け取り
#  返り値: dict
# ========================================================================== #
def check_args():
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-dir', help='directory path', required=True)
  parser.add_argument('-delete', help='delete old file', action='store_true')
  args = parser.parse_args()

  try:
    result = {}
    result['dir'] = args.dir
    result['delete'] = args.delete
    return result
  except Exception as e:
    print(f'引数指定に誤りがありそうです{e}')
    return 1

# -------------------------------------------------------------------------- #
#  クラス名     MyTool
#  説明        ファイル変換クラス
#  引数1       dict(コマンドライン引数)
# -------------------------------------------------------------------------- #
class MyTool:
  def __init__(self, args):
    self.def_name = 'init'
    self.target_dir_path = args['dir']
    self.delete = args['delete']

  # ====================================================================== #
  #  関数名: printLog
  # ---------------------------------------------------------------------- #
  #  説明: ログ
  # ====================================================================== #
  def printLog(self, level, message):
    # with open(r'self.log_path', 'a') as f:
    #     f.write(f'[{level}] {message}\n')
    print(f'[{level}] {message}')

  # ========================================================================== #
  #  関数名: count_files
  # -------------------------------------------------------------------------- #
  #  説明: fileをリスト化
  # ========================================================================== #
  def count_files(self):
    self.def_name = 'countfiles'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    # フォルダ内のwebpをリスト化
    files = glob.glob('*.webp')
    self.printLog('INFO', f'"{len(files)}" files found.')

    # ログ作業後処理
    message = f'"{self.def_name}" completed.'
    self.printLog('INFO', f'[ OK ] {message}')

    return files

  # ========================================================================== #
  #  関数名: convert
  # -------------------------------------------------------------------------- #
  #  説明: 変換
  # ========================================================================== #
  def convert(self, file):
    self.def_name = 'convert'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    # 拡張子なしのファイル名
    name = os.path.splitext(os.path.basename(file))[0]
    jpg = Image.open(file).convert('RGB')
    jpg.save(name + '.jpg', 'jpeg')
    # webpは削除
    if self.delete:
      os.remove(file)

    # ログ作業後処理
    message = f'"{self.def_name}" completed. {name}.webp -> {name}.jpg'
    self.printLog('INFO', f'[ OK ] {message}')

# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
  args = check_args()
  tool = MyTool(args)
  os.chdir(tool.target_dir_path)
  files = tool.count_files()
  for f in files:
    tool.convert(f)

if __name__ == '__main__':
  main()
