import os
from PIL import Image

def get_max_dimensions(image_dir):
    max_width, max_height = 0, 0
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            path = os.path.join(image_dir, filename)
            with Image.open(path) as img:
                width, height = img.size
                max_width = max(max_width, width)
                max_height = max(max_height, height)
    return max_width, max_height

def resize_images_to_max_height(image_dir, max_height, output_dir=None):
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            path = os.path.join(image_dir, filename)
            with Image.open(path) as img:
                width, height = img.size
                if height != max_height:
                    # Calculate new width to maintain aspect ratio
                    new_width = int((max_height / height) * width)
                    resized_img = img.resize((new_width, max_height))
                else:
                    resized_img = img

                # Save image
                save_path = os.path.join(output_dir if output_dir else image_dir, filename)
                resized_img.save(save_path)

# Example usage
image_directory = "/Users/shinil/Downloads/grandma"
output_directory = "/Users/shinil/Downloads/grandma_resize"  # or None to overwrite
_, max_height = get_max_dimensions(image_directory)
resize_images_to_max_height(image_directory, max_height, output_directory)