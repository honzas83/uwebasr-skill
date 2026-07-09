---
name: uwebasr-client
description: Provides ASR (Automatic Speech Recognition) services via uwebasr.zcu.cz. Use this skill to transcribe audio files in multiple languages (CS, SK, EN, DE, PL, HU, HR, SR, NL) using state-of-the-art models like Zipformer.
---

# UWebASR Client & Skill

This skill provides an interface to the UWebASR service from the University of West Bohemia for Automatic Speech Recognition (ASR).

## Operational Requirements

- **Network Connectivity**: This skill requires an active internet connection to communicate with the UWebASR API at `https://uwebasr.zcu.cz`.
- **Performance**: Transcription speed is typically **10x faster than real-time** (e.g., a 10-minute recording takes approximately 1 minute to process). However, processing time depends on the current server load and file size.
- **Dependencies**: No external Python libraries are required. `ffmpeg` is recommended for automatic audio format conversion.

## Supported Languages & Models

### Model Selection Strategy
1. **Zipformer (Recommended)**: Use for best general accuracy.
   - Format: `lindat/generic/{lang}/zipformer`
   - Available for: `cs` (Czech), `sk` (Slovak), `en` (English), `de` (German), `pl` (Polish), `hu` (Hungarian), `hr` (Croatian), `sr` (Serbian).
2. **Adapted Zipformer (Oral History / MALACH)**: Use for oral histories.
   - Format: `lindat/malach/{lang}/zipformer`
   - Available for: `cs`, `sk`, `en`, `de`, `pl`, `hu`.
3. **Wav2Vec 2.0**: Use for Dutch or if Zipformer is unavailable.
   - Format: `lindat/generic/{lang}`
   - Available for: `cs`, `sk`, `de`, `en`, `nl` (Dutch).
4. **Deprecated MALACH Wav2Vec 2.0**: Use only when specifically requested.
   - Format: `lindat/malach/{lang}`
   - Available for: `cs`, `sk`, `de`, `en`.

### Language Codes
- `cs`: Czech (Default)
- `sk`: Slovak
- `en`: English
- `de`: German
- `nl`: Dutch (Wav2Vec only)
- `pl`: Polish
- `hu`: Hungarian
- `hr`: Croatian
- `sr`: Serbian

## Workflows

### Transcribing Audio
Use the `scripts/uwebasr.py` script to process audio files.

**Command Structure:**
```bash
python3 scripts/uwebasr.py [INSTANCE/MODEL] [FILES...] --format [FORMAT]
```

Use the full model path, including the instance prefix, e.g. `lindat/generic/cs/zipformer`.

## Agent Guidelines
1. **Choose the best model**: Always prefer `zipformer` models (e.g., `lindat/generic/cs/zipformer`) unless the language is only supported by Wav2Vec (Dutch) or the context is MALACH (Oral History).
2. **Use MALACH for oral history**: For interviews, oral history, archival recordings, testimonies, historical recordings, or similar humanities research material, prefer `lindat/malach/{lang}/zipformer` when available.
3. **Language Selection**:
   - If the user specifies a language, use that language.
   - If the language is clear from the conversation, file name, or surrounding context, choose the matching model.
   - If the language is unclear, ask before transcribing.
   - Do not guess for multilingual, research-critical, legal, medical, or otherwise high-stakes recordings.
4. **Default Agent Output**:
   - If the user does not request a format, use `--format txt` to produce a single plain-text transcript.
   - Use `--format vtt` for subtitles or captions.
   - Use `--format json` for downstream processing that needs word-level timestamps and confidence scores.
   - Use `--format speechcloud_json` when debugging API output or when conversion to another format fails.
5. **CLI Format Selection**:
   - No `--format`: generate the default output set (`speechcloud_json`, `txt`, `s.txt`, `vtt`, `s.vtt`, `json`, `trs`, `extended.trs`).
   - `txt`: API `format=plaintext`.
   - `s.txt`: API `format=plaintext&sp=0.3&pau=2.0`.
   - `vtt`: API `format=webvtt`.
   - `s.vtt`: API `format=sentvtt&sp=0.3&pau=2.0`.
   - `json`: API `format=json` with word-level timestamps and confidence scores.
   - `speechcloud_json`: API `format=speechcloud_json`, raw SpeechCloud JSON.
   - `trs`: API `format=trs`, Transcriber XML.
   - `extended.trs`: API `format=extended_trs`, Transcriber XML with confidence values.
6. **Output Files**:
   - By default, output files are written next to the input file.
   - Use `--output-dir` when the user requests a separate transcript directory.
   - Output names are derived from the input basename plus the selected format extension.
   - Do not use `--overwrite` unless the user explicitly requested replacement or you are replacing output files from your own immediately previous attempt.
7. **FFmpeg**: By default the script uses local `ffmpeg` to convert audio before upload. If local `ffmpeg` is missing or conversion should happen server-side, use `--no-ffmpeg`; the file is then submitted directly to the UWebASR API, which accepts audio formats supported by server-side FFmpeg.
8. **Error Handling**:
   - On HTTP 503, the script retries automatically; if it still fails, tell the user the backend is likely busy and suggest retrying later.
   - If local `ffmpeg` fails, retry with `--no-ffmpeg` when appropriate, or tell the user that local `ffmpeg` needs to be installed/fixed.
   - If conversion to a requested format fails, try `--format speechcloud_json` to preserve the raw recognition result before attempting another conversion.

## Examples

### Transcribe Polish with Zipformer
```bash
python3 scripts/uwebasr.py lindat/generic/pl/zipformer interview.mp3 --format txt
```

### Create German Subtitles
```bash
python3 scripts/uwebasr.py lindat/generic/de/zipformer video_audio.wav --format vtt
```

### Oral History Transcription (Czech)
```bash
python3 scripts/uwebasr.py lindat/malach/cs/zipformer archive_tape.mp3 --format s.txt
```
