import os
import natsort

def rename_images(directory):
    # Get all image files in the directory
    images = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Sort images in alphabetical order
    images = natsort.natsorted(images)

    # Renaming logic
    day = 7  # Start from Day 7
    index = 0  # Track the image index (0 or 1)

    for image in images:
        new_name = f"Day_{day}_{index}.jpg"  # New file name
        old_path = os.path.join(directory, image)
        new_path = os.path.join(directory, new_name)
        
        os.rename(old_path, new_path)
        print(f"Renamed: {image} -> {new_name}")

        # Toggle index and increment day after every two images
        if index == 1:
            day += 1
            index = 0
        else:
            index = 1

    print("Renaming completed!")

# Example usage
rename_images("/path")  # Change this to your actual folder path