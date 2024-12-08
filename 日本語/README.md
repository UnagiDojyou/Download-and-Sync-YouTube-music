# Download-and-Sync-YouTube-music
YouTubeの再生リストをダウンロードし、ChatGPTを使用してアーティスト・タイトルを判定します。その後タグ付け・ファイル変更を行います。<br>
ChatGPTに判定させるために、手動でのコピー・ペーストが必要です。
再生リストに新たな楽曲を加えた場合はもう一度実行すれば追加分だけダウンロード・タグ付け・ファイル名変更がされます。<br>

# 事前準備
1. ライブラリのインストール<br>
`pip install -r requirements.txt`<br>
多分これで足ります。
2. FFmpegのインストール<br>
既にインストール済みの人は大丈夫です。

# 使い方(一般的な再生リスト)
1. YouTubeの再生リストのURLをコピー<br>
https://www.youtube.com/playlist?list="ID"
みたいな感じだと思います。再生リストは公開設定にしてください。
2. ダウンロード<br>
`python youtube_download-sync_json.py <URL> (download limit)`<br>
でダウンロードが開始します。download limitは一度のコマンドでダウンロードする最大の数です。未指定では100になっています。
3. ChatGPTでアーティスト・タイトルの取得<br>
`python gpt_tag.py <play list name>`<br>
でChatGPTへのコマンドの生成と、その貼り付けを行います。<br>
`Copy the message below and paste ChatGPT response here.`
と
`To terminate input, enter a blank line.`
の間の部分をコピーして、ChatGPTに貼り付けし、JSON部分の返答をコンソールに貼り付け、Enterを押します。<br>
これを終わるまで繰り返します。
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