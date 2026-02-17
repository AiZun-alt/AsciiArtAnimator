from PIL import Image
import os
import argparse
import sys # Added for sys.exit

def get_ascii_char(pixel_intensity, char_set):
    """Maps a pixel intensity (0-255) to an ASCII character.
    The char_set should be ordered from brightest to darkest for typical dark-on-light terminal backgrounds.
    E.g., ' .:-=+*#%@' means ' ' is brightest (for black pixels) and '@' is darkest (for white pixels).
    """
    index = int(pixel_intensity / 256 * len(char_set))
    return char_set[index]

def image_to_ascii(image_path, output_width=100, char_set=' .:-=+*#%@'):
    """Converts an image to ASCII art string.
    
    Args:
        image_path (str): Path to the image file.
        output_width (int): Desired width of the ASCII art output in characters.
        char_set (str): String of characters to use for ASCII art, ordered brightest to darkest.

    Returns:
        str: The ASCII art representation of the image, or an error message.
    """
    if not os.path.exists(image_path):
        # This check is now also done in the main block before calling, but kept for function robustness.
        return f"Error: Image '{image_path}' not found."

    try:
        image = Image.open(image_path)
    except Exception as e:
        return f"Error opening image: {e}"

    # Calculate aspect ratio and new height. Terminal characters are typically taller than wide,
    # so we adjust the height to prevent the image from looking stretched.
    width, height = image.size
    aspect_ratio = height / width
    output_height = int(output_width * aspect_ratio * 0.55) # 0.55 is an approximate terminal character aspect ratio

    # Resize image and convert to grayscale ('L' mode)
    image = image.resize((output_width, output_height))
    image = image.convert('L') 

    pixels = image.getdata()
    ascii_art_chars = []
    for i, pixel_intensity in enumerate(pixels):
        ascii_art_chars.append(get_ascii_char(pixel_intensity, char_set))
        if (i + 1) % output_width == 0: # Add a newline after each row
            ascii_art_chars.append('\n')
    return "".join(ascii_art_chars)

if __name__ == "__main__":
    # Usage: python main.py <path_to_image.jpg>
    parser = argparse.ArgumentParser(description='Convert an image to ASCII art and display it in the terminal.')
    parser.add_argument('image_path', help='Path to the input image file (e.g., image.jpg)')
    args = parser.parse_args()

    # Implement basic error handling
    if not os.path.exists(args.image_path):
        print(f"Error: Image file not found at '{args.image_path}'")
        sys.exit(1)

    print("Welcome to AsciiArtAnimator!")
    print("----------------------------")
    print("To run this, you need to install Pillow: pip install Pillow")
    print("Provide the image path as a command-line argument.")
    print("----------------------------\n")

    # Replace hardcoded image path with the command-line argument
    image_file = args.image_path 

    # The auto-download logic is removed as the user is expected to provide an existing image path.

    print(f"Converting '{image_file}' to ASCII art...")
    # Adjust output_width for your terminal size for best results.
    # Common values are 80-120 characters.
    art = image_to_ascii(image_file, output_width=80)
    
    # Check if image_to_ascii returned an error message
    if art.startswith("Error:"):
        print(art)
        sys.exit(1)
    else:
        print(art)

    print("\n--- AsciiArtAnimator ---\n")
    print("This is just the beginning! Here are some ideas to expand this project:")
    print("- **GIF Animation:** Load multi-frame GIFs, clear the console (os.system('cls' or 'clear')), and print each frame sequentially to create animations.")
    print("- **Color Support:** Use ANSI escape codes to add color to the ASCII characters, based on the original pixel's color.")
    print("- **Custom Character Sets:** Allow users to define or select different sets of ASCII characters for varied visual styles.")
    print("- **Web Interface:** Build a simple web application (using Flask or FastAPI) where users can upload images and see the generated ASCII art in their browser.")
    print("- **Real-time Camera Input:** Convert a live webcam feed into ASCII art for a really cool, interactive experience (requires OpenCV library).")
    print("- **Image Filters:** Add options to apply simple image filters (e.g., contrast, brightness, edge detection) before ASCII conversion.")