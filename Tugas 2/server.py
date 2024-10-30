import sys
import socket
import logging
from coba import decryption
from coba import encryption
from coba import encrypt_text
from coba import decrypt_text
from coba import stringToBinary

logging.basicConfig(level=logging.INFO)
key = 'abcdefgh'
message = 'aulia daffa'

try:
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port
    server_address = ('0.0.0.0', 10000)  # Bind to all available interfaces
    logging.info(f"Starting up on {server_address}")
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        logging.info("Waiting for a connection")
        connection, client_address = sock.accept()
        logging.info(f"Connection from {client_address}")

        try:
            while True:
                data = connection.recv(1024)  # Receive data
                if not data:
                    logging.info("No more data from client. Closing connection.")
                    break  # Client closed connection

                # Decode the data
                data = data.decode('utf-8')
                logging.info(f"Received from client: {data}")

                # Decrypt the received message
                print('data:',data)
                enc_to_binary = stringToBinary(data)
                logging.info(f"enc to binary: {enc_to_binary}")
                decrypted_message = decrypt_text(enc_to_binary, key)
                logging.info(f"Decrypted message: {decrypted_message}")

                # Encrypt the response message
                message_to_send = encrypt_text(decrypted_message, key)  # Assuming you meant 'key' not 'round_key'
                logging.info(f"Encrypted message to send: {message_to_send}")

                # Send the message back to the client
                connection.sendall(decrypted_message.encode('utf-8'))

        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")

        finally:
            logging.info("Closing connection")
            connection.close()

except Exception as ee:
    logging.error(f"ERROR: {str(ee)}")
finally:
    logging.info('Closing server socket')
    sock.close()
