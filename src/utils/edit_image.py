import os
from PIL import Image


def resize_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        new_width = int(width * 1.5)
        new_height = int(height * 1.5)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        img.save(image_path)


def search_and_resize(root_folder):
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".png"):
                full_path = os.path.join(dirpath, filename)
                resize_image(full_path)


if __name__ == "__main__":
    root_folder = "graphics\\weapons\\pickaxe"
    search_and_resize(root_folder)
