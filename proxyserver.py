import os
from socket import *
import sys
import time

if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.

# Create a folder for the cache
if not os.path.exists("cache/"):
    os.makedirs("cache/")

# Assign a port number
tcp_server_port = 8888

# Bind the socket to server address and server port
tcpSerSock.bind(("", tcp_server_port))

# Listen to at most 1 connection at a time
tcpSerSock.listen(1)

# Fill in end.

while 1:
    # Start receiving data from the client
    print('Ready to serve...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)

    # Start measuring the time
    start_time = time.time()

    # Fill in start.

    message = b""
    co = 1
    while True:
        data = tcpCliSock.recv(1)
        message += data
        co += 1
        if data == b'\r':
            data = tcpCliSock.recv(3)
            if data == b'\n\r\n':
                break
            else:
                message += data
    
    # Fill in end.
    print(message)
    
    # Extract the filename from the given message
    
    full_addr = message.split()[1].partition(b'/')[2].partition(b'/')
    filename = full_addr[2]
    hostname = full_addr[0]
    print("File name: ", filename)
    print("Host name: ", hostname)
    fileExist = "false"
    filetouse = b'/' + hostname + b'-' + filename.replace(b'/', b'-', 1)
    print("File: ", filetouse)

    try:
        # Check wether the file exist in the cache
        path_to_file = (b'cache/' + filetouse[1:]).decode()
        f = open(path_to_file, "rb")
        outputdata = f.readlines()
        fileExist = "true"

        # Cached file already contains the header
        #tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        #tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())

        # Fill in start.

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            tcpCliSock.send(outputdata[i])
        tcpCliSock.send("\r\n".encode())
        
        # Fill in end.

        print('Read from cache')

    # Error handling for file not found in cache
    except IOError:
        if fileExist == "false":
            # Create a socket on the proxyserver
            # Fill in start.
            tcpProxyCliSock = socket(AF_INET, SOCK_STREAM)
            # Fill in end.

            try:
                # Connect to the socket to port 80 ???
                server_port = 80
                server_addr = hostname
                if (b':' in hostname):
                    server_addr = hostname.partition(b':')[0].decode()
                    server_port = hostname.partition(b':')[2].decode()
                # Fill in start.
                tcpProxyCliSock.connect((server_addr, int(server_port)))

                # Fill in end.

                # Create a temporary file on this socket and ask port 80 for the file requested by the client
                fileobj = tcpProxyCliSock.makefile('wb', 0)
                request_msg = ("GET /"
                                + filename.decode() 
                                + " HTTP/1.0\r\nHost: " 
                                + hostname.decode()
                                + "\r\n\r\n").encode()
                print("Request from proxy: ", request_msg)
                fileobj.write(request_msg)
                # Read the response into buffer

                # Fill in start.

                fileobj.flush()
                fileobj_response = tcpProxyCliSock.makefile('rb', 0)
                message = fileobj_response.readlines()
                print("Response to proxy: ", message)
                tcpProxyCliSock.close()

                # Fill in end.

                # Create a new file in the cache for the requested file.
                tmpFile = open("./cache" + filetouse.decode(), "wb")

                # Fill in start.
                
                # Fill out the file and close it
                for i in range(0, len(message)):
                    tmpFile.write(message[i])
                tmpFile.close()

                # Also send the response in the buffer to client socket
                for i in range(0, len(message)):
                    tcpCliSock.send(message[i])
                tcpCliSock.send("\r\n".encode())

                tcpProxyCliSock.close()

                # Fill in end.

            except Exception as e:
                print("Illegal request: ", e)

        #else:
            # HTTP response message for file not found
            # Isn't that true that you never get into this block?
            # If file is not found then the exception is raised and 
            # you create/store this file with the data from the target host 
            # If file is found, then it is read from the cache before except block 
            
            # Fill in start.
            # Fill in end.

    #Close the client and the server sockets
    tcpCliSock.close()
    
    end_time = time.time()

    print("Load time: ", end_time - start_time)

# Fill in start.
tcpSerSock.close()
# Fill in end.