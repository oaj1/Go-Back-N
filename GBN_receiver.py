import socket
import pickle

# Stop and wait program on the RECEIVER side

# ------------------------------------------ STEP 0: DECLARATIONS (depends on the protocol that we design) ------------------------------------------
# addresses
receiver_ip = socket.gethostbyname(socket.gethostname())
port = 5051
receiver_addr = (receiver_ip, port)

sender_port = 15200
sender_ip = socket.gethostbyname(socket.gethostname())
sender_addr = (sender_ip, sender_port)

# socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# need to bind so we can receive data
sock.bind(receiver_addr)
# timeout is 100s until data is being received. This allows sender to run code and enter input.
sock.settimeout(100)
start_receive = False

# protocols
buff_size = 1300

# data stuff
# this is the message indicating to stop waiting for data.
kill_conn_message = "FINISH"
# this is where we'll put all the decoded data that we receive
file_data = []
filename = "COSC635_P2_DataReceived.txt"

print("Awaiting data on:", receiver_addr)

# ------------------------------------------ STEP 1: RECEIVING THE DATA ------------------------------------------
nextseqnum = 0
max_data = None
while True:
    # these lines let it know when to stop trying to receive
    if max_data is not None:
        if max_data == nextseqnum:
            break
    try:
        # receive the data
        data, sender_addr = sock.recvfrom(buff_size)

        # fix timeout
        if start_receive is False and data is not None:
            print("Begun receiving data...")
            sock.settimeout(2)
            start_receive = True

        # unpack data
        data_rec = pickle.loads(data)
        max_data = data_rec[0]

        if data_rec[1] == nextseqnum:
            file_data.append(data_rec[2])
            data_list = [1, nextseqnum]
            data_to_send = pickle.dumps(data_list)
            sock.sendto(data_to_send, sender_addr)
            nextseqnum += 1
        else:
            data_list = [0, nextseqnum]
            data_to_send = pickle.dumps(data_list)
            sock.sendto(data_to_send, sender_addr)

    except socket.timeout:
        continue
print("Data has been received...")
# ------------------------------------------ STEP 1: RECEIVING THE DATA ------------------------------------------

print("writing the data to a file called", filename)

# creates the new file within the project directory if it doesn't already exist
# append the file by writing all the data received to it
file = open(filename, "a")
for data in file_data:
    file.write(data)
file.close()

print("file has been created and written to! Check your directory for", filename)
