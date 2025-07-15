
# 🎬 YouTube Slide Extractor (PDF Generator)

A Python tool to automatically download videos or full playlists from YouTube, extract **1 frame per second**, detect **unique slides**, and export them as a **high-quality PDF** — all fully automated.

---

## ✨ Features

- ✅ Supports individual videos or full playlists
- ✅ Downloads **1080p video only** (no audio, for speed)
- ✅ Extracts **1 frame per second**
- ✅ Detects and saves only **unique-looking slides**
- ✅ Exports slides to **PDF with exact image resolution**
- ✅ Automatically names each PDF after the **video title**
- ✅ Cleans up all temporary files after each run

---

## 📦 Requirements

Install dependencies with pip:

```bash
pip install yt-dlp opencv-python pillow fpdf2 scikit-image
````

Also ensure you have [**FFmpeg**](https://www.gyan.dev/ffmpeg/builds/) installed (only needed if you ever switch back to merging audio+video).

---

## 🚀 How to Use

### 1. Run the script

```bash
python yt_slides_to_pdf.py
```

### 2. Paste any YouTube video or playlist URL

```text
🔗 Enter YouTube video or playlist URL: https://www.youtube.com/playlist?list=...
```

---

## 🧠 Output

- Each video in the playlist is processed one-by-one.
- For every video:

  - Unique slides are saved as images temporarily
  - A PDF is generated: `Video Title.pdf`
  - All temp files are deleted after each video

---

## ⚙️ Customization

You can modify these for advanced use:

| Option           | File/Location                   | Description                                                         |
| ---------------- | ------------------------------- | ------------------------------------------------------------------- |
| `SSIM_THRESHOLD` | top of script                   | Controls how similar two images must be to be considered duplicates |
| `RESIZE_TO`      | top of script                   | Resize before comparing (affects speed/accuracy)                    |
| `fps` logic      | `capture_frames_every_second()` | Adjust to capture every 2s, 5s, etc.                                |
| `video height`   | `download_video()`              | Switch between 1080p / 720p / best                                  |

---

## 📁 Folder Structure

```text
project/
│
├── yt_slides_to_pdf.py        # Main script
├── README.md                  # You are here
├── video.mp4                  # Downloaded temp video (auto deleted)
├── frames/                    # Extracted frames (auto deleted)
└── unique_slides/            # Unique slides (auto deleted)
```

---

## ✅ Example Output

- `Introduction to Linear Algebra.pdf`
- `Machine Learning Lecture 01.pdf`
- ...

Each PDF contains only **clean, distinct slides** — perfect for studying or archiving.

---

## 🙌 Credits

- Developed by **Ashrafi Khandaker Abir**
- Fetches metadata or resources from [**devabir.com**](https://devabir.com)
- Powered by:

  - [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
  - `OpenCV`
  - `Pillow`
  - `fpdf2`
  - `scikit-image`

---

## 🤝 License

MIT — free to use, modify, and distribute.

---

```

Let me know if you'd like to:
- Add a banner or badge (GitHub-ready)
- Publish this as an open-source repo template

You're building a polished and professional tool — great work! 🧠💡
```
