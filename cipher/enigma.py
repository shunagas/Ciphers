import random

class Rotor:
    def __init__(self, wiring, notch, offset=0):
        self.wiring = wiring
        self.notch = notch
        self.offset = offset

    def encrypt_forward(self, c):
        index = (ord(c) - ord('A') + self.offset) % 26
        return self.wiring[index]

    def encrypt_backward(self, c):
        index = (self.wiring.index(c) - self.offset) % 26
        return chr(index + ord('A'))

    def rotate(self):
        self.offset = (self.offset + 1) % 26
        return self.notch == chr((ord('A') + self.offset - 1) % 26)

class Enigma:
    def __init__(self, rotor1, rotor2, rotor3, reflector, plugboard=None):
        self.rotor1 = rotor1
        self.rotor2 = rotor2
        self.rotor3 = rotor3
        self.reflector = reflector
        self.plugboard = plugboard or {}
        self.initial_offsets = (rotor1.offset, rotor2.offset, rotor3.offset)

    def reset_rotors(self):
        # ローターの初期位置をリセットする
        self.rotor1.offset, self.rotor2.offset, self.rotor3.offset = self.initial_offsets

    def apply_plugboard(self, char):
        return self.plugboard.get(char, char)

    def encrypt(self, plaintext):
        ciphertext = ''
        for char in plaintext.upper():
            if char < 'A' or char > 'Z':
                ciphertext += char
                continue

            char = self.apply_plugboard(char)

            step1 = self.rotor1.encrypt_forward(char)
            step2 = self.rotor2.encrypt_forward(step1)
            step3 = self.rotor3.encrypt_forward(step2)
            reflected = self.reflector[ord(step3) - ord('A')]
            step4 = self.rotor3.encrypt_backward(reflected)
            step5 = self.rotor2.encrypt_backward(step4)
            step6 = self.rotor1.encrypt_backward(step5)

            step6 = self.apply_plugboard(step6)

            if self.rotor1.rotate():
                if self.rotor2.rotate():
                    self.rotor3.rotate()
            
            ciphertext += step6
        return ciphertext

# 利用可能なローターとリフレクターの定義
available_rotors = [
    Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q'),
    Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E'),
    Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V'),
    Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J'), 
    Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
]
reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

# ランダムにローターを選択して初期位置を設定
selected_rotors = random.sample(available_rotors, 3)
for rotor in selected_rotors:
    rotor.offset = random.randint(0, 25)

# プラグボード設定の生成
alphabet = [chr(i) for i in range(ord('A'), ord('Z')+1)]
random.shuffle(alphabet)
plugboard_config = {alphabet[i]: alphabet[i+1] for i in range(0, len(alphabet), 2)}
plugboard_config.update({v: k for k, v in plugboard_config.items()})

# エニグマインスタンスの作成
enigma = Enigma(selected_rotors[0], selected_rotors[1], selected_rotors[2], reflector, plugboard_config)

# テスト
plaintext = "HELLO HOGEHOGE"
ciphertext = enigma.encrypt(plaintext)
print("Encrypted:", ciphertext)
enigma.reset_rotors()
decrypted = enigma.encrypt(ciphertext)
print("Decrypted:", decrypted)