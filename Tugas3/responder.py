import socket
import json
import os

from utils.mitecom import PublicKeyRequest, HandshakeMessage, read_all
from utils.RSA import RSA
from utils.DES import DES

PKA_HOST='127.0.0.1'
PKA_PORT=12345

INITIATOR_HOST='127.0.0.1'
INITIATOR_PORT=12346

PUBLIC_KEYS = {}

rsa = RSA("responder")

def read_pka_pub_key():
  dir = os.path.dirname(__file__)
  file = os.path.join(dir, "utils/pub_keys/pka.pem")
  with open(file, "r") as f:
    PUBLIC_KEYS["pka"] = tuple(map(int, f.read().split(",")))

def get_initiator_pub_key():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((PKA_HOST, PKA_PORT))
  request = PublicKeyRequest("initiator", "responder")
  
  client.sendall(json.dumps(request.to_msg()).encode('utf-8'))
  
  response = read_all(client)
  ciphertext = json.loads(response)
  
  decrypted_response = rsa.decrypt(ciphertext, PUBLIC_KEYS["pka"])
  
  plaintext = json.loads(decrypted_response)
  
  is_found = False
  if plaintext['type'] == "error":
    print(f"Error: {plaintext['message']}")
  else:
    PUBLIC_KEYS["initiator"] = plaintext['value']
    is_found = True
    
  client.close()
  
  return is_found

def handshake(client):
  data = read_all(client)  
  ciphertext = json.loads(data)
    
  decrypted_data = rsa.decrypt(ciphertext)
    
  plaintext = json.loads(decrypted_data)
  initiator = plaintext['id']
    
  print(f"Received handshake from {initiator}")
  
  if not get_initiator_pub_key():
    print("Handshake failed!")
    client.close()
    return False

  n2 = os.urandom(16)
  combined = n2 + bytes.fromhex(plaintext['nonce'])
  response = HandshakeMessage("responder", combined)
  
  ciphertext = rsa.encrypt(json.dumps(response.to_msg()), PUBLIC_KEYS["initiator"])
  client.sendall(json.dumps(ciphertext).encode('utf-8'))
  
  # check if initiator sends n2 back
  data = read_all(client)
  
  ciphertext = json.loads(data)
  decrypted_data = rsa.decrypt(ciphertext)
  
  plaintext = json.loads(decrypted_data)
  nonce = bytes.fromhex(plaintext['nonce'])
  
  if nonce != n2:
    print(f"Handshake failed! Nonce mismatch: {nonce} != {n2}")
    client.close()
    return False
  
  print("Handshake successful!")
  return True

def update_des_key(data):
  # decrypt with private key
  decrypted_data = rsa.decrypt(data)
  
  # decrypt again with initiator public key
  key = rsa.decrypt(decrypted_data, PUBLIC_KEYS["initiator"])

  return key

def start_listener():
  print("Start listening...")
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.bind((INITIATOR_HOST, INITIATOR_PORT))
  server.listen(5)
  
  counter = 0
  des = None
  handshake_successful = False
  
  try:
    client, _ = server.accept()
    while True:
      if not handshake_successful:
        handshake_successful = handshake(client)
      
      if handshake_successful:
        data = read_all(client).decode()
        
        if counter % 5 == 0:
          new_key = update_des_key(data)
          des = DES(new_key)
          print(f"New DES Key: {new_key}")
        elif des is not None:
          plaintext = des.decrypt(data)
          print(f"Cipher Text: {data}")
          print(f"Plain Text: {plaintext}")
        else:
          print("DES key not initialized.")
        
        counter += 1
      else:
        print("Handshake failed!")
        client.close()
  except KeyboardInterrupt:
    print("Exiting...")
  except Exception as e:
    print(f"An error occurred: {e}")
  finally:
    server.close()

if __name__ == "__main__":
  read_pka_pub_key()
  start_listener()
