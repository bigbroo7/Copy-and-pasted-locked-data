import pyautogui
import pyperclip
import time
import threading
from pynput import keyboard, mouse

# --- CONFIGURATION ---
TRIGGER_KEY = keyboard.Key.shift_l  # Hold Left Shift to activate
EXIT_KEY = keyboard.Key.esc         # Press Esc to exit the script
POLLING_INTERVAL = 0.1              # How often to check for text under the cursor (in seconds)

# --- GLOBAL STATE ---
last_copied_text = ""
running = True

def get_text_under_cursor():
    """Attempts to get text under the cursor using OCR."""
    try:
        # Define a small region around the cursor to capture
        x, y = pyautogui.position()
        region = (x - 50, y - 15, 100, 30) # (left, top, width, height)

        # Take a screenshot of the region
        screenshot = pyautogui.screenshot(region=region)

        # Convert the screenshot to text using OCR
        # Note: This requires an OCR engine like Tesseract to be installed.
        # If you get an error, you may need to install it:
        # - Windows: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
        # - macOS: `brew install tesseract`
        # - Linux: `sudo apt-get install tesseract-ocr`
        text = pyautogui.image_to_string(screenshot, lang='eng', config='--psm 7')

        return text.strip()

    except Exception as e:
        # This can fail if Tesseract is not installed or other issues occur.
        print(f"Error during OCR: {e}")
        return None

def on_key_press(key):
    """Handles key press events."""
    global last_copied_text
    if key == TRIGGER_KEY:
        # When trigger key is pressed, get text and copy it
        current_text = get_text_under_cursor()
        if current_text and current_text != last_copied_text:
            pyperclip.copy(current_text)
            last_copied_text = current_text
            print(f"Copied to clipboard: '{current_text}'")
    elif key == EXIT_KEY:
        global running
        running = False
        return False  # Stop the listener

def main():
    """Main function to run the listener."""
    print("--- Magic Mouse Script ---")
    print(f"Hold '{TRIGGER_KEY}' to copy text under the cursor.")
    print(f"Press '{EXIT_KEY}' to exit.")
    print("Note: This script requires Tesseract OCR to be installed.")
    print("---------------------------\n")

    # Start the keyboard listener in a non-blocking way
    with keyboard.Listener(on_press=on_key_press) as listener:
        while running:
            # Keep the main thread alive to listen for key presses
            time.sleep(0.1)
        
        listener.stop()

if __name__ == "__main__":
    main()