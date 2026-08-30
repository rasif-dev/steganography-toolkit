from cryptography.fernet import Fernet, InvalidToken

# We need to pick two "invisible" Unicode characters.
# \u200B = Zero Width Space (We will use this for BIT 1)
# \u200C = Zero Width Non-Joiner (We will use this for BIT 0)
CHAR_ONE = '\u200B'   
CHAR_ZERO = '\u200C'   

class zeroWidthSteg():
    def __init__(self):
        pass

    def hide(self, real_text, mask_text):

        print("\n\nUSING ZERO WIDTH STEGNOGRAPHY\n\n")
        # 1a. Generate a password (In a real app, the sender/receiver agree on this).
        # Fernet.generate_key() creates a random password for us.
        key = Fernet.generate_key()
        print(f"This is the key for text stegnography: {key.decode()}\n")

        # 1b. Create a cipher tool using that password.
        cipher = Fernet(key)

        # 1d. Encrypt it!
        # The encrypt() function needs bytes, not a string. So we use .encode() to turn text into bytes.
        encrypted_bytes = cipher.encrypt(real_text.encode())

        # Let's see what encryption does.
        print(f"Original text: {real_text}")
        print(f"Encrypted bytes (gibberish): {encrypted_bytes.decode()}")

        # Now we convert the ebcrypted message into binary and see which bits are 1 and 0
        binary_secret = ''.join(format(byte, '08b') for byte in encrypted_bytes)

        final_message = []
        bit_index  = 0

        for char in mask_text:
            final_message.append(char)

            if (bit_index < len(binary_secret)):
                if (binary_secret[bit_index] == '1'):
                    final_message.append(CHAR_ONE)
                elif (binary_secret[bit_index] == '0'):
                    final_message.append(CHAR_ZERO)
                bit_index += 1

        for char in binary_secret[bit_index:]:
            if (char == '1'):
                final_message.append(CHAR_ONE)
            elif (char == '0'):
                final_message.append(CHAR_ZERO)
            bit_index += 1


        final_message = ''.join(final_message)
        print ("Final message: ", final_message)
        print(f"Total characters in final text (visible + invisible): {len(final_message)}")
        return (final_message, key)


    def find(self, final_message, key):

        print("\n\nUSING ZERO WIDTH STEGNOGRAPHY DECODER\n\n")

        mask_text = []
        real_message = []
        for char in final_message:
            if (char == CHAR_ONE):
                real_message.append("1")
            elif (char == CHAR_ZERO):
                real_message.append("0")
            else:
                mask_text.append(char)

        if not real_message:
            print("❌ No hidden bits found in this text.")
            return None

        big_int = int(''.join(real_message), 2)
        real_message = big_int.to_bytes((len(real_message) + 7) // 8, byteorder="big")
        
        try:
            cipher = Fernet(key)
            print(f"🔑 Using key: {key}\n")
            real_message = cipher.decrypt(real_message).decode()
        except InvalidToken:
            print("❌ Decryption failed: Invalid key or corrupted data.")
            return None
        except Exception as e:
            print(f"❌ An error occurred during decryption: {e}")
            return None

        mask_text = ''.join(mask_text)
        print("Mask text: ", mask_text)
        print("Real (Secret Message): ", real_message)
        return (real_message, mask_text)
