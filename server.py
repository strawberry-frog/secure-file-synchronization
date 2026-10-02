import socket       #Socket for Server and client communication 
import os           #for terminal commands 
import time         #For controlling sleep and server functions 
import multiprocessing   #thread for multiple client connections 
import ssl          #ssl/tls connection for secure communication
import re           #checking fort special characters 
import bcrypt       #Encryption for password 
#import smtplib
#import pyotp
#import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



class Server: 
    #creates the server
    #accepts the client at the insecure state of the client and makes it secure 
    threadClient = {}
    countThread = 0
    dirCa = os.getcwd()
    manager = multiprocessing.Manager()
    clientDB = manager.dict()
    observer = Observer()
    
    recent_action = manager.dict()
    uploadQ = manager.Queue()
    deleteQ = manager.Queue()
    downloadQ = manager.Queue()
    
    #sender_email = "authenticatorserverpro@gmail.com"
    #password = "dick ejgo ragb nfsa" 
    def __init__(self, server, insecure, client, address, thread, local_files, authBit, authUser, email):
        self.server = server
        self.insecure = insecure
        self.client = client
        self.address = address 
        self.thread = thread
        self.local_files = {}
        self.authBit = 0
        self.authUser = 0
        self.email = email
        
# ALL USER LOG IN FUNCTIONS

    #connects to sql cursor         
    def sqlDatabase(self):
        dir = os.getcwd()
        
        saltPass = bcrypt.gensalt()
        passwd = "admin$et561"
        passwd = bcrypt.hashpw(passwd.encode(), saltPass)
        secureQ = "2000" + "Coffee" + "BMW2015"
        saltQ = bcrypt.gensalt()
        hSecure = bcrypt.hashpw(secureQ.encode(), saltQ)
        dir = os.getcwd()
        dir += "/Katherine(Server)/admin"
        Server.clientDB['admin'] = Server.manager.dict({'username': 'admin', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir, 'email': "kthrnbotticelli@gmail.com", 'phone':"+1 7624225765", 'birth': "09-10-99", 'first': "Admin", 'last':"ProjectTest"})
        dir = os.getcwd()
        saltPass = bcrypt.gensalt()
        passwd = "Fish$!NThe3"
        passwd = bcrypt.hashpw(passwd.encode(), saltPass)
        secureQ = "2019" + "Hager" + "HONDA2012"
        saltQ = bcrypt.gensalt()
        hSecure = bcrypt.hashpw(secureQ.encode(), saltQ)
        dir = os.getcwd()
        dir += "/Katherine(Server)/Katherine"
        Server.clientDB['Katherine'] = {'username': 'Katherine', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir, 'email': "kthrnbotticelli@gmail.com", 'phone':"+1 7624225765", 'birth': '06-16-99', 'first': "Katherine", 'last':"Botticelli"}
        #emailContext = ssl.create_default_context()
        #gmailPort = 465
        #smtp_server = "smtp.gmail.com"
        
        #self.email = smtplib.SMTP_SSL(smtp_server, gmailPort, context=emailContext)
        
        
        # Server.clientDB = sqlite3.connect('KatherineSrver.db', autocommit=True)
        
        # Server.clientDB.execute("""CREATE TABLE IF NOT EXISTS USER (username TEXT PRIMARY KEY NOT NULL, passwd TEXT NOT NULL, SaltPasswd TEXT NOT NULL, secureQ TEXT NOT NULL, SaltSecure TEXT NOT NULL, lockedBit INTEGER NOT NULL, FOREIGN KEY (username) REFERENCES directory(username))""")
        #Server.clientDB.execute(''' 
                #CREATE TABLE IF NOT EXISTS directory(
                    #username TEXT NOT NULL,
                    #FILE TEXT 
                #)
            #''')
        self.createServer()
        
    #Creates socket server
    #Binds it to ip address =  0.0.0.0 and port = 5001
    #Listens for clients    
    def createServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket is listening..... ")
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 5001))
        self.server.listen()
        try: 
            upload = multiprocessing.Process(target=self.upload, args=(Server.uploadQ,  ))
            delete = multiprocessing.Process(target=self.delete, args=(Server.deleteQ,  ))
            download = multiprocessing.Process(target=self.download, args=(Server.downloadQ,))
            upload.daemon = True
            upload.start()
            delete.daemon = True
            delete.start()
            download.daemon = True
            download.start()
            event = Handler(Server.recent_action, self.local_files, Server.uploadQ, Server.deleteQ, Server.downloadQ, username=None)
            Server.observer.schedule(event, os.getcwd(), recursive=True)
            Server.observer.start()
            while (True):
                try:
                
                #Server.observer.daemon = True 
                
                    self.insecure, self.address = self.server.accept()
                    Server.countThread += 1
                    try:
                        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                        context.verify_mode = ssl.CERT_REQUIRED 
                        ca = Server.dirCa + "/ca.crt"
                        pem = Server.dirCa + "/server.pem"
                        key = Server.dirCa + "/server.key"
                        context.load_verify_locations(ca)

                        context.load_cert_chain(pem, keyfile=key ,password="cookie")
                        context.verify_flags = context.verify_flags & ~ssl.VERIFY_X509_STRICT
                        self.thread = multiprocessing.Process(target=self.serverAuth, args=(context, ))
                        #self.thread.daemon = True 
                        self.thread.start()
                    
                        #while (True):  
                    except FileNotFoundError as e:
                        print(e)
                        print(os.getcwd())
                        self.insecure.close()
                        time.sleep(3)
                except IOError: 
                    #print("connection error")
                    print("Client '%s' disconnected." % self.insecure)
                    #Out of Server directory
                    #close thread and secure client connect
                    #calls on server to close the insecure connection 
                    for i in Server.threadClient:
                        if (Server.threadClient[i]['client'] == self.insecure):
                            self.server = Server.threadClient.pop(i)
                        #print(server)
                    self.insecure.close()
                    time.sleep (3)
                except ConnectionRefusedError: 
                    #print("Waiting for connection.....")
                    for i in Server.threadClient:
                        if (Server.threadClient[i]['client'] == self.insecure):
                            self.server = Server.threadClient.pop(i)
                        #print(server)
                    self.insecure.close()
                    time.sleep(3)
                except ConnectionResetError:
                    #print("Server lost a client waiting for new connection")
                    #close thread and secure client connect
                    #calls on server to close the insecure connection 
                    for i in Server.threadClient:
                        if (Server.threadClient[i]['client'] == self.client):
                            self.server = Server.threadClient.pop(i)
                        
                
                    self.thread.close()
                    self.thread.join()
                    self.client.close()
                    self.insecure.close()
                    time.sleep(3)
                except KeyboardInterrupt:
                
                    self.authBit = 0 
                    for i in Server.threadClient:
                        if (Server.threadClient[i]['client'] == self.insecure):
                            self.server = Server.threadClient.pop(i)
                        
                            self.thread.close()
                            self.insecure.close()
                            break
                        elif (Server.threadClient[i]['client'] == self.client):
                            self.server = Server.threadClient.pop(i)
                        
                            self.thread.close()
                            self.thread.join()
                            self.client.close()
                            self.insecure.close()
                            break
            
                    break
        except KeyboardInterrupt:
            upload.join()
            delete.join()
            download.join()
            Server.observer.stop()
            Server.observer.join()    
    def serverAuth(self, context):
        #insecure client is not secured client. 
        
        Server.threadClient[Server.countThread] = {'client':self.client, 'username': None, 'loggedIn': 0, 'dir': Server.dirCa, 'needed': Server.recent_action}    
        
        try:
            self.client = context.wrap_socket(self.insecure, server_side=True)
            cert = self.client.getpeercert()
            
            if (cert == None):
                
                self.client.close()
                time.sleep(3)
            elif(cert != None):
                
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        Server.threadClient[i]['client'] = self.client
                self.files = Server.manager.dict()
                try:
                    os.chdir("Katherine(Server)")
                    
                    try: 
                        os.mkdir("admin")
                        os.mkdir("Katherine")
            
                        self.logIn()
                    except FileExistsError:
                        
                        self.logIn()
                except FileNotFoundError:
                    os.mkdir("Katherine(Server)")
                    os.chdir("Katherine(Server)")
                    try: 
                        os.mkdir("admin")
                        os.mkdir("Katherine")
                        self.logIn()
                    except FileExistsError:
                        
                        self.logIn()
        except ConnectionError as e:
            print(e)
            #Out of Server directory
            print("Client '%s' disconnected." % str(self.address))
            #close thread and secure client connect
            #calls on server to close the insecure connection 
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    self.server = Server.threadClient.pop(i)
                    #print(server)
            self.client.close()
            self.insecure.close()
            time.sleep(3)
        except ssl.SSLEOFError:
            print("Client " + str(self.address)+ " disconnected. No Cert")
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    self.server = Server.threadClient.pop(i)
                    #print(server)
            self.client.close()
            self.insecure.close()
            time.sleep(3)

    #Asks user where to create an account or Login
    def logIn(self):
        login = "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n************ WELCOME TO KATHERINE'S SERVER ************\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        self.client.sendall(login.encode())
        self.clientResponse()
        
    #Check for username; 3 tries 
    #Check Password; 3 tries 
    def clientAuth(self):
        tries = 3
        self.client.sendall(b"account")
        self.client.sendall(b"~~~~~~~~~~~~ LOGIN ON KATHERINE'S SERVER ~~~~~~~~~~~~ ")
        while tries != 0:
            self.client.sendall(b"Enter Username: ")
            self.username = self.client.recv(1024).decode()
            if (len(Server.clientDB) == 0):
                find = None
            elif(self.username in Server.clientDB):
                find = Server.clientDB[self.username]
            else:
                find = None
            if (find == None and tries == 1):
                
                self.client.sendall(b"stop")
                self.username = "Guest User" 
                message = "========== USER NOT FOUND ==========\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            elif(find == None): 
                if (tries == 3):
                    message = "========== USERNAME DOES NOT EXIST ==========\n--------- 2 ATTEMPTS LEFT ---------\n"
                else:
                    
                    message = "========== USERNAME DOES NOT EXIST ==========\n--------- 1 ATTEMPT LEFT ---------\n"
                tries -= 1
                self.client.sendall(message.encode())
            elif(find != None):
                lockedBit = find['lockedBit']
                if (lockedBit == 1):
                    
                    if (tries == 3):
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 2 ATTEMPTS LEFT ---------\n"
                    else:
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 1 ATTEMPT LEFT ---------\n"
                    tries -= 1
                    self.client.sendall(message.encode())
                else:
                    tries = 3
                    
                    self.authUser = 1
                    self.authBit = 0
                    pssWd = Server.clientDB[self.username]['passwd']
                    salt = Server.clientDB[self.username]['SaltPass']
                    #Server.clientDB.close()
                    self.client.sendall(b"secure")
                    while tries != 0:
                        self.client.sendall(b"Enter Password: ")
                        #must encrypt password to get answer
                        passwd = self.client.recv(1024)
                        passwd = bcrypt.hashpw(passwd, salt)
                        if ((pssWd != passwd) and (tries == 1)):
                            
                            self.client.sendall(b"stop")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (F)Forgot Password\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                            self.clientResponse()
                        elif(pssWd != passwd):
                            
                            if (tries == 3):
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                            else:
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                            tries -= 1
                            self.client.sendall(message.encode())
                        else: 
                            self.client.sendall(b"stop")
                            #message = "~~~~~~~~~~~~ USER HAS BEEN SENT AUTHENTICATION CODE ON EMAIL ~~~~~~~~~~~~\nEnter code: "
                            #self.client.sendall(message.encode())
                            #email = Server.clientDB[self.username]['email']
                            #secretKey = pyotp.random_base32()
                            #messageUser = pyotp.TOTP(secretKey)
                            #messageUser = messageUser.now()
                            #print(messageUser)
                            #self.email.login(Server.sender_email, Server.password)
                            #self.email.sendmail(Server.sender_email, email, messageUser)
                            #code = self.client.recv(1024).decode()
                            #verifyIn = pyotp.TOTP(secretKey)
                            
                            #if (verifyIn.verify(code)):
                            print(self.username + " Logged in as client: " + str(self.address))
                            self.client.sendall(b"authenticated")
                            
                            os.chdir(self.username)
                            
                            self.authBit = 1
                            for i in Server.threadClient:
                                if (Server.threadClient[i]['client'] == self.client):
                                    Server.threadClient[i]['username'] = self.username
                                    Server.threadClient[i]['loggedIn'] = self.authBit
                                    Server.threadClient[i]['dir'] = os.getcwd()
                            message = self.username 
                            self.client.sendall(message.encode())
                            #Server.recent_action[self.username] = Server.manager.dict()
                            self.welcomeMessage()
                            #else:
                                #self.client.sendall(b"stop")
                                #self.client.sendall(b"========== AUTHENTICATION CODE WRONG LOGIN FAILED ==========\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                                #self.clientResponse()
                        
    #resets user password then asks them to login again or they can exit.
    def forgotPassword(self):
        #check that the user is 
        #connect = sqlite3.connect('KatherineSrver.db')
        #Server.clientDB = connect.cursor()
        #Server.clientDB.execute("BEGIN")
        self.client.sendall(b"account")
        self.client.sendall(b"secure")
        tries = 3
        if (len(Server.clientDB) == 0):
            find = None
        elif(self.username in Server.clientDB):
                find = Server.clientDB[self.username]
        else:
            find = None
        saltQ = find['SaltSecure']
        secureQ = find['secureQ']
        self.client.sendall(b"~~~~~~~~~~~~ RESET PASSWORD ~~~~~~~~~~~~\n======= Security Questions =======\n--------- Case Sensitive ---------\n")
        while tries != 0:
            self.client.sendall(b"What year did you graduate from High School: ")
            message = self.client.recv(1024)
            self.client.sendall(b"What was your mothers maiden name: ")
            message += self.client.recv(1024)
            self.client.sendall(b"What was your first cars' make and year (Example:HONDA2012): ")
            message += self.client.recv(1024)  
            #encyprt message 
            message = bcrypt.hashpw(message, saltQ)
            if (message != secureQ and tries == 1):
                self.username = "Guest User"
                print("Authentication error! No such account exists")
                self.client.sendall(b"stop")
                self.client.sendall(b"stop")
                message = "--------- SECURITY QUESTIONS INVALID ---------\n======= ACCOUNT "+ self.username +" LOCKED ======= \n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: "
                self.client.sendall(message.encode())
                    
                find['lockBit'] = 1
                #Server.clientDB.close()
                self.username = "Guest User"
                self.clientResponse(self)
            elif(message != secureQ): 
                
                if (tries == 3):
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                tries -= 1
                self.client.sendall(message.encode())
            else:
                self.client.sendall(b"stop")
                
                passwd, salt = self.checkPasswd()
                    
                find[self.username]['passwd'] = passwd
                find[self.username]['SaltPass'] = salt
                    
                    #Server.clientDB.close()
                
                #if (self.authBit == 1 and self.authUser == 1):
                    
                    #message = "======= PASSWORD UPDATED =======\nn~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (U)Upload\n         (D)Download\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n" + self.username + ": "
 
                    #self.client.sendall(message.encode())
                    #self.clientResponse()
                #else:
                self.username = "Guest User"
                self.client.sendall(b"======= PASSWORD UPDATED =======\n")
                self.client.sendall(b"stop")
                self.client.sendall(b"~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.clientResponse()
                break
    # checks if password has all critria
    # One lowercase
    # One Uppercase
    # One special Character
    # One number 
    # 8 characters long
    def checkPasswd(self):
        tries = 3
        self.client.sendall(b"secure")
        while tries != 0: 
            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD MUST CONTAIN ~~~~~~~~~~~~~~~~\nONE lowercase letter\nONE uppercase letter\nONE number (0123456789)\nONE special character(~!@#$%^&*()_-+=><[{]}|/?)\n\nEnter Password: ")
            passwd = self.client.recv(1024).decode()
            digit = any(char.isdigit() for char in passwd)
            upper = any(char.isupper() for char in passwd)
            lower = any(char.islower() for char in passwd)
            special = "~!@#$%^&*()_-+=><[{]}|/?"
            spec = False
            for c in passwd:
                for s in special:
                    if (c == s):
                        spec = True
                        
            if(len(passwd) >= 8 and digit and lower and upper and spec):
            
                
                passwd = passwd.encode()
                salt = bcrypt.gensalt()
                passwd = bcrypt.hashpw(passwd, salt)
                tries = 3
                while tries != 0:
                    self.client.sendall(b"Verify Password: ")
                    verPass = self.client.recv(1024).decode()
                    verPass = verPass.encode()
                    verPass = bcrypt.hashpw(verPass, salt)
                    if (verPass != passwd and tries == 1):
                        self.client.sendall(b"stop")
                        
                        self.username = "Guest User"
                        self.client.sendall(b"stop")
                        self.client.sendall(b"--------- PASSWORDS DO NOT MATCH ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: ")
                        self.clientResponse()
                    elif(verPass != passwd):
                        
                        if (tries == 3):
                            message = ("--------- PASSWORDS DO NOT MATCH ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                        else:
                            message = ("--------- PASSWORD DO NOT MATCH ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                        self.client.sendall(message.encode()) 
                    elif(verPass == passwd):
                        
                        if (self.authBit == 1 and self.authUser == 1 ):
        
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            return passwd, salt
                        else:
                            self.client.sendall(b"stop")
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ PASSWORD ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            return passwd, salt
            elif( tries == 1):
                self.client.sendall(b"stop")
                
            
                self.username = "Guest User"
                self.client.sendall(b"--------- PASSWORD IS NOT ADEQUATE ---------\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n          (C)Create Account\n          (F)Forgot Password\n        (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n Guest User: ")
            
                self.clientResponse()
            else:
                if (tries == 3):
                    message = ("--------- PASSWORD IS NOT ADEQUATE ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- PASSWORD IS NOT ADEQUATE ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                tries -= 1
                self.client.sendall(message.encode())      
                
    #create a client account
    def clientCreate(self):
        self.client.sendall(b"account")
        self.client.sendall(b"~~~~~~~~~~~~ CREATE ACCOUNT TO KATHERINE'S SERVER ~~~~~~~~~~~~")
        tries = 3
        find = 0
        while (tries > 0):
            
            self.client.sendall(b"Enter username: ")
            self.username = self.client.recv(1024).decode()
            if (len(Server.clientDB) == 0 ):
                find = 0
            elif(self.username in Server.clientDB):
                find = 1
            if (find != 0 and tries == 1):
                self.client.sendall(b"stop")
                message = "--------- USER NAME MUST BE UNIQUE ---------\n--------- NO ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            elif (find != 0):
                if (tries == 3):
                    message = ("--------- USER NAME MUST BE UNIQUE ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- USER NAME MUST BE UNIQUE ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                self.client.sendall(message.encode())
                tries -= 1
            else: 
                
                break
        #self.client.sendall(b"stop")
        passwd, salt = self.checkPasswd() 
        if (len(passwd) > 0):  
            self.client.sendall(b"======= User Information =======\n")
            self.client.sendall(b"First Name: ")
            first = self.client.recv(1024)
            self.client.sendall(b"Last Name: ")
            last = self.client.recv(1024)
            self.client.sendall(b"Email: ")
            email = self.client.recv(1024)
            self.client.sendall(b"Phone Number: ")
            phoneNum = self.client.recv(1024)
            self.client.sendall(b"Birthday(MM-DD-YYYY): ")
            birth = self.client.recv(1024)
            self.client.sendall(b"======= Security Questions =======\n")
            self.client.sendall(b"--------- Case Sensitive ---------")
            self.client.sendall(b"secure")
            self.client.sendall(b"What year did you graduate from High School: ")
            message = self.client.recv(1024)
            self.client.sendall(b"What was your mothers maiden name: ")
            message += self.client.recv(1024)
            self.client.sendall(b"What was your first cars make and year (Example:HONDA2012): ")
            message += self.client.recv(1024)
            self.client.sendall(b"stop")
            self.client.sendall(b"~~~~~~~~~~~~~~~~~ SECURITY ANSWERS ACCEPTED ~~~~~~~~~~~~~~~~\n")
            secureQ = message
            saltQ = bcrypt.gensalt()
            hSecure = bcrypt.hashpw(secureQ, saltQ)
            try:
                thisDir = os.getcwd()
                os.mkdir(self.username)
                print("Directory create " + self.username)
            
                os.chdir(self.username)
                dirClient = os.getcwd()
                Server.clientDB[self.username] = {'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dirClient, 'email': email, 'phone': phoneNum, 'birth': birth, 'first': first, 'last':last, 'login': datetime.datetime.now()}
                os.chdir("..")
                if(thisDir == os.getcwd()):
                    self.client.sendall(b"stop")
                    message = "~~~~~~~~~~~~ " + self.username +" USER CREATED ON SERVER ~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    self.client.sendall(message.encode())
                    self.username = "Guest User"
                    self.clientResponse()
            except FileExistsError:
                thisDir = os.getcwd()
                os.chdir(self.username)
                dirClient = os.getcwd()
                Server.clientDB[self.username] = {'username': self.username, 'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dirClient, 'email': email, 'phone': phoneNum, 'birth': birth, 'first': first, 'last':last, 'login': datetime.datetime.now()}
                
                if(thisDir == os.getcwd()):
                    self.client.sendall(b"stop")
                    message = "~~~~~~~~~~~~ " + self.username +" USER CREATED ON SERVER ~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                    self.client.sendall(message.encode())
                    self.username = "Guest User"
                    self.clientResponse()
                    

    
            
    def welcomeMessage(self): 
        message ="============= WELCOME " + self.username + " TO "
        message += "\n"
        message += r" _  __     _   _               _            _       ____"
        message += "\n"
        message += r"| |/ /__ _| |_| |__   ___ _ __(_)_ __   ___( )___  / ___|  ___ _ ____   _____ _ __" 
        message += "\n"
        message += r"| ' // _` | __| '_ \ / _ \ '__| | '_ \ / _ \// __| \___ \ / _ \ '__\ \ / / _ \ '__|"
        message += "\n"
        message += r"| . \ (_| | |_| | | |  __/ |  | | | | |  __/ \__ \  ___) |  __/ |   \ V /  __/ |"   
        message += "\n"
        message += r"|_|\_\__,_|\__|_| |_|\___|_|  |_|_| |_|\___| |___/ |____/ \___|_|    \_/ \___|_|"   
        message += "\n\n\n"                                                                                    
        message += "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n"
        self.client.sendall(message.encode())
        time.sleep(3)
        path = os.getcwd
        file_lists = os.listdir()
        count = self.client.recv(1024).decode()
        count = int(count, 2)
        for c in range(count):
            file = self.client.recv(1024).decode()
            size = self.client.recv(1024).decode()
            timing = self.client.recv(1024).decode()
            size = int(size, 2)
            timing = float(timing)
            count = 1
            if len(file_lists) == 0:
                self.client.sendall(b"upload")
            else:
                for filed in file_lists:
                    if file == filed:
                        if size == os.path.getsize(filed):
                            self.client.sendall(b"ignore")
                            break
                        elif size > os.path.getsize(filed):
                            self.client.sendall(b"upload")
                            break
                    elif file != filed and len(file_lists)-1 == count:
                        self.client.sendall(b"upload")
                        break
                    count += 1
        self.clientSynchro()
            
    def clientResponse(self): 
        message = self.client.recv(1024).decode()
        
        # if (self.authUser == 1 and self.authBit == 1): 
        #     if ((message == "D") or (message == "d") or (message == "Download") or (message == "download")):
        #         self.clientDownload()
        #     elif ((message == "U" ) or  (message == "u") or (message == "Upload") or (message == "upload")): 
        #         self.clientUpload()
        #     elif ((message == "R" ) or ( message == "r") or (message == "Read") or (message == "read")): 
        #         self.readFile()
        #     elif ((message == "W" ) or ( message == "w") or (message == "Write") or (message == "write")): 
        #         self.writeInFile() 
        #     elif ((message == "M" ) or ( message == "m") or (message == "Modify") or (message == "modify")): 
        #         self.writeInFile() 
        #     elif ((message == "#" )): 
        #         self.userInfo() 
        #     elif ((message == "$" )): 
        #         self.updateUser() 
        #     elif ((message == "?" )): 
        #         self.serverInfo() 
        #     elif ((message == "%" )): 
        #         self.resetSecureQ() 
        #     elif ((message == "SOS" )): 
        #         self.deleteAcc() 
        #     elif ((message == "F" ) or  (message == "f") or (message == "File") or (message == "file")): 
        #         self.client.sendall(b"start")
        #         self.client.sendall(b"~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
        #         self.clientResponse()
                
        #     elif ((message == "!" ) or  (message == "H") or (message == "h") or (message == "Home") or (message == "home")): 
        #         self.client.sendall(b"start")
        #         self.client.sendall(b"\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #         self.clientResponse()
                
        #     elif ((message == "A" ) or  (message == "a") or (message == "Account") or (message == "account")): 
        #         self.client.sendall(b"start")
        #         self.client.sendall(b"\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           (%)Reset Security Questions\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #         self.clientResponse()
        #     elif ((message == "P" ) or ( message == "p") or (message == "Print") or (message == "print")):
        #         self.client.sendall(b"print") 
        #         files = self.printServerFiles()
        #         self.client.sendall(b"stop") 
        #         if (files == 0):
                    
        #             self.client.sendall(b"============ NO FILES IN SERVER ============\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #         else:
        #             self.client.sendall(b"\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #         self.clientResponse()
        #     elif((message =="*")):
        #         self.logOut()
        #     elif(message == "empty"):
        #         if(len(message) == 0):
        #             self.client.sendall(b"start")
        #             time.sleep(1)
        #             self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #             self.clientResponse()
        #         else:
        #             self.client.sendall(b"start")
        #             time.sleep(1)
        #             self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #             self.clientResponse() 
        #     else:
        #         self.client.sendall(b"start")
        #         time.sleep(1)
        #         self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        #         self.clientResponse() 
        
        if((self.authUser == 0 and self.authBit == 0) or (self.authUser == 1 and self.authBit == 0)):
            if ((message == "L" ) or ( message == "l") or (message == "Login") or (message == "login")): 
                self.clientAuth()
            elif ((message == "C" ) or ( message == "c") or (message == "Create") or (message == "create")): 
                self.clientCreate()
            elif ((message == "F" ) or ( message == "f") or (message == "Forgot") or (message == "forgot")): 
                self.forgotPassword()
            elif ((message == "E") or (message ==  "e") or (message == "Exit") or (message == "exit")):
                self.client.sendall(b"end")
                time.sleep(1)
                #Out of user directory
                message = "========== BYE HOPE YOU HAD FUN ==========\n"
                message += "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n\n~~~~~~~~~~~~~~~~ KATHERINE SERVER CLOSED ~~~~~~~~~~~~~~~~"                                                                                                                   
                self.client.sendall(message.encode()) 
                if (os.getcwd == self.username):
                    os.chdir("..")
                    os.chdir("..")
                    #Out of Server directory
                else:
                    os.chdir("..")
                    print("Client '%s' disconnected." % self.client)
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                self.authBit = 0
                self.authUser = 0
                self.username = "Guest User"
                if(self.client in Server.clientDB):
                    find = Server.clientDB[self.client]
                find.popitem()
                self.client.close()
                self.insecure.close()
                self.thread.join()
                self.clientAuth()
            elif(message == "empty"):
                if(len(message) == 0):
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    self.clientResponse()
                else:
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                    self.clientResponse()
            else:
                self.client.sendall(b"start")
                time.sleep(1)
                self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n           (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.clientResponse()                


    def clientSynchro(self):
        
        filing = Server.manager.dict()
        filing['UPLOAD'] = Server.manager.list()
        filing['DOWNLOAD'] = Server.manager.list()
        filing['DELETE'] = Server.manager.list()
    
                
                    
        #process = multiprocessing.Process(target=self.getFiles, args=(filing, files, ))
        while True:
                message = self.client.recv(1024).decode()
            
                count = 0
                counted = 0
                if (message == "None"):
                    print(self.username + " at " + str(self.address) +  " sends:")
                    print("UPLOAD [] \nDOWNLOAD [] \nDELETE []\n")
                    self.serverSynchro(self.local_files, count)
                elif (message == "count"):
                    count = self.client.recv(1024).decode()
                    counted = self.client.recv(1024).decode()
                    count = int(count, 2)
                    counted = int(counted, 2)
                    for count in range(count):
                        message = self.client.recv(1024).decode()
                        filing['UPLOAD'].append(message)
                    for counted in range(counted):
                        message = self.client.recv(1024).decode()
                        filing['DELETE'].append(message)
                    print(self.username + " at " + str(self.address) + ":")    
                    for outer, value in filing.items():
                        print(outer, value)

                elif(message == "upload"):
                    for pages in filing['UPLOAD']:
                        #print(pages)
                        bytes = self.client.recv(1024).decode()
                        #print(bytes)
                        bytes = int(bytes, 2)
                        filename = open(pages, 'wb')
                        write = self.client.recv(bytes)
                        count = len(write)
                        while (count != bytes):
                            filename.write(write)
                            write = self.client.recv(bytes)
                            count += len(write)
                
                        filename.write(write)
                        filename.close()
                        #Server.recent_action[self.username] = Server.manager.dict({pages: 'UPLOAD'}) 
                        #Server.upload.put(self.address)
                        
                        self.local_files[pages] = 'UPLOAD'
                        filing['UPLOAD'].remove(pages)
                elif(message == "delete"):
                    for pages in filing['DELETE']:
                        try:
                            os.remove(pages)
                            self.local_files[pages] = 'DELETE' 
                            filing['DELETE'].remove(pages)
                        except FileNotFoundError:
                            pages = pages
                            filing['DELETE'].remove(pages)
                    #Server.recent_action[self.username] = {pages: 'DELETE'} 
                        #self.local_files[pages] = 'DELETE' 
                    #Server.delete.put(self.address)
                        
                elif(message == "done"):
                    for outer in self.local_files.items():
                        count += 1
                    done = self.serverSynchro(self.local_files, count)
        
                
    def serverSynchro(self, local_files, count):
        
        temp_dict = {}
        download = []
        delete = []
        upload = []
        temp_dict['UPLOAD'] = []
        temp_dict['DOWNLOAD'] = []
        temp_dict['DELETE'] = []
        # for action, file in Server.recent_action[self.username].items():
        #     print(action, file)
        #     print(file)
        #     counting = 0
        #     print(count)
        #     for item, last_action in local_files.items():
        #         print(last_action, item)
        #         if item == file:
        #             if action == last_action:
        #                 file = file 
        #                 print(file)
                        
        #             elif action == 'UPLOAD' and last_action != action:
        #                 upload.append(item)
        #                 temp_dict['DOWNLOAD'].append(file)
        #                 #download += 1
        #             elif action == 'DOWNLOAD' and last_action != action:
        #                 download.append(item)
        #                 temp_dict['DOWNLOAD'].append(file)
        #                 #download += 1
        #             elif action == 'DELETE' and last_action != action:
        #                 delete.append(item)
        #                 temp_dict['DELETE'].append(file)
        #                 #delete += 1
        #             break
        #         elif item != file and count-1 == counting: 
        #             # local_files[file] = ''
        #             # temp_dict['DOWNLOAD'].append(file)
        #             # download.append(item)
        time.sleep(10)
        dirt = os.getcwd()
        
        path = os.getcwd
        file_lists = os.listdir()
        count = self.client.recv(1024).decode()
        count = int(count, 2)
        for c in range(count):
            file = self.client.recv(1024).decode()
            size = self.client.recv(1024).decode()
            timing = self.client.recv(1024).decode()
            size = int(size, 2)
            timing = float(timing)
            count = 0
            for filed in file_lists:
                if file == filed:
                    if size == os.path.getsize(filed):
                        self.local_files[filed] = 'UPLOAD'
                    elif size < os.path.getsize(filed):
                        self.local_files[filed] = 'downloading'
                elif file != filed and len(file_lists)-1 == count:
                    self.local_files[filed] = 'downloading'
                count += 1
                
                    

        user_files = os.listdir(dirt)
        for user in user_files:
            if os.path.isfile(user):
                if user not in self.local_files:
                    self.local_files[user] = 'downloading'
                    temp_dict['DOWNLOAD'].append(user)
                    download.append(user)

                elif user in self.local_files and self.local_files[user] != 'UPLOAD':
                        self.local_files[user] = 'downloading'
                        temp_dict['DOWNLOAD'].append(user)
                        download.append(user)
                else:
                    for i in self.local_files:
                        if i not in user_files:
                            
                            self.local_files[user] = 'deleting'
                            delete.append(user)
                            temp_dict['DELETE'].append(user)
        down = len(download)
        dele = len(delete)
        downloading = bin(down).encode()
        deleting = bin(dele).encode()
        self.client.sendall(downloading)
        self.client.sendall(deleting)
        
        print(self.username + " at " + str(self.address) + " needs: ")
        for value,file in temp_dict.items():
            print(value, file)
        
        
        
        if delete == 0 and down == 0:
            return "done"
        else: 
            for items in download:
                self.client.sendall(items.encode())
            for items in upload:
                self.client.sendall(items.encode())
        
            for items in delete:
                self.client.sendall(items.encode())
            
            for i in temp_dict['DOWNLOAD']:
                
                bytes = os.path.getsize(i)
                            
                bytes2 = bin(bytes).encode()
                            
                self.client.sendall(bytes2)
                            #Server.timing[file].append(datetime.datetime)
                uploading = open(i, 'rb')
                contents = uploading.read()
            
                uploading.close()
            
                self.client.sendall(contents)
                if (bytes > 1024):
                    bytes -= 1024
                while(bytes != 0):
                    if ((bytes) <= 1024):
                        bytes = 0
                    else: 
                        bytes -= 1024
                self.local_files[i] = 'DOWNLOAD'
                
                temp_dict['DOWNLOAD'].remove(i)
                
            for i in temp_dict['DELETE']:
                self.local_files[i] = 'DELETE'
                temp_dict['DOWNLOAD'].remove(i)
        
        return "done"
                        

            
            
                        
    
    
    
    
        # download = 0
        # delete = 0
        # for outer, value in Server.recent_action[self.username].items():
        #     counting = 0
        #     for file, action in local_files.items():
        #         if(outer == file):
        #             if(value == 'DELETE' and action != value):
        #                 local_files[file] = 'DELETE'
        #                 delete += 1
        #             elif(value == 'DOWNLOAD' and action != value):
        #                 local_files[file] = 'DOWNLOAD'
        #                 download += 1
        #         elif(outer != file and counting == count-1):
        #             local_files[file] = 'DOWNLOAD'
        #             download += 1
        #         counting += 1
        # downloading = bin(download).encode()
        # deleting = bin(delete).encode()
        # self.client.sendall(downloading)
        # self.client.sendall(deleting) 
        
        # if (download > 0):
        #     for file, value in local_files.items():
        #         if value == 'DOWNLOAD':
        #             self.client.sendall(file.encode())
        #             time = self.client.recv(1024).decode()
        #             time = int(time, 2)
        #             if time == 0:
        #                 file = file 
        #             elif time < os.getmtime(file):
        #                 self.client.sendall(b"download")
        #             else:
        #                 self.client.sendall(b"ignore")
        # if(delete > 0):
        #     for file, value in local_files.items():
        #         if value == 'DELETE':
        #             self.client.sendall(file.encode())
        # if(download > 0):
        #     for file, value in local_files.items():
        #         filename = open(file, 'rb')
        #         contents = filename.read()
        #         self.client.sendall(contents)
        #         filename.close()
        #         Server.download.put(self.address)

    def upload(self, upload):
        item = upload.get()
        
        while item:
            if item in Server.clientDB.items():
                if item in Server.recent_action.keys():
                    file = upload.get()
                    Server.recent_action[item].update({file: 'UPLOAD'})
                else:
                    file = upload.get()
                    Server.recent_action[item] = Server.manager.dict({file: 'UPLOAD'})
            item = upload.get()
        #Server.uploadQ = Server.manager.Queue()  
        
    def download(self, download):
        item = download.get()
        
        while item:
            if item in Server.clientDB.items():
                if item in Server.recent_action.keys():
                    file = download.get()
                    Server.recent_action[item].update({file: 'UPLOAD'})
                else:
                    file = download.get()
                    Server.recent_action[item] = Server.manager.dict({file: 'UPLOAD'})
            item = download.get()
        #Server.downloadQ = Server.manager.Queue() 
    def delete(self, delete):
        item = delete.get()
        
        while item:
            if item in Server.clientDB.items():
                if item in Server.recent_action.keys():
                    file = delete.get()
                
                    Server.recent_action[item].update({file: 'DELETE'})
                else:
                    file = delete.get()
                    Server.recent_action[item] = Server.manager.dict({file: 'DELETE'})
            item = delete.get()
        #Server.deleteQ = Server.manager.Queue()        
class Handler(FileSystemEventHandler):
        def __init__(self, action, local, upload, delete, download, username):
            self.action = action
            self.local = local
            self.upload = upload
            self.delete = delete 
            self.download = download
            self.username = username 
            
        def on_any_event(self,event): 
            if event.is_directory:
                return None
        
        
        
            elif event.event_type == 'modified':
        
                path = os.getcwd()
                list_file = os.listdir(path)
                path += "/."
            
                file = event.src_path.split("/")
                for f in file:
                    if f in Server.recent_action.keys():
                        self.username = f
                        
                    for filed in list_file:
                        if os.path.isfile(filed): 
                            if (f == filed) and not f.endswith("swx") and not f.endswith("swp") :
                            
                                if Server.recent_action[self.username][f] == 'UPLOAD':
                                    #Server.recent_action[self.username][f] = 'DOWNLOAD'
                                    #print("file is modified" + f)
                                    self.download.put(self.username)
                                    self.download.put(f)
                Server.downloadQ = self.download
            
            elif event.event_type == 'created': 
    
                path = os.getcwd()
                list_file = os.listdir(path)
            
            
                file = event.src_path.split("/")
                for f in file: 
                    if f in Server.recent_action.keys():
                        self.username = f
                        
                    for filed in list_file:
                        if os.path.isfile(filed):
                            if (f == filed) and not f.endswith("swx") and not f.endswith("swp") :
                                if Server.recent_action[self.username][f] == 'DOWNLOAD':
                                #Server.recent_action[self.username] = Server.manager.dict({f:'UPLOAD'})
                                    self.upload.put(self.username)
                                    self.upload.put(f)
                                #print("file is created" + f)
                Server.uploadQ = self.upload
            elif event.event_type == 'deleted':
                path = os.getcwd()
                list_file = os.listdir(path)
                path += "/."
        
                filed = event.src_path.split("/")
                for f in filed: 
                    if f in Server.recent_action.keys():
                        self.username = f
                        
                    elif (".") in f :
                        if (f.endswith(".swp")) or (".swp" in f) or ("/" in f) or (path in f) or (f.endswith(".swx")):
                            break
                        elif f not in os.listdir(path):
                            self.delete.put(self.username)
                            self.delete.put(f)
                            #print("file is deleted" + f)
                            break
                        
                Server.deleteQ = self.delete
        Server.recent_action.update(Server.recent_action)
    
                
        

            
def main(): 
    s = Server(server=None, insecure = None, client=None, address=None, thread=None, local_files={}, authBit = 0, authUser = 0, email=None)
    s.sqlDatabase()
if __name__ == "__main__":
    main()
