# A Distributed memory Store 
A crude version of a distributed memory store systems which are indexed using a folder structure. It also has two other components to use different transactions and demonstrate the various features of the underlying distributed system (i.e. the database): i) A sensor application which simulates raw data values and feeds into the database at a given destination IP ii) A basic application which queries the database to get required data.

Main functionalities: 
    - Multiple users can write to a distributed memory store
    - Multiple users can read the past values written by all users
    - Multiple users can concurrently operate the system
    - The memory store also offers a persistent storage capability in case of system shutdown
    
Components: 
1) Users
2) Group management service
3) Middleware
4) Process replica (Leader)
5) Process replica (Follower)

List of functions used in the development process:

**Middleware**:
node_status_check(node_id)
group_update(node_id, elected_leader_id):
write_request(elected_leader_id):
read_request(elected_leader_id):
listen_to_new_node(node_id):
listen_to_user(user_id):

**Process replicas**:
get_master_copy_from_leader(leader_id, node_id):
read_from_file():
node_start_up(node_id):
connect_with_followers(leader_id, node_id, value_to_be_written):
initiate_multicast(value_to_be_written):
listen_new_nodes_as_leader(leader_id, node_id):
initiate_leader_to_new_node():
write_to_file():
server_connect(node_id):
listen_to_leader(leader_id, node_id):

**Users**:
user_write_request(user_id, value_to_be_written):
user_read_request(user_id):


**There are 4 types of files attached:**
-----------------------------
a) Users (Representing clients which can operate the system_
b) middleware (representing the middleware and the group management service)
c) Nodes (representing each process replica)
d) Text file (representing the storage file on disk for persistence)

**Running instructions**
---------------------
a) The system is designed to run on Linux-based virtual machines (implementation was done on AWS)

a) Upload files pertaining to i) users ii) middleware iii) text file iv) nodes 1, 2 as well as 3, to the AWS server with Public IP 34.243.81.104 (user as ubuntu)

b) Upload the files pertaining to i) text file ii) nodes 4 and 5, to the AWS server with Public IP 3.16.164.181 (user as ubuntu)

c) Make the necessary configuration changes like security clearances and file permissions.

d) Run middleware.py and then start the nodes in any order

e) Run the users file to operate the system as desired.


