from PIL import Image
import os

folder = "shooter/assets/"  # Change this if needed

for root, _, files in os.walk(folder):
    for file in files:
        if file.endswith(".png"):
            img_path = os.path.join(root, file)
            img = Image.open(img_path)
            
            # Check if ICC profile exists
            if "icc_profile" in img.info:
                print(f"ICC profile still exists in: {img_path}")
            else:
                print(f"No ICC profile in: {img_path}")
