import socket
import multiprocessing as mp
import time
import json

node_id = 4
#stored_string = ""
nodes = [1,2,3,4,5]

manager = mp.Manager()
node_wise_write_update = manager.list([0]*5)
stored_string = manager.list([""])

node_status = [0,0,0,0,0]
leader_node_id = 0

start = time.time()

def convert(string): 
    global node_status
    node_status = list(string.split(" "))
    for i in range(0, len(node_status)):
        node_status[i] = int(node_status[i])
    #print(node_status)
    #return li

def get_master_copy_from_leader(leader_id, node_id):
    if node_id>=4:
    	if leader_id>=4:
    		IP = '0.0.0.0'
    	else:
    		IP = '34.243.81.104'
    if node_id<4:
    	if leader_id<4:
    		IP = '0.0.0.0'
    	else:
    		IP = '3.16.164.181'
    print("Initiate master copy download...................................")
    port = ((90+leader_id)*100) + node_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        print("Socket error: ", e)
        return
    send_download_request = 'request_master_copy'
    client.send(send_download_request)
    from_leader = client.recv(4096)
    print(from_leader)
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    client.close()
    return from_leader

def read_from_file():
    global stored_string
    with open('persistent_storage.txt', 'r') as file:
        data = file.read()
        stored_string[0] = data

def node_start_up(node_id):
    global leader_node_id
    global stored_string
    global node_status
    IP= '34.243.81.104'
    print("Node start up initiated...................................")
    port = (50000) + node_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    try: 
        client.connect((IP, port))
    except socket.error, e:
        print("Socket error: ", e)
        return
    send_download_request = 'ping_new_node'
    client.send(send_download_request)
    from_server = client.recv(4096)
    print(from_server)
    rcvd_mssg = json.loads(from_server)
    leader_node_id = int(rcvd_mssg["leader_node_id"])
    #node_status[node_id-1] = True
    #node_age[node_id-1] = rcvd_mssg["age"]
    convert(rcvd_mssg["node_status"])
    if sum(node_status) == 0:
        read_from_file()
        print("Local copy updated at start-up from file: ", stored_string[0])
    else:
        stored_string[0] = get_master_copy_from_leader(leader_node_id, node_id)
        if stored_string[0] is None or stored_string[0]=="blank":
    	   stored_string[0] =''
    print('New nodes local copy updated to: ', stored_string[0])
    client.close()

node_start_up(node_id)

def connect_with_followers(leader_id, node_id, value_to_be_written):
    if node_id>=4:
    	if leader_id>=4:
    		IP = '0.0.0.0'
    	else:
    		IP = '3.16.164.181'
    if node_id<4:
    	if leader_id<4:
    		IP = '0.0.0.0'
    	else:
    		IP = '34.243.81.104'
    port = ((leader_id+10)*1000) + node_id
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3.0)
    print('Leader connected with socket: ', port)
    try:
        client.connect((IP, port))
    except socket.error, e:
        print("Socket error: ", e)
        node_wise_write_update[node_id-1]=0
        return
    message_to_followers = value_to_be_written
    client.send(message_to_followers)
    from_server = client.recv(4096)
    client.close()
    print(from_server)
    #if int(from_server)==1:
    if (from_server=="1"):
        node_wise_write_update[node_id-1]=1


def initiate_multicast(value_to_be_written):
    # pop up multiple processes
    print('Multicast initiated...................................')
    global nodes
    global node_status
    global leader_node_id
    multi_cast_procs = []
    for i in range(0,len(nodes)):
        #print(' For i: ', i)
        # connect to node only if it's active and the node is not the leader itself
        print(' For i: ', i, ' Node status: ', node_status[i], ' node number: ', nodes[i])
        if (node_status[i]==1 and nodes[i]!=leader_node_id):
            p = mp.Process(target=connect_with_followers, args=(leader_node_id,nodes[i],value_to_be_written,))
            multi_cast_procs.append(p)
            p.start()
            p.join()
        #time.sleep(2)
    time.sleep(2)
    # check if all active nodes were updated with the latest write
    write_transaction_fail_count = 0
    for j in range(0,len(nodes)):
        if write_transaction_fail_count>1:
            return 0 # indicating failure
        if j == (leader_node_id-1):
            continue # skip for the leader itself
        if (node_status[j]==1 and node_wise_write_update[j]==0):
            write_transaction_fail_count = write_transaction_fail_count + 1
    return 1

def listen_new_nodes_as_leader(leader_id, node_id):
    # printing process id
    #global stored_string
    print("Acting as a leader for new nodes..............................")
    port = ((90+leader_id)*100) + node_id
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind(('0.0.0.0', port))
    except socket.error, e:
        skip_temp = 0
    print('Listening to any new nodes at port : ', port)
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_new_node = ''
        while True:
            data = conn.recv(4096)
            if not data: break
            from_new_node += data
            print('Received message from Node ', node_id, ' : ', from_new_node)
            message_master_copy=stored_string[0]
            if message_master_copy=='':
                print("Yes blank message detected.. converted to None")
                message_master_copy = "blank"
            conn.send(message_master_copy)
        conn.close()
        print('Connection closed at leaders end....................................')
        #print('sending from: ', port)
#def leader_broadcast():

def initiate_leader_to_new_node():
    # pop up multiple processes
    print('Initiate leader_to_new_node initiated...................................')
    global nodes
    global node_status
    global leader_node_id
    listen_new_node_procs = []
    for i in range(0,len(nodes)):
        # connect to node only if it's active and the node is not the leader itself
        #if (node_status[i]==1 and nodes[i]!=leader_node_id):
        if (nodes[i]!=leader_node_id):
            p = mp.Process(target=listen_new_nodes_as_leader, args=(leader_node_id,nodes[i],))
            listen_new_node_procs.append(p)
            p.start()
            #p.join()


def write_to_file():
    global stored_string
    text_file = open("persistent_storage.txt", "w")
    text_file.write(stored_string[0])
    text_file.close()
    print("---------------- Written to File ----------------------")

def server_connect(node_id): 
    # printing process id
    global node_status
    global leader_node_id
    global stored_string
    global start
    sole_replica_first_time = False
    last_time_heard_from_cluster = time.time()
    port = (10000) + node_id
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind(('0.0.0.0', port))
    except socket.error, e:
        skip_temp = 0
    print('Listening at: ', port)
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_client = ''
        temp_variable = False
        while True:
            data = conn.recv(4096)
            if not data: break
            from_client += data
            print(from_client)
            rcvd_mssg = json.loads(from_client)
            if rcvd_mssg["activity"]=="node_status_check":
                print('Node status check received.....................................')
                age = time.time() - start
                response_message = '{"age":' + str(round(age,2)) + '}'
                conn.send(response_message)
            if rcvd_mssg["activity"]=="group_update":
                print('Group update received...........................................')
                #if rcvd_mssg["leader_node_id"]==node_id:
                response_message = 'Group update received by Node ' + str(node_id)
                conn.send(response_message)
                ##############################################################################################
                this_time_heard = time.time()
                print ("xxxxxxxxxxxxxxxxxxx ", this_time_heard-last_time_heard_from_cluster, " xxxxxxxxxxxx")
                if (this_time_heard-last_time_heard_from_cluster)>40:
                    print("Yes more time taken")
                    start = time.time()
                    node_start_up(node_id)
                last_time_heard_from_cluster = time.time()
                ##############################################################################################
                # update local copy of leader_node_id
                leader_node_id = int(rcvd_mssg["leader_node_id"])
                # update local copy of node_status
                convert(rcvd_mssg["node_status"])
                print('updated local copy of node_status: ', node_status)
                if sum(node_status)==1 and node_status[node_id-1]==1 and sole_replica_first_time==False:
                    ######## print("xxxxxxxxxxxxxxxxxxx Written local copy to disk xxxxxxxxxxxxxxxxxxx")
                    sole_replica_first_time = True
                    write_to_file()
                if sum(node_status)>1:
                    sole_replica_first_time=False
                if rcvd_mssg["leader_node_id"]!=node_id:
                    # close connection as the next following function call exits the function
                    #conn.close()
                    #print('Connection closed at listeners end (listener to client)....................................')
                    # act as follower (listen to leader) (single process)
                    temp_variable = True
                    #listen_to_leader(leader_node_id, node_id)
                    #print("ignore me")
                if rcvd_mssg["leader_node_id"]==node_id:
                    initiate_leader_to_new_node()
            if rcvd_mssg["activity"]=="write_request":
                print('Write request received...........................................')
                # only possible when this node is leader
                # update the local copy of the leader
                stored_string[0] = stored_string[0] + rcvd_mssg["value_to_be_written"]
                print('Leaders local copy updated to ........', stored_string[0])
                # act as leader and send to all nodes (client function). Need to run multiple processes
                result = initiate_multicast(rcvd_mssg["value_to_be_written"])
                print("Write status update from all followers: ", result)
                response_message = str(result)
                conn.send(response_message)
                if sum(node_status)==1 and node_status[node_id-1]==1:
                    ######## print("xxxxxxxxxxxxxxxxxxx Written local copy to disk xxxxxxxxxxxxxxxxxxx")
                    write_to_file()
            if rcvd_mssg["activity"]=="read_request":
                # only possible when the node is the leader
                response_message = stored_string[0]
                conn.send(response_message)
            #message = "I am node " + str(node_id) + 'alive since ' + str(age)
            #if activity = write and leader = this node, then update array and run leader broadcast function
            #if activity = write and leader = others, then run server function to listen to broadcasts and confirm back if updated array
            
        conn.shutdown(1)
        conn.close()
        print('Connection closed at listeners end (listener to client)....................................')
        if temp_variable==True:
            print('temp variable is true.....')
            p1 = mp.Process(target=listen_to_leader, args=(leader_node_id, node_id,))
            p1.start()
            #listen_to_leader(leader_node_id, node_id)
            print('moving ahead........')
        #print('sending from: ', port)

def listen_to_leader(leader_id, node_id):
    # printing process id
    #global stored_string
    print("Acting as a follower to Node: ", leader_id, "..............................")
    port = ((leader_id+10)*1000) + node_id
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv.bind(('0.0.0.0', port))
    except socket.error, e:
        skip_temp = 0
    print('Listening to the leader at port : ', port)
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        from_leader = ''
        while True:
            data = conn.recv(4096)
            if not data: break
            from_leader += data
            print('Received message from Node ', leader_id, ' : ', from_leader)
            stored_string[0] = stored_string[0] + from_leader
            # just update local copy of the array (as a follower)
            print('Local copy updated to ', stored_string[0])
            #message = '{"age":' + str(round(age,2)) + '}'
            #message = "received update at node: " + str(node_id)
            message="1"
            conn.send(message)
        conn.close()
        print('Connection closed at listeners end (listener to leader)....................................')
        #print('sending from: ', port)
#def leader_broadcast():

#p1 = mp.Process(target=server_connect, args=(node_id,))
#p1.start()

server_connect(node_id)



