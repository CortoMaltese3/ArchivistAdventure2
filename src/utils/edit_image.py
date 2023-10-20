import os
import logging
from PIL import Image

# Setting up basic logging configuration
logging.basicConfig(level=logging.INFO, format='[%(levelname)s]: %(message)s')

class ImageEditor:
    def __init__(self, image_path):
        self.image_path = image_path

    def resize_image(self):
        """Resize the image by a factor of 1.5 using the LANCZOS filter."""
        try:
            if os.path.exists(self.image_path):
                with Image.open(self.image_path) as img:
                    width, height = img.size
                    new_width = int(width * 1.5)
                    new_height = int(height * 1.5)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    img.save(self.image_path)
            else:
                logging.error(f"Image not found at {self.image_path}")
        except Exception as e:
            logging.error(f"Error resizing image at {self.image_path}. Error: {e}")

    def search_images(self, action_function):
        """Search for PNG images in the specified directory and apply the action function."""
        for dirpath, _, filenames in os.walk(self.image_path):
            for filename in filenames:
                if filename.endswith(".png"):
                    full_path = os.path.join(dirpath, filename)
                    action_function(full_path)

    def detect_background_color(self):
        """Detect the background color of the image by checking the top-left pixel."""
        with Image.open(self.image_path) as img:
            return img.getpixel((0, 0))

    def remove_background(self, background_color=(255, 255, 255)):
        """Remove the background of the image based on the specified background color."""
        try:
            if os.path.exists(self.image_path):
                img = Image.open(self.image_path).convert("RGBA")
                data = img.getdata()

                new_data = [
                    (0, 0, 0, 0) if item[:3] == background_color else item for item in data
                ]

                img.putdata(new_data)
                img.save(self.image_path, "PNG")
            else:
                logging.error(f"Image not found at {self.image_path}")
        except Exception as e:
            logging.error(f"Error removing background from {self.image_path}. Error: {e}")

if __name__ == "__main__":
    root_folder = "graphics\\entities\\player\\up"
    image_editor = ImageEditor(root_folder)
    
    logging.info("Resizing images...")
    image_editor.search_images(image_editor.resize_image)

    logging.info("Removing backgrounds...")
    image_editor.search_images(image_editor.remove_background)

    logging.info("Done!")
