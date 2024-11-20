import socket
import json
import os

from utils.mitecom import PublicKeyResponse, read_all
from utils.RSA import RSA

HOST='127.0.0.1'
PORT=12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

PUBLIC_KEYS = {}

def read_keys():
  start_dir = os.path.dirname(__file__)
  keys_dir = os.path.join(start_dir, "utils/pub_keys")
  for filename in os.listdir(keys_dir):
    if filename.endswith(".pem"):
      node = filename.split(".")[0]
      if node != "pka": # PKA's key will instantly be read by the RSA class
        with open(os.path.join(keys_dir, filename)) as f:
          key = tuple(map(int, f.read().split(",")))
          PUBLIC_KEYS[node] = key

def handle_request(client):
  data = read_all(client).decode()
  response = PublicKeyResponse()

  try:
    request = json.loads(data)
    if request['request_for'] not in PUBLIC_KEYS:
      response.type = "error"
      response.message = "The requested public key not found"
    elif request['requested_by'] not in PUBLIC_KEYS:
      response.type = "error"
      response.message = "Unaothorized requester!"
    else:
      response.type = "success"
      response.value = PUBLIC_KEYS[request['request_for']]
  except json.JSONDecodeError:
    response.type = "error"
    response.message = "Invalid JSON"

  return json.dumps(response.to_msg())

if __name__ == "__main__":
  read_keys()
  rsa = RSA("pka")

  while True:
    try:
      client, addr = server.accept()
      response = handle_request(client)
      ciphertext = rsa.encrypt(response, rsa.private_key)
      
      client.sendall(json.dumps(ciphertext).encode())

      client.close()
    except KeyboardInterrupt:
      print("Exiting...")
      break
    
  server.close()