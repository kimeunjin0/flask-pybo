import os

# Define the directory for the images
image_dir = 'C:/projects/myproject/myshop/static/images'

# Define the target filenames
image_filenames = [
    "cotton_shirt.jpg",
    "denim_jeans.jpg",
    "summer_dress.jpg",
    "leather_jacket.jpg",
    "sneakers.jpg",
    "wool_coat.jpg",
    "casual_trousers.jpg",
    "silk_scarf.jpg",
    "linen_shorts.jpg",
    "baseball_cap.jpg"
]

# List all jpg files in the directory
jpg_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Ensure there are exactly 10 jpg files
if len(jpg_files) != 10:
    raise ValueError("The directory must contain exactly 10 jpg files.")

# Rename the files
for old_name, new_name in zip(jpg_files, image_filenames):
    old_path = os.path.join(image_dir, old_name)
    new_path = os.path.join(image_dir, new_name)
    os.rename(old_path, new_path)

print("Files have been renamed successfully.")
