# Download-and-Sync-YouTube-music
YouTubeの再生リストをダウンロードし、ChatGPTを使用してアーティスト・タイトルを自動で判定します。その後タグ付け・ファイル変更を行います。<br>
再生リストに新たな楽曲を加えた場合はもう一度実行すれば追加分だけダウンロード・タグ付け・ファイル名変更がされます。<br>
アーティスト・タイトルの判定にChatGPT-4を使用するのでPlusを契約していないと使えません。

# 事前準備
1. ライブラリのインストール<br>
`pip install -r requirements.txt`<br>
多分これで足ります。
2. FireFoxのインストール<br>
既にインストール済みの人は大丈夫です。
3. FireFoxでプロファイルの作成<br>
about:profilesでこのプログラム用のプロファイルを作成し、そのプロファイルでChatGPTにログインしてください。また、アルファ機能のロケールをON(アルファに参加する)にしてください。
4. プロファイルのパスをメモ<br>
about:profilesで作成したプロファイルのパスをコピーしてください。
5. geckodriverのダウンロード<br>
[こちら](https://github.com/mozilla/geckodriver/releases)からgeckodriverをダウンロードしてgpt_tag.pyと同じフォルダに置いてください。
6. プロファイルの登録<br>
`python gpt_tag.py test`
を実行し、プロファイルの登録を行ってください。

# 使い方(一般的な再生リスト)
1. YouTubeの再生リストのURLをコピー<br>
https://www.youtube.com/playlist?list="ID"
みたいな感じだと思います。再生リストは公開設定にしてください。
2. ダウンロード<br>
`python youtube_download-sync_json.py <URL> (download limit)`<br>
でダウンロードが開始します。download limitは一度のコマンドでダウンロードする最大の数です。未指定では100になっています。
3. ChatGPTでアーティスト・タイトルの取得<br>
`python gpt_tag.py <play list name>`<br>
でChatGPTを起動して、タイトル、チャンネル名からアーティスト・タイトルを判定させます。
4. タグ付け、ファイル名変更<br>
`python tag_and_rename.py <play list name>`<br>
でChatGPTで判定したタグをタグ付けし、名前をartist「title」.m4aに変更します。

# 使い方(アルバムの再生リスト)
再生リストがアルバムとなっている用です。ジャケット写真を指定、トラック番号、リリース年の追加、専用のファイル命名ができます。<br>
1. 使い方(一般的な再生リスト)の1~3と同じです。
2. ジャケット写真のダウンロード<br>
プレイリスト名のフォルダ内にジャケット写真を保存してください。cove.jpg、cover.pngのどちらかで保存してくだいさい。
3. タグ付け、ファイル名変更<br>
`python tag_and_rename.py <play list name> album <album name> <artist> <year>`<br>
出力名は、tracknum.title.m4aです。