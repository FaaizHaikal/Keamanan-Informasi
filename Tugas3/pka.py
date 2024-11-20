import socket
import json
import os

from utils.RSA import RSA

HOST='127.0.0.1'
PORT=12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

NODES = ["initiator", "responder"]
PUBLIC_KEYS = {}
class Response:
  def __init__(self, type, value=None, message=None):
    self.type = type
    self.value = value
    self.message = message
    
  def to_json(self):
    return json.dumps(self.__dict__)
  
# This reads all public keys for each nodes
def read_keys():
  start_dir = os.path.dirname(__file__)

  for node in NODES:
    dir = os.path.join(start_dir, f"utils/pub_keys/{node}.pem")
    with open(dir) as f:
      key = tuple(map(int, f.read().split(",")))
      PUBLIC_KEYS[node] = key

def handle_request(client):
  data = client.recv(1024).decode()
  print(f"Received: {data}") 
  response = Response("error")

  try:
    request = json.loads(data)
    if request['type'] == 'GET':
      key = request['key']
      if key in PUBLIC_KEYS:
        response.type = "ok"
        response.value = PUBLIC_KEYS[key]
      else:
        response.type = "error"
        response.message = "Key not found"
    else:
      response.type = "error"
      response.message = "Invalid request type"
  except json.JSONDecodeError:
    response.type = "error"
    response.message = "Invalid JSON"
  
  return response.to_json()

if __name__ == "__main__":
  read_keys()
  rsa = RSA("pka")

  while True:
    try:
      client, addr = server.accept()
      message = handle_request(client)
      ciphertext = rsa.encrypt(message)
      print(f"Sending: {ciphertext}")
      client.sendall(ciphertext)

      client.close()
    except KeyboardInterrupt:
      print("Exiting...")
      break
    
  server.close()