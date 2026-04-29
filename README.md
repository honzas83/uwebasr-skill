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

## Acknowledgments & Citations

The UWebASR service is integrated into the national research infrastructure **[LINDAT/CLARIAH-CZ](https://lindat.cz)**, which is part of the European **CLARIN ERIC** network.

### Citing the service
If you use this service for your research, please cite the following papers:

- **English, German, and Czech Models:**
  Lehečka, J., Švec, J., Psutka, J.V., Ircing, P. (2023) *Transformer-based Speech Recognition Models for Oral History Archives in English, German, and Czech*. Proc. INTERSPEECH 2023, 201-205, doi: [10.21437/Interspeech.2023-872](https://doi.org/10.21437/Interspeech.2023-872)

- **Slovak Model:**
  Lehečka, J., Psutka, J.V., Psutka, J. (2023) *Transfer Learning of Transformer-Based Speech Recognition Models from Czech to Slovak*. In: Text, Speech, and Dialogue. TSD 2023. Lecture Notes in Computer Science, vol 14286. Springer, Cham. [https://doi.org/10.1007/978-3-031-40498-6_29](https://doi.org/10.1007/978-3-031-40498-6_29)

## Contributing
This project is optimized for agentic workflows. If you add new functionality, please update `SKILL.md` accordingly.
