import socket

HOST='127.0.0.0'
PORT=12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_request(data):
  client.sendall(data.encode())
  print(f"Sent: {data}")
  
  # response = client.recv(1024).decode()
  
# send json string
data = '{"name": "John Doe", "age": 30}'
send_request(data)

# client.close()