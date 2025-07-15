import os
import cv2
import subprocess


def download_video(url, output_path="downloaded_video.mp4"):
    print(f"🎬 Starting download for: {url}\n")

    command = [
        "yt-dlp",
        "-f",
        "bestvideo+bestaudio",
        "--merge-output-format",
        "mp4",
        "-o",
        output_path,
        url,
    ]

    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error downloading video:\n", result.stderr)
        exit(1)

    print(f"✅ Download complete: {output_path}\n")
    return output_path


def capture_frames_every_second(video_path, output_folder="frames"):
    print(f"📥 Opening video: {video_path}")
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        print(
            "❌ Error: FPS is zero. Cannot read video. Make sure it’s a valid .mp4 file with video stream."
        )
        return

    fps = int(fps)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_seconds = int(total_frames / fps)

    print(f"⏱️ Duration: {duration_seconds} seconds")
    print(f"🎞️ FPS: {fps}")
    print(f"📊 Total frames: {total_frames}\n")

    print(f"📸 Starting to extract 1 frame per second...\n")
    for sec in range(duration_seconds):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        ret, frame = cap.read()
        if ret:
            filename = os.path.join(output_folder, f"frame_{sec:04d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"✅ Saved: {filename}")
        else:
            print(f"⚠️ Failed to capture frame at {sec}s")

    cap.release()
    print("\n✅ Frame extraction complete. All frames saved in:", output_folder)


if __name__ == "__main__":
    print("📥 YouTube Slide Extractor - 1 frame per second")
    video_url = input("🔗 Enter YouTube video URL: ").strip()

    # Step 1: Download video
    downloaded_video = download_video(video_url)

    # Step 2: Extract frames
    capture_frames_every_second(downloaded_video)
