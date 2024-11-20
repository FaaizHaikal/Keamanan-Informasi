import socket
import json
import os

from utils.mitecom import PublicKeyRequest, read_all

HOST='127.0.0.1'
PORT=12345

dir = os.path.dirname(__file__)
file = os.path.join(dir, "utils/pub_keys/pka.pem")
with open(file, "r") as f:
  PUBLIC_KEY = tuple(map(int, f.read().split(",")))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def decrypt(ciphertext):
    d, n = PUBLIC_KEY
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

def send_request(data):
  client.sendall(data.encode('utf-8'))
  print(f"Sent: {data}")

request = PublicKeyRequest("brob", "initiator")
send_request(json.dumps(request.to_msg()))

response = read_all(client)
ciphertext = json.loads(response)

print(f"Received: {ciphertext}")

decrypted_response = decrypt(ciphertext)

print(f"Decrypted Response: {decrypted_response}")

# client.close()