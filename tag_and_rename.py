import os
import json
import sys
from mutagen.mp4 import MP4, MP4Cover


# ノーマルモードでタグを追加
def writetag(dirname):
    # JSONファイルからデータを読み込む
    jsonname = dirname + '_tag.json'
    with open(jsonname, 'r', encoding='utf-8') as file:
        data = json.load(file)

    folder_path = os.path.join(os.getcwd(), dirname)

    # 各ファイルに対してメタデータを更新する
    for filename_without_extension, metadata in data.items():
        filename = filename_without_extension + ".m4a"  # .m4aを付加
        file_path = os.path.join(folder_path, filename)  # フォルダのパスを追加

        # ファイルの存在を確認
        if not os.path.exists(file_path):
            print(f"{filename} does not exist. Skipping...")
            continue

        audio = MP4(file_path)
        print(filename)
        audio["\xa9nam"] = [metadata["title"]]  # title タグをセット
        audio["\xa9ART"] = [metadata["artist"]]  # artist タグをセット
        audio["\xa9alb"] = dirname  # アルバム名を追加
        audio["\xa9cmt"] = filename_without_extension  # コメントにIDを追加
        audio.save()
        print("done")

    print("All files tagged")


# ファイルの名前変更
def rename(dirname, albummode):
    # 使用禁止文字のリスト
    forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # ファイルの一覧を取得
    jsonname = dirname + '_tag.json'
    with open(jsonname, 'r', encoding='utf-8') as file:
        filenames = json.load(file)

    # カレントディレクトリ内のdirnameフォルダのパスを取得
    folder_path = os.path.join(os.getcwd(), dirname)

    for filename_without_extension in filenames:
        filename = filename_without_extension + ".m4a"
        file_path = os.path.join(folder_path, filename)
        if os.path.exists(file_path):  # 存在するかどうか
            audio = MP4(file_path)

            # タグ情報を取得
            title = audio.get("\xa9nam", ["Unknown Title"])[0]
            # 使用禁止文字を削除
            for char in forbidden_chars:
                title = title.replace(char, '')

            if albummode:
                track_number = audio.get("trkn", [(0, 0)])[0][0]  # トラック番号を取得
                album = audio.get("\xa9alb", ["Unknown Album"])[0]  # アルバム名
            else:
                artist = audio.get("\xa9ART", ["Unknown Artist"])[0]
                # 使用禁止文字を削除
                for char in forbidden_chars:
                    artist = artist.replace(char, '')

            # 新しいファイル名を生成
            if albummode:
                new_filename = f"{track_number} {title}.m4a"
            else:
                new_filename = f"{artist}「{title}」.m4a"

            # ファイルをリネーム
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

        else:
            print(f"{filename} does not exist. Skipping...")

    if albummode:
        # フォルダをリネーム
        old_folder_path = os.path.join(os.getcwd(), dirname)
        new_folder_path = os.path.join(os.getcwd(), album)
        os.rename(old_folder_path, new_folder_path)
        print(f"Renamed folder {old_folder_path} to {new_file_path}")


def checkalbumpic(dirname):
    # 検索対象のディレクトリとファイル名
    target_directory = os.path.join(os.getcwd(), dirname)
    file_names = ['cover.jpg', 'cover.jpeg', 'cover.png']

    # 各ファイル名について存在確認を行う
    for file_name in file_names:
        target_path = os.path.join(target_directory, file_name)
        if os.path.exists(target_path):
            print(f"{file_name} exists in {target_directory}")
            return file_name
        else:
            print(
                f"Neither cover.jpg nor cover.png exists in {target_directory}")
            return False


# アルバム用のタグの書き換え
def writealbumtag(dirname, album, artist, year, coverfile):
    # JSONファイルからデータを読み込む
    jsonname = dirname + '_tag.json'
    with open(jsonname, 'r', encoding='utf-8') as file:
        data = json.load(file)

    folder_path = os.path.join(os.getcwd(), dirname)

    cover_path = os.path.join(folder_path, coverfile)

    # ジャケット写真が存在するか確認
    cover_exists = os.path.exists(cover_path)
    if cover_exists:
        with open(cover_path, 'rb') as f:
            cover_data = f.read()
            if coverfile in "jpeg" or coverfile in "jpg":
                cover = MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)
            else:
                cover = MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)

    # 各ファイルに対してメタデータを更新する
    for filename_without_extension, metadata in data.items():
        filename = filename_without_extension + ".m4a"
        file_path = os.path.join(folder_path, filename)

        if not os.path.exists(file_path):
            print(f"{filename} does not exist. Skipping...")
            continue

        audio = MP4(file_path)
        print(filename)
        audio["\xa9nam"] = [metadata["title"]]  # title タグをセット
        audio["\xa9ART"] = artist  # artist タグをセット
        audio["\xa9alb"] = album  # アルバム名を追加
        audio["trkn"] = [(metadata["num"], 0)]  # トラック番号をセット
        audio["\xa9day"] = year

        # ジャケット写真を設定
        if cover_exists:
            audio["covr"] = [cover]

        audio.save()
        print("done")

    print("All files tagged")


if __name__ == '__main__':
    albummode = False
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage (nomal mode)")
        print("python tag_and_rename.py <dir name>")
        print("Usage (album mode)")
        print("python tag_and_rename.py <dir name> album <album name> <artist> <year>")
        print("and you must place cover.jpg or cover.png under <dir name>")
        sys.exit(1)
    dirname = sys.argv[1]
    if len(args) >= 2:
        if str(sys.argv[2]) == "album":
            albummode = True
            print("Album Mode!")
            if len(args) == 5:
                album = str(sys.argv[3])
                artist = str(sys.argv[4])
                year = str(sys.argv[5])
                coverfile = checkalbumpic(dirname)
                if coverfile == False:
                    print(f"cover image is not exist under {dirname}")
            else:
                print("Not enough arguments.")
                sys.exit()

    if albummode:
        writealbumtag(dirname, album, artist, year, coverfile)

    else:
        writetag(dirname)

    rename(dirname, albummode)
