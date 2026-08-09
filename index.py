from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    # Open the original image
    input_image = Image.open(input_path)
    
    # Process and remove the background
    output_image = remove(input_image)
    
    # Save the result as a PNG to preserve transparency
    output_image.save(output_path, "PNG")
    print(f"Success! Saved to {output_path}")

if __name__ == "__main__":
    remove_background("my-photo.jpeg", "output_transparent.png")
