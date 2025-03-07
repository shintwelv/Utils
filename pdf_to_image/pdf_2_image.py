import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images(pdf_path, output_folder):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Open the PDF
    doc = fitz.open(pdf_path)

    for page_number in range(len(doc)):
        # Render page to a pixmap (image)
        page = doc[page_number]
        pix = page.get_pixmap()

        # Convert to an image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Calculate 1% margin for cropping
        margin_x = int(0.01 * pix.width)
        margin_y = int(0.01 * pix.height)

        # Crop the image (remove 1% margin from edges)
        cropped_img = img.crop((margin_x, margin_y, pix.width - margin_x, pix.height - margin_y))

        # Save as JPEG with an indexed name
        output_path = os.path.join(output_folder, f"page_{page_number + 1}.jpg")
        cropped_img.save(output_path, "JPEG")

        print(f"Saved: {output_path}")

    print("PDF conversion completed!")

# Example usage
pdf_to_images("/path", "output_images")