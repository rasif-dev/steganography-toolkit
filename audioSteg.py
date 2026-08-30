import os
import wave
import numpy as np
from cryptography.fernet import Fernet, InvalidToken

HEADER_SIZE = 32

class audioSteg():
    def __init__(self):
        pass

    def hide(self, secret_message, input_audio_path, output_audio_path):

        # 1. Check input file exists
        if not os.path.exists(input_audio_path):
            print(f"\n❌ ERROR: Input file '{input_audio_path}' does not exist!")
            return None

        print("\n\nUSING AUDIO STEGNOGRAPHY\n\n")
        
        # --- GUARD RAILS (Force WAV) ---
        if not input_audio_path.lower().endswith('.wav'):
            print("ERROR: Only WAV files are supported.")
            return None
        
        if not output_audio_path.lower().endswith('.wav'):
            base, _ = os.path.splitext(output_audio_path)
            output_audio_path = base + '.wav'
            print(f"[!] Output forced to: {output_audio_path}")

        key = Fernet.generate_key()
        cipher = Fernet(key)
        print(f"Audio stego key: {key.decode()}\n")

        # encrypt the secret message
        encrypt_secret = cipher.encrypt(secret_message.encode())

        # get encrypted bits in raw bits
        secret_byte = bytearray()
        for byte in encrypt_secret:
            for i in range(7, -1, -1):
                bit = (byte >> i) & 1
                secret_byte.append(bit)

        if (len(secret_byte) > 2**HEADER_SIZE):
            print("SIZE ERROR: Secret text is too big!")
            return None
        try:
            with wave.open(input_audio_path, 'rb') as wav:
                # 1. Read the header parameters
                params = wav.getparams()
                
                nchannels, sampwidth, framerate, nframes = params[:4]

                if (len(secret_byte) > nframes - HEADER_SIZE):
                    print("SIZE ERROR: Audio is too small to hide the secret in it!")
                    return None

                print(f"Channels: {nchannels}")
                print(f"Sample width: {sampwidth} bytes (16-bit)")
                print(f"Frame rate: {framerate} Hz")
                print(f"Total frames: {nframes}")

                # 2. Read ALL audio data as raw bytes
                frames = wav.readframes(nframes)
                samples = self.read_samples(frames, sampwidth)

                # convert the size of encrypted secret into bytes array
                size_byte = len(secret_byte).to_bytes(4, byteorder="big")
                size_array = bytearray()
                for byte in size_byte:
                    for i in range(7, -1, -1):
                        bit = (byte >> i) & 1
                        size_array.append(bit)

                size_array.extend(secret_byte)

                # embed the secret message into the audio file
                byte_index = 0
                for bit in size_array:
                    if (bit):
                        samples[byte_index] = samples[byte_index] | 1
                    else:
                        samples[byte_index] = samples[byte_index] & 0xFE
                    byte_index += 1
                
                # convert modified integer array frames for wav file
                modified_frames = self.write_samples(samples, sampwidth)

                # store the new data into a file
                with wave.open(output_audio_path, 'wb') as wav:
                    wav.setparams(params)
                    wav.writeframes(modified_frames)
            return key

        except Exception as e:
                    print(f"❌ Error reading audio file: {e}")
                    return None
    
    def find(self, input_audio_path, key):

        # --- FILE EXISTENCE CHECK (NEW) ---
        if not os.path.exists(input_audio_path):
            print(f"❌ Error: File not found at '{input_audio_path}'")
            return None

        # --- GUARD RAILS (Force WAV) ---
        if not input_audio_path.lower().endswith('.wav'):
            print("ERROR: Only WAV files are supported.")
            return None

        print("\n\nUSING AUDIO STEGNOGRAPHY DECODER\n\n")

        # set up the cipher
        try:
            cipher = Fernet(key)
            print(f"🔑 Using key: {key}\n")
        except Exception as e:
            print(f"❌ Invalid key")
            return None
        try:
            with wave.open(input_audio_path, "rb") as wav:

                # read the raw bytes from the file to a int array
                frame_size = wav.getnframes()
                frames = wav.readframes(frame_size)
                samples = self.read_samples(frames, wav.getsampwidth())

                if len(samples) < HEADER_SIZE:
                    print("❌ Audio file is too small to contain a hidden message.")
                    return None
                
                # get secret message size
                secret_size = 0
                index = 0
                while (index < HEADER_SIZE):
                    secret_size = (secret_size << 1)
                    if (samples[index] & 1):
                        secret_size = secret_size | 1
                    index += 1
 
                if secret_size > len(samples) * 8:
                    print("❌ Corrupted header or malformed audio file (size mismatch).")
                    return None

                # read the secret message
                encrypted_bits = 0
                end_index = index + secret_size
                while (index < end_index):
                    encrypted_bits = encrypted_bits << 1
                    if (samples[index] & 1):
                        encrypted_bits = encrypted_bits | 1
                    index += 1
                
                try:
                    secret_message = cipher.decrypt(encrypted_bits.to_bytes((secret_size + 7) // 8, byteorder="big")).decode()
                except InvalidToken:
                    print("❌ Decryption failed: Invalid key or corrupted audio data.")
                    return None
                except Exception as e:
                    print(f"❌ Decryption error: {e}")
                    return None

                print("Secret Message is: " + secret_message)
                
        except Exception as e:
            print(f"❌ Error reading audio file: {e}")
            return None


    def read_samples(self, frames, sampwidth):
        # Convert raw WAV bytes to a numpy array, keeping native dtype when possible.
        if sampwidth == 1:
            # 8-bit WAV is unsigned (0 to 255). Keep it as uint8.
            return np.frombuffer(frames, dtype=np.uint8).copy()
        elif sampwidth == 2:
            # 16-bit signed little-endian
            return np.frombuffer(frames, dtype='<i2').copy()
        elif sampwidth == 3:
            # 24-bit has no native type -> convert to signed int32
            b = np.frombuffer(frames, dtype=np.uint8).reshape(-1, 3)
            val = b[:, 0] | (b[:, 1] << 8) | (b[:, 2] << 16)
            # Sign extend (if the 24th bit is set, subtract 2^24)
            val = np.where(val & 0x800000, val - 0x1000000, val)
            return val.astype(np.int32).copy()
        elif sampwidth == 4:
            # 32-bit signed little-endian
            return np.frombuffer(frames, dtype='<i4').copy()
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth} bytes")

    def write_samples(self, samples, sampwidth):
        if sampwidth == 1:
            return samples.astype(np.uint8).tobytes()
        elif sampwidth == 2:
            return samples.astype('<i2').tobytes()
        elif sampwidth == 3:
            # Clamp to signed 24-bit range
            samples = np.clip(samples, -8388608, 8388607).astype(np.int32)
            # Mask to 24 bits (keeps the sign bits in the correct place)
            masked = samples & 0x00FFFFFF
            b0 = (masked & 0x0000FF).astype(np.uint8)
            b1 = ((masked >> 8) & 0x0000FF).astype(np.uint8)
            b2 = ((masked >> 16) & 0x0000FF).astype(np.uint8)
            return np.stack([b0, b1, b2], axis=1).tobytes()
        elif sampwidth == 4:
            return samples.astype('<i4').tobytes()
        else:
            raise ValueError(f"Unsupported sample width: {sampwidth} bytes")

