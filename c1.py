"""
Client that receive the file (acceptor)
"""
import socket
import tqdm
import os
import argparse
import threading
import time
#import multiThreading
totalconnection =1
port = 5001
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4 #4KB
s=socket.socket()
s.connect((socket.gethostname(), port))
print("[+] Connected.")

def friends(s):
    menu = s.recv(4096).decode('utf-8')
    print(menu)
    while True:
        x = int(input())
        lines = menu.count('\n')
        if x not in range(lines):
            print("Wrong input, try again")
        else:
            break
    print("Chosen File is ", x )
    s.send(bytes(str(x),'utf-8'))

    #################################################

    option =  s.recv(4096).decode('utf-8')
    print(option)
    while True:
        x = int(input())
        if x not in range(1,11):
            print("Wrong input, try again")
        else:
            break
    s.send(bytes(str(x),'utf-8'))

    ########################################################

    received = s.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    print( filename , filesize )
    filesize = int(filesize)

    def receiveit( sock, filename,id):
        partition_size = int(sock.recv(BUFFER_SIZE))
        progress = tqdm.tqdm(range(partition_size), f"Receiving {filename}", unit="B",unit_scale=True, unit_divisor=1024)
        filename = str(id) + "_" + filename[:-4] + ".bin"
        f =open(filename, "wb")
        while True:
                bytes_read = sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    # nothing is received
                    # file transmitting is done

                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        progress.close()

        f.close()


    totalconnection = int (s.recv(BUFFER_SIZE).decode())
    clist = []
    Thread_list =[]
    for i in range(totalconnection):
            temp = socket.socket()
            temp.connect((socket.gethostname(),port))
            temp.send(bytes(str(i+1),'utf-8'))
            clist.append(temp)


    start_time = time.time()


    for i in range(totalconnection):
            function = threading.Thread(target=receiveit, args=(clist[i],filename,i+1,))
            Thread_list.append(function)
            function.start()

    for x in Thread_list:
        x.join()
    downtime = time.time() - start_time
    print("------------File is downloaded in  %s seconds ----------" % (downtime))
    print(f"Average Speed = {(filesize/(1024*1024))/downtime} MB/sec")
    f= open("download_"+filename, "wb")

    for i in range(totalconnection):
        i+=1
        #print("doing for ",i)
        rf_name= str(i) + "_" + filename[:-4] + ".bin"
        with open(rf_name, "rb") as rf:
            while True:
                bytes_read = rf.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done

                    break
                f.write(bytes_read)
        os.remove(rf_name)

    f.close()

    print("Want to download more - Y/N")
    x = input()
    if x == "Y" or x == "y":
        s.send(bytes("1",'utf-8'))
        friends(s)
    else:
        s.send(bytes("0",'utf-8'))
        s.close()

friends(s)
