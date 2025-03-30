from PIL import Image
import os

# Set the directory containing your images
image_dir = "/Users/shinil/Downloads/grandma_resize"

# Supported image extensions
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")

max_width = 0
max_height = 0

# Iterate over all files in the directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith(image_extensions):
        image_path = os.path.join(image_dir, filename)
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                if width > max_width:
                    max_width = width
                if height > max_height:
                    max_height = height
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"Maximum width: {max_width}")
print(f"Maximum height: {max_height}")