#Assignment 1 by Aman Varshney(201402188) and Vinay Kumar Singh(201402035)
import commands
import socket
import sys
import os
import hashlib

HOST = 'localhost'
PORT = 5000

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Server Created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

s.listen(1)
print 'Server now listning'



while (1):
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    reqCommand = conn.recv(1024)
    print 'Client> %s' %(reqCommand)
    string = reqCommand.split(' ')
    if (reqCommand == 'quit'):
        break
    elif (reqCommand == 'lls'):
        toSend=""
        path = os.getcwd()
        dirs=os.listdir(path)
        for f in dirs:
            toSend=toSend+f+' '
        conn.send(toSend)
        #print path

    elif (string[1]=='shortlist'):
        path = os.getcwd()
        command = 'find '+path+ ' -type f -newermt '+string[2]+' '+string[3]+ ' ! -newermt '+string[4]+' '+string[5]
        var = commands.getstatusoutput(command)
        var1 = var[1]
        var=var1.split('\n')
        rslt = ""
        for i in var:
            comm = "ls -l "+i+" | awk '{print $9, $5, $6, $7, $8}'"
            tup=commands.getstatusoutput(comm)
            tup1=tup[1]
            str=tup1.split(' ')
            str1=str[0]
            str2=str1.split('/')
            rslt=rslt+str2[-1]+' '+str[1]+' '+str[2]+' '+str[3]+' '+str[4]+'\n'
        conn.send(rslt)

    elif (string[1]=='longlist'):
        path = os.getcwd()
        var= commands.getstatusoutput("ls -l "+path+" | awk '{print $9, $5, $6, $7, $8}'")
        var1 = ""
        var1= var1+''+var[1]
        conn.send(var1)

    elif (string[0] == 'FileHash'):
        if(string[1]== 'verify'):
            BLOCKSIZE = 65536
            hasher = hashlib.sha1()
            with open(string[2], 'rb') as afile:
                buf = afile.read(BLOCKSIZE)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(BLOCKSIZE)
            conn.send(hasher.hexdigest())
            print 'Hash Successful'




        elif (string[1] == 'checkall'):
            BLOCKSIZE = 65536
            hasher = hashlib.sha1()

            path = os.getcwd()
            dirs=os.listdir(path)
            for f in dirs:
                conn.send(f)
                with open(f, 'rb') as afile:
                    buf = afile.read(BLOCKSIZE)
                    while len(buf) > 0:
                        hasher.update(buf)
                        buf = afile.read(BLOCKSIZE)
                conn.send(hasher.hexdigest())
                print 'Hash Successful'





    else:
        string = reqCommand.split(' ')   #in case of 'put' and 'get' method
        if(len(string) > 1):
	        reqFile = string[1]

	        if (string[0] == 'FileUpload'):
	            file_to_write = open(reqFile,'wb')
                    si = string[2:]
                    for p in si:
                        p = p + " "
                        print "Command ka bacha hua" + p
                        file_to_write.write(p)
                    while True:
                        data = conn.recv(1024)
        	        print "kuch BHi data" +data
                        if not data:
                            break
                        file_to_write.write(data)
                    file_to_write.close()
        	    print 'Receive Successful'
	        elif (string[0] == 'FileDownload'):
	            with open(reqFile, 'rb') as file_to_send:
	                for data in file_to_send:
	                    conn.sendall(data)
	            print 'Send Successful'
    conn.close()

s.close()
