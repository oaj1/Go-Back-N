import socket
import pickle
import random
import time
import os

# Stop and wait program on the SENDER side

# ------------------------------------------ STEP 0: DECLARATIONS (depends on the protocol that we design) ------------------------------------------
# get user input for simulated packet loss
seed = input("Enter a number between 0-99. Note: This number is the approximate percentage of packets that will be lost during transmission")
# cast it to an int, otherwise python thinks it's a string for some reason
seed = int(seed)

# addresses
# both are this local machine for now
# using different ports for send and receive, can't be listening on same port
# receiver_ip = "192.168.1.201"
receiver_ip = socket.gethostbyname(socket.gethostname())
receiver_port = 5051
receiver_addr = (receiver_ip, receiver_port)

sender_port = 15200
sender_ip = socket.gethostbyname(socket.gethostname())
sender_addr = (sender_ip, sender_port)

# socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# need to bind so we can receive ACK
sock.bind(sender_addr)
# doing 2 second timeout here since the code relies on the timeout
sock.settimeout(2)

# protocols
window_size = 7
buff_size = 1300 * window_size
# this is minimum payload_size. The number of bytes from the file that we want to send at one time. Note: 1 byte = 1 char.
# setting this as 8 for now
payload_size = 8

# data - gonna put all of the packets we want to send into a list so that we
# can just iterate through the list to send everything in order
#
# header changes with each packet so we can just do something like header = SEQ = index of data in list % 2
# (will be either 0 or 1)
packets = []
# name of the file to be sent, should be located within the project directory so we don't have to navigate to it.
filename = "COSC635_P2_DataSent.txt"

# Statistic data
# total frames sent
frames_sent = 0
# total frames lost
frames_lost = 0
# size of file in bytes
file_size = os.path.getsize(filename)

# ------------------------------------------ STEP 1: DEALING WITH THE FILE ------------------------------------------
# this step deals with: Open the file, read the file, add encoded (utf-8) bytes into the packets list


# tell the user that the file is being read
print("parsing the file...")

# open file, r is the mode to open the file in. All the resources I looked at used r.
file = open(filename, "r")

# iterate over file (character by character) and add the encoded strings to the packets list
# I think this should work as expected but not 100%. Not sure if it breaks out of while loop correctly.
while 1:
    payload = ""
    char = ''
    # read in a payloads worth of chars
    for i in range(payload_size):
        # read 1 character
        char = file.read(1)
        if not char:
            break
        # concatenate char to decoded payload
        payload += char
    # encodes in utf-8 by default
    # payload_encoded = payload_decoded.encode()
    packets.append(payload)
    # breaks while loop if no char stored from for loop
    if not char:
        break
file.close()

# No need for kill_conn_message on this one, that's done by "max_data"

print("parsing complete!")

# ------------------------------------------ STEP 2: SEND THE DATA ------------------------------------------

print("sending the data...")

# data_length is the total number of "frames" that are being sent, doesn't change throughout the loop, only declare once
max_data = len(packets)

start = time.perf_counter()
send_base = 0
nextseqnum = 0
while nextseqnum < max_data:
    skip = False
    try:
        # -------- Simulated packet loss --------
        random_number = random.randint(0, 99)
        if random_number < seed:
            # packet isn't actually being "lost" so this code needs to be commented out
            # data_list = [max_data, nextseqnum, ""]
            # data_to_send = pickle.dumps(data_list)
            # sock.sendto(data_to_send, receiver_addr)
            skip = True

        # try to send data
        # if packet is being "lost" then only do this if skip = False
        if nextseqnum < send_base + window_size:
            data_list = [max_data, nextseqnum, packets[nextseqnum]]
            data_to_send = pickle.dumps(data_list)
            sock.sendto(data_to_send, receiver_addr)
            nextseqnum += 1

        # try to receive data
        data, sender_addr = sock.recvfrom(buff_size)
        if data is not None:
            data_rec = pickle.loads(data)
            if data_rec[0] == 1:
                if data_rec[1] == send_base:
                    send_base += 1
                    if skip is False:
                        frames_sent += 1
                    else:
                        frames_lost += 1
                else:
                    # wait for timeout, this isn't the ACK for the SEQ we expected
                    # frames_lost += 1
                    time.sleep(2)
        else:
            # wait for timeout, we got a rejected ACK
            # frames_lost += 1
            time.sleep(2)
    # timeout means that we need to go back and resend certain packets
    except socket.timeout:
        # send all packets again
        nextseqnum = send_base
        # frames_sent = send_base
        continue


stop = time.perf_counter()
print("data has been sent!")

# ------------------------------------------ STEP 3: DISPLAY STATISTICS ------------------------------------------
# transmission time
transmission_time = stop-start
# percentage of lost frames
if max_data > 0:
    loss_percent = (frames_lost/max_data)*100
else:
    loss_percent = 100

print("-------------------")
print("")
print("Transmission Statistics")
print("")
print("Transmission time: ", transmission_time, "seconds")
print("File Size:", file_size, "bytes")
print("Total frames in file:", max_data)
print("Total frames sent:", frames_sent)
print("Total frames 'lost' (simulated):", frames_lost)
print("Percentage of lost frames:", loss_percent, "%")
print("")
print("-------------------")
