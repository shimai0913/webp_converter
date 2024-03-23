import argparse
import glob
import os
import shutil
from PIL import Image

# ========================================================================== #
#  関数名: check_args
# -------------------------------------------------------------------------- #
#  説明: コマンドライン引数の受け取り
#  返り値: dict
# ========================================================================== #
def check_args():
  parser = argparse.ArgumentParser(add_help=False)
  parser.add_argument('-path', help='full path', required=True)
  parser.add_argument('-delete', help='delete old file', action='store_true')
  args = parser.parse_args()

  try:
    result = {}
    result['path'] = args.path
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
    self.full_path = args['path']
    self.dirname = os.path.dirname(self.full_path)
    self.basename = os.path.basename(self.full_path)
    self.filename, self.ext = os.path.splitext(self.basename)
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

    os.chdir(f'{self.dirname}/{self.filename}')
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
  #  関数名: dir_to_zip
  # -------------------------------------------------------------------------- #
  #  説明: dirをzipに変換
  # ========================================================================== #
  def dir_to_zip(self):
    self.def_name = 'dir_to_zip'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    os.chdir(self.dirname)
    shutil.make_archive(self.filename, format='zip', root_dir=self.filename)
    shutil.rmtree(f'{self.dirname}/{self.filename}')

    # ログ作業後処理
    message = f'"{self.def_name}" completed.'
    self.printLog('INFO', f'[ OK ] {message}')

  # ========================================================================== #
  #  関数名: zip_to_dir
  # -------------------------------------------------------------------------- #
  #  説明: zipをdirに変換
  # ========================================================================== #
  def zip_to_dir(self):
    self.def_name = 'zip_to_dir'
    description = f'Processing of "{self.def_name}" function is started.'
    self.printLog('INFO', f'[ OK ] {description}')

    # os.chdir(self.dirname)
    shutil.unpack_archive(self.full_path, f'{self.dirname}/{self.filename}')

    # ログ作業後処理
    message = f'"{self.def_name}" completed.'
    self.printLog('INFO', f'[ OK ] {message}')

# ========================================================================== #
#  メインパート
# ========================================================================== #
def main():
  args = check_args()
  tool = MyTool(args)
  tool.zip_to_dir()

  files = tool.count_files()

  for f in files:
    tool.convert(f)

  os.rename(tool.full_path, f'{tool.dirname}/{tool.filename}_old{tool.ext}')
  tool.dir_to_zip()

if __name__ == '__main__':
  main()
