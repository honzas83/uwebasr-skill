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
   python3 uwebasr.py lindat/generic/cs/zipformer your_audio.mp3 --format txt
   ```
   *Note: No external dependencies required. Only Python 3 and optionally [ffmpeg](https://ffmpeg.org/) for audio conversion.*

### General Command Structure
If you have cloned the repository, run from the root:
```bash
python3 scripts/uwebasr.py [INSTANCE/MODEL] [FILES...] --format [FORMAT]
```

**Example:**
```bash
python3 scripts/uwebasr.py lindat/generic/cs/zipformer HDS09.mp3 --format txt
```

Use the full UWebASR model path, including the instance prefix. Public UWebASR models listed on the service page use the `lindat/` prefix, for example `lindat/generic/cs/zipformer`.

### Supported Formats
- No `--format`: generate the default output set (`speechcloud_json`, `txt`, `s.txt`, `vtt`, `s.vtt`, `json`, `trs`, `extended.trs`).
- `txt`: Plain text
- `s.txt`: Segmented plain text using `sp=0.3` and `pau=2.0`
- `vtt`: WebVTT subtitles
- `s.vtt`: Segmented WebVTT using `sp=0.3` and `pau=2.0`
- `json`: Word-level API JSON with timestamps and confidence scores
- `speechcloud_json`: Raw SpeechCloud JSON
- `trs`: Transcriber XML
- `extended.trs`: Extended Transcriber XML with confidence values

### Advanced Options
- `--format`: Generate only the selected format. Can be used multiple times.
- `--n-workers`: Number of parallel threads for processing multiple files.
- `--no-ffmpeg`: Skip ffmpeg (requires 16kHz mono Ogg/Vorbis files).
- `--no-cookies`: Disable cookie handling between API calls.
- `--overwrite`: Allow overwriting existing output files.
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

### With Google Antigravity
Google Antigravity can use this repository as project context and run the client script from its terminal-enabled agent workflow.
1. Clone the skill into the project where you want to use it:
   ```bash
   cd /path/to/your/project
   git clone git@github.com:honzas83/uwebasr-skill.git
   ```
2. Add or update your project `AGENTS.md` with a short instruction that points Antigravity to this skill:
   ```markdown
   Use the UWebASR skill from `uwebasr-skill/SKILL.md` for speech-to-text tasks.
   Run the client with `python3 uwebasr-skill/scripts/uwebasr.py [MODEL] [FILES...] --format [FORMAT]`.
   ```
3. In Antigravity, open the target project and ask the agent to transcribe an audio file using UWebASR.

### As a Claude Code Skill
To install this skill in Claude Code:
1. Clone the repository into your personal Claude Code skills directory:
   ```bash
   git clone git@github.com:honzas83/uwebasr-skill.git ~/.claude/skills/uwebasr-client
   ```
2. Start or restart Claude Code. The skill is available as `/uwebasr-client` and can also be selected automatically when you ask for speech-to-text transcription.

For project-local installation, clone it into `.claude/skills/uwebasr-client` inside the target repository instead.

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

- **UWebASR Service and Zipformer Models:**
  Švec, J., Lehečka, J., Ircing, P. (2025) *Current State of the UWebASR - Web-Based ASR Service for Czech, Slovak, German, and English*. CLARIN, ISSN 2773-2177.

- **English, German, and Czech Models:**
  Lehečka, J., Švec, J., Psutka, J.V., Ircing, P. (2023) *Transformer-based Speech Recognition Models for Oral History Archives in English, German, and Czech*. Proc. INTERSPEECH 2023, 201-205, doi: [10.21437/Interspeech.2023-872](https://doi.org/10.21437/Interspeech.2023-872)

- **Slovak Model:**
  Lehečka, J., Psutka, J.V., Psutka, J. (2023) *Transfer Learning of Transformer-Based Speech Recognition Models from Czech to Slovak*. In: Text, Speech, and Dialogue. TSD 2023. Lecture Notes in Computer Science, vol 14286. Springer, Cham. [https://doi.org/10.1007/978-3-031-40498-6_29](https://doi.org/10.1007/978-3-031-40498-6_29)
