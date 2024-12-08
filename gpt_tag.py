from bs4 import BeautifulSoup
import json
import sys
import os
import html

# jsonファイルの読み込み
def readjson(filename):
    # データを読み込む
    with open(filename, 'r', encoding='utf-8') as f:
        jsonlist = json.load(f)
    return jsonlist

# jsonファイルの比較
def checkjson(filename, input_data):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            output_data = json.load(f)
    else:
        output_data = []

    jsonlist = {key: value for key,
                value in input_data.items() if key not in output_data}
    return jsonlist

# jsonのjsonlen文字ずつへの分割
def splitjson(jsonlist, jsonlen):
    data = jsonlist

    current_data = {}
    current_length = 0
    output = []

    for key, value in data.items():
        temp_data = {key: value}
        temp_length = len(json.dumps(temp_data, ensure_ascii=False))

        if current_length + temp_length <= jsonlen:
            current_data[key] = value
            current_length += temp_length
        else:
            # Add the current data to the output list
            output.append(current_data)

            # Start a new current_data
            current_data = {key: value}
            current_length = temp_length

    # Add any remaining data to the output list
    if current_data:
        output.append(current_data)

    return output

# ChatGPTの出力からJson形式を取得
def extract_json_from_string(s: str) -> dict:
    for i in range(len(s)):
        for j in range(i, len(s)):
            try:
                potential_json = s[i:j+1]
                output = json.loads(potential_json)
                return output
            except json.JSONDecodeError:
                continue
    return None

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
        # HTMLエンティティをデコード
        input = html.unescape(input)
        new_data = json.loads(input)
    elif isinstance(input, dict):
        # 各キー・値のペアでHTMLエンティティをデコード
        new_data = {html.unescape(key): html.unescape(value)
                    for key, value in input.items()}

    # 新しいデータを既存のデータに結合
    combined_data = {**existing_data, **new_data}  # 2つの辞書を結合

    # 結合したデータをoutput.jsonに書き込む
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, ensure_ascii=False, indent=4)

    print(f"write {filename}")

def read_chatgpt_retrun():
    message = []
    print('To terminate input, enter a blank line.')
    for line in sys.stdin:
        line = line.strip()
        if line == "":
            break
        message.append(line)

    # 入力された複数行を1つの文字列に結合
    all_message = "\n".join(message)
    return all_message

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python gpt_tag.py <dir name>")
        sys.exit(1)
    listname = sys.argv[1]

    filename = listname + '.json'
    jsonlen = 1000  # ChatGPTに送るjsonの文字列の量
    jsonlist = readjson(filename)  # jsonファイルの読み出し
    print(f"read {filename}")
    print(f"read music num:{len(jsonlist)}")
    filename = listname + '_tag.json'
    jsonlist = checkjson(filename, jsonlist)  # 比較
    print(f"check {filename}")
    if len(jsonlist) == 0:
        print("All file was already asked")
        sys.exit(1)
    jsonlist = splitjson(jsonlist, jsonlen)  # 分割
    input = []
    for i in range(len(jsonlist)):
        tmp = """以下のjsonファイルはYouTubeでのチャンネル名とタイトルから
"ID":{
    "num": number
    "uploader": チャンネル名,
    "title": タイトル
}
になっています。このファイル名から曲名、アーティスト名を推測して、
"ID":{
    "num": number
    "title": 曲名,
    "artist": アーティスト名
}
とjson形式で答えてください。なお、featやftとかで示される歌手名は曲名の方に入れてください。
回答は「以下がjsonファイルです。」で始めてください。
"""
        tmp = tmp + str(jsonlist[i])
        #print(tmp)
        input.append(tmp)

    filename = listname + '_tag.json'
    j = 0
    for message in input:
        print('Copy the message below and paste ChatGPT response here.')
        print()
        print()
        print(message)
        print()
        print()
        output = []
        output.append(read_chatgpt_retrun())
        j += 1
        # json抜き出し
        for i in range(len(output)):
            output[i] = extract_json_from_string(output[i])
            # 保存
            output[i] = makejson(output[i], filename)

    print("All finish!!!")
