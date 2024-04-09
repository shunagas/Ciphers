class CaesarCipher:
    def __init__(self) :
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    def decrypt_caesar_cipher(self, text, shift):
        result = ''

        for c in text:
            if c.isalpha():
                is_upper = c.isupper()
                lower_char = c.lower()
                index = self.alphabet.index(lower_char)
                shifted_index = (index - shift +26) % 26
                shifted_char = self.alphabet[shifted_index]
                result += shifted_char.upper() if is_upper else shifted_char
            else:
                result += c
        return result     

    def try_all_shifts(self, encrypted_text):
        for shift in range(26):
            decrypted_text = self.decrypt_caesar_cipher(encrypted_text, shift)
            print(f'Shift {shift}: {decrypted_text}')   

if __name__ == '__main__':
    cipher = CaesarCipher()
    encrypted_text = 'EAYHM'
    cipher.try_all_shifts(encrypted_text)