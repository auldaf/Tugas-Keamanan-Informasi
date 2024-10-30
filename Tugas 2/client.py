import sys
import socket
import logging
from coba import encryption
from coba import encrypt_text
from coba import decrypt_text
from coba import decryption
import base64

key = 'abcdefgh'
message = 'aulia daffa'

# Set basic logging
logging.basicConfig(level=logging.INFO)

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.16.16.101', 10000)  # Change to your server IP
    logging.info(f"Connecting to {server_address}")
    sock.connect(server_address)

    logging.info(f"Sending: {message}")

    # Encrypt the message before sending
    encrypted_message = encrypt_text(message, key)
    logging.info(f"Encrypted message: {encrypted_message}\n")

    # Send the encrypted message
    sock.sendall(encrypted_message.encode('utf-8'))

    # Receive the response from the server
    while True:
        data = sock.recv(1024)
        if not data:
            break  # Exit the loop if no more data
        data = data.decode('utf-8')
        logging.info(f"Received from server: {data}")

        # Decrypt the message using the same key
        decrypted_message = decrypt_text(data, key)
        logging.info(f"Decrypted message: {decrypted_message}\n")

except Exception as e:
    logging.error(f"ERROR: {str(e)}")
finally:
    logging.info("Closing connection")
    sock.close()
