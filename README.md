# Distributed-downloading-system

Socket programming in python.

1. It can be use to share files of any type between two machines using sockets and TCP. 
For speed up the sharing process, a single file is partitioned into multiple subfiles and shared over a seperate TCP connection. At the reciever/client side, these subfile merge in a single original files.
2.It can also use to share files between system on a same LAN. 
3.To use this over android system, install pydroid and run c1.py or s1.py using it. 

4. The server_shared_files location can be changed according to the need. All the files in this folder is available for downloading to the client. 
5. Change the IP address in the c1.py file before running according to your machine.
