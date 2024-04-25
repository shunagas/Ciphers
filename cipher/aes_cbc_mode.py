from Crypto.Cipher import AES # AES encryption using pycrypto library. (pycryptodome)
import os

def encrypt_aes(plaintext, key):
    # Ensure plaintext is in bytes
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()  # Convert plaintext to bytes if it's a string

    # Padding to make sure plaintext is a multiple of 16 bytes
    padding_length = 16 - (len(plaintext) % 16) # 足りなかった分は詰め物
    padding = (chr(padding_length) * padding_length).encode()
    plaintext_padded = plaintext + padding # PKCS#7 padding
    
    # Create an AES cipher object
    iv = os.urandom(16) #128bitの初期化ベクトル
    cipher = AES.new(key, AES.MODE_CBC, iv) # CBC mode
    ciphertext = cipher.encrypt(plaintext_padded)
    return ciphertext, iv

def decrypt_aes(ciphertext, key, iv):
    #AES decryption using pycryptodome library.
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    print("Padded plaintext", plaintext_padded)

    # Remove PKCS#7 padding
    padding_length = plaintext_padded[-1]
    plaintext = plaintext_padded[:-padding_length]
    return plaintext.decode()

# 正しいキー長でランダムなキーを生成する
key = os.urandom(32)  # 32バイトのキーでAES-256を使用
plaintext = "I will go on a trip to Langkawi with my girlfriend from May 3 to May 7.We will stay at The Ritz-Carlton Langkawi and The Westin Langkawi for four days."
crypttext, iv = encrypt_aes(plaintext, key)
decrypted_message = decrypt_aes(crypttext, key, iv)
print("Plain text:", plaintext)
print("Encrypt message:", crypttext)
print("Initial vector:", iv)
print("Decrypted message:", decrypted_message)