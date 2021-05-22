<h1 align='center'><a href='https://github.com/mytja/harmonoid-music-bot'>Harmonoid Music Bot</a></h1>
<h4 align='center'>🎵 Music bot for Discord. Supports lyrics, queues & plays using both YT Music & YouTube.</h4>
<p align='center'><a href='https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608'>Invite</a> | <a href='https://discord.com/invite/ZG7Pj9SREG'>Discord</a> | <a href='https://mytja.github.io/harmonoid-music-bot'>Website</a></p>

<table>
  <tr>
    <td><img src='https://github.com/mytja/harmonoid-music-bot/blob/screenshots/1.PNG?raw=true'></img></td>
    <td><img src='https://github.com/mytja/harmonoid-music-bot/blob/screenshots/2.PNG?raw=true'></img></td>
    <td><img src='https://github.com/mytja/harmonoid-music-bot/blob/screenshots/3.PNG?raw=true'></img></td>
  </tr>
</table>

## 💜 Support

You may join our [Discord](https://discord.com/invite/ZG7Pj9SREG) server to provide feedback, report bugs in the bot or just chill.

## 🎵 Invite

To use me in your server, use [this](https://discord.com/oauth2/authorize?client_id=802600265005137980&scope=bot&permissions=36932608) link to invite me.

## 🎹 Commands

<h3>🎵 Playback Commands</h3>
<table>
<thead>
<tr>
<th>Command</th>
<th>Aliases</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>-play   <song name or link></td>
<td>-p</td>
<td>Plays or adds a track to queue from YouTube Music.</td>
</tr>
<tr>
<td>-playYT <song name or link></td>
<td>-py</td>
<td>Plays or adds a track to queue from YouTube.</td>
</tr>
<tr>
<td>-pause</td>
<td></td>
<td>Pauses playback.</td>
</tr>
<tr>
<td>-resume</td>
<td></td>
<td>Resumes playback.</td>
</tr>
<tr>
<td>-togglePlayback</td>
<td>-pp</td>
<td>Switches between pause &amp; play states.</td>
</tr>
</tbody>
</table>
<br>
<h3>📑 Queue Commands</h3>
<table>
<thead>
<tr>
<th>Command</th>
<th>Aliases</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>-queue</td>
<td>-q</td>
<td>Displays the current queue.</td>
</tr>
<tr>
<td>-next</td>
<td>-n</td>
<td>Jumps to next track in the queue.</td>
</tr>
<tr>
<td>-back</td>
<td>-b</td>
<td>Jumps to previous track in the queue.</td>
</tr>
<tr>
<td>-jump   <position></td>
<td>-j</td>
<td>Jumps to specific track in the queue based on its position.</td>
</tr>
<tr>
<td>-delete <position></td>
<td>-d</td>
<td>Removes track from the queue from the given position.</td>
</tr>
<tr>
<td>-clear</td>
<td>-c</td>
<td>Clears the queue.</td>
</tr>
</tbody>
</table>
<br>
<h3>🧰 Utility Commands</h3>
<table>
<thead>
<tr>
<th>Command</th>
<th>Aliases</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>-lyrics     <song name></td>
<td>-l</td>
<td>Shows lyrics of a track.</td>
</tr>
<tr>
<td>-lyricsSend <song name></td>
<td>-ls</td>
<td>Sends lyrics of a track in a TXT file.</td>
</tr>
<tr>
<td>-changeChannel <voice channel name></td>
<td>-cc</td>
<td>Changes voice channel where music should be played.</td>
</tr>
</tbody>
</table>
<br>
<h3>📖 Other Commands</h3>
<table>
<thead>
<tr>
<th>Command</th>
<th>Aliases</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td>-status</td>
<td>-s</td>
<td>Displays bot's statistics.</td>
</tr>
<tr>
<td>-about</td>
<td>-a</td>
<td>Displays information about bot.</td>
</tr>
</tbody>
</table>
<br>

## 🔐 Deploy Personally

You can deploy this bot on Heroku or on a self hosted machine.

#### Deploying to Heroku
- Create an account on Heroku if you don't have it yet
- Create an app
- Create a fork of our repo on GitHub & Deploy it on Heroku
- Get a Discord Bot Token from Discord
- Add a secret key called DISCORD_TOKEN with value of a discord token, you got earlier, to Heroku app
- Flip a toggle switch on main page of your app

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## ⭐ Acknowledgements
- [Danny](https://github.com/Rapptz) for [discord.py](https://github.com/Rapptz/discord.py)
- [sigmatics](https://github.com/sigma67) for [ytmusicapi](https://github.com/sigma67/ytmusicapi)
- [alexmercerind](https://github.com/alexmercerind) for [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
- [PyTube](https://github.com/pytube) for [PyTube](https://github.com/pytube/pytube)
- [Encode](https://github.com/encode) for [httpx](https://github.com/encode/httpx)
- [Tin Tvrtković](https://github.com/Tinche) for [aiofiles](https://github.com/Tinche/aiofiles)
- [Python Cryptographic Authority](https://github.com/pyca) for [PyNaCl](https://github.com/pyca/pynacl/)

## Disclaimer
Note, that this bot is strictly intended for personal & non-commercial use.
