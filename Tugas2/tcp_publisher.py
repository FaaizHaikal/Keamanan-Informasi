import socket
from DES import DES

HOST = '127.0.0.1'  # IP address of the server
PORT = 12345      # Port to connect to the server

def start_tcp_publisher(host=HOST, port=PORT):
    des = DES()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            
            while True:
                # Get user input message
                message = input("Enter message to send (type 'exit' to quit): ")
                if message.lower() == 'exit':
                    print("Exiting...")
                    break

                # Encrypt the message
                encrypted_message = des.encrypt(message)

                # Send the encrypted message to the server
                s.sendall(encrypted_message.encode())
                print(f"Sent Encrypted Message: {encrypted_message}")
                
                # Receive the encrypted response from the server
                data = s.recv(1024)
                if data:
                    received_ciphertext = data.decode()
                    received_plaintext = des.decrypt(received_ciphertext)
                    
                    print(f"Received Cipher Text: {received_ciphertext}")
                    print(f"Decrypted Response: {received_plaintext}")

        except ConnectionError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("Closing the connection...")

if __name__ == "__main__":
    start_tcp_publisher()
