import socket
import sys

#---------------------The program starts with the script and a port number as a parameter----------------------

ip = "127.0.0.1"
portnr = int(sys.argv[1])

#establishing a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((ip, portnr))
server_socket.listen()

#Creating an empty list for the chatroom
established = []
names = []


while True:

    # Add as many clients you want to the chatroom
    if len(established) == 0:

        print("waiting for the first client to join...")

    client_socket, client_address = server_socket.accept()
    #Adding the client-socket in the established list
    established.append(client_socket)

    #Adding the name of the client in the names list
    connection_msg = client_socket.recv(1024).decode()
    names.append(connection_msg)

    #Printing name of the client if a connedtion is established
    print("----Client " + connection_msg + " has joined succesfully!----")

    #Giving the option to add more clients to the chatroom
    input_msg = input("Do you wish to add more clients to the chatroom?, y/n? , write: 'quit' to exit " )
    if input_msg == 'y':
        number_of_elements = len(established)
        print("Currently ", number_of_elements, "client(s) have joined the chatroom")
        print("waiting for the next client to join...")


    if input_msg == 'n':
        break

    #With this command the server gets terminated before starting the chatroom
    if input_msg == 'quit':
        server_socket.close()
        print("Server terminated")
        exit()

#--------------starting chatroom---------------------------

#Telling the server how many clients that are connected to the server
print("---------chat (",len(established),") client(s)------------")

#Printing out a tutorial on how to use the different commands
print("hint: write 'kick' to exit a client")
print("hint: write 'exit' to shutdown the chatroom")

#A loop that goes through rest of the code
while True:

    #Telling the server to write a message
    host_msg = input("Write something: ")

    #Command to close the chatroom
    if host_msg == 'quit':
        server_socket.close()
        client_socket.close()
        print("Chatroom closing...")
        break

    #Command to kick the clients
    if host_msg == 'kick':

        sjekk = True

        while sjekk:

            host_msg = input("Who do you want to kick?: write: 'exit' to go back ")

            #Go back to the chatroom
            if host_msg == 'exit':
                break


            count = 0

            #Checking through the names list and trying to find a match
            for i in names:
                if i == host_msg:

                    #Removing the client-socket from the established list.
                    established.pop(count)
                    #printing to server
                    print(names[count] + " is removed")

                    #telling all the clients that someone has been kicked
                    sendmsg = names[count].encode() + " have been kicked".encode()
                    for z in established:
                        z.send(sendmsg)

                    sjekk = False
                    break

                count += 1
        #This command is needed to skip the current itteration.
        continue


    #Print server message on terminal
    host_msg = ("Server: " + host_msg)
    print(host_msg)

    # Sending/receiving message
    for i in established:
        i.send(host_msg.encode())
    for i in established:
        input_msg = i.recv(1024).decode()
        print(input_msg)

        # Sends message to the other clients
        for z in established:
            if z != i:
                z.send(input_msg.encode())




