import socket
import os
import multiprocessing as mp
import time
import json

print(os.getpid())

def listToString(s):  
    str1 = " " 
    return (str1.join(s))

def node_status_check(node_id):
    if node_id>=4:
        IP = '3.16.164.181'
    else:
        IP= '0.0.0.0'
    port = (10000) + node_id
    print("Status check initiated...................................")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        #print("Socket error: ", e)
        node_status[node_id-1] = 0
        node_age[node_id-1] = 0
        return
    status_check_message = '{"activity":"node_status_check","checked_node_id":'+str(node_id)+'}'
    client.send(status_check_message)
    from_server = client.recv(4096)
    rcvd_mssg = json.loads(from_server)
    node_status[node_id-1] = 1
    node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    print('My port is :', port, 'the age of the pinged node is: ', node_age[node_id-1], ' seconds')
    #print(node_age)

def group_update(node_id, elected_leader_id):
    if node_id>=4:
        IP = '3.16.164.181'
    else:
        IP= '0.0.0.0'
    print("Group update initiated...................................")
    port = (10000) + node_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        #print("Socket error: ", e)
        node_status[node_id-1] = 0
        node_age[node_id-1] = 0
        return
    status_mssg = ' '.join([str(elem) for elem in node_status])
    #print(status_mssg)
    send_update_message = '{"activity":"group_update","leader_node_id":'+str(elected_leader_id)+',"node_status":"'+status_mssg+'"}'
    client.send(send_update_message)
    from_server = client.recv(4096)
    print(from_server)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    #print('My port is :', port, 'I got the message: ', node_age[node_id-1])

def write_request(elected_leader_id):
    global request_array
    response_array = []
    print('Response array: ', response_array)
    if elected_leader_id>=4:
        IP = '3.16.164.181'
    else:
        IP= '0.0.0.0'
    print("Write request initiated...................................")
    port = (10000) + elected_leader_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        print("Socket error: ", e)
        return "Could not connect with leader"
    while len(request_array)>0:
        send_write_message = '{"activity":"write_request","value_to_be_written":"'+ request_array[0]+'"}'
        client.send(send_write_message)
        from_server = client.recv(4096)
        rcvd_mssg = from_server
        print('Received write message udpate statue from Leader node: ', rcvd_mssg)
        response_array.append(str(rcvd_mssg))
        request_array.pop(0)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    return_response_array = listToString(response_array)
    return return_response_array
    #print('My port is :', port, 'I got the message: ', node_age[node_id-1])

def read_request(elected_leader_id):
    if elected_leader_id>=4:
        IP = '3.16.164.181'
    else:
        IP= '0.0.0.0'
    print("Read request initiated...................................")
    port = (10000) + elected_leader_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        print("Socket error: ", e)
        return "Could not connect with leader"
    send_write_message = '{"activity":"read_request"}'
    client.send(send_write_message)
    from_server = client.recv(4096)
    rcvd_mssg = from_server
    print('Read result: ', rcvd_mssg)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    return rcvd_mssg
    #print('My port is :', port, 'I got the message: ', node_age[node_id-1])


def listen_to_new_node(node_id):
    print("Listening to any new nodes.............. ")
    port = (50000) + node_id
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('0.0.0.0', port))
    print('Listening for new node at port : ', port)
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_new_node = ''
        while True:
            data = conn.recv(4096)
            if not data: break
            from_new_node += data
            print('Received message from new node')
            if from_new_node=='ping_new_node':
                status_mssg = ' '.join([str(elem) for elem in node_status])
                #print(status_mssg)
                send_update_message = '{"activity":"group_update","leader_node_id":'+str(leader_node_id[0])+',"node_status":"'+status_mssg+'"}'                
                conn.send(send_update_message)
        conn.close()
        print('Connection closed at listeners end (listener to leader)....................................')


def listen_to_user(user_id):
    print("Listening to users.............. ")
    port = (8000) + user_id
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('0.0.0.0', port))
    print('Listening for new node at port : ', port)
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_user = ''
        while True:
            data = conn.recv(4096)
            if not data: break
            from_user += data
            rcvd_mssg = from_user
            print('Received message from user')
            rcvd_mssg = json.loads(from_user)
            if rcvd_mssg["activity"]=="user_write_request":
                print('Write request received at Group_man from user...........................................')
                print('Current leader is ........', leader_node_id[0])
                request_array.append(rcvd_mssg["value_to_be_written"])
                print(request_array)
                #consistency_state_of_write = write_request(leader_node_id[0], rcvd_mssg["value_to_be_written"])
                consistency_state_of_write = write_request(leader_node_id[0])
                conn.send(consistency_state_of_write)
            if rcvd_mssg["activity"]=="user_read_request":
                print('Write request received at Group_man from user...........................................')
                print('Current leader is ........', leader_node_id[0])
                read_result = read_request(leader_node_id[0])
                conn.send(read_result)
        conn.shutdown(1)
        conn.close()
        print('Connection closed at group_man with the user...................................')


manager = mp.Manager()
node_age = manager.list([0]*5)
node_status = manager.list([0]*5)
leader_node_id = manager.list([0])
request_array = manager.list()
#node_age = [0,0,0]
status_check_procs = []
group_update_procs = []
listen_new_node_procs = []
listen_user_procs = []
nodes = [1,2,3,4,5]
users = [1,2]

for i in users:
    #print i
    p = mp.Process(target=listen_to_user, args=(i,))
    listen_user_procs.append(p)
    p.start()
    #p.join()
    #time.sleep(2)

for i in nodes:
    #print i
    p = mp.Process(target=listen_to_new_node, args=(i,))
    listen_new_node_procs.append(p)
    p.start()
    #p.join()
    #time.sleep(2)

try:
    while True:
        #print("Staring new loop...............................................................................")
        time.sleep(20)
        for i in nodes:
            #print i
            p = mp.Process(target=node_status_check, args=(i,))
            status_check_procs.append(p)
            p.start()
            p.join()
            #time.sleep(2)

        time.sleep(5)
        #leader election
        print(node_status)
        print(node_age)
        if sum(node_age)==0:
            leader_node_id[0] = 0
        else:
            leader_node_id[0] = node_age.index(max(node_age))+1
        print('The leader elected is Node ', leader_node_id[0])

        for j in nodes:
            #print i
            #if node_status[j]==1:
            p = mp.Process(target=group_update, args=(j,leader_node_id[0]))
            group_update_procs.append(p)
            p.start()
            p.join()
        #print("Ending new loop.....xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
except KeyboardInterrupt:
    pass

#############
#7000:10004,10006:65000/tcp