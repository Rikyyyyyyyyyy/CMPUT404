#!/usr/bin/env python3
import socket
import time

#define address & buffer size

##host is our address
HOST = socket.gethostbyname( socket.gethostname() )
PORT = 8001

## buffer size is the header szie we want to receive
BUFFER_SIZE = 1024

def main():
    ## here we create a new socket
    ## and the first parameter is the category of socket we want to create
    ## the seccond parameter is the way we want teh socket to pass data
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        ## which mean everthing that connect to this address will hit the socket
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            ## it blocks, it wait this line here for a new connection,
            ## we store the connet address
            ## and the connection is object that we can send information back to the address
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            ##her is actually the lenth for the data we gonna receive
            ## the second recv will be the actal message 
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            conn.sendall(full_data)
            conn.close()

if __name__ == "__main__":
    main()
