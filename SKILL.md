---
name: uwebasr-client
description: Provides ASR (Automatic Speech Recognition) services via uwebasr.zcu.cz. Use this skill to transcribe audio files into various formats (txt, vtt, json, etc.) using models like zipformer.
---

# UWebASR Client Skill

This skill provides an interface to the UWebASR service from the University of West Bohemia for Automatic Speech Recognition (ASR).

## Workflows

### Transcribing Audio
Use the `scripts/uwebasr.py` script to process audio files. The script can handle multiple files and output formats.

**Command Structure:**
```bash
python scripts/uwebasr.py [MODEL] [FILES...] --format [FORMAT]
```

### Parameters
- `MODEL`: The SpeechCloud model ID. Standard Czech model: `speechcloud/generic/cs/zipformer`.
- `FILES`: Path(s) to audio files (mp3, wav, ogg, etc.).
- `--format`: Desired output format (`txt`, `vtt`, `json`, `jsonl`, `s.txt`, `s.vtt`).
- `--n-workers`: Number of parallel workers for multiple files.
- `--output-dir`: Directory to save the results.

## Agent Guidelines
1. **Model Selection**: Default to `speechcloud/generic/cs/zipformer` for Czech unless specified otherwise.
2. **Format Selection**: 
   - Use `txt` for simple transcriptions.
   - Use `vtt` if the user mentions subtitles or video.
   - Use `json` if detailed metadata is needed.
3. **Audio Pre-processing**: The script uses `ffmpeg` for conversion. If `ffmpeg` is missing, use `--no-ffmpeg` and ensure files are in a supported format (Ogg/Vorbis 16kHz mono).

## Examples

### Basic Transcription
```bash
python scripts/uwebasr.py speechcloud/generic/cs/zipformer audio.mp3 --format txt
```

### Batch Processing with Subtitles
```bash
python scripts/uwebasr.py speechcloud/generic/cs/zipformer clip1.mp3 clip2.mp3 --format vtt --n-workers 2
```
