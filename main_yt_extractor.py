import os
import re
import cv2
import shutil
import subprocess
from PIL import Image
from fpdf import FPDF
from skimage.metrics import structural_similarity as ssim

# === CONFIG ===
SSIM_THRESHOLD = 0.90
RESIZE_TO = (800, 600)
FRAMES_DIR = "frames"
UNIQUE_DIR = "unique_slides"
TEMP_VIDEO_FILE = "video.mp4"


# === UTILITY ===
def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(result.stderr)
    return result.stdout


def sanitize_filename(title):
    clean = re.sub(r'[<>:"/\\|?*]', "", title).strip()
    return clean[:100]


def get_playlist_videos(url):
    print("🔗 Fetching video URLs from playlist...")
    result = run_command(["yt-dlp", "--flat-playlist", "--print", "url", url])
    return [line.strip() for line in result.splitlines() if line.strip()]


def get_video_title(url):
    title = run_command(["yt-dlp", "--get-title", url]).strip()
    return sanitize_filename(title)


def download_video(url):
    print(f"\n🎬 Downloading 1080p video (no audio): {url}")
    run_command(
        [
            "yt-dlp",
            "-f",
            "bv[height=1080][ext=mp4]",  # best video-only at 1080p, mp4 format
            "--user-agent",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "-o",
            "video.mp4",
            url,
        ]
    )

    if os.path.exists("video.mp4"):
        print("✅ Downloaded: video.mp4 (1080p, no audio)")
        return "video.mp4"

    raise Exception("❌ 1080p video-only file not downloaded.")


# === FRAME EXTRACTION ===
def capture_frames_every_second(video_path):
    print(f"📥 Extracting frames...")
    os.makedirs(FRAMES_DIR, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = int(total_frames / fps)

    for sec in range(duration_seconds):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(FRAMES_DIR, f"frame_{sec:04d}.jpg")
            cv2.imwrite(filename, frame)
    cap.release()


# === UNIQUE SLIDE DETECTION ===
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, RESIZE_TO)
    norm = cv2.equalizeHist(resized)
    return norm


def are_similar(img1, img2):
    return ssim(preprocess(img1), preprocess(img2), full=False) > SSIM_THRESHOLD


def extract_unique_slides():
    os.makedirs(UNIQUE_DIR, exist_ok=True)
    image_files = sorted(
        f
        for f in os.listdir(FRAMES_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    last_unique = None
    count = 0

    for filename in image_files:
        path = os.path.join(FRAMES_DIR, filename)
        image = cv2.imread(path)
        if image is None:
            continue
        if last_unique is None or not are_similar(image, last_unique):
            last_unique = image
            out_path = os.path.join(UNIQUE_DIR, f"slide_{count:04d}.jpg")
            cv2.imwrite(out_path, image)
            print(f"✅ Saved: {out_path}")
            count += 1
    return count


# === PDF CREATION ===
def create_pdf_from_unique_slides(pdf_filename):
    print(f"📄 Creating PDF: {pdf_filename}")
    pdf = FPDF(unit="pt")
    slide_files = sorted(
        f
        for f in os.listdir(UNIQUE_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    for filename in slide_files:
        path = os.path.join(UNIQUE_DIR, filename)
        with Image.open(path) as img:
            img = img.convert("RGB")
            width, height = img.size
            pdf.add_page(format=(width, height))
            pdf.image(path, x=0, y=0, w=width, h=height)
    if slide_files:
        pdf.output(pdf_filename)
        print(f"✅ PDF saved: {pdf_filename}")
    else:
        print("❌ No slides found.")


# === CLEANUP ===
def clean_temp():
    for f in [TEMP_VIDEO_FILE]:
        if os.path.exists(f):
            os.remove(f)
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    shutil.rmtree(UNIQUE_DIR, ignore_errors=True)


# === PROCESS SINGLE VIDEO ===
def process_video(url):
    try:
        clean_temp()
        title = get_video_title(url)
        pdf_name = f"{title}.pdf"
        download_video(url)
        capture_frames_every_second(TEMP_VIDEO_FILE)
        slide_count = extract_unique_slides()
        if slide_count > 0:
            create_pdf_from_unique_slides(pdf_name)
        else:
            print("⚠️ No unique slides detected.")
    except Exception as e:
        print(f"❌ Error processing video: {e}")
    finally:
        clean_temp()


# === MAIN ===
def main():
    input_url = input("🔗 Enter YouTube video or playlist URL: ").strip()
    is_playlist = "playlist" in input_url or "list=" in input_url
    video_urls = get_playlist_videos(input_url) if is_playlist else [input_url]

    for idx, url in enumerate(video_urls, 1):
        print(f"\n📦 Processing video {idx}/{len(video_urls)}")
        process_video(url)


if __name__ == "__main__":
    main()
