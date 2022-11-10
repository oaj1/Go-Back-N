#--------imports-----------#
import socket
import pickle
import time
#import hashlib
import random
import os

#---------------------------------------------------Declarations------------------------------------------------######
#get user input for simulated packet loss
seed = input("Enter a number between 0-99. Note: This number is the approximate percentage of packets that will be lost during transmission ")

seed = int(seed) #cast to an int


#UDP socket server
sendServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#host IP address server
sendIP= socket.gethostbyname(socket.gethostname())#"127.0.0.1"
#port number server
sendPort = 5051

senderAddress = (sendIP,sendPort)


#UDP socket client
recieveServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#host IP address client
recievetIP = socket.gethostbyname(socket.gethostname())#"127.0.0.1"
#port number client
recievePort = 15200

clientAddress = (recieveServer,recievePort)

#Bind to allow ACK
sendServer.bind(senderAddress)

#sender base is the seq num of the oldest un-ack packet
sender_base=0 

#next sequence number related to the next packet to send
nextSeqnum=0 

#windowSize will be seven
windowSize=7
#lower window bound, got from internet,  not sure if needed
#window = []

#list where we will store the file packets
packets = []

#variable to hold last acknowledge time
#lastAckRecieved = time.time()

#variable that will hold whether process is finished
finished = False

#payload_size for reading file
payload_size = 1024

#user inputs the name of the file
fileName = "COSC635_P2_DataSent.txt"

# Statistic data
# total frames sent
frames_sent = 0
# total frames lost
frames_lost = 0
# size of file in bytes
file_size = os.path.getsize(fileName)
#------------------------Dealing with the File-------------------------------------------------------------##

#read file
file = open(fileName, "r")

print("parsing the file...")

#read contents of file char by char, append to packets
while 1:
    payload_decoded = ""
    char = ''
    for i in range(payload_size):
        char = file.read(1)
        if not char:
            break
        payload_decoded += char
    packets.append(payload_decoded)
    if not char:
        break
#close the file
file.close()

kill_conn_message = "FINISH"
packets.append(kill_conn_message)


print("parsing complete!")#File has been read completely




#-------------Begin sending data-----------#
print("Sending the data....")

for i in range(len(packets)):
    data = packets[i]#packet to send
    data_length = len(b'data')#byte length of data
    data_list = [data_length, data,nextSeqnum]
    data_to_send = pickle.dumps(data_list)

     # -------- Simulated packet loss --------THIS NEEDS TO GO INTO WHILE LOOP
  #  random_number = random.randint(0, 99)
   # if random_number < seed:
    #    frames_lost += 1
     #   continue
    
    #Begining of go-back-n, not sure where to increment sender_base..., it increments after receiving an ack,  I'll need some of ya'lls thoughts
    while True:
        #Maybe declare nextSeq and send_base here
        start = time.perf_counter()#start timer
        random_number = random.randit(0,99) #I think this is to send packets one at a time, where it is only sent if random num is less than seed
        if random_number < seed:
            frames_lost += 1
            continue
        #packets transferred until next sequence number is equal to or greater than sender_base + windowSize
        if (nextSeqnum < sender_base + windowSize):
            #I think this is the correct sendTo
            sendServer.sendto(data_to_send,clientAddress)#this doesn't work, not sure why
            nextSeqnum +=1 #increment the SEQ num
            #If the file has been read completely, done is true
            if (not file):
                break

    #Receipt of an Ack, used Raymond's as base, not sure what is going on here, receiving ACK's confuses me, sender base increments here
        try:
            rcvPacket, addrRecieved = sendServer.recvfrom(1024)#loop back to this, needs a header
            #rcvPacket = []
            rcvPacket_list = pickle.loads(rcvPacket)
            #This is where the ACK would go, not sure how I would want to code that though
            #Maybe subtract, versus plus ????
            sender_base = n + 1 #maybe data[-1] or something to that affect?
            socket.setdefaulttimeout(5)
            if sender_base == nextSeqnum:
                #stop a timer
                stop = time.perf_counter()
            else:
                start = time.perf_counter() #come back and look
        except socket.timeout:
            print("timeout error")
            #perhaps more code? See link https://www.baeldung.com/cs/networking-go-back-n-protocol
            break #should we just break here
    file.close()
    print("connection is closed")
    
