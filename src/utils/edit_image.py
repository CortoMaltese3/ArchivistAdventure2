import os
import logging
from PIL import Image

# Setting up basic logging configuration
logging.basicConfig(level=logging.INFO, format="[%(levelname)s]: %(message)s")


class ImageEditor:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def resize_image(self, image_path):
        """Resize the image by a factor of 1.5 using the LANCZOS filter."""
        try:
            if os.path.exists(image_path):
                with Image.open(image_path) as img:
                    width, height = img.size
                    new_width = int(width * 1.5)
                    new_height = int(height * 1.5)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    img.save(image_path)
            else:
                logging.error(f"Image not found at {image_path}")
        except Exception as e:
            logging.error(f"Error resizing image at {image_path}. Error: {e}")

    def search_images(self, action_function):
        """Search for PNG images in the specified directory and apply the action function."""
        for dirpath, _, filenames in os.walk(self.directory_path):
            for filename in filenames:
                if filename.endswith(".png"):
                    full_path = os.path.join(dirpath, filename)
                    action_function(full_path)

    def detect_background_color(self, image_path):
        """Detect the background color of the image by averaging the colors of the four corners."""
        with Image.open(image_path) as img:
            # Get the colors of the four corners
            top_left = img.getpixel((0, 0))
            top_right = img.getpixel((img.width - 1, 0))
            bottom_left = img.getpixel((0, img.height - 1))
            bottom_right = img.getpixel((img.width - 1, img.height - 1))

            # Calculate the average color
            average_color = tuple(
                int(sum(x) / 4) for x in zip(top_left, top_right, bottom_left, bottom_right)
            )

            return average_color[:3]  # Return only the RGB values

    def remove_background(self, image_path):
        """Remove the background of the image based on the detected background color."""
        try:
            if os.path.exists(image_path):
                background_color = self.detect_background_color(image_path)
                print(background_color)
                img = Image.open(image_path).convert("RGBA")
                data = img.getdata()

                new_data = [(0, 0, 0, 0) if item[:3] == background_color else item for item in data]

                img.putdata(new_data)
                img.save(image_path, "PNG")
            else:
                logging.error(f"Image not found at {image_path}")
        except Exception as e:
            logging.error(f"Error removing background from {image_path}. Error: {e}")


if __name__ == "__main__":
    root_folder = "graphics\\entities\\player"
    image_editor = ImageEditor(root_folder)

    logging.info("Removing backgrounds...")
    image_editor.search_images(image_editor.remove_background)

    logging.info("Resizing images...")
    image_editor.search_images(image_editor.resize_image)

    logging.info("Done!")
