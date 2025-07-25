# MP3 CLI made with Python

## Features

Features:
- merge MP3 files into a single one
- print metadata
- edit metadata

## Installation

It's recommended to use a Python virtual environment: `python -m venv venv`

Activation on Linux: `source venv/bin/activate`

Activation on Linux: `.\venv\Scripts\activate`

Install dependencies: `pip install -r requirements.txt`

You will also need [ffmpeg](https://www.ffmpeg.org/).

## Usage

Merge MP3 files: `python mp3.py merge FILES OUTPUT`

Example: `python mp3.py merge song1.mp3 song2.mp3 song3.mp3 album.mp3`

---

Print metadata: `python mp3.py read-tags FILE`

Example: `python mp3.py read-tags song1.mp3`

You can configure which tag to print in `config.ini`.

---

Edit metadata: `python mp3.py edit-tags FILE JSON_FILE`

Example: `python mp3.py edit-tags song1.mp3 tags.json`

You can find a JSON template in `template.json`.
