import socket
import os
import multiprocessing as mp
import time
import json

user_id = 1

#######################################################################################################
def user_write_request(user_id, value_to_be_written):
    print("Write request initiated...................................")
    port = (8000) + user_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        client.connect(('0.0.0.0', port))
    except socket.error, e:
        print("Socket error: ", e)
        return
    send_write_message = '{"activity":"user_write_request","value_to_be_written":"'+ value_to_be_written+'"}'
    client.send(send_write_message)
    from_server = client.recv(4096)
    rcvd_mssg = from_server
    print('Received write message udpate statue from Group man: ', rcvd_mssg)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    #print('My port is :', port, 'I got the message: ', node_age[node_id-1])

######################################################################################################

def user_read_request(user_id):
    print("Read request initiated...................................")
    port = (8000) + user_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try: 
        client.connect(('0.0.0.0', port))
    except socket.error, e:
        print("Socket error: ", e)
        return
    send_write_message = '{"activity":"user_read_request"}'
    client.send(send_write_message)
    from_server = client.recv(4096)
    rcvd_mssg = from_server
    print('Received read result: ', rcvd_mssg)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    #print('My port is :', port, 'I got the message: ', node_age[node_id-1])

############################################################################################################
seek_intent = raw_input("Do you want to read / write (r/w) : ") 
print(seek_intent)
user_write_value = ""
if seek_intent == "w":
    user_write_value = raw_input("Enter alphabet to be written : ")
    print(user_write_value)

if seek_intent=="w":
    time.sleep(5)
    user_write_request(user_id, user_write_value)

if seek_intent=="r":
    time.sleep(5)
    user_read_request(user_id)
################################################################################################


