# UWebASR Client & Skill

A Python client for the [UWebASR](https://uwebasr.zcu.cz/) ASR service. This repository is structured as a **Skill for agent**, allowing AI agents to use it as a tool for speech-to-text tasks.

## Usage

### Quick Start (Standalone Script)
If you just want to use the transcription script directly without cloning the whole repository:

1. **Download**:
   ```bash
   curl -O https://raw.githubusercontent.com/honzas83/uwebasr-skill/main/scripts/uwebasr.py
   chmod +x uwebasr.py
   ```
2. **Run**:
   ```bash
   python3 uwebasr.py speechcloud/generic/cs/zipformer your_audio.mp3 --format txt
   ```
   *Note: No external dependencies required. Only Python 3 and optionally [ffmpeg](https://ffmpeg.org/) for audio conversion.*

### General Command Structure
If you have cloned the repository, run from the root:
```bash
python scripts/uwebasr.py [MODEL] [FILES...] --format [FORMAT]
```

**Example:**
```bash
python scripts/uwebasr.py speechcloud/generic/cs/zipformer HDS09.mp3 --format txt
```

### Supported Formats
- `txt`: Plain text (default)
- `vtt`: WebVTT subtitles
- `json`: Original SpeechCloud JSON with timestamps
- `s.txt` / `s.vtt`: Segmentation enabled
- `jsonl`: Line-delimited JSON

### Advanced Options
- `--n-workers`: Number of parallel threads for processing multiple files.
- `--no-ffmpeg`: Skip ffmpeg (requires 16kHz mono Ogg/Vorbis files).
- `--output-dir`: Specify a custom directory for output files.
- `--suffix`: Add a custom suffix to output filenames.

## Installation & Skill Setup

### As a local repository
If you prefer to have the full project structure:
1. Clone the repository:
   ```bash
   git clone git@github.com:honzas83/uwebasr-skill.git
   cd uwebasr-skill
   ```
2. (Optional) External dependencies are no longer required, but you can check `requirements.txt`.

### As a Skill for agent
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

## Acknowledgments & Citations

The UWebASR service is integrated into the national research infrastructure **[LINDAT/CLARIAH-CZ](https://lindat.cz)**, which is part of the European **CLARIN ERIC** network.

### Citing the service
If you use this service for your research, please cite the following papers:

- **English, German, and Czech Models:**
  Lehečka, J., Švec, J., Psutka, J.V., Ircing, P. (2023) *Transformer-based Speech Recognition Models for Oral History Archives in English, German, and Czech*. Proc. INTERSPEECH 2023, 201-205, doi: [10.21437/Interspeech.2023-872](https://doi.org/10.21437/Interspeech.2023-872)

- **Slovak Model:**
  Lehečka, J., Psutka, J.V., Psutka, J. (2023) *Transfer Learning of Transformer-Based Speech Recognition Models from Czech to Slovak*. In: Text, Speech, and Dialogue. TSD 2023. Lecture Notes in Computer Science, vol 14286. Springer, Cham. [https://doi.org/10.1007/978-3-031-40498-6_29](https://doi.org/10.1007/978-3-031-40498-6_29)
