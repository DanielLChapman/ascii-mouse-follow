from PIL import Image
import numpy as np

def image_to_ascii(image_path, output_width=100):
    # Load the image
    img = Image.open(image_path)
    
    # Calculate the target height of the image to maintain aspect ratio
    aspect_ratio = img.height / img.width
    output_height = int(output_width * aspect_ratio)
    
    # Resize the image
    img = img.resize((output_width, output_height))
    
    # Convert image to grayscale
    img = img.convert("L")
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Updated ASCII character set with a better range of brightness levels
    ascii_chars = "     *.++.++. "  # Dark to light characters

    # Ensure the character mapping covers the full grayscale range correctly
    # The length of your character set is 10, so we divide by 256/10 to map the full range of values
    factor = 256 / len(ascii_chars)

    # Map each pixel to an ASCII char
    ascii_str = ""
    for row in img_array:  # Assuming img_array is a 2D array; each row represents a row of pixels
        for pixel in row:  # Iterate over each pixel in a row
            ascii_str += ascii_chars[int(pixel // factor)]
        ascii_str += '\n'
    
    return ascii_str

# Example usage
image_path = './third_pass/frame_0.png'
ascii_art = image_to_ascii(image_path, output_width=100)
print(ascii_art)

# Optionally, save the ASCII art to a text file
with open('ascii_art.txt', 'w') as file:
    file.write(ascii_art)
