from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import json
import sys
import time
import os
import html
import re
import platform


def startgpt(ver4, profile):

    if platform.system() == 'Windows':
        driver_path = './geckodriver.exe'
    else:
        driver_path = './geckodriver'

    # optionsを使用するやつ
    options = Options()
    options.add_argument("-profile")
    options.add_argument(profile)
    service = Service(executable_path=driver_path)
    driver = webdriver.Firefox(service=service, options=options)

    driver.get('https://chat.openai.com/')
    time.sleep(3)

    # Okey,let's go
    try:
        lets = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/div/div[2]/div/div[4]/button')
        # 存在する場合
        print("let's go!")
        lets.click()
    except NoSuchElementException:
        pass
    # print("OK")
    time.sleep(1)

    # GPT4かの選択
    # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/div[1]/div/div/ul/li[2]/button/div
    # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/div[1]/div/div/ul/li[2]/button/div
    if ver4:
        try:
            select_gpt4 = driver.find_element(
                By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/div[1]/div/div/ul/li[2]/button/div')
            select_gpt4.click()
            print('GPT4 selected')
        except NoSuchElementException:
            print('are you plus???')
            sys.exit()
    time.sleep(1)
    return driver


def chatgpt(driver, input, num):
    output = []

    for i in range(len(input)):
        # 要件の入力
        # //*[@id="prompt-textarea"]
        messeage = driver.find_element(By.XPATH, '//*[@id="prompt-textarea"]')
        messeage.send_keys(input[i])
        time.sleep(0.5)

        # メッセージの送信
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button
        # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button
        send = driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button')
        send.click()
        print(f'send "{input[i]}"')
        time.sleep(5)

        # メッセージ受信完了まで待機
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/div[2]/div/divが存在する→受信中
        # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/div[2]/div/div
        # data-testid="send-button"が存在する→送信完了
        # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/buttonが存在する→受信終了
        end = True
        while end:
            try:
                endd = driver.find_element(
                    By.XPATH, '/html/body/div[1]/div[1]/div[2]/main/div[1]/div[2]/form/div/div[2]/div/button')
                # 存在する場合
                end = False
                print("received!")
            except NoSuchElementException:
                print("waiting...")
                time.sleep(5)

        # 読み取り
        # 1つめ↓
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div
        # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[1]/div/div
        # 2つめ↓
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[4]/div/div/div[2]/div/div[1]/div/div
        # /html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[4]/div/div/div[2]/div/div[1]/div/div
        # 3つめ↓
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[6]/div/div/div[2]/div/div[1]/div/div
        # 4つめ↓
        # /html/body/div[1]/div/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[8]/div/div/div[2]/div/div[1]/div/div
        receive = driver.find_element(
            By.XPATH, f'/html/body/div[1]/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div[{(i+num)*2+2}]/div/div/div[2]/div/div[1]/div/div')
        receive = receive.get_attribute("outerHTML")
        # 見やすく
        receive = receive.replace(
            '<div class="markdown prose w-full break-words dark:prose-invert dark">', '').replace('</div>', '')
        # .replace('<p>', '').replace('</p>', '\n').replace('<pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 gizmo:dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>', '').replace('</span><button class="flex ml-auto gizmo:ml-0 gap-2 items-center"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="icon-sm" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button><div class="p-4 overflow-y-auto">', '')
        soup = BeautifulSoup(receive, 'html.parser')
        #receive = soup.get_text()
        # スクリプトやスタイル要素を削除
        for script in soup(["script", "style"]):
            script.extract()
        # テキストの取得
        receive = soup.get_text()
        # ゼロ幅スペースの削除
        receive = receive.replace('&#8203;', '')
        # 不要なマークアップの削除
        receive = re.sub('&#8203;``【oaicite:1】``&#8203;', '', receive)
        print(receive)
        output.append(receive)
    return(output)


def endgpt(driver):

    # トークを消す
    # /html/body/div[1]/div/div[2]/div[1]/div[1]/div/div/div/nav/div[3]/div/div/span[1]/div[1]/ol/li[1]/a/div[2]/button[2]
    # /html/body/div[1]/div[1]/div[1]/div/div/div/nav/div[3]/div/div/span[1]/div[1]/ol/li[1]/a/div[2]/button[2]
    deleate = driver.find_element(
        By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div/div/nav/div[3]/div/div/span[1]/div[1]/ol/li[1]/a/div[2]/button[2]')
    deleate.click()
    time.sleep(0.5)
    # /html/body/div[5]/div/div/div/div[2]/div/div/button[1]
    # /html/body/div[6]/div/div/div/div[2]/div/div/button[1]
    deleate = driver.find_element(
        By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/button[1]')
    deleate.click()

    time.sleep(5)
    driver.quit()
    print("Chat GPT finish")


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


if __name__ == '__main__':

    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: python gpt_tag.py <dir name>")
        sys.exit(1)
    listname = sys.argv[1]

    # Profileが存在するかどうか？
    if os.path.exists("profile.config"):
        print("config was found")
        with open('profile.config', 'r') as file:
            profile = file.read()
        print(profile)
    else:
        print("!Setup was not done!")
        print("1. You have to setup Firefox.")
        print("2. download geckodriver https://github.com/mozilla/geckodriver/releases and place binary in the same directory as this program")
        print(
            "3. Make Profile for this program. Access about:profiles and make new profile.")
        print("4. Login to ChatGPT with Plus")
        print("5. Get profile path in about:profiles")
        profile = input("6. input path hear:")
        with open('profile.config', 'w') as file:
            file.write(profile)
        print(f"write {profile} to profile.config.")

    filename = listname + '.json'
    jsonlen = 800  # ChatGPTに送るjsonの文字列の量
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
        print(tmp)
        input.append(tmp)

    filename = listname + '_tag.json'
    # ChatGPTでの処理開始
    driver = startgpt(True, profile)  # 開始
    j = 0
    for mes in input:
        send = []
        send.append(mes)
        # ChatGPTへ送る
        output = chatgpt(driver, send, j)
        j = j + 1
        # json抜き出し
        for i in range(len(output)):
            output[i] = extract_json_from_string(output[i])
            # 保存
            output[i] = makejson(output[i], filename)
    # ChatGPTを終了
    endgpt(driver)

    print("All finish!!!")
