# UWebASR Client Skill

A Python client for the [UWebASR](https://uwebasr.zcu.cz/) ASR service. This repository is structured as a **Gemini Skill**, allowing AI agents to use it as a tool for speech-to-text tasks.

## Installation

### As a standalone script
1. Clone the repository:
   ```bash
   git clone git@github.com:honzas83/uwebasr-skill.git
   cd uwebasr-skill
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install `ffmpeg` for automatic audio conversion:
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### As a Gemini Skill
To use this as a tool within Gemini CLI:
1. Install the skill:
   ```bash
   gemini skills install git@github.com:honzas83/uwebasr-skill.git --scope user
   ```
2. Reload skills in your Gemini session:
   ```bash
   /skills reload
   ```

### As a Codex Skill
To install this skill in [Codex](https://github.com/google/codex):
1. Clone the repository into your Codex skills directory:
   ```bash
   git clone git@github.com:honzas83/uwebasr-skill.git ~/.codex/skills/uwebasr-client
   ```
2. The skill will be automatically detected in your next Codex session.

## Usage

Run the script from the root directory:

```bash
python scripts/uwebasr.py [MODEL] [FILE] --format [FORMAT]
```

Example:
```bash
python scripts/uwebasr.py speechcloud/generic/cs/zipformer HDS09.mp3 --format txt
```

### Supported Formats
- `json`: Original SpeechCloud JSON
- `txt`: Plain text
- `s.txt`: Text with segmentation
- `vtt`: WebVTT subtitles
- `s.vtt`: WebVTT with segmentation
- `jsonl`: Line-delimited JSON

### Options
- `--n-workers`: Number of parallel threads.
- `--no-ffmpeg`: Do not use ffmpeg (submit files directly).
- `--output-dir`: Directory to save results.

## Contributing
This project is optimized for agentic workflows. If you add new functionality, please update `SKILL.md` accordingly.
