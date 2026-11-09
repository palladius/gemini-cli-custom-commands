#!/usr/bin/env python3
"""
================================================================================
🎹🥁 ANALYZE_METER_TIMELINE.PY — Musical Meter (4/4, 3/4, 5/8, 7/8) & HTML DAW
================================================================================

🤖 DEAR AI AGENT — QUICK HOWTO & INTERNAL DSP ARCHITECTURE:
If the user asks "what time signature is this song actually in?", "did Lyria
cheat with 4/4 instead of 7/8?", or "show me an interactive multitrack timeline
where I can click on meter transitions", run this script!

🚀 QUICK HOWTO (1-Liner — ffmpeg handles everything automatically):
  # Pass any MP3 (or WAV): it auto-detects the matching .srt sidecar, extracts
  # a temporary 48kHz WAV via ffmpeg, encodes a lightweight 48kbps MP3 (~1MB)
  # for inline base64 HTML embedding, and outputs <stem>_meter.json + <stem>_meter_player.html!
  python3 scripts/analyze_meter_timeline.py --mp3 path/to/song.mp3

  # Or specify all paths explicitly:
  python3 scripts/analyze_meter_timeline.py \\
      --wav song.wav --mp3 song.mp3 --srt song.srt \\
      --out-json song_meter.json --out-html song_meter_player.html \\
      --title "Can-Utility Take 3"

🔬 HOW THE DSP ENGINE WORKS (Zero external Python dependencies — stdlib only!):
1. TRANSIENT EXTRACTION (50 Hz / 20 ms ONSET FLUX):
   Reads 16-bit PCM audio from the 48 kHz WAV file and computes mean amplitude
   energy every 20 ms (50 frames/sec). Applies a half-wave rectified first-order
   difference:
       Flux[t] = max(0, Energy[t] - Energy[t-1])
   This isolates percussive attacks (kick, snare, 12-string acoustic plucks)
   while ignoring sustained pads (e.g., Mellotron strings or choral swells).

2. 3-BAND SPECTRAL STEM DECOMPOSITION (TIME-DOMAIN IIR FILTER BANK):
   Runs cascaded one-pole IIR filters on the decimated signal to extract 3
   distinct frequency-band envelopes (rendered as 3 DAW tracks):
   - 🥁 LOW (< 260 Hz):      Bass Pedals (Rutherford style) & Kick/Toms
   - 🎹🎤 MID (260-2800 Hz): Lead Vocals (Gabriel), Mellotron M400 & Hammond Organ
   - 🎸 HIGH (> 2800 Hz):    12-String Acoustic Fingerpicking, Hi-Hats & Cymbals

3. SLIDING-WINDOW HARMONIC AUTOCORRELATION (TEMPOGRAM & METER CLASSIFIER):
   Slides an 8.0-second analysis window with a 1.0-second hop across the entire
   track. At each second, computes the Normalized Autocorrelation Function (ACF):
       R(lag) = sum(Flux[t] * Flux[t + lag]) / sum(Flux[t]^2)
   Locates the fundamental eighth-note subdivision pulse (delta_8, 160-410 ms)
   and compares harmonic periodicity energy across integer multiples of delta_8:
   - 🔵 Binary (4/4, 2/4):       multiples [2, 4, 8] * delta_8
   - 🟢 Ternary (3/4, 6/8):      multiples [3, 6, 9] * delta_8
   - 🟣 Odd 5/8 (Aksak 2+3):     multiples [5, 10]   * delta_8
   - 🟠 Odd 7/8 (Aksak 2+2+3):   multiples [7, 14]   * delta_8

4. SMOOTHING, SEGMENTATION & KARAOKE (.SRT) ALIGNMENT:
   Applies a 5-second moving-average smoother and merges short islands (< 6s)
   into clean structural Meter Transition Blocks (e.g. [0:00->1:08 4/4],
   [1:08->1:14 3/4], [2:31->2:43 7/8]), cross-referencing with .srt subtitles.

5. SELF-CONTAINED INTERACTIVE MULTITRACK HTML DAW (WEB AUDIO API):
   Produces a single standalone .html file (with base64-encoded 48kbps MP3 data
   URI) featuring:
   - Clickable Transition Pills & Meter Blocks (with -2s Pre-Roll toggle!)
   - Real-time WebAudio BiquadFilterNode (Lowpass / Bandpass / Highpass) SOLO
     and MUTE buttons for Bass/Drums, Mellotron/Vocals, and 12-String/Hi-Hats!
   - Live Smart Metronome Synthesizer (OscillatorNode at 1046Hz on Beat 1 and
     523Hz on subdivisions) that dynamically switches between 4/4, 3/4, and 7/8!
================================================================================
"""

import argparse
import base64
import json
import math
import os
import re
import struct
import subprocess
import tempfile
import wave


def parse_srt(srt_path: str):
  if not srt_path or not os.path.exists(srt_path):
    return []
  with open(srt_path, "r", encoding="utf-8") as f:
    raw = f.read().strip()
  cues = []
  for block in re.split(r"\n\s*\n", raw):
    lines = [l.strip() for l in block.strip().splitlines() if l.strip()]
    if len(lines) >= 3 and "-->" in lines[1]:
      m = re.match(
          r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)",
          lines[1],
      )
      if m:
        g = [int(x) for x in m.groups()]
        start = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000.0
        end = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000.0
        text = " ".join(lines[2:])
        is_sec = (
            text.startswith("♪ [")
            or text.startswith("[")
            or "🎸" in text
            or "🎹" in text
        )
        cues.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "text": text,
            "is_section": is_sec,
        })
  return cues


def compute_multiband_onset_flux(wav_path: str, hop_sec: float = 0.02):
  w = wave.open(wav_path, "rb")
  sr = w.getframerate()
  nch = w.getnchannels()
  nframes = w.getnframes()
  duration = nframes / float(sr)

  hop_samples = int(sr * hop_sec)
  raw = w.readframes(nframes)
  w.close()

  stride_bytes = hop_samples * nch * 2
  total_hops = len(raw) // stride_bytes

  energies = []
  low_env = []
  mid_env = []
  high_env = []

  # 1-pole IIR filter states on decimated 8kHz mono stream
  lp_state = 0.0
  bp_state = 0.0
  alpha_low = 0.18   # ~260 Hz cutoff
  alpha_mid = 0.65   # ~2.8 kHz cutoff

  for h in range(total_hops):
    offset = h * stride_bytes
    samples = struct.unpack_from("<" + "h" * (hop_samples * nch), raw, offset)
    mono = samples[0 :: (6 * nch)]

    e_tot = 0.0
    e_low = 0.0
    e_mid = 0.0
    e_high = 0.0
    for x in mono:
      fx = float(x)
      lp_state += alpha_low * (fx - lp_state)
      bp_state += alpha_mid * (fx - bp_state)
      low_val = lp_state
      mid_val = bp_state - lp_state
      high_val = fx - bp_state

      e_tot += abs(fx)
      e_low += abs(low_val)
      e_mid += abs(mid_val)
      e_high += abs(high_val)

    n_m = max(1, len(mono))
    energies.append(e_tot / n_m)
    low_env.append(e_low / n_m)
    mid_env.append(e_mid / n_m)
    high_env.append(e_high / n_m)

  # Half-wave rectified broadband transient onset flux
  flux = [0.0]
  for i in range(1, len(energies)):
    diff = energies[i] - energies[i - 1]
    flux.append(diff if diff > 0 else 0.0)

  return flux, energies, low_env, mid_env, high_env, duration, hop_sec


def analyze_sliding_meter(
    flux,
    energies,
    low_env,
    mid_env,
    high_env,
    duration,
    hop_sec=0.02,
    win_sec=8.0,
    step_sec=1.0,
):
  fps = int(round(1.0 / hop_sec))  # 50 Hz
  win_frames = int(win_sec * fps)
  num_steps = int(math.ceil(duration / step_sec))

  max_e = max(energies) if energies else 1.0
  max_l = max(low_env) if low_env else 1.0
  max_m = max(mid_env) if mid_env else 1.0
  max_h = max(high_env) if high_env else 1.0

  timeline = []

  for s in range(num_steps):
    center_t = s * step_sec
    start_f = max(0, int((center_t - win_sec / 2.0) * fps))
    end_f = min(len(flux), start_f + win_frames)
    if end_f - start_f < fps * 3:
      start_f = max(0, end_f - fps * 4)

    seg = flux[start_f:end_f]
    mean_v = sum(seg) / max(1, len(seg))
    seg_z = [v - mean_v for v in seg]

    def acf(lag):
      if lag <= 0 or lag >= len(seg_z):
        return 0.0
      n = len(seg_z) - lag
      return sum(seg_z[i] * seg_z[i + lag] for i in range(n)) / float(n)

    r0 = max(1e-9, sum(v * v for v in seg_z) / float(len(seg_z)))

    best_e8 = 18.5
    best_e8_score = -1.0
    for candidate_frames in [x * 0.5 for x in range(16, 42)]:
      l1 = int(round(candidate_frames))
      l2 = int(round(candidate_frames * 2))
      sc = 0.6 * (acf(l1) / r0) + 0.4 * (acf(l2) / r0)
      if sc > best_e8_score:
        best_e8_score = sc
        best_e8 = candidate_frames

    def multi_score(multipliers):
      vals = []
      for m in multipliers:
        lag = int(round(best_e8 * m))
        pk = max(acf(lag - 1), acf(lag), acf(lag + 1)) / r0
        vals.append(max(0.0, pk))
      return sum(vals) / len(vals)

    raw_4_4 = multi_score([2, 4, 8])
    raw_3_4 = multi_score([3, 6, 9])
    raw_5_8 = multi_score([5, 10])
    raw_7_8 = multi_score([7, 14])

    total_m = max(1e-6, raw_4_4 + raw_3_4 + raw_5_8 + raw_7_8)
    p_4_4 = round(raw_4_4 / total_m, 3)
    p_3_4 = round(raw_3_4 / total_m, 3)
    p_5_8 = round(raw_5_8 / total_m, 3)
    p_7_8 = round(raw_7_8 / total_m, 3)

    e_start = max(0, int(center_t * fps))
    e_end = min(len(energies), int((center_t + 1.0) * fps))
    span = max(1, e_end - e_start)

    quarter_sec = (best_e8 * 2.0) * hop_sec
    bpm = round(60.0 / quarter_sec, 1)
    if bpm > 155:
      bpm = round(bpm / 2.0, 1)

    timeline.append({
        "t": s,
        "energy": round(sum(energies[e_start:e_end]) / span / max_e, 3),
        "stem_low": round(sum(low_env[e_start:e_end]) / span / max_l, 3),
        "stem_mid": round(sum(mid_env[e_start:e_end]) / span / max_m, 3),
        "stem_high": round(sum(high_env[e_start:e_end]) / span / max_h, 3),
        "bpm": bpm,
        "eighth_ms": round(best_e8 * hop_sec * 1000.0, 1),
        "scores": {
            "4/4": p_4_4,
            "3/4 (6/8)": p_3_4,
            "5/8": p_5_8,
            "7/8": p_7_8,
        },
    })

  for i in range(len(timeline)):
    w_slice = timeline[max(0, i - 2) : min(len(timeline), i + 3)]
    avg = {}
    for k in ["4/4", "3/4 (6/8)", "5/8", "7/8"]:
      avg[k] = round(sum(x["scores"][k] for x in w_slice) / len(w_slice), 3)
    timeline[i]["smoothed"] = avg
    best_k = max(avg.items(), key=lambda x: x[1])[0]
    timeline[i]["meter"] = best_k

  meters = [x["meter"] for x in timeline]
  for _ in range(3):
    for i in range(1, len(meters) - 1):
      if meters[i] != meters[i - 1] and meters[i - 1] == meters[i + 1]:
        meters[i] = meters[i - 1]
    i = 0
    while i < len(meters):
      j = i
      while j < len(meters) and meters[j] == meters[i]:
        j += 1
      if (j - i) < 6 and i > 0:
        for k in range(i, j):
          meters[k] = meters[i - 1]
      i = j

  for i, m in enumerate(meters):
    timeline[i]["meter"] = m

  segments = []
  i = 0
  while i < len(timeline):
    j = i
    m = timeline[i]["meter"]
    while j < len(timeline) and timeline[j]["meter"] == m:
      j += 1
    slice_items = timeline[i:j]
    avg_bpm = round(sum(x["bpm"] for x in slice_items) / len(slice_items), 1)
    avg_conf = round(
        sum(x["smoothed"][m] for x in slice_items) / len(slice_items) * 100, 1
    )
    segments.append({
        "id": len(segments) + 1,
        "start": float(i),
        "end": round(min(duration, float(j)), 2),
        "duration": round(min(duration, float(j)) - float(i), 2),
        "meter": m,
        "bpm": avg_bpm,
        "confidence_pct": avg_conf,
    })
    i = j

  return timeline, segments


def build_html_player(data: dict, audio_b64: str) -> str:
  json_payload = json.dumps(data)
  return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Interactive Multitrack Meter & Time Signature DAW Player -->
  <meta charset="UTF-8" />
  <title>{data['title']} — Meter & Multitrack Timeline</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .meter-44 {{ background: linear-gradient(135deg, #4f46e5, #3b82f6); }}
    .meter-34 {{ background: linear-gradient(135deg, #059669, #10b981); }}
    .meter-78 {{ background: linear-gradient(135deg, #d97706, #ef4444); }}
    .meter-58 {{ background: linear-gradient(135deg, #9333ea, #ec4899); }}
    .playhead-line {{
      position: absolute;
      top: 0;
      bottom: 0;
      width: 2px;
      background: #f43f5e;
      box-shadow: 0 0 8px #f43f5e;
      pointer-events: none;
      z-index: 30;
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--app-foreground)] font-[var(--vscode-font-family)] antialiased p-3 select-none">
  <div class="bg-[var(--app-card)] text-[var(--app-foreground)] border border-[var(--app-border)] rounded-xl p-4 shadow-sm space-y-3">
    <!-- Top Header & Transport Bar -->
    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-[var(--app-border)] pb-2.5">
      <div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400">DSP Autocorrelation DAW</span>
          <h2 class="text-[var(--app-foreground)] font-bold text-base">{data['title']}</h2>
        </div>
        <p class="text-[var(--app-muted-foreground)] text-xs mt-0.5">
          Click any meter block (<code>4/4</code>, <code>3/4 (6/8)</code>, <code>5/8</code>, <code>7/8</code>) or stem lane to jump to that transition • Toggle <b>Solo/Mute</b> or <b>Live Metronome Click</b>!
        </p>
      </div>

      <div class="flex items-center gap-2">
        <button id="btnPlay" class="px-3.5 py-1.5 rounded-lg font-semibold text-xs bg-indigo-600 hover:bg-indigo-500 text-white shadow transition flex items-center gap-1.5">
          <span id="playIcon">▶</span> <span id="playText">Play</span>
        </button>
        <button id="btnPreroll" class="px-2.5 py-1.5 rounded-lg font-medium text-xs border border-[var(--app-border)] hover:bg-[var(--app-muted)] transition" title="Start playback 2 seconds before the selected meter transition so you can hear the shift!">
          ⏮ Pre-Roll -2s: <span id="prerollState" class="font-bold text-emerald-400">ON</span>
        </button>
        <button id="btnMetro" class="px-2.5 py-1.5 rounded-lg font-medium text-xs border border-[var(--app-border)] hover:bg-[var(--app-muted)] transition">
          ⏱️ Metronome Click: <span id="metroState" class="font-bold text-amber-400">ON</span>
        </button>
        <div class="px-2.5 py-1 rounded bg-[var(--app-muted)] text-xs font-mono">
          <span id="curTime">0:00.0</span> / <span id="totTime">{int(data['duration']//60)}:{data['duration']%60:04.1f}</span>
          <span id="liveBadge" class="ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold bg-indigo-600 text-white">4/4 • 81 BPM</span>
        </div>
      </div>
    </div>

    <!-- Live Beat Counter & Current Lyric Banner -->
    <div class="flex items-center justify-between gap-3 px-3 py-2 rounded-lg bg-[var(--app-muted)] border border-[var(--app-border)]">
      <div class="flex items-center gap-2 min-w-[185px]">
        <span class="text-[11px] uppercase tracking-wider text-[var(--app-muted-foreground)] font-semibold">Bar Pulses:</span>
        <div id="beatDots" class="flex items-center gap-1"></div>
      </div>
      <div id="lyricDisplay" class="text-xs font-medium truncate text-center flex-1 italic">
        🎸 Click any transition pill or meter block below to audition the time-signature shift!
      </div>
      <div class="text-[11px] font-mono text-[var(--app-muted-foreground)] hidden sm:block" id="confDisplay">
        ACF Conf: --%
      </div>
    </div>

    <!-- Transition Pills (Quick Jump Buttons) -->
    <div class="flex flex-wrap gap-1.5" id="segmentPills"></div>

    <!-- Interactive Multitrack Timeline Container -->
    <div class="relative border border-[var(--app-border)] rounded-lg overflow-hidden bg-black/20" id="timelineContainer">
      <div id="playhead" class="playhead-line" style="left: 0%;"></div>

      <!-- Time Ruler -->
      <div class="h-5 border-b border-[var(--app-border)] relative text-[10px] font-mono text-[var(--app-muted-foreground)] flex items-center" id="timeRuler"></div>

      <!-- LANE 1: Time Signature Transition Blocks -->
      <div class="flex items-stretch border-b border-[var(--app-border)] h-9">
        <div class="w-36 shrink-0 px-2 flex items-center justify-between bg-[var(--app-card)] border-r border-[var(--app-border)] text-[11px] font-semibold">
          <span>📐 Meter (ACF)</span>
          <span class="text-[9px] text-[var(--app-muted-foreground)]">Click Jump</span>
        </div>
        <div class="relative flex-1 h-full cursor-pointer" id="meterLane"></div>
      </div>

      <!-- LANE 2: Stem 1 — Bass Pedals & Drums (< 260 Hz) -->
      <div class="flex items-stretch border-b border-[var(--app-border)] h-9">
        <div class="w-36 shrink-0 px-2 flex items-center justify-between bg-[var(--app-card)] border-r border-[var(--app-border)] text-[11px]">
          <span class="truncate font-medium">🥁 Bass & Drums</span>
          <div class="flex gap-1">
            <button onclick="toggleStem('low', 'mute')" id="mute-low" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-red-500/20" title="Mute Low Stem (<260Hz)">M</button>
            <button onclick="toggleStem('low', 'solo')" id="solo-low" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-amber-500/20" title="Solo Low Stem (<260Hz)">S</button>
          </div>
        </div>
        <div class="relative flex-1 h-full cursor-pointer" onclick="seekFromEvent(event)">
          <canvas id="canvasLow" class="w-full h-full block"></canvas>
        </div>
      </div>

      <!-- LANE 3: Stem 2 — Mellotron Strings, Hammond & Vocals (260 Hz - 2.8 kHz) -->
      <div class="flex items-stretch border-b border-[var(--app-border)] h-9">
        <div class="w-36 shrink-0 px-2 flex items-center justify-between bg-[var(--app-card)] border-r border-[var(--app-border)] text-[11px]">
          <span class="truncate font-medium">🎹🎤 Mellotron/Vox</span>
          <div class="flex gap-1">
            <button onclick="toggleStem('mid', 'mute')" id="mute-mid" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-red-500/20" title="Mute Mid Stem (260-2800Hz)">M</button>
            <button onclick="toggleStem('mid', 'solo')" id="solo-mid" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-amber-500/20" title="Solo Mid Stem (260-2800Hz)">S</button>
          </div>
        </div>
        <div class="relative flex-1 h-full cursor-pointer" onclick="seekFromEvent(event)">
          <canvas id="canvasMid" class="w-full h-full block"></canvas>
        </div>
      </div>

      <!-- LANE 4: Stem 3 — 12-String Acoustic Guitar & Cymbals (> 2.8 kHz) -->
      <div class="flex items-stretch border-b border-[var(--app-border)] h-9">
        <div class="w-36 shrink-0 px-2 flex items-center justify-between bg-[var(--app-card)] border-r border-[var(--app-border)] text-[11px]">
          <span class="truncate font-medium">🎸 12-String/Hats</span>
          <div class="flex gap-1">
            <button onclick="toggleStem('high', 'mute')" id="mute-high" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-red-500/20" title="Mute High Stem (>2.8kHz)">M</button>
            <button onclick="toggleStem('high', 'solo')" id="solo-high" class="px-1.5 py-0.5 rounded text-[9px] font-bold border border-[var(--app-border)] hover:bg-amber-500/20" title="Solo High Stem (>2.8kHz)">S</button>
          </div>
        </div>
        <div class="relative flex-1 h-full cursor-pointer" onclick="seekFromEvent(event)">
          <canvas id="canvasHigh" class="w-full h-full block"></canvas>
        </div>
      </div>

      <!-- LANE 5: Continuous Meter Probability Curve -->
      <div class="flex items-stretch h-11">
        <div class="w-36 shrink-0 px-2 flex flex-col justify-center bg-[var(--app-card)] border-r border-[var(--app-border)] text-[10px]">
          <span class="font-semibold">📈 Probabilities</span>
          <span class="text-[9px] text-[var(--app-muted-foreground)]">🔵4/4 🟢3/4 🟣5/8 🟠7/8</span>
        </div>
        <div class="relative flex-1 h-full cursor-pointer" onclick="seekFromEvent(event)">
          <canvas id="canvasProbs" class="w-full h-full block"></canvas>
        </div>
      </div>
    </div>

    <audio id="audioEl" preload="auto" src="data:audio/mp3;base64,{audio_b64}"></audio>
  </div>

  <script>
    const DATA = {json_payload};
    const DURATION = DATA.duration;
    const audio = document.getElementById('audioEl');
    let prerollEnabled = true;
    let metroEnabled = true;
    let stemState = {{
      low: {{ mute: false, solo: false }},
      mid: {{ mute: false, solo: false }},
      high: {{ mute: false, solo: false }}
    }};

    let audioCtx = null;
    let gainLow = null, gainMid = null, gainHigh = null;
    let lastBeatIndex = -1;

    function initWebAudio() {{
      if (audioCtx) return;
      const AC = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AC();
      const source = audioCtx.createMediaElementSource(audio);

      const fLow = audioCtx.createBiquadFilter();
      fLow.type = 'lowpass';
      fLow.frequency.value = 260;
      gainLow = audioCtx.createGain();
      source.connect(fLow);
      fLow.connect(gainLow);
      gainLow.connect(audioCtx.destination);

      const fMid = audioCtx.createBiquadFilter();
      fMid.type = 'bandpass';
      fMid.frequency.value = 880;
      fMid.Q.value = 0.55;
      gainMid = audioCtx.createGain();
      source.connect(fMid);
      fMid.connect(gainMid);
      gainMid.connect(audioCtx.destination);

      const fHigh = audioCtx.createBiquadFilter();
      fHigh.type = 'highpass';
      fHigh.frequency.value = 2600;
      gainHigh = audioCtx.createGain();
      source.connect(fHigh);
      fHigh.connect(gainHigh);
      gainHigh.connect(audioCtx.destination);

      updateStemGains();
    }}

    function updateStemGains() {{
      const anySolo = stemState.low.solo || stemState.mid.solo || stemState.high.solo;
      ['low', 'mid', 'high'].forEach(k => {{
        const mBtn = document.getElementById('mute-' + k);
        const sBtn = document.getElementById('solo-' + k);
        mBtn.className = 'px-1.5 py-0.5 rounded text-[9px] font-bold border ' + (stemState[k].mute ? 'bg-red-600 text-white border-red-500' : 'border-[var(--app-border)]');
        sBtn.className = 'px-1.5 py-0.5 rounded text-[9px] font-bold border ' + (stemState[k].solo ? 'bg-amber-500 text-black border-amber-400' : 'border-[var(--app-border)]');
      }});
      if (!audioCtx) return;
      ['low', 'mid', 'high'].forEach(k => {{
        let active = !stemState[k].mute;
        if (anySolo) active = stemState[k].solo && !stemState[k].mute;
        const gNode = k === 'low' ? gainLow : (k === 'mid' ? gainMid : gainHigh);
        gNode.gain.setTargetAtTime(active ? 1.0 : 0.0, audioCtx.currentTime, 0.015);
      }});
    }}

    window.toggleStem = function(stem, mode) {{
      initWebAudio();
      stemState[stem][mode] = !stemState[stem][mode];
      updateStemGains();
    }};

    function triggerMetronomeClick(isDownbeat, isSubAccent) {{
      if (!metroEnabled || !audioCtx || audio.paused) return;
      const osc = audioCtx.createOscillator();
      const g = audioCtx.createGain();
      osc.type = isDownbeat ? 'triangle' : 'sine';
      osc.frequency.value = isDownbeat ? 1046.5 : (isSubAccent ? 784.0 : 523.25);
      g.gain.setValueAtTime(isDownbeat ? 0.18 : 0.08, audioCtx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.065);
      osc.connect(g);
      g.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.07);
    }}

    function fmtTime(sec) {{
      const m = Math.floor(sec / 60);
      const s = (sec % 60).toFixed(1).padStart(4, '0');
      return `${{m}}:${{s}}`;
    }}

    function meterClass(m) {{
      if (m.startsWith('4/4')) return 'meter-44';
      if (m.startsWith('3/4')) return 'meter-34';
      if (m.startsWith('7/8')) return 'meter-78';
      return 'meter-58';
    }}

    const pillsEl = document.getElementById('segmentPills');
    const meterLane = document.getElementById('meterLane');
    DATA.segments.forEach((seg, idx) => {{
      const pctLeft = (seg.start / DURATION) * 100;
      const pctWidth = ((seg.end - seg.start) / DURATION) * 100;

      const blk = document.createElement('div');
      blk.className = `absolute top-0 bottom-0 ${{meterClass(seg.meter)}} border-r border-white/30 flex items-center justify-center overflow-hidden text-white font-bold text-[10px] hover:brightness-110 transition`;
      blk.style.left = pctLeft + '%';
      blk.style.width = pctWidth + '%';
      blk.title = `#${{seg.id}} [${{fmtTime(seg.start)}} -> ${{fmtTime(seg.end)}}] ${{seg.meter}} (~${{seg.bpm}} BPM) | ${{seg.sample_lyric}}`;
      blk.innerHTML = pctWidth > 5 ? `<span>${{seg.meter.replace(' (6/8)', '')}}</span>` : '';
      blk.onclick = (e) => {{
        e.stopPropagation();
        jumpToTransition(seg.start, idx > 0);
      }};
      meterLane.appendChild(blk);

      const pill = document.createElement('button');
      pill.className = `px-2 py-1 rounded-md text-[11px] font-medium text-white shadow-sm flex items-center gap-1 hover:scale-[1.02] transition ${{meterClass(seg.meter)}}`;
      pill.innerHTML = `<span class="font-mono opacity-85">${{fmtTime(seg.start).slice(0,4)}}</span> <b>${{seg.meter}}</b>`;
      pill.title = `Jump to transition #${{seg.id}}: ${{seg.section_label}}`;
      pill.onclick = () => jumpToTransition(seg.start, idx > 0);
      pillsEl.appendChild(pill);
    }});

    const ruler = document.getElementById('timeRuler');
    for (let t = 0; t <= DURATION; t += 15) {{
      const tick = document.createElement('div');
      tick.className = 'absolute top-0 bottom-0 border-l border-[var(--app-border)] pl-1 flex items-center';
      tick.style.left = `calc(9rem + (100% - 9rem) * ${{t / DURATION}})`;
      tick.textContent = `${{Math.floor(t/60)}}:${{String(t%60).padStart(2,'0')}}`;
      ruler.appendChild(tick);
    }}

    function jumpToTransition(targetSec, isTransition) {{
      initWebAudio();
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
      const dest = (prerollEnabled && isTransition) ? Math.max(0, targetSec - 2.0) : targetSec;
      audio.currentTime = dest;
      audio.play();
      updatePlayBtn();
    }}

    window.seekFromEvent = function(e) {{
      initWebAudio();
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
      const rect = e.currentTarget.getBoundingClientRect();
      const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      audio.currentTime = ratio * DURATION;
      if (audio.paused) audio.play();
      updatePlayBtn();
    }};

    function drawStemCanvas(canvasId, key, colorHex) {{
      const canvas = document.getElementById(canvasId);
      const dpr = window.devicePixelRatio || 1;
      const w = canvas.clientWidth || 600;
      const h = canvas.clientHeight || 36;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      const ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);
      const n = DATA.timeline.length;
      const barW = w / n;
      ctx.fillStyle = colorHex;
      DATA.timeline.forEach((pt, i) => {{
        const val = pt[key] || 0;
        const bh = Math.max(2, val * (h - 4));
        ctx.fillRect(i * barW, (h - bh) / 2, Math.max(1, barW - 0.5), bh);
      }});
    }}

    function drawProbsCanvas() {{
      const canvas = document.getElementById('canvasProbs');
      const dpr = window.devicePixelRatio || 1;
      const w = canvas.clientWidth || 600;
      const h = canvas.clientHeight || 44;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      const ctx = canvas.getContext('2d');
      ctx.scale(dpr, dpr);
      const n = DATA.timeline.length;
      const curves = [
        {{ key: '4/4', color: '#60a5fa' }},
        {{ key: '3/4 (6/8)', color: '#34d399' }},
        {{ key: '5/8', color: '#c084fc' }},
        {{ key: '7/8', color: '#f59e0b' }}
      ];
      curves.forEach(c => {{
        ctx.beginPath();
        ctx.strokeStyle = c.color;
        ctx.lineWidth = 1.8;
        DATA.timeline.forEach((pt, i) => {{
          const x = (i / (n - 1)) * w;
          const y = h - 3 - (pt.smoothed[c.key] || 0) * (h - 6);
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }});
        ctx.stroke();
      }});
    }}

    setTimeout(() => {{
      drawStemCanvas('canvasLow', 'stem_low', '#818cf8');
      drawStemCanvas('canvasMid', 'stem_mid', '#34d399');
      drawStemCanvas('canvasHigh', 'stem_high', '#fbbf24');
      drawProbsCanvas();
    }}, 80);

    document.getElementById('btnPlay').onclick = () => {{
      initWebAudio();
      if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
      if (audio.paused) audio.play();
      else audio.pause();
      updatePlayBtn();
    }};

    document.getElementById('btnPreroll').onclick = () => {{
      prerollEnabled = !prerollEnabled;
      const el = document.getElementById('prerollState');
      el.textContent = prerollEnabled ? 'ON' : 'OFF';
      el.className = 'font-bold ' + (prerollEnabled ? 'text-emerald-400' : 'text-gray-400');
    }};

    document.getElementById('btnMetro').onclick = () => {{
      initWebAudio();
      metroEnabled = !metroEnabled;
      const el = document.getElementById('metroState');
      el.textContent = metroEnabled ? 'ON' : 'OFF';
      el.className = 'font-bold ' + (metroEnabled ? 'text-amber-400' : 'text-gray-400');
    }};

    function updatePlayBtn() {{
      document.getElementById('playIcon').textContent = audio.paused ? '▶' : '⏸';
      document.getElementById('playText').textContent = audio.paused ? 'Play' : 'Pause';
    }}

    function updateLoop() {{
      const t = audio.currentTime || 0;
      document.getElementById('curTime').textContent = fmtTime(t);
      document.getElementById('playhead').style.left = `calc(9rem + (100% - 9rem) * ${{t / DURATION}})`;

      const seg = DATA.segments.find(s => t >= s.start && t <= s.end) || DATA.segments[0];
      const frame = DATA.timeline[Math.min(DATA.timeline.length - 1, Math.floor(t))] || DATA.timeline[0];

      if (seg) {{
        const badge = document.getElementById('liveBadge');
        badge.textContent = `${{seg.meter}} • ${{seg.bpm}} BPM`;
        badge.className = `ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold text-white ${{meterClass(seg.meter)}}`;
        document.getElementById('confDisplay').textContent = `ACF: ${{Math.round((frame.smoothed[seg.meter] || 0)*100)}}%`;

        const numPulses = seg.meter.startsWith('7/8') ? 7 : (seg.meter.startsWith('5/8') ? 5 : (seg.meter.startsWith('3/4') ? 3 : 4));
        const pulseDur = (seg.meter.startsWith('7/8') || seg.meter.startsWith('5/8')) ? (60 / seg.bpm / 2) : (60 / seg.bpm);
        const totalBeatIdx = Math.floor((t - seg.start) / pulseDur);
        const beatInBar = ((totalBeatIdx % numPulses) + numPulses) % numPulses;

        if (totalBeatIdx !== lastBeatIndex && !audio.paused) {{
          lastBeatIndex = totalBeatIdx;
          triggerMetronomeClick(beatInBar === 0, (numPulses === 7 && (beatInBar === 2 || beatInBar === 4)) || (numPulses === 5 && beatInBar === 3));
        }}

        const dotsEl = document.getElementById('beatDots');
        let dotsHtml = '';
        for (let b = 0; b < numPulses; b++) {{
          const active = b === beatInBar;
          const color = active ? (b === 0 ? 'bg-rose-500 scale-125' : 'bg-amber-400 scale-110') : 'bg-gray-600/50';
          dotsHtml += `<span class="w-4 h-4 rounded-full flex items-center justify-center text-[9px] font-bold text-white transition ${{color}}">${{b + 1}}</span>`;
        }}
        dotsEl.innerHTML = dotsHtml;
      }}

      const cue = DATA.cues.find(c => t >= c.start && t <= c.end);
      if (cue) {{
        document.getElementById('lyricDisplay').textContent = cue.text;
      }}

      requestAnimationFrame(updateLoop);
    }}
    requestAnimationFrame(updateLoop);
  </script>
</body>
</html>
"""


def main():
  parser = argparse.ArgumentParser(
      prog="analyze_meter_timeline.py",
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=(
          "🎹🥁 Musical Meter & Time-Signature Autocorrelation Analyzer (4/4 vs"
          " 3/4-6/8 vs 5/8 vs 7/8)\nGenerates a tokenized JSON meter timeline"
          " and a self-contained Interactive Multitrack HTML DAW Player."
      ),
      epilog=(
          "========================================================================\n"
          "🤖 DEAR AI AGENT (CARA AI):\n"
          "If you need to know how the DSP algorithm works under the hood (50Hz\n"
          "Onset Flux, harmonic autocorrelation across 4/4, 3/4, 5/8, and 7/8,\n"
          "3-band IIR stem decomposition, and WebAudio BiquadFilter DAW), READ THE\n"
          "TOP-OF-FILE COMMENT / DOCSTRING (`head -n 75 analyze_meter_timeline.py`)!\n"
          "========================================================================"
      ),
  )
  parser.add_argument(
      "--mp3",
      default="",
      help="Input MP3 file (auto-converts to WAV via ffmpeg if --wav is omitted)",
  )
  parser.add_argument(
      "--wav",
      default="",
      help="Input 16-bit PCM WAV file (optional if --mp3 is provided)",
  )
  parser.add_argument(
      "--srt",
      default="",
      help="Input .srt subtitle file (auto-detected from audio basename if omitted)",
  )
  parser.add_argument(
      "--out-json",
      default="",
      help="Output JSON timeline path (defaults to <basename>_meter.json)",
  )
  parser.add_argument(
      "--out-html",
      default="",
      help="Output Interactive HTML DAW path (defaults to <basename>_meter_player.html)",
  )
  parser.add_argument(
      "--embed-mp3",
      default="",
      help="Optional pre-compressed 48kbps MP3 for base64 embedding (auto-generated via ffmpeg if omitted)",
  )
  parser.add_argument(
      "--title",
      default="",
      help="Track title displayed in the HTML DAW header",
  )
  args = parser.parse_args()

  if not args.wav and not args.mp3:
    parser.error("You must provide at least --mp3 or --wav! (Pass --help for usage info)")

  primary_audio = args.mp3 or args.wav
  base_stem = os.path.splitext(primary_audio)[0]

  srt_path = args.srt or (base_stem + ".srt" if os.path.exists(base_stem + ".srt") else "")
  out_json = args.out_json or (base_stem + "_meter.json")
  out_html = args.out_html or (base_stem + "_meter_player.html")
  title = args.title or os.path.basename(base_stem).replace("_", " ").title()

  temp_files = []
  try:
    wav_path = args.wav
    if not wav_path or not os.path.exists(wav_path):
      fd, tmp_wav = tempfile.mkstemp(suffix=".wav")
      os.close(fd)
      temp_files.append(tmp_wav)
      subprocess.run(
          ["ffmpeg", "-y", "-i", args.mp3, "-ac", "2", "-ar", "48000", tmp_wav],
          check=True,
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
      )
      wav_path = tmp_wav

    embed_mp3 = args.embed_mp3
    if not embed_mp3 or not os.path.exists(embed_mp3):
      fd, tmp_mp3 = tempfile.mkstemp(suffix="_48k.mp3")
      os.close(fd)
      temp_files.append(tmp_mp3)
      subprocess.run(
          ["ffmpeg", "-y", "-i", wav_path, "-ac", "1", "-ar", "24000", "-b:a", "48k", tmp_mp3],
          check=True,
          stdout=subprocess.DEVNULL,
          stderr=subprocess.DEVNULL,
      )
      embed_mp3 = tmp_mp3

    flux, energies, low_env, mid_env, high_env, duration, hop_sec = (
        compute_multiband_onset_flux(wav_path)
    )
    timeline, segments = analyze_sliding_meter(
        flux, energies, low_env, mid_env, high_env, duration, hop_sec
    )
    cues = parse_srt(srt_path)

    for seg in segments:
      overlapping = [
          c["text"]
          for c in cues
          if c["end"] > seg["start"] and c["start"] < seg["end"]
      ]
      sec_tags = [t for t in overlapping if "[" in t]
      lyr_tags = [t for t in overlapping if "[" not in t]
      seg["section_label"] = sec_tags[0] if sec_tags else "Musical Passage"
      seg["sample_lyric"] = lyr_tags[0] if lyr_tags else "(Instrumental)"

    data = {
        "title": title,
        "duration": round(duration, 2),
        "segments": segments,
        "cues": cues,
        "timeline": timeline,
    }

    with open(out_json, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)

    with open(embed_mp3, "rb") as f:
      audio_b64 = base64.b64encode(f.read()).decode("ascii")

    html_str = build_html_player(data, audio_b64)
    with open(out_html, "w", encoding="utf-8") as f:
      f.write(html_str)

    print(f"✅ Analyzed {duration:.2f}s into {len(segments)} meter transitions:")
    for s in segments:
      m1, s1 = divmod(int(s["start"]), 60)
      m2, s2 = divmod(int(s["end"]), 60)
      print(
          f"   #{s['id']:02d} [{m1}:{s1:02d} -> {m2}:{s2:02d}]"
          f" ({s['duration']:4.0f}s) | {s['meter']:10s} | ~{s['bpm']} BPM |"
          f" {s['sample_lyric'][:45]}"
      )
    print(f"📄 Tokenized JSON: {out_json}")
    print(f"🎛️  Interactive HTML DAW: {out_html}")
  finally:
    for tf in temp_files:
      if os.path.exists(tf):
        os.remove(tf)


if __name__ == "__main__":
  main()
