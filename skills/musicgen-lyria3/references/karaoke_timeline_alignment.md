# Karaoke & Subtitle Alignment (.srt / .lrc)

When users request synchronized lyrics for karaoke, teleprompters, or subtitles from songs generated with Lyria 3.5, follow this standard automated alignment process.

## 1. Overview

Generated songs have known lyrics saved in `<song>.txt`. Because singing tempos, intros, guitar solos, and pacing vary, transcription via Whisper audio-alignment extracts exact millisecond boundaries for each lyric line.

Supported standard formats:
- **`.srt` (SubRip Subtitles)**: Standard for media players (VLC, QuickTime), YouTube, video editors, and projector slides.
- **`.lrc` (Karaoke Lyrics)**: Standard for music players and karaoke teleprompters with `[mm:ss.xx]` tags.

## 2. Automated Alignment Process (Using Whisper via `uv`)

Run the lightweight Whisper model to extract timestamped segments and word boundaries:

```bash
uv run --with openai-whisper python3 -c '
import whisper
model = whisper.load_model("base")
res = model.transcribe("path/to/song.mp3", language="it", word_timestamps=True)
for seg in res["segments"]:
    print(f"{seg[\"start\"]:6.2f} - {seg[\"end\"]:6.2f} : {seg[\"text\"].strip()}")
'
```

## 3. Formatting Standards

### SRT Format (`.srt`)
```srt
1
00:00:13,500 --> 00:00:17,000
Dicono a Roma che qui c'è il silenzio,

2
00:00:17,000 --> 00:00:20,500
Che questa regione sia solo un miraggio...
```

### LRC Format (`.lrc`)
```lrc
[ti:Song Title]
[ar:Artist Name feat. Google Lyria 3.5]
[length:02:41.41]
[00:13.50]Dicono a Roma che qui c'è il silenzio,
[00:17.00]Che questa regione sia solo un miraggio...
```

## 4. Best Practices for Slide Karaoke

- **Intro & Instrumental breaks**: Always mark instrumentals or guitar solos (e.g. `🎸 [Intro Rock di chitarre...]` or `🎸 [Assolo di chitarra...]`) so singers know when to wait.
- **Sidecar convention**: Always save `.srt` and `.lrc` alongside the audio file with identical basename:
  - `assets/my_song.mp3`
  - `assets/my_song.txt`
  - `assets/my_song.srt`
  - `assets/my_song.lrc`
- **Teleprompter visual styles**: Highlight the active singing line with high-contrast text (`#facc15` gold) and gentle scale (`1.05x`) with smooth auto-scroll to center.
