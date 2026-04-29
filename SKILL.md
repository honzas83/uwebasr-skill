---
name: uwebasr-client
description: Provides ASR (Automatic Speech Recognition) services via uwebasr.zcu.cz. Use this skill to transcribe audio files in multiple languages (CS, SK, EN, DE, PL, HU, HR, SR, NL) using state-of-the-art models like Zipformer.
---

# UWebASR Client Skill

This skill provides an interface to the UWebASR service from the University of West Bohemia for Automatic Speech Recognition (ASR).

## Supported Languages & Models

### Model Selection Strategy
1. **Zipformer (Recommended)**: Use for best general accuracy.
   - Format: `speechcloud/generic/{lang}/zipformer`
   - Available for: `cs` (Czech), `sk` (Slovak), `en` (English), `de` (German), `pl` (Polish), `hu` (Hungarian), `hr` (Croatian), `sr` (Serbian).
2. **Wav2Vec 2.0**: Use for Dutch or if Zipformer is unavailable.
   - Format: `speechcloud/generic/{lang}`
   - Available for: `cs`, `sk`, `de`, `en`, `nl` (Dutch).
3. **Malach (Oral History)**: Optimized for historical recordings and specific oral history dialects.
   - Format: `speechcloud/malach/{lang}`
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
python scripts/uwebasr.py [MODEL] [FILES...] --format [FORMAT]
```

## Agent Guidelines
1. **Choose the best model**: Always prefer `zipformer` models (e.g., `speechcloud/generic/cs/zipformer`) unless the language is only supported by Wav2Vec (Dutch) or the context is Oral History (Malach).
2. **Language Detection**: If the user doesn't specify a language but provides a file, ask or attempt to detect (Czech is the default).
3. **Format Selection**: 
   - `txt`: Plain text (default).
   - `vtt`: Subtitles.
   - `json`: Word-level timestamps and confidence scores.
   - `s.txt` / `s.vtt`: Segmentation enabled.
4. **FFmpeg**: The script uses `ffmpeg` for conversion. If missing, use `--no-ffmpeg` (requires 16kHz mono Ogg/Vorbis).

## Examples

### Transcribe Polish with Zipformer
```bash
python scripts/uwebasr.py speechcloud/generic/pl/zipformer interview.mp3 --format txt
```

### Create German Subtitles
```bash
python scripts/generic/de/zipformer video_audio.wav --format vtt
```

### Oral History Transcription (Czech)
```bash
python scripts/uwebasr.py speechcloud/malach/cs archive_tape.mp3 --format s.txt
```
