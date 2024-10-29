import socket
from DES import DES

HOST='0.0.0.0'
PORT=12345

def start_tcp_listener(host=HOST, port=PORT):
  des = DES()

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Listening on {host}:{port}")
    conn, addr = s.accept()
    with conn:
      print(f"Connected by {addr}")
      while True:
        data = conn.recv(1024)
        if not data:
          break
        ciphertext = data.decode()
        plaintext = des.decrypt(ciphertext)

        print(f"Cipher Text: {ciphertext}")
        print(f"Plain Text: {plaintext}")

        conn.sendall(data)

if __name__ == "__main__":
  start_tcp_listener()