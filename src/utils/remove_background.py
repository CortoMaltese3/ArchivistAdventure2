from PIL import Image
import glob

def remove_background(image_path):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    background_color = (255, 255, 255)

    new_data = []
    for item in data:
        if item[0] in list(range(background_color[0] - 10, background_color[0] + 10)) and \
           item[1] in list(range(background_color[1] - 10, background_color[1] + 10)) and \
           item[2] in list(range(background_color[2] - 10, background_color[2] + 10)):
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(image_path, "PNG")

# Path to the companions folder
companions_path = 'graphics/companions/*/*/*.png'

# Use glob to iterate through all PNG files in the specified path
for filename in glob.glob(companions_path):
    print(f"Processing {filename}")
    remove_background(filename)

print("Done!")
