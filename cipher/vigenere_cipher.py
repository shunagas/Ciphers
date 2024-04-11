def encrypt_vigenere(plaintext, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ciphertext = ''

    extended_key = (key * (len(plaintext) // len(key) + 1))[:len(plaintext)]

    # encrypt plaintext
    for p, k in zip(plaintext, extended_key):
        # Find position on the alphabet
        p_index = alphabet.index(p.upper())
        k_index = alphabet.index(k.upper())
        # Convert characters based on sum of positions (modulo 26)
        c = alphabet[(p_index + k_index) % 26]
        ciphertext += c
    
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    plaintext = ''

    extended_key = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]

    # decrypt ciphertext
    for c, k in zip(ciphertext, extended_key):
        # Find position on the alphabet
        c_index = alphabet.index(c.upper())
        k_index = alphabet.index(k.upper())
        # Convert characters based on sum of positions (modulo 26)
        p = alphabet[(c_index - k_index) % 26]
        plaintext += p
    
    return plaintext


plaintext = "HELLOHOGE"
key = "KEY"

ciphertext = encrypt_vigenere(plaintext, key)
print(f"Encrypted: {ciphertext}")

plaintext = decrypt_vigenere(ciphertext, key)
print(f"Decrypted: {plaintext}")