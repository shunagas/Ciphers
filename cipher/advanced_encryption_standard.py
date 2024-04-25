'''ガロア体GF(2^8）を用意してS_BOXを生成する。(256bit)
    MixColumns関数で行われる計算'''
def galois_multiplication(a, b):
    """Perform multiplication in GF(2^8)."""
    p = 0
    for i in range(8):
        if b & 0x01:# &はビット単位のAND演算子
            p ^= a
        carry = a & 0x80 
        a <<= 1
        if carry: #あふれがあれば、削除する処理
            a ^= 0x11b  # x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p

def inverse_sbox(byte):
    """Find multiplicative inverse in GF(2^8)."""
    if byte == 0:
        return 0
    # Find the inverse in GF(2^8)
    for i in range(256):
        if galois_multiplication(i, byte) == 1:
            return i

def affine_transformation(byte):
    """Apply the affine transformation used in the AES S-Box."""
    mask = 0x63  # 01100011
    result = 0
    for i in range(8):
        temp = byte
        for j in range(4):
            temp ^= (byte >> (j+1)) & 0x01
        result |= ((temp ^ mask) & 0x01) << i
        byte >>= 1
    return result

def generate_sbox():
    """Generate the AES S-Box."""
    sbox = [0] * 256
    for i in range(256):
        inv = inverse_sbox(i)
        sbox[i] = affine_transformation(inv)
    return sbox

# S-Boxの生成
sbox = generate_sbox()
S_BOX = sbox

# ShiftRows関数
def shift_rows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state

# MixColumns関数
def mix_columns(state):
    # MixColumnsの固定行列（ガロア体の乗算を含む）
    matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    # 4x4の状態行列を作成
    new_state = [[0] * 4 for _ in range(4)]

    # ガロア体上での乗算と加算を行う
    for r in range(4):
        for c in range(4):
            new_state[r][c] = sum(galois_mult(matrix[r][x], state[x][c]) for x in range(4))

    return new_state

def galois_mult(a, b):
    """Perform multiplication in GF(2^8)."""
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        carry = a & 0x80
        a <<= 1
        if carry:
            a ^= 0x11b
        b >>= 1
    return p

 # 4x4のキー行列にフォーマット変換
def format_key(key):
    return [key[i*4:(i+1)*4] for i in range(4)]

# AddRoundKey関数
def add_round_key(state, key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]
    return state

# 暗号化関数
def aes_encrypt(plaintext, key):
    state = [[0] * 4 for _ in range(4)] # 4×4の状態行列を初期化

    # 平文を状態行列にロード
    for i in range(4):
        for j in range(4):
            state[j][i] = plaintext[i * 4 + j]

    key = format_key(key)  # キーを4x4の行列にフォーマット
    state = add_round_key(state, key) # 初期ラウンドキー加算

    # ラウンド数(AES-128では10ラウンド)
    for round in range(1, 10):
        # S_BOXを適用
        state = [[S_BOX[b] for b in row] for row in state]
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key)
    # 最終ラウンド（MixColumnsは適用しない）
    state = [[S_BOX[b] for b in row] for row in state]
    state = shift_rows(state)
    state = add_round_key(state, key)

    # 暗号文を抽出
    ciphertext = []
    for i in range(4):
        for j in range(4):
            ciphertext.append(state[j][i])
    return bytes(ciphertext)

plaintext = [0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x15, 0x88, 0x09, 0xcf, 0x4f, 0x3c]  # キー（AES-128の例）

encrypted = aes_encrypt(plaintext, key)
print("Encrypted:", encrypted)