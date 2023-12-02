# Code based on code from the textbook "Computer Networking A Top-Down Approach" The 8th edition. Code based on code given on pages 163-4. Textbook written by James F. Kurose, and Keith W. Ross.  Viewed on 7/1/2022
from socket import *

serverPort = 3002                                                       # Port number to be used
# Setting up the socket
with socket(AF_INET, SOCK_STREAM) as serverSocket:
    serverSocket.bind(('',serverPort))
    serverSocket.listen()
    connectionSocket, addr = serverSocket.accept()

    # looping to keep the server open to receive and respond to messages
    while True:
        sentence = connectionSocket.recv(1024).decode()
        print(sentence)
        data = input("Enter Server Message: ")
        # If statement to break the loop if /q is entered
        if data == "/q":
            break
        connectionSocket.send(data.encode())
    connectionSocket.close()                                             # Closing the socket after the client connected
