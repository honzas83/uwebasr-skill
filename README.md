# UWebASR Client

A Python client for the [uwebasr.zcu.cz](https://uwebasr.zcu.cz/) ASR service. This repository is structured as a **Gemini Skill**, allowing AI agents to use it as a tool for speech-to-text tasks.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/uwebasr-client.git
   cd uwebasr-client
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install `ffmpeg` for automatic audio conversion:
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

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

## Skill Integration
This project includes a `SKILL.md` file, which enables Gemini CLI and other agentic tools to understand and use this script autonomously.
