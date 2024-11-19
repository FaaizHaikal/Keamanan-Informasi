import socket
import json

HOST='127.0.0.0'
PORT=12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

PUBLIC_KEYS={}

def handle_request(client):
  data = client.recv(1024).decode()
  print(f"Received: {data}") 
  response = {}

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
    elif request['type'] == 'PUT':
      key = request['key']
      value = request['value']
      PUBLIC_KEYS[key] = value
      
      response.type = "ok"
    else:
      response.type = "error"
      response.message = "Invalid request type"
  except json.JSONDecodeError:
    response.type = "error"
    response.message = "Invalid JSON"
  
  # TODO: Encrypt the response using PKA's private key
  client.sendall(json.dumps(response).encode())

while True:
  client, addr = server.accept()
  handle_request(client)
  client.close()