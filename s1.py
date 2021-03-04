import socket
import tqdm
import os
import threading
import math
SHARED_FOLDER = "F:\\STUDY\\Trimester-2\\CN\\server_shared_files"


SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
# create the server socket
# TCP socket
## no. of parallel connections or no. of parts in which the file transfer
totalconnection = 5

##############################################################
#############################################################
#  helping functions
def menucreation():

    filelist = []
    filepath = []
    for file in os.listdir(SHARED_FOLDER):
        path = os.path.join(SHARED_FOLDER,file)
        filepath.append(path)
        filelist.append((file ,os.path.getsize(path)))
    menu = ""
    for i in range(len(filelist)):
        menu += f'{i} . {filelist[i][0]}   {str(filelist[i][1]//1024)}KB \n'

    menu += 'choose the file you want to download'
    return menu ,filelist, filepath

def connectit(client, address, i):
    msg = client.recv(1024).decode("utf-8")


    if(i == int(msg)):
        print("connected to subclient =  {}".format(i))

#-----------------------------------------------------
def servit(sock,add, id,skip_4kb_count,file_location,filename,filesize):

    f = open(file_location, "rb")

    readingpostion = id*skip_4kb_count*4096
    f.seek(readingpostion,0)

    if id == totalconnection -1:
        totalsize = filesize - readingpostion
    else:
        totalsize= skip_4kb_count*4096
    sock.send(bytes(str(totalsize),'utf-8'))

    #print(f" id == {id} ,fileposition ==  {f.tell()} ",end='\n')
    progress = tqdm.tqdm(range(totalsize), f"Sending {filename} by Thread {id+1}", unit="B", unit_scale=True, unit_divisor=1024)
    for _ in range(skip_4kb_count):
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done

                    break
                # we use sendall to assure transimission in
                # busy networks
                sock.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
    f.close()

def kuch_bhi_rakhde(client_socket):
    ###### menu recreation
    print("in this")
    menu,filelist, filepath  = menucreation()
    ## sending menu
    client_socket.send(bytes(menu,'utf-8'))

    ## receiving required file index
    file_no = client_socket.recv(1024).decode('utf-8')
    file_no=int(file_no)

    #####################################################################
    ### asking for number of connections
    client_socket.send(bytes("download file in 1 - 10 parts \nChoose between 1 to 10",'utf-8'))
    temp = client_socket.recv(1024).decode('utf-8')
    totalconnection= int(temp)

    #############################################################


    filename = filelist[file_no][0]
    filesize = filelist[file_no][1]
    file_location = filepath[file_no]
    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
    client_socket.send(bytes(str(totalconnection),'utf-8'))

    #------------------------------------------------------------------------------

    skip_4kb_count= math.ceil(math.ceil((filesize//1024))/(4*totalconnection))
    # print(f"file size = {filesize}")
    #
    # print("shipkbcount ", skip_4kb_count)

    #---------------------------------------------------------------------
    # setting up the connections

    Thread_list=[]
    subclient_list = []
    for i in range(totalconnection):
        c1, ad = s.accept()
        #print(f"[+] {ad} is connected.")
        subclient_list.append((c1, ad))
        connectit(c1,ad,i+1)
    ###########################################################
    # sending the file
    for i in range(totalconnection):
        c1,ad = subclient_list[i]
        function = threading.Thread(target=servit, args=(c1, ad, i,skip_4kb_count,file_location,filename,filesize, ))
        Thread_list.append(function)
        function.start()
    #---------------------------------------------joining the threads
    for item in Thread_list:
        item.join()
    #----------------------------------------------closing the connections
    for item in subclient_list:
        item[0].close()


    what_to_do = client_socket.recv(1024).decode('utf-8')
    if what_to_do == "1":
        kuch_bhi_rakhde(client_socket)

##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
##############################################################
#%%

s = socket.socket()
# bind the socket to our local address
s.bind(('', SERVER_PORT))




#### Initial connection setup
####

s.listen(100)
print(f"[*] Listening as :{SERVER_PORT}")
# accept connection if there is any
client_socket, address = s.accept()
# if below code is executed, that means the sender is connected
print(f"[+] {address} is connected.")

########################################################3
kuch_bhi_rakhde(client_socket)




#---------------------------------------------





# receive the file infos
# receive using client socket, not server socket
