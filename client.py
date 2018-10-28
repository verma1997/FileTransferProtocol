#Assignment 1 by Aman Varshney(201402188) and Vinay Kumar Singh(201402035)


import socket
import sys
import os
import hashlib

HOST = '10.100.112.170'   #server name goes in here
PORT = 5000


def put(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    string = commandName.split(' ')
    inputFile = string[1]
    with open(inputFile, 'rb') as file_to_send:
        for data in file_to_send:
            print "Client se jaata hua " + data
            socket1.send(data)
    print 'Upload Successful'
    socket1.close()
    return


def get(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    string = commandName.split(' ')
    inputFile = string[1]
    with open(inputFile, 'wb') as file_to_write:
        while True:
            data = socket1.recv(1024)
            if not data:
                break
            # print data
            file_to_write.write(data)
    file_to_write.close()
    print 'Download Successful'
    socket1.close()
    return

def FileHash(commandName):
    string = commandName.split(' ')
    if string[1] == 'verify':
        verify(commandName)
    elif string[1] == 'checkall':
        checkall(commandName)


def verify(commandName):
    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    hashValServer=socket1.recv(1024)

    string = commandName.split(' ')
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(string[2], 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    hashValClient = hasher.hexdigest()
    print('hashValServer= %s', (hashValServer))
    print('hashValClient= %s', (hashValClient))
    if hashValClient == hashValServer:
        print 'No updates'
    else:
        print 'Update Available'

    socket1.close()
    return


def checkall(commandName):
    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)

    string = commandName.split(' ')
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    # f=socket1.recv(1024)

    while True:
        f=socket1.recv(1024)

        with open(f, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        hashValClient = hasher.hexdigest()
        hashValServer=socket1.recv(1024)

        print ('Filename =    %s', f)
        print('hashValServer= %s', (hashValServer))
        print('hashValClient= %s', (hashValClient))
        if hashValClient == hashValServer:
            print 'No updates'
        else:
            print 'Update Available'
        if not f:
            break



    socket1.close()
    return





def quit():
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    socket1.close()
    return
def IndexGet(commandName):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    string = commandName.split(' ')
    if string[1] == 'shortlist':
        socket1.send(commandName)
        strng=socket1.recv(1024)
        strng=strng.split('\n')
        for f in strng:
            print f

    elif (string[1]=='longlist'):
        socket1.send(commandName)
        path=socket1.recv(1024)
        rslt=path.split('\n')
        for f in rslt[1:]:
            print f

    socket1.close()
    return

def serverList(commandName):
    socket1=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket1.connect((HOST, PORT))
    socket1.send(commandName)
    fileStr=socket1.recv(1024)
    fileList=fileStr.split(' ')
    for f in fileList[:-1]:
        print f

    socket1.close()
    return

msg = raw_input('Enter your name: ')
while(1):
    print "\n"
    print "****************"
    print 'Instruction'
    print '"FileUpload [filename]" to send the file the server '
    print '"FileDownload [filename]" to download the file from the server '
    print '"ls" to list all files in this directory'
    print '"lls" to list all files in the server'
    print '"IndexGet shortlist <starttimestamp> <endtimestamp>" to list the files modified in mentioned timestamp.'
    print '"IndexGet longlist" similar to shortlist but with complete file listing'
    print '"FileHash verify <filename>" checksum of the modification of the mentioned file.'
    print '"quit" to exit'
    print "\n"
    sys.stdout.write ('%s> ' %msg)
    inputCommand = sys.stdin.readline().strip()
    if (inputCommand == 'quit'):
        quit()
        break
    elif (inputCommand == 'ls'):
    	path = os.getcwd()
    	dirs = os.listdir(path)
    	for f in dirs:
    		print f
    elif (inputCommand == 'lls'):
    	serverList('lls')

    else:
    	string = inputCommand.split(' ')
    	if string[0] == 'FileDownload':
    		get(inputCommand)
    	elif string[0] == 'FileUpload':
    		put(inputCommand)
        elif string[0] =='IndexGet':
            IndexGet(inputCommand)
        elif string[0] == 'FileHash':
            FileHash(inputCommand)
