import os
import cv2
from PIL import Image
from fpdf import FPDF
from skimage.metrics import structural_similarity as ssim
from fpdf import FPDF
from PIL import Image
import os

# Settings
FRAMES_DIR = "frames"
UNIQUE_DIR = "unique_slides"
PDF_OUTPUT = "unique_slides.pdf"
SSIM_THRESHOLD = 0.90
RESIZE_TO = (800, 600)


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, RESIZE_TO)
    norm = cv2.equalizeHist(resized)
    return norm


def are_similar(img1, img2, threshold=SSIM_THRESHOLD):
    gray1 = preprocess(img1)
    gray2 = preprocess(img2)
    score, _ = ssim(gray1, gray2, full=True)
    return score > threshold


def extract_unique_slides():
    print("🔍 Checking images in:", FRAMES_DIR)
    os.makedirs(UNIQUE_DIR, exist_ok=True)
    image_files = sorted(
        [
            f
            for f in os.listdir(FRAMES_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    )

    last_unique = None
    unique_count = 0

    for filename in image_files:
        path = os.path.join(FRAMES_DIR, filename)
        image = cv2.imread(path)
        if image is None:
            continue

        if last_unique is None or not are_similar(image, last_unique):
            last_unique = image
            output_filename = f"slide_{unique_count:04d}.jpg"
            output_path = os.path.join(UNIQUE_DIR, output_filename)
            cv2.imwrite(output_path, image)
            print(f"✅ Saved unique slide: {output_filename}")
            unique_count += 1
        else:
            print(f"🟡 Skipped duplicate: {filename}")

    return unique_count


def create_pdf_from_unique_slides():
    print("\n📄 Creating PDF from unique slides...")
    pdf = FPDF(unit="pt")  # use points for pixel-perfect layout
    slide_files = sorted(
        [
            f
            for f in os.listdir(UNIQUE_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    )

    for filename in slide_files:
        path = os.path.join(UNIQUE_DIR, filename)
        with Image.open(path) as img:
            img = img.convert("RGB")
            width, height = img.size  # get actual pixel size
            pdf.add_page(format=(width, height))
            pdf.image(path, x=0, y=0, w=width, h=height)
            print(f"📎 Added to PDF: {filename}")

    if slide_files:
        pdf.output(PDF_OUTPUT)
        print(f"\n✅ PDF created with {len(slide_files)} slides → {PDF_OUTPUT}")
    else:
        print("❌ No slides to include in PDF.")


if __name__ == "__main__":
    # count = extract_unique_slides()
    # print(f"\n✅ Total unique slides found: {count}")
    create_pdf_from_unique_slides()
