import pyautogui
import pyperclip
import time
import sys
from pynput import keyboard, mouse
import pytesseract
from PIL import ImageGrab

# --- CONFIGURATION ---
TRIGGER_KEY = keyboard.Key.shift_l  # Hold Left Shift to activate
EXIT_KEY = keyboard.Key.esc         # Press Esc to exit the script
POLLING_INTERVAL = 0.1              # How often to check for text under the cursor (in seconds)

# --- GLOBAL STATE ---
last_copied_text = ""
running = True
shift_pressed = False

def get_text_under_cursor():
    """Attempts to get text under the cursor using OCR."""
    try:
        # Define a region around the cursor to capture
        x, y = pyautogui.position()
        region = (x - 100, y - 50, 200, 100)  # (left, top, width, height)
        
        # Ensure region is within screen bounds
        left, top, width, height = region
        if left < 0:
            left = 0
        if top < 0:
            top = 0

        # Take a screenshot of the region
        screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

        # Convert the screenshot to text using OCR
        text = pytesseract.image_to_string(screenshot)

        return text.strip() if text else None

    except Exception as e:
        print(f"Error during OCR: {e}")
        return None

def on_key_press(key):
    """Handles key press events."""
    global last_copied_text, shift_pressed, running
    
    try:
        if key == TRIGGER_KEY:
            shift_pressed = True
            print("Shift pressed - capturing text...")
            current_text = get_text_under_cursor()
            if current_text and current_text != last_copied_text:
                pyperclip.copy(current_text)
                last_copied_text = current_text
                print(f"✓ Copied to clipboard: '{current_text}'")
            elif current_text:
                print(f"(Same text as before: '{current_text}')")
            else:
                print("No text detected under cursor")
        
        elif key == EXIT_KEY:
            print("\nExiting Magic Mouse...")
            running = False
            return False  # Stop the listener
    
    except AttributeError:
        pass

def on_key_release(key):
    """Handles key release events."""
    global shift_pressed
    try:
        if key == TRIGGER_KEY:
            shift_pressed = False
    except AttributeError:
        pass

def main():
    """Main function to run the listener."""
    print("╔════════════════════════════════════════╗")
    print("║     🖱���  MAGIC MOUSE - NOW ACTIVE 🖱️     ║")
    print("╚════════════════════════════════════════╝")
    print() 
    print("📋 INSTRUCTIONS:")
    print("  • Hold LEFT SHIFT over any text to copy it")
    print("  • Press ESC to exit")
    print() 
    print("⚙️  REQUIREMENTS:")
    print("  • Tesseract OCR must be installed")
    print("  • Python dependencies installed from requirements.txt")
    print() 
    print("💡 TIP: Move your mouse over text and hold SHIFT to capture it!")
    print("════════════════════════════════════════\n")

    # Start the keyboard listener
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        try:
            while running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nScript interrupted by user.")
            running = False
        
        listener.stop()
    
    print("\n✓ Magic Mouse closed successfully!")

if __name__ == "__main__":
    main()