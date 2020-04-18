There are 4 types of files attached:
-----------------------------
a) Users (Representing clients which can operate the system_
b) middleware (representing the middleware and the group management service)
c) Nodes (representing each process replica)
d) Text file (representing the storage file on disk for persistence)

Running instructions
---------------------
a) The system is designed to run on Linux-based virtual machines (implementation was done on AWS)

a) Upload files pertaining to i) users ii) middleware iii) text file iv) nodes 1, 2 as well as 3, to the AWS server with Public IP 34.243.81.104 (user as ubuntu)

b) Upload the files pertaining to i) text file ii) nodes 4 and 5, to the AWS server with Public IP 3.16.164.181 (user as ubuntu)

c) Make the necessary configuration changes like security clearances and file permissions.

d) Run middleware.py and then start the nodes in any order

e) Run the users file to operate the system as desired.

