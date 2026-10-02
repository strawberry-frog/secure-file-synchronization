import socket       # Creates Socket 
import os           # For command line handling with file and directory execution. 
import time         # controlling the sleep of the socket as have more control over communications. 
import ssl          # SSL/TLS tunnel for encrypted and secure network communication.
import re           # checking fort special characters
import maskpass     # Masks password from user terminal
import subprocess   # helps read and write files in the clients terminal 
import sys          # 
import stat         #


class Server():
    #server object the client authenticates 
    #message it has received from the server
    def __init__(self, insecure, server, message, prompt, authBit):
        self.insecure = insecure
        self.server = server
        self.message = message
        self.prompt = prompt
        self.authBit = authBit

        
    def serverConnect(self):
        while (True):
            #Uses default ssl settings
            context = ssl.create_default_context()
            context.verify_mode = ssl.CERT_REQUIRED 
            context.check_hostname = True
            context.load_verify_locations("ca.crt")
            
            context.load_cert_chain("client.pem", keyfile="client.key", password="cookie")
            #sslTunnel.load_cert_chain("./katherineServer.pem", keyfile="./server.key")
            self.insecure = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try: 
                address = socket.gethostname()
                bindingAdd = socket.gethostbyname(address)
                #reuses an ipaddress. 
                self.insecure.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.insecure.connect((bindingAdd, 5001))
                context.verify_flags = context.verify_flags & ~ssl.VERIFY_X509_STRICT
                self.server = context.wrap_socket(self.insecure, server_side=False, server_hostname="Server")
                cert = self.server.getpeercert()
                if (cert == None):
                    print("Server is not authenticated")
                    self.authBit = 0
                    self.server.close()
                    self.insecure.close()
                    time.sleep(3)
                else:
                    self.client_options()
            except ConnectionRefusedError: 
                print("Retrying for connection")
                self.authBit = 0
                self.insecure.close()
                time.sleep(3)
            except ConnectionResetError:
                print("Server lost waiting for connection ....")
                self.authBit = 0
                self.insecure.close()
                time.sleep(3)
            except KeyboardInterrupt:
                print("Client closed")
                self.authBit = 0 
                self.insecure.close()
                break
            
    # client_options
    # Takes in a server reply and passes it to client_response.  
    def client_options(self):
        self.message = self.server.recv(1024).decode()
        print(self.message)
        self.client_response()
        
    # client_response 
    # Takes in the users input and sends it back to the server. 
    # Then waits for a reply, to then handle the message to the appropriate action from user.
    def client_response(self):
        if (self.authBit == 1): 
            response = input(self.prompt)
            if(response == ""):
                response = "empty"
            self.server.sendall(response.encode())
            self.message = self.server.recv(1024).decode()
        else: 
            response = input("Guest User: ")
            self.server.sendall(response.encode())
            self.message = self.server.recv(1024).decode()
        if (self.message == "start"):
            self.client_options()
        elif (self.message == "Downloading"):
            self.clientDownload()
        elif (self.message == "uploading"):
            self.clientUpload()
        elif (self.message == "account"):
            self.clientAccount()
        elif(self.message == "end"):
            self.message = self.server.recv(2024).decode()
            print(self.message)
            exit()  
        elif(self.message == "logout"):
            self.authBit = 0
            self.client_options()
        elif(self.message == "read"):
            self.readC()
        elif(self.message == "write"):
            self.writeC()
        elif(self.message == "print"):
            self.print()
        elif(self.message == "info"):
            self.message = self.server.recv(6000).decode()
            print(self.message)
            self.client_options()
    # clientAccount 
    # Handles looping through every thing the server sends the user for passwords, username, and creating account.
    def clientAccount(self):
        self.prompt = self.server.recv(1024).decode()
        while (True):
            if (self.prompt == "stop"):
                self.client_options()
            elif (self.prompt == "authenticated"):
                self.authBit = 1
                self.prompt = self.server.recv(1024).decode()
                self.message = self.server.recv(7000).decode()
                print(self.message)
                self.client_response()
            elif(re.search(':', self.prompt)):
                response = input(self.prompt)
                self.server.sendall(response.encode())
            elif(self.prompt != "secure" and  self.prompt != "authenticated" and self.prompt != "stop"):
                print(self.prompt)
            elif(self.prompt == "secure"):
                self.prompt = self.server.recv(1024).decode() 
                while (True):
                    if (self.prompt == "stop"):
                        break
                    elif(re.search(':', self.prompt)):
                        secure = maskpass.askpass(self.prompt)
                        self.server.sendall(secure.encode()) 
                    else:
                        print(self.prompt)
                    self.prompt = self.server.recv(1024).decode()
            self.prompt = self.server.recv(1024).decode()      
        
    # clientDownload 
    # handles the downloading of a file from the server onto the client. 
    def clientDownload(self):
        #Server : What file would you like to Download?
        #printing the files in the system
        message = self.server.recv(100).decode()
        print(message)
        message = self.server.recv(100).decode()
        while (True):
            if (message == "NOFile"):
                message == "NOFile"
                self.client_options()
            elif(message == "stop"):
                self.downloading()
            elif (message == "time"):
                message = self.server.recv(1024).decode()
                message = float(message)
                message =  time.ctime(message)
                print("Last Modified: " + message + "\n")
            elif(int(message, 2)):
                message = int(message,2)
                message = self.server.recv(message).decode()
                
                print(message)
            message = self.server.recv(30).decode()
            
    def downloading(self):
        message = self.server.recv(1024).decode()
        print(message)
        response = input(self.prompt)
        if(response == ""):
                response = "empty"
        time.sleep(2)
        self.server.sendall(response.encode())
        time.sleep(1)
        fileName = self.server.recv(100).decode()
        if (fileName == "start"):
                self.client_options()
        else: 
            try: 
                fileSize = self.server.recv(100).decode()
                bytes = int(fileSize,2)
                time.sleep(1)
                file = open(fileName, 'wb')
                write = self.server.recv(bytes)
                count = len(write)
                while (count != bytes):
                    
                    file.write(write)
                    write = self.server.recv(bytes)
                    count += len(write)
                file.write(write)
                file.close()
                full = os.path.getsize(fileName)
                print("File is '%s' bytes." % full)
                self.server.sendall(bin(full).encode())
                message = self.server.recv(100).decode()
                print(message)
                self.client_options()
            except IOError:
                print("I can't open " + fileName) 
                
                
    # clientUpload
    # shows user the files in teh directory they are in, asks if they want to change directories. 
    # User chooses file from directory and then sends in to the server. 
    # Verifies whether or not the upload was successful. 
    def clientUpload(self):
        self.message = self.server.recv(1024).decode()
        print(self.message)
        iterator = 0
        print("============= UPLOAD A FILE ONTO SERVER =============")
        while (iterator <= 5):
            iterator += 1
            printFile = input("Would you like to print files in current directory " +  os.getcwd() + " (Y or N)?\n" + self.prompt)
            if ((printFile == "Y" ) or (printFile == "Yes") or (printFile == "y") or (printFile == "yes") or (printFile == "")):
                dir = os.getcwd()
                fileList = os.listdir(dir)
                for file in fileList:
                    if (os.path.isfile(file)):
                        print(file)
            dir = input ("Would you like to change directories (Y or N)?\n" + self.prompt)
            if (( dir == "Y" ) or (dir == "Yes") or (dir == "y") or (dir == "yes") or (dir == "")):
                print("What directory would you like to change to? ")
                dir = input("WARNING Incorrect Input Will Result In No Change To Directory.\n============= EXAMPLES OF ACCEPTED INPUT =============\n Absolute path: Example /home/Botticelli/Project\n Subdirectory of current directory: Example (CS610) \n Parent Process: Example (..)\n" + self.prompt)
                try :
                    os.chdir(dir)
                    dir = os.getcwd()
                    print("Now in " + dir )
                except OSError:
                    print("DIRECTORY DID NOT CHANGE.")
            else:
                iterator = 6
        print("What file would you like to upload to server?")
        fileName = input(self.prompt)
        print("******* ATTEMPTING UPLOAD OF FILE "+ fileName + " ON TO SERVER *******")
        file = 0
        attempt = 3
        while (file <= 3):
            if (os.path.isfile(fileName)):
                print("******* FILE "+ fileName + " FOUND *******")
                self.uploadingServer(fileName)
            elif (fileName.__contains__("/")):
                print("------- File MUST BE EXACT FILE Name -------\n   (File can not contain '/')")
                print("%s ATTEMPTS LEFT" % attempt)
                fileName = input(self.prompt)
                file += 1
                attempt -=1
            elif (file == 3):
                print("------- FAILED: CAN NOT OPEN FILE " + fileName + " -------")
                self.server.sendall(b"failed")
                os.system('clr')
                self.client_options()
            else: 
                print("------- FAILED: FILE " + fileName+" DOES NOT EXIST -------")
                print("%s ATTEMPTS LEFT" % attempt)
                fileName = input(self.prompt)
                file += 1
                attempt -=1
                
    # uploadingServer 
    # handles the file so that it can be readable for Server.
    def uploadingServer(self, fileName):
        try: 
            tryFile = open(fileName, 'rb')
            try:
                tryFile.read()
                tryFile.close()
            except UnicodeDecodeError:
                print("------- FAILED: CAN NOT DECODE FILE " + fileName+ " -------")
                self.server.sendall(b"failed")
                os.system('clr')
                self.client_options()
            file = open(fileName, 'rb')
            self.server.sendall(fileName.encode())
            time.sleep(1)
            bytes = os.path.getsize(fileName)
            print(fileName + " HAS '%s' BYTES OF MEMORY" % bytes)
            self.server.sendall(bin(bytes).encode())
            time.sleep(1)
            contents = file.read()
            self.server.sendall(contents)
            file.close()
            if (bytes > 1024):
                    bytes -= 1024
                    while(bytes != 0):
                        if ((bytes) <= 1024):
                            bytes = 0
                        else: 
                            bytes -= 1024
            self.message = self.server.recv(1024).decode()
            print(self.message)
            self.client_response()
        except IOError:
            print("------- FAILED: CAN'T OPEN FILE " + fileName + " -------")
            self.server.sendall(b"failed")
            self.client_options()
            
    def readC(self):
        #Server : What file would you like to Download?
        #printing the files in the system
        message = self.server.recv(100).decode()
        print(message)
        message = self.server.recv(100).decode()
        while (True):
            if (message == "NOFile"):
                message == "NOFile"
                self.client_options()
            elif(message == "stop"):
                self.reading()
            elif (message == "time"):
                message = self.server.recv(1024).decode()
                message = float(message)
                message =  time.ctime(message)
                print("Last Modified: " + message + "\n")
            elif(int(message, 2)):
                message = int(message,2)
                message = self.server.recv(message).decode()
                
                print(message)
            message = self.server.recv(30).decode()
            
            
    def reading(self):
        message = self.server.recv(1024).decode()
        print(message)
        fileName = input(self.prompt)
        self.server.sendall(fileName.encode())
        message = self.server.recv(100).decode()
        if (message == "stop"):
            self.client_options()
        else: 
            print(message)
            message = self.server.recv(100).decode()
            if (message == "stop"):
                self.client_options()
            else:
                fileSize = self.server.recv(100).decode()
                bytes = int(fileSize,2)
                time.sleep(1)
                print("~~~~~~~~~~~~~~~~ READING " + fileName + " ~~~~~~~~~~~~~~~~")
                write = self.server.recv(bytes).decode()
                count = len(write)
                while (count != bytes):
                    write += self.server.recv(bytes).decode()
                    count += len(write)
                print(write)
                self.server.sendall(bin(count).encode())
                print("-------- DONE READING " + fileName +" --------")
                self.server.sendall(b"read")
                self.client_options()
                
    def writeC(self):
        #Server : What file would you like to Download?
        #printing the files in the system
        message = self.server.recv(100).decode()
        print(message)
        message = self.server.recv(100).decode()
        while (True):
            if (message == "NOFile"):
                message == "NOFile"
                self.client_options()
            elif(message == "stop"):
                self.writing()
            elif (message == "time"):
                message = self.server.recv(1024).decode()
                message = float(message)
                message =  time.ctime(message)
                print("Last Modified: " + message + "\n")
            elif(int(message, 2)):
                message = int(message,2)
                message = self.server.recv(message).decode()
                
                print(message)
            message = self.server.recv(30).decode()
            
    def writing(self):
        message = self.server.recv(4000).decode()   
        while (message != "stop"):
            if (message == "file"):
                fileSize = self.server.recv(100).decode()
                bytes = int(fileSize,2)
                
                time.sleep(1)
                lines = self.server.recv(100).decode()
                lines = int(lines)
                
                write = self.server.recv(bytes).decode()
                count = len(write)
                while (count != bytes):
                    write += self.server.recv(bytes).decode()
                    count += len(write)
                print(write)
                answer = bin(count)
                self.server.sendall(answer.encode())
                time.sleep(2)
            elif( message == "start"):
                self.writeC()
            elif(message != "file"): 
                print(message)
                answer = input(self.prompt)
                self.server.sendall(answer.encode())
            message = self.server.recv(4000).decode() 
        self.client_options()
        
    # clientDownload 
    # handles the downloading of a file from the server onto the client. 
    def print(self):
        #Server : What file would you like to Download?
        #printing the files in the system
        message = self.server.recv(100).decode()
        print(message)
        message = self.server.recv(100).decode()
        while (True):
            if(message == "stop"):
                self.client_options()
            elif (message == "time"):
                message = self.server.recv(1024).decode()
                message = float(message)
                message =  time.ctime(message)
                print("Last Modified: " + message + "\n")
            elif(int(message, 2)):
                message = int(message,2)
                message = self.server.recv(message).decode()
                
                print(message)
            message = self.server.recv(30).decode()
            
                
def main():
    s = Server(insecure = None, server=None, message=None, prompt="Guest User: ", authBit = 0)
    s.serverConnect()
if __name__ == "__main__":
    main()