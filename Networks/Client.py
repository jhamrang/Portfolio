# Code based on code from the textbook "Computer Networking A Top-Down Approach" The 8th edition. Code based on code given on page 161. Textbook written by James F. Kurose, and Keith W. Ross.  Viewed on 7/1/2022
from socket import *
serverName = '127.0.0.1'
serverPort = 3002                                                       # Port number to be used
# Setting up the socket
with socket(AF_INET, SOCK_STREAM) as clientSocket:
    clientSocket.connect((serverName,serverPort))
    test_input = input("Enter client message: ")

    clientSocket.send(test_input.encode())

    while True:
        sentence = clientSocket.recv(1024).decode()
        print(sentence)
        data = input("Enter client message: ")
        # If statement to break the loop if /q is entered
        if data == "/q":
            break
        clientSocket.send(data.encode())


    #pretty sure this statmeent is not needed since there is a with statment for clientSocket
    clientSocket.close()
