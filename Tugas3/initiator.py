import socket
import json
import os

from utils.mitecom import PublicKeyRequest, HandshakeMessage, read_all
from utils.RSA import RSA
from utils.DES import DES

PKA_HOST='127.0.0.1'
PKA_PORT=12345

RESPONDER_HOST='127.0.0.1'
RESPONDER_PORT=12346

PUBLIC_KEYS = {}

rsa = RSA("initiator")

def read_pka_pub_key():
  dir = os.path.dirname(__file__)
  file = os.path.join(dir, "utils/pub_keys/pka.pem")
  with open(file, "r") as f:
    PUBLIC_KEYS["pka"] = tuple(map(int, f.read().split(",")))
  
def get_responder_pub_key():
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((PKA_HOST, PKA_PORT))
  
  request = PublicKeyRequest("responder", "initiator")
  
  client.sendall(json.dumps(request.to_msg()).encode('utf-8'))
  
  response = read_all(client)
  ciphertext = json.loads(response)
  
  decrypted_response = rsa.decrypt(ciphertext, PUBLIC_KEYS["pka"])
  
  plaintext = json.loads(decrypted_response)
  
  is_found = False
  if plaintext['type'] == "error":
    print(f"Error: {plaintext['message']}")
  else:
    PUBLIC_KEYS["responder"] = plaintext['value']
    is_found = True
    
  client.close()
  
  return is_found

def handshake(client):
  n1 = os.urandom(16)
  request = HandshakeMessage("initiator", n1)
  
  ciphertext = rsa.encrypt(json.dumps(request.to_msg()), PUBLIC_KEYS["responder"])
  client.sendall(json.dumps(ciphertext).encode('utf-8'))
  
  response = read_all(client)
  
  ciphertext = json.loads(response)
  
  decrypted_response = rsa.decrypt(ciphertext)
  
  # check if n1 is in combined nonce
  plaintext = json.loads(decrypted_response)
  combined_nonce = bytes.fromhex(plaintext['nonce'])
  is_success = False
  if n1 in combined_nonce:
    # send n2 from combined nonce back to responder
    n2 = combined_nonce[:16]
    response = HandshakeMessage("initiator", n2)
    ciphertext = rsa.encrypt(json.dumps(response.to_msg()), PUBLIC_KEYS["responder"])
    client.sendall(json.dumps(ciphertext).encode('utf-8'))
    is_success = True
  else:
    print(f"Nonce not found in combined nonce: {n1} not in {combined_nonce}")
  
  return is_success
  
def generate_des_key():
  return os.urandom(4).hex()
  
def send_des_key(new_key, client):
    try:
        # Encrypt with initiator's private key
        ciphertext = rsa.encrypt(new_key, rsa.private_key)
        # Encrypt again with responder's public key
        encrypted_ciphertext = rsa.encrypt(ciphertext, PUBLIC_KEYS["responder"])
        
        client.sendall(encrypted_ciphertext.encode('utf-8'))
    except Exception as e:
        print(f"Error while sending DES key: {e}") 
  
def start_publisher():
    print("Starting publisher...")
    des = None
    counter = 0

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((RESPONDER_HOST, RESPONDER_PORT))
        if handshake(client):
          print("Handshake success!")
          while True:
              if counter % 5 == 0:
                  new_key = generate_des_key()
                  des = DES(new_key)
                  send_des_key(new_key, client)
                  print(f"Sent new DES key: {new_key}")
              else:
                # input message
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                  print("Exiting...")
                  break
                
                encrypted = des.encrypt(message)
                
                client.sendall(encrypted.encode('utf-8'))
                print(f"Sent Encrypted Message: {encrypted}")
              counter += 1
    except Exception as e:
        print(f"Error in publisher: {e}")
    finally:
        client.close()

  
if __name__ == "__main__":
  read_pka_pub_key()
  if get_responder_pub_key():
    start_publisher()
