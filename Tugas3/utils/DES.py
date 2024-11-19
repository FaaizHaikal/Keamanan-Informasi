from bitarray import bitarray
from bitarray.util import ba2int, int2ba

# 1, 2, 3, 4, 5, 6, 7, 8,
# 9, 10, 11, 12, 13, 14, 15, 16,
# 17, 18, 19, 20, 21, 22, 23, 24,
# 25, 26, 27, 28, 29, 30, 31, 32,
# 33, 34, 35, 36, 37, 38, 39, 40,
# 41, 42, 43, 44, 45, 46, 47, 48,
# 49, 50, 51, 52, 53, 54, 55, 56,
# 57, 58, 59, 60, 61, 62, 63, 64

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

INV_IP = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

EXPANSION = [32, 1, 2, 3, 4, 5, 4, 5,
            6, 7, 8, 9, 8, 9, 10, 11,
            12, 13, 12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21, 20, 21,
            22, 23, 24, 25, 24, 25, 26, 27,
            28, 29, 28, 29, 30, 31, 32, 1]

S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

PERM = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

PC1 = [57, 49, 41, 33, 25, 17, 9,
   1, 58, 50, 42, 34, 26, 18,
   10, 2, 59, 51, 43, 35, 27,
   19, 11, 3, 60, 52, 44, 36,
   63, 55, 47, 39, 31, 23, 15,
   7, 62, 54, 46, 38, 30, 22,
   14, 6, 61, 53, 45, 37, 29,
   21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
   3, 28, 15, 6, 21, 10,
   23, 19, 12, 4, 26, 8,
   16, 7, 27, 20, 13, 2,
   41, 52, 31, 37, 47, 55,
   30, 40, 51, 45, 33, 48,
   44, 49, 39, 56, 34, 53,
   46, 42, 50, 36, 29, 32]

SHIFT = [1, 1, 2, 2, 2, 2, 2, 2,
         1, 2, 2, 2, 2, 2, 2, 1]

class DES:
  def __init__(self, key="APALAHKEY"):
    self.rounds = 16
    self.key = self.str_to_bitarray(key)
    self.subkeys = self.generate_subkeys()
  
  def generate_subkeys(self):
    key_56 = self.permute(self.key, PC1)

    subkeys = []
    left = key_56[:28]
    right = key_56[28:]

    for i in range(self.rounds):
      left = self.left_shift(left, SHIFT[i])
      right = self.left_shift(right, SHIFT[i])
      subkey = self.permute(left + right, PC2)
      subkeys.append(subkey)

    return subkeys

  def str_to_bitarray(self, s):
    ba = bitarray()
    ba.frombytes(s.encode('utf-8'))

    return ba
  
  def bitarray_to_str(self, ba):
    return ba.tobytes().decode('utf-8')
  
  def bitarray_to_hex(self, ba):
    return ba.tobytes().hex()
  
  def hex_to_bitarray(self, s):
    ba = bitarray()
    ba.frombytes(bytes.fromhex(s))

    return ba
  
  def bitarray_to_str(self, b):
    return b.tobytes().decode('utf-8')
  
  def permute(self, bits, table):
    return bitarray([bits[i - 1] for i in table])
  
  def expand(self, bits):
    return self.permute(bits, EXPANSION)
  
  def left_shift(self, bits, n):
    return bits[n:] + bits[:n]
  
  def xor(self, a, b):
    return a ^ b
  
  def s_box(self, bits):
    output = bitarray()
    for i in range(8):
      block = bits[i * 6:(i + 1) * 6]
      row = ba2int(block[:1] + block[5:])
      col = ba2int(block[1:5])
      val = S_BOX[i][row][col]
      output.extend(int2ba(val, length=4))

    return output
  
  def f_function(self, right, subkey):
    right_expanded = self.expand(right)
    right_expanded = self.xor(right_expanded, subkey)
    right_expanded = self.s_box(right_expanded)

    return self.permute(right_expanded, PERM)
  
  def pad(self, s):
    pad_len = 8 - (len(s) % 8)
    return s + chr(pad_len) * pad_len

  def unpad(self, s):
    pad_len = ord(s[-1])
    return s[:-pad_len]

  def encrypt(self, plaintext):
    plaintext = self.pad(plaintext)
    ciphertext = bitarray()
  
    for i in range(0, len(plaintext), 8):
      block = self.str_to_bitarray(plaintext[i:i + 8])
      block = self.permute(block, IP)

      left = block[:32]
      right = block[32:]

      for subkey in self.subkeys:
        left, right = right, self.xor(left, self.f_function(right, subkey))

      ciphertext += self.permute(right + left, INV_IP)

    return self.bitarray_to_hex(ciphertext)
  
  def decrypt(self, ciphertext):
    ciphertext = self.hex_to_bitarray(ciphertext)
    plaintext = bitarray()

    for i in range(0, len(ciphertext), 64):
      block = ciphertext[i:i + 64]
      block = self.permute(block, IP)

      left = block[:32]
      right = block[32:]

      for subkey in reversed(self.subkeys):
        left, right = right, self.xor(left, self.f_function(right, subkey))

      plaintext += self.permute(right + left, INV_IP)
    
    return self.unpad(self.bitarray_to_str(plaintext))
  
if __name__ == "__main__":
  KEY = "APALAHKEY"
  des = DES(KEY)
  plaintext = "CHAHAHAHAHB"
  ciphertext = des.encrypt(plaintext)
  decrypted = des.decrypt(ciphertext)
  print(f"Plaintext: {plaintext}")
  print(f"Ciphertext: {ciphertext}")
  print(f"Decrypted: {decrypted}")
  print(f"Match: {plaintext == decrypted}")