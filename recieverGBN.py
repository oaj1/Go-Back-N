#--------imports-----------#
import socket
import pickle
import time
#import hashlib #will be used to encode
import random

# Go-Back-N program on the RECEIVER side

# ------------------------------------------ STEP 0: DECLARATIONS (depends on the protocol that we design) ------------------------------------------
# addresses
recieveIP = socket.gethostbyname(socket.gethostname())
recievePort = 15200
recieveAddress = (recieveIP, recievePort)

sendPort = 5051
sendIP = socket.gethostbyname(socket.gethostname())
sender_addr = (sendIP, sendPort)

# socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# need to bind so we can receive data
sock.bind(recieveAddress)
sock.settimeout(5)

# protocols
buff_size = 1024

expected_seq_num = 1 #I think the expected sequence number should be 1, from internet research
#ACK = 1
#ack_list = []

# data stuff
# this is the message indicating to stop waiting for data.
kill_conn_message = "FINISH"
# this is where we'll put all the decoded data that we receive
file_data = []
filename = "COSC635_P2_DataReceived.txt"

print("Awaiting data on:", recieveAddress)

# ------------------------------------------ STEP 1: RECEIVING THE DATA ------------------------------------------

f = open(filename, "a")
nextSeqNum = 0
transmission_start = False


while True:
    # receive the data
    data, sender_addr = sock.recvfrom(buff_size)

    # lets user know that data is being received
    if transmission_start is False:
        print("Receiving data!")
        transmission_start = True
    else:
        print("Error receiving data")
    
     # unpack the data
    data_received_list = pickle.loads(data)

    # length of data received
    data_received_len = data_received_list[0] #how is this portion the length of the data received, and not the first index of the list?

    if(data_received_list[2]==expected_seq_num): #I believe this code is for if packet recieved successfully, [2] is the sequence number
        print("received in order packets")
        #I think we have to send something back for ACK right here in the code
        #nextSeqNum +=1 #not sure if we want this here or not
        if data_received_list[1]: #[1] is the characters, or the string
            f.write(data_received_list[1])#write the file
            #nextSeqNum +=1
            expected_seq_num += 1
        else:
            print("end of file")
            #send a reject
            #we will need code logic here
            break
    

print("file has been created and written to! Check your directory for", filename)
f.close()
# maybe give the user an option to read the data? idk, we can just open the txt file from the directory after this.
