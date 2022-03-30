import socket
import sys
import random
#---------------------The program starts with three parameters in addition to the script--------------------------

#Our usable bot list
bots = ["Morten", "Erik", "Petter", "Sondre"]

ip = str(sys.argv[1])
port = int(sys.argv[2])
name = str(sys.argv[3])

#Checking if the input name is in the bot list
if name not in bots:
    print("Please choose one of our participants: Morten, Erik, Petter and Sondre")
    exit()

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((ip, port))

#Sending the server the name of the client
clientSocket.send(name.encode())

#Telling the client to wait when the connection is established
print("Chatroom joined! Wait for a question...")


#Lists with words
good_list = ["facetime", "drink", "work", "eat", "golf", "sing", "write", "party", "study"]
bad_list = ["kill", "steal", "sleep", "clean", "scream", "kidnap"]
random_stuff = random.choice(["play fotball", "play cricket", "play golf", "play tennis", "do laundry" ])



#Bot functions
def morten(a):

    if a in good_list:
        return "Morten: I am not really a big fan of {}ing... Let's {} instead".format(a, random_stuff)
    else:
        return "Morten: Yesss! {} sounds funnnnn!".format(a + "ing")

def erik(a, b = None):
    if a in bad_list:
        return "Erik: I have always enoyed {} :)".format(a + "ing")
    else:
        return "Erik: Are you serious??, do you really think i enjoy {}?, i would rather go {}".format(a + "ing", b)

def petter(a, b = None):
    if a in bad_list:
        return "Petter: I don't really like to {}, but you guys can choose...".format(a)
    else: return "Petter: {} sounds fine, but i would rather {}".format(a + "ing", b)

def sondre(a):
    return "Sondre: I am not coming to {}. I am a very anti-social person".format(a)


#A loop that goes through rest of the code
while True:

    #Testing the connection
    try:

        host_msg = clientSocket.recv(1024).decode('utf-8')

        print(host_msg)

    except:
        clientSocket.close()


    try:
        #understanding the word on the "6" place
        split = host_msg.split()
        action = split[5]

        random_list = random.choice(["play fotball", "play tennis", "do laundry"])

        # Calls the bot functions dependent on the bot parameter
        if name == 'Morten':
            message = "{}".format(morten(action))
        if name == 'Erik':
            message = "{}".format(erik(action, random_list))
        if name == 'Petter':
            message = "{}".format(petter(action, random_list))
        if name == 'Sondre':
            message = "{}".format(sondre(action))

    #Delivers a message if not understood (the sixth word is unrecognized))
    except:
        message = ("Could not understand, please try again...")


    try:

        #Making sure that the bots only answer the server's question
        check = split[0]


        if check == "Server:":
            clientSocket.send(message.encode())

            print(message)

    #If the check is null the clientconnection gets terminated
    except:
        print("Connection lost, closing socket")
        clientSocket.close()
        exit()

