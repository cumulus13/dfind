# 🔍 dfind - Duplicate File Finder

`dfind.py` is a command-line tool for finding duplicate files between two folders by comparing their SHA256 hashes. It uses the `rich` library to display progress and formatted output.

## 📦 Features

- Compares files in two folders recursively
- Supports limiting search depth
- Detects duplicates based on file content (hashes)
- Optionally shows files that are unique to each folder
- Beautiful terminal output with `rich`

## 🚀 Usage

```bash
python dfind.py folder1 folder2 [options]
```

### Options

| Option                | Description                                   |
|-----------------------|-----------------------------------------------|
| `-l`, `--max-depth`   | Set maximum directory depth to scan          |
| `-u`, `--unique`      | Show files that are unique to each folder    |

### Examples

Compare two folders for duplicates:

```bash
python dfind.py /path/to/folder1 /path/to/folder2
```

Compare two folders but only up to 2 levels deep:

```bash
python dfind.py folder1 folder2 -l 2
```

Show duplicates and also list unique files:

```bash
python dfind.py folder1 folder2 --unique
```

## 📦 Requirements

- Python 3.8+
- [`rich`](https://github.com/Textualize/rich)
- [`psutil`](https://pypi.org/project/psutil/)

Install dependencies:

```bash
pip install rich psutil
```

## 🧠 How It Works

1. Recursively collects file paths from both folders.
2. Computes SHA256 hash of each file.
3. Matches files with the same hash.
4. Displays results in a rich-formatted table.

## 📁 Output

- **Duplicate Files**: Pairs of files with identical content.
- **Unique Files** (optional): Files only found in one folder.

## 📜 License

MIT License

## Author
[Hadi Cahyadi](mailto:cumulus13@gmail.com)
    

## Coffee
[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/cumulus13)

[![Donate via Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/cumulus13)

[Support me on Patreon](https://www.patreon.com/cumulus13)