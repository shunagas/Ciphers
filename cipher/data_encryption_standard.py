# generator style
# def xor(a, b):
#     # XOR function for two strings of binary numbers
#     return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

# for roop style（上のジェネレーター方式と同じ内容）
def xor(a, b):
    # XOR function for two strings of binary numbers
    result = []
    for x, y in zip(a, b):
        result.append(str(int(x) ^ int(y))) # ^ はXOR演算子
    return ''.join(result) # resultリストの文字間の間に何も入れない。

# XOR test code
a = '1100110011001100110011001100110011001100110011001100110011001100'
b = '1010101010111011000010010001100000100111001101101100110011011101'
print(xor(a, b))  # Output the result of the XOR operation

def f_function(right, subkey):
    # Placeholder for the round function F
    # この関数は暗号アルゴリズムと核となるため、実装する際は適正な関数にする
    return xor(right, subkey)

def generate_subkeys(key):
    # Plaseholder for generaring subkeys
    # 実装するときは適切なキー・スケジューリングにする必要があります。
    return [key] * 16 # simple same subkey

def des_encrypt(block, key):
    # Encrypt a single block of 64 bits using DES algorithm
    if len(block) != 64:
        raise ValueError("Block must be exactly 64 bits long")
    
    # Initital permuration(IP) step is skipped for simplicity
    left, right = block[:32], block[32:] # スライスを使用　[:32]index[0]（最初）からindex[31], [32:]index[32]からindex[63]（最後）

    subkeys = generate_subkeys(key)

    for round_number in range(16):
        new_right = xor(left, f_function(right, subkeys[round_number]))
        left = right
        right = new_right

    return left + right    

key = '1010101010111011000010010001100000100111001101101100110011011101'[:56]  # example key (56-bit)
block = '1100110011001100110011001100110011001100110011001100110011001100'  # example 64-bit block

encrypted = des_encrypt(block, key)
print(f"Encrypted block: {encrypted}")