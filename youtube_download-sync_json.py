import sys
import yt_dlp
import os
import json


# 再生リストの情報を取得する。
def extract_playlist_info(playlist_url):
    url_list = []
    id_list = []
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)
        list_name = info_dict.get('title', None)  # 再生リストの名前を取得
        print(f"get data of {list_name}")

        if 'entries' in info_dict:
            for entry in info_dict['entries']:
                if entry is None:
                    continue
                video_id = entry.get('id')
                title = entry.get('title')
                url = entry.get('url')
                print(f"ID: {video_id}, Title: {title}")
                url_list.append(url)
                id_list.append(video_id)

    return list_name, url_list, id_list


# jsonファイルと比較して、既にダウンロード済みか確認する。
def check_playlist(video_list):
    list_name = video_list[0]
    url_list = video_list[1]
    id_list = video_list[2]
    num_list = list(range(1, len(id_list)+1))  # プレイリストでの番号

    new_url_list = []
    new_num_list = []
    filename = list_name + '.json'

    # ファイルが存在するか確認
    if not os.path.exists(filename):
        print("This play list had not downloaded")
        return list_name, url_list, num_list

    try:
        # JSONファイルを開く
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # キーが存在するか確認
        for i in range(len(id_list)):
            if id_list[i] in data:
                print(f"{id_list[i]} already downloaded")
            else:
                print(f"{id_list[i]} will download")
                new_url_list.append(url_list[i])
                new_num_list.append(num_list[i])
    except json.JSONDecodeError:
        return f"Error: Failed to decode JSON from {filename}."
    return list_name, new_url_list, new_num_list


def download_playlist(video_list):
    list_name = video_list[0]
    url_list = video_list[1]
    num_list = video_list[2]
    filename = list_name + '.json'

    if not os.path.exists(list_name):
        os.makedirs(list_name)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '256',
        }, {
            'key': 'EmbedThumbnail',  # サムネイルを埋め込むためのポストプロセッサ
        }],
        'outtmpl': os.path.join(list_name, '%(id)s'),
        'writethumbnail': True,  # サムネイルをダウンロードするためのオプション
        'ignoreerrors': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        count = 0
        for url in url_list:
            info = ydl.extract_info(url, download=True)
            if info is None:
                print(f"Error while downloading {[url]}")
                continue

            # ダウンロード
            ydl.download([url])

            video_info = [info['id'], num_list[count],
                          info['uploader'],  info['title']]

            # json形式に
            video_dict = {
                video_info[0]: {
                    "num":  video_info[1],
                    "uploader": video_info[2],
                    "title": video_info[3]
                }
            }
            # 書き込み
            makejson(video_dict, filename)

            print(f"{count+1}/{len(url_list)} Downloaded")
            print(
                f"ID: {info['id']}, Title: {info['title']}")
            count += 1


# 既に存在するjsonファイルを読み込みjsonファイルを追記
def makejson(input, filename):
    # 既に存在するjsonからデータを読み込む
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}

    # inputが文字列型であるか確認し、JSONデータを読み込む
    if isinstance(input, str):
        new_data = json.loads(input)
    elif isinstance(input, dict):
        new_data = input

    # 新しいデータを既存のデータに結合
    combined_data = {**existing_data, **new_data}  # 2つの辞書を結合

    # 結合したデータをoutput.jsonに書き込む
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, ensure_ascii=False, indent=4)

    print(f"write {filename}")


# jsonファイルの作成
def addjson(video_list):
    print(video_list[0])
    output_file = video_list[0] + '.json'
    print(output_file)
    # 既存のJSONファイルを読み込む
    existing_files = set()
    if os.path.exists(output_file):
        with open(output_file, 'r') as infile:
            existing_files = set(json.load(infile))

    # 指定されたフォルダ内の.m4aファイルをリストアップ
    file_list = set(f for f in os.listdir(video_list[0]) if f.endswith('.m4a'))

    # 既存のリストと新しいリストを結合
    combined_list = list(existing_files.union(file_list))

    # JSON形式で出力
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(combined_list, outfile, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    limit = 100  # 一度にダウンロードする量
    args = sys.argv[1:]

    if len(args) < 1:
        print("Usage: python  youtube_download-sync.py <YouTube Playlist URL> <download limit>")
        sys.exit(1)
    elif len(args) == 2:
        limit = int(args[1])
    playlist_url = sys.argv[1]
    print(f"Download limit:{limit}")

    # 返り値は[list_name, url_list, id_list]
    video_list = extract_playlist_info(playlist_url)

    # jsonファイルと比較[list_name, new_url_list, new_num_list]
    video_list = check_playlist(video_list)

    # video_listがlimit以下の長さになるようにする
    video_list = [sublist[:limit] for sublist in video_list]
    print("↓will be download")
    for i in range(len(video_list[1])):
        print(f"{video_list[2][i]} URL:{video_list[1][i]}")

    download_playlist(video_list)  # ダウンロード
    # addjson(video_list)  # jsonに書き出し
