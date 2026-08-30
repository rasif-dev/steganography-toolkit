from cryptography.fernet import Fernet, InvalidToken
from PIL import Image
import numpy as np
import os

HEADER_SIZE = 32

class imageSteg():
    def __init__(self):
        pass

    def hide(self, secret_message, input_img_path, output_img_path):

        # Open image and convert it into an array of bytes
        try:
            img = Image.open(input_img_path)
        except Exception:
            print(f"\n❌ File does not exist.")
            return None
                
        print("\n\nUSING IMAGE STEGNOGRAPHY\n\n")
        # Set up the cipher to encrypt the secret message
        key = Fernet.generate_key()
        cipher = Fernet(key)
        print(f"This is the key for image stegnography: {key.decode()}\n")

        # Encrypt message and get byte string
        secret_message = cipher.encrypt(secret_message.encode())
        secret_bytes = ''.join(format(byte, "08b") for byte in secret_message)
        
        # Check whether secret message size could fit in the header
        if (len(secret_bytes) >= 2**HEADER_SIZE):
            print("SIZE ERROR: Secret text is too big!")
            return
        
        pixels = np.array(img)
        original_shape = pixels.shape
        pixels = pixels.flatten()

        # Get the size of input in bits
        if (len(secret_bytes) > (len(pixels) - HEADER_SIZE)):
            print("SIZE ERROR: Image too small to hide the text!")
            return
        
        # Convert secret text size into raw bytes string
        size_bytes = len(secret_bytes).to_bytes(4, byteorder="big")
        size_string = ''.join(format(byte, "08b") for byte in size_bytes)

        data_load = size_string + secret_bytes

        byte_index = 0
        for char in data_load:
            if (char == "1"):
                pixels[byte_index] = pixels[byte_index] | 1
            elif (char == "0"):
                pixels[byte_index] = pixels[byte_index] & 0xFE
            byte_index += 1
        
        pixels = pixels.reshape(original_shape)
        output_image = Image.fromarray(pixels)

        if not output_img_path.lower().endswith((".png")):
            base, ext = os.path.splitext(output_img_path)
            output_img_path = base + ".png" 

        output_image.save(output_img_path)
        print(f"[+] Stego image saved: {output_img_path}")
    
    def find(self, img_path, key):

        print("\n\nUSING IMAGE STEGNOGRAPHY DECODER\n\n")

        if not os.path.exists(img_path):
            print(f"❌ Error: File not found at '{img_path}'")
            return None

        # Set up the cipher to encrypt the secret message
        try:
            cipher = Fernet(key)
            print(f"🔑 Using key: {key}\n")
        except Exception as e:
            print(f"❌ Invalid key")
            return None

        # Open image and them make a array of bytes
        try:
            img = Image.open(img_path)
        except Exception:
            print(f"❌ Error: Could not open image file.")
            return None
        
        pixels = np.array(img).flatten()

        if len(pixels) < HEADER_SIZE:
            print("❌ Image is too small to contain a hidden message.")
            return None

        counter = 0
        encrypted_size = []
        while (counter < HEADER_SIZE):
            encrypted_size.append(str(pixels[counter] & 1))
            counter += 1
        
        size = int(''.join(encrypted_size), 2)

        if size > len(pixels) - HEADER_SIZE:
            print("❌ Corrupted header or malformed image data (size mismatch).")
            return None


        end_count = size + counter
        encrypted_secret = []
        while (counter <  end_count):
            encrypted_secret.append(str(pixels[counter] & 1))
            counter += 1
        
        secret_num = int(''.join(encrypted_secret), 2)
        encrypted_secret = secret_num.to_bytes((len(encrypted_secret) + 7) // 8, byteorder='big')

        try:
            secret = cipher.decrypt(encrypted_secret).decode()
        except InvalidToken:
            print("❌ Decryption failed: Invalid key or corrupted image data.")
            return None
        except Exception as e:
            print(f"❌ Decryption error: {e}")
            return None

        print("The secret message is: " + secret)
        return secret





        




        

        

            








