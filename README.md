# Download-and-Sync-YouTube-music
Download YouTube playlists and use ChatGPT to automatically detect the artist and title. It then tags and modifies the files. <br>
If you add new songs to the playlist, running it again will only download, tag, and rename the new additions. <br>
ChatGPT-4 is used to identify the artist and title, so it won't work without a Plus subscription.

# Prerequisites
1. Library installation<br>
`pip install -r requirements.txt`<br>
This should suffice.
2. Install Firefox<br>
If you've already installed it, you're good to go.
3. Create a profile in Firefox<br>
Create a profile for this program in about:profiles and log into ChatGPT with that profile. Also, turn the locale of the alpha feature to ON (participate in the alpha).
4. Note down the profile path<br>
Copy the path of the profile you created in about:profiles.
5. Download geckodriver<br>
Download geckodriver from [here](https://github.com/mozilla/geckodriver/releases) and place it in the same folder as gpt_tag.py.
6. Register your profile<br>
Execute `python gpt_tag.py test` and register your profile.

# Usage (for regular playlists)
1. Copy the URL of the YouTube playlist<br>
It's probably something like https://www.youtube.com/playlist?list="ID". Make sure the playlist is set to public.
2. Download<br>
Start the download with `python youtube_download-sync_json.py <URL> (download limit)`<br>
The download limit is the maximum number of downloads in one command. If not specified, it defaults to 100.
3. Fetch artist & title with ChatGPT<br>
Launch ChatGPT with `python gpt_tag.py <play list name>` and determine the artist and title from the title and channel name.
4. Tag and rename files<br>
Use `python tag_and_rename.py <play list name>` to tag the files with the data determined by ChatGPT and rename them to artist「title」.m4a.

# Usage (for album playlists)
This is for playlists that are set up as albums. You can specify album covers, add track numbers, release year, and use a dedicated file naming scheme.<br>
1. Steps 1-3 are the same as for regular playlists.
2. Download the album cover<br>
Save the album cover inside the playlist's folder. Please save it as either cover.jpg or cover.png.
3. Tag and rename files<br>
Use `python tag_and_rename.py <play list name> album <album name> <artist> <year>`<br>
The output name is tracknum.title.m4a.
