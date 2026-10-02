import socket       # Creates Socket 
import os           # For command line handling with file and directory execution. 
import time         # controlling the sleep of the socket as have more control over communications. 
import ssl          # SSL/TLS tunnel for encrypted and secure network communication.
import re           # checking fort special characters
import maskpass     # Masks password from user terminal
import subprocess   # helps read and write files in the clients terminal 
import sys          # 
import stat         #
#import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import  multiprocessing

class Server():
    #server object the client authenticates 
    #message it has received from the server
    manager = multiprocessing.Manager()

    filing = manager.dict()
    filing['UPLOAD'] = manager.list()
    filing['DOWNLOAD'] = manager.list()
    filing['DELETE'] = manager.list()

    files = manager.dict()
    
    uploadQ = manager.Queue()
    deleteQ = manager.Queue()
    downloadQ = manager.Queue()

    files['UPLOAD'] = manager.list()
    files['DOWNLOAD'] = manager.list()
    files['DELETE'] = manager.list()
    
    timing = manager.dict()
    
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
        elif (self.message == "reset"):
            self.clientReset()
    
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
                self.clientEvents()
            elif(re.search(':', self.prompt)):
                response = input(self.prompt)
                if(response == ""):
                    response = "empty"
                self.server.sendall(response.encode())
            elif(self.prompt != "secure" and  self.prompt != "authenticated" and self.prompt != "stop"):
                print(self.prompt)
            elif(self.prompt == "secure"):
                self.prompt = self.server.recv(1024).decode() 
                while (True):
                    if (self.prompt == "stop"):
                        break
                    elif(re.search(':', self.prompt)):
                        trying = 0
                        while (trying < 3):
                            secure = maskpass.askpass(self.prompt)
                            if(secure == "" and trying == 3):
                                print("CAN NOT TAKE NO INPUT USING DEFAULT: Default$ption56")
                                secure = "Default$ption56"
                                break
                            elif(secure == ""):
                                print("NOT AN OPTION TRY AGAIN")
                                trying += 1
                            else:
                                break
                        self.server.sendall(secure.encode()) 
                    else:
                        print(self.prompt)
                    self.prompt = self.server.recv(1024).decode()
            self.prompt = self.server.recv(1024).decode()
    def getServer(self):
        return self.server


    def clientEvents(self):
        try:
            os.chdir(self.prompt)
        except FileNotFoundError:
            os.mkdir(self.prompt)
            os.chdir(self.prompt)
        filled = os.listdir()
        count = 0
        print("---- SYNCHING WITH SERVER FOR FIRST LOG IN ----")
        for file in filled:
            if os.path.isfile(file):
                count += 1
        counting = bin(count).encode()
        self.server.sendall(counting)
        for file in filled: 
            if os.path.isfile(file):
                self.server.sendall(file.encode())
                bytes = os.path.getsize(file)
                bytes2 = bin(bytes).encode()
                self.server.sendall(bytes2)
                timing = str(os.path.getmtime(file)).encode()
                self.server.sendall(timing)
                toDo = self.server.recv(1024).decode()
                if toDo == "upload":
                    Server.uploadQ.put(file)
                else:
                    file = file 
        print("--------- CLIENT READY TO SYNC ---------")
        upload = multiprocessing.Process(target=self.upload, args=(Server.uploadQ, Server.files, ))
        delete = multiprocessing.Process(target=self.delete, args=(Server.deleteQ, Server.files,  ))
        upload.daemon = True
        upload.start()
        delete.daemon = True
        delete.start()
        print(self.prompt + " user is logged in waiting 12 seconds to sync........")
    
        observer = Observer()
        event = Handler(Server.filing, Server.uploadQ, Server.deleteQ)
        observer.schedule(event, os.getcwd(), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(12)
                count = 0
                counted = 0
                print("******* SYNCING...... *******")
                #reset the event dictionary. 
                #files = self.getFiles(Server.filing, Server.files)
                for outer, values in Server.files.items(): 
                    print(outer, values) 
                    for i in values:
                        if (outer == 'UPLOAD'):
                            count += 1
                        elif (outer == 'DELETE'):
                            counted += 1    
                        i = i
                
                if (count == 0 and counted == 0):
                    print("******* NO ACTION ON USER *******")
                    self.server.sendall(b"None")
                else:
                    print("******* SENDING JOBS TO SERVER *******")
                    self.server.sendall(b"count")
                    count = bin(count).encode()
                    counted = bin(counted).encode()
                    self.server.sendall(count)
                    self.server.sendall(counted)
                    time.sleep(1)
                    for outer in Server.files['UPLOAD']:
                        self.server.sendall(outer.encode())
                    for outer in Server.files['DELETE']:
                        self.server.sendall(outer.encode())
                    
                    done = self.serverUpload(Server.files)
                # Need to read these files to the server. 
                    self.server.sendall(done.encode())
                print("******* SERVER SYNCING..... *******")
                actions = self.serverSync()
                if actions == None:
                    print("+++++ SERVER HAS NO ACTIONS +++++")
                else:
                    print("+++++ SERVER HAS COMPLETED ACTIONS +++++")
                print("******* SYNCING COMPLETE *******")
                Server.files['UPLOAD'] = Server.manager.list()
                Server.files['DOWNLOAD'] = Server.manager.list()
                Server.files['DELETE'] = Server.manager.list()
                print("\nWaiting 12 seconds.......\n")
                
        except:
            observer.stop()
        observer.join()
        upload.join()
        delete.join()
        
    def upload(self, u, files):
        
        item = u.get()
        while item:
            
            if item in files['UPLOAD']:
                item = item 
            else: 
                files['UPLOAD'].append(item)
            item = u.get()
        Server.files.update(files)
        return files
            
    def delete(self, d, files):
        item = d.get()
        
        delete_this = None
        new_files = {}
        while item:
            #print("deleted item: "+ item)
            if item in files['UPLOAD']:
                #files['UPLOAD'].pop(item)
                files['UPLOAD'].remove(item)
                
            if item in files['DELETE']:
                item = item 
            else: 
                files['DELETE'].append(item)
            if delete_this != None: 
                for outer, value in files.items():
                    if outer == 'UPLOAD' and value == delete_this:
                        outer = outer
                    else:
                        files['DELETE'].append(value)
                files = new_files
            item = d.get()
        Server.files.update(files)
        return files
    
    def serverSync(self):
        time.sleep(10)
        filled = os.listdir()
        count = 0
        for file in filled:
            if os.path.isfile(file):
                count += 1
        counting = bin(count).encode()
        self.server.sendall(counting)
        
        for file in filled: 
            if os.path.isfile(file):
                self.server.sendall(file.encode())
                bytes = os.path.getsize(file)
                bytes2 = bin(bytes).encode()
                self.server.sendall(bytes2)
                timing = str(os.path.getmtime(file)).encode()
                self.server.sendall(timing)
        server_files = {}
        
        server_files['UPLOAD'] = []
        server_files['DOWNLOAD'] = []
        server_files['DELETE'] = []
        downloading = self.server.recv(1024).decode()
        deleting = self.server.recv(1024).decode()
        
        download = int(downloading, 2)
        delete = int(deleting, 2)
        
        if(delete == 0 and download == 0):
            return None
        if(download > 0):
            for i in range(download):
                filer = self.server.recv(1024).decode()
                server_files['DOWNLOAD'].append(filer)
        if (delete > 0): 
            for i in range(delete):
                filer = self.server.recv(1024).decode()
                server_files['DELETE'].append(filer)
            
        for outer, value in server_files.items():
            print(outer, value)
    
        for pages in server_files['DOWNLOAD']:
            
            bytes = self.server.recv(1024).decode()
            
            bytes = int(bytes, 2)
            filename = open(pages, 'wb')
            write = self.server.recv(bytes)
            count = len(write)
            while (count != bytes):
                filename.write(write)
                write = self.server.recv(bytes)
                count += len(write)
            
            filename.write(write)
            filename.close()

            server_files['DOWNLOAD'].remove(pages)
            time.sleep(2)
        for pages  in server_files['DELETE']:  
                os.remove(pages)
                server_files['DELETE'].remove(pages)
        
        return "completed"
        
    def serverUpload(self, files):
        self.server.sendall(b"upload")
        for file in files['UPLOAD']:
            
            
            bytes = os.path.getsize(file)
            
            bytes2 = bin(bytes).encode()
                
            self.server.sendall(bytes2)
            #Server.timing[file].append(datetime.datetime)
            uploading = open(file, 'rb')
            contents = uploading.read()
            
            uploading.close()
            
            self.server.sendall(contents)
            if (bytes > 1024):
                bytes -= 1024
                while(bytes != 0):
                    if ((bytes) <= 1024):
                        bytes = 0
                    else: 
                        bytes -= 1024
            
            

        for file in files['DELETE']:
            self.server.sendall(b"delete")
            files['DELETE'].remove(file)
        return "done"

class Handler(FileSystemEventHandler):
    def __init__(self, filing, upload, delete):
        self.filing = filing
        
        self.upload = upload
        self.delete = delete

    def on_any_event(self,event): 
        if event.is_directory:
            return None
        
        
        
        elif event.event_type == 'modified':
        
            path = os.getcwd()
            list_file = os.listdir(path)
            path += "/."
            
            file = event.src_path.split("/")
            for f in file: 
                for filed in list_file:
                    if (f == filed) and not f.endswith("swx") and not f.endswith("swp") :
                        f = f
                        if (f in self.filing['DELETE']) or f in self.filing['UPLOAD']:
                            f = f
                        else:
                            self.upload.put(f)
            Server.uploadQ = self.upload
            
        elif event.event_type == 'created': 
    
            path = os.getcwd()
            list_file = os.listdir(path)
            path += "/."
            
            file = event.src_path.split("/")
            for f in file: 
                
                for filed in list_file:
                    
                    if (f == filed) and not f.endswith("swx") and not f.endswith("swp") or f in self.filing['DOWNLOAD']:
                        self.upload.put(f)
                        
                    else:
                        file = file
            Server.uploadQ = self.upload
        elif event.event_type == 'deleted':
            path = os.getcwd()
            list_file = os.listdir(path)
            path += "/."
        
            filed = event.src_path.split("/")
            for f in filed: 
                if (".") in f :
                    if (f.endswith(".swp")) or (".swp" in f) or ("/" in f) or (path in f) or (f.endswith(".swx") ):
                        break
                    elif f not in os.listdir(path):
                        if f in self.filing['DELETE']:
                            f = f 
                            break
                        elif f in self.filing['UPLOAD']:
                            self.filing['UPLOAD'].remove(f)
                            self.delete.put(f)
                            break
                        else:
                            self.delete.put(f)
                            break
            Server.deleteQ = self.delete
        Server.filing.update(self.filing)
        

        

            
                
def main():
    s = Server(insecure = None, server=None, message=None, prompt="Guest User: ", authBit = 0)
    s.serverConnect()
if __name__ == "__main__":
    main()
