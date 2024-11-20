import os

class RSA:
  def __init__(self, node):
    self.node = node
    self.read_keys()
    
  def read_keys(self):
    dir = os.path.dirname(__file__)
    public_key_path = os.path.join(dir, f"pub_keys/{self.node}.pem")
    
    with open(public_key_path, "r") as f:
      self.public_key = tuple(map(int, f.read().split(",")))
      
    private_key_path = os.path.join(dir, f"priv_keys/{self.node}.pem")
    
    with open(private_key_path, "r") as f:
      self.private_key = tuple(map(int, f.read().split(",")))
    
  def encrypt(self, plaintext, key=None):
    if key is None:
      e, n = self.public_key
    else:
      e, n = key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

  def decrypt(self, ciphertext, key=None):
    if key is None:
      d, n = self.private_key
    else:
      d, n = key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

if __name__ == "__main__":
  rsa = RSA("initiator")
  
  plaintext = "Hello, World!"
  ciphertext = rsa.encrypt(plaintext)
  
  print("Plain Text:", plaintext)
  print("Cipher Text:", ciphertext)
  
  decrypted_msg = rsa.decrypt(ciphertext)
  
  print("Decrypted Message:", decrypted_msg)
  