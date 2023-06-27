# Import the socket library.
import socket

# https://www.geeksforgeeks.org/socket-programming-python/

# Create a socket object.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created.")

# Reserve a port on the system.
port = 11111

# Bind to the port.
# Entering an empty string in the IP field makes the server listen to requests coming in from other computers on the network.
s.bind(("", port))
print(f"Socket binded to {port}")

# Put the socket into listening mode.
# The 5 means that 5 connections are kept waiting if the server is busy and if a 6th socket tries to connect then the connection is refused.
s.listen(5)
print("Socket is listening.")

# A forever loop until we interrupt it or an error occurs.

while True:

    # Establish a connection with a client.
    c, addr = s.accept()
    print(f"Received a connection from: {addr}")

    # Send a thank you message to the client, encoding it to send byte type.
    c.send("Thank you for connecting to the blue server.".encode())

    # Close the connection with the client.
    c.close()

    # Break the loop once the connection is closed.
    break
