import sys
from pyfiglet import Figlet

# Import your steganography modules
from zeroWidthChara import zeroWidthSteg
from imageSteg import imageSteg
from audioSteg import audioSteg


def get_valid_choice(prompt: str, min_val: int, max_val: int) -> int:
    """
    Safely get an integer input from the user.
    Prevents crashes from non-numeric or out-of-range inputs.
    This is the ONLY crash protection we need in main.py.
    """
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            print(f"[-] Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("[-] Invalid input. Please enter a number.")


def main():
    # Print the banner ONCE at startup
    fig = Figlet('slant', justify="center")
    print(fig.renderText('Steganography'))
    print("=" * 50)
    print(" Secure Covert Channel Toolkit")
    print(" AES-128-CBC + LSB Steganography")
    print("=" * 50)

    while True:
        print("\n--- Main Menu ---")
        print(" 1. Hide secret in TEXT (zero-width encoding)")
        print(" 2. Hide secret in IMAGE (LSB steganography)")
        print(" 3. Hide secret in AUDIO (LSB steganography)")
        print(" 4. Extract secret from TEXT")
        print(" 5. Extract secret from IMAGE")
        print(" 6. Extract secret from AUDIO")
        print(" 7. Exit")

        choice = get_valid_choice(" Enter your choice (1-7): ", 1, 7)
        print()  # Blank line for readability

        # --- TEXT ENCODING ---
        if choice == 1:
            secret = input(" Enter your secret message: ")
            mask = input(" Enter the cover text (mask): ")
            steg = zeroWidthSteg()
            steg.hide(secret, mask)

        # --- IMAGE ENCODING ---
        elif choice == 2:
            secret = input(" Enter your secret message: ")
            input_path = input(" Enter path to the cover IMAGE: ")
            output_path = input(" Enter path to save the output IMAGE: ")
            steg = imageSteg()
            steg.hide(secret, input_path, output_path)

        # --- AUDIO ENCODING ---
        elif choice == 3:
            secret = input(" Enter your secret message: ")
            input_path = input(" Enter path to the cover AUDIO: ")
            output_path = input(" Enter path to save the output AUDIO: ")
            steg = audioSteg()
            steg.hide(secret, input_path, output_path)

        # --- TEXT DECODING ---
        elif choice == 4:
            text = input(" Enter the text to extract the secret from: ")
            key = input(" Enter the decryption key: ")
            steg = zeroWidthSteg()
            steg.find(text, key)

        # --- IMAGE DECODING ---
        elif choice == 5:
            img_path = input(" Enter path to the IMAGE to extract from: ")
            key = input(" Enter the decryption key: ")
            steg = imageSteg()
            steg.find(img_path, key)

        # --- AUDIO DECODING ---
        elif choice == 6:
            audio_path = input(" Enter path to the AUDIO to extract from: ")
            key = input(" Enter the decryption key: ")
            steg = audioSteg()
            steg.find(audio_path, key)

        # --- EXIT ---
        elif choice == 7:
            print("[+] Exiting toolkit. Goodbye!")
            sys.exit(0)


if __name__ == "__main__":
    main()