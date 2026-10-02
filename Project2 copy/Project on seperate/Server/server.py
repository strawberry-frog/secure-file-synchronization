import socket       #Socket for Server and client communication 
import os           #for terminal commands 
import time         #For controlling sleep and server functions 
import multiprocessing   #thread for multiple client connections 
import ssl          #ssl/tls connection for secure communication
import re           #checking fort special characters 
import bcrypt       #Encryption for password 
import smtplib
import pyotp
import datetime

class Server: 
    #creates the server
    #accepts the client at the insecure state of the client and makes it secure 
    threadClient = {}
    countThread = 0
    dirCa = os.getcwd()
    manager = multiprocessing.Manager()
    clientDB = manager.dict()
    sender_email = "authenticatorserverpro@gmail.com"
    password = "dick ejgo ragb nfsa" 
    def __init__(self, server, insecure, client, address, thread, files, authBit, authUser, email):
        self.server = server
        self.insecure = insecure
        self.client = client
        self.address = address 
        self.thread = thread
        self.files = files
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
        Server.clientDB['admin'] = Server.manager.dict({'username': 'admin', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir, 'email': "kthrnbotticelli@gmail.com", 'phone':"+1 7624225765", 'birth': "09-10-99", 'first': "Admin", 'last':"ProjectTest", 'login': datetime.datetime.now()})
        dir = os.getcwd()
        saltPass = bcrypt.gensalt()
        passwd = "Fish$!NThe3"
        passwd = bcrypt.hashpw(passwd.encode(), saltPass)
        secureQ = "2019" + "Hager" + "HONDA2012"
        saltQ = bcrypt.gensalt()
        hSecure = bcrypt.hashpw(secureQ.encode(), saltQ)
        dir = os.getcwd()
        dir += "/Katherine(Server)/Katherine"
        Server.clientDB['Katherine'] = {'username': 'Katherine', 'passwd': passwd, 'SaltPass': saltPass, 'secureQ': hSecure, 'SaltSecure': saltQ, 'lockedBit': 0, 'dirClient': dir, 'email': "kthrnbotticelli@gmail.com", 'phone':"+1 7624225765", 'birth': '06-16-99', 'first': "Katherine", 'last':"Botticelli", 'login': datetime.datetime.now()}
        emailContext = ssl.create_default_context()
        gmailPort = 465
        smtp_server = "smtp.gmail.com"
        
        self.email = smtplib.SMTP_SSL(smtp_server, gmailPort, context=emailContext)
        
        
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
        print("Socket was created")
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', 5001))
        self.server.listen()
        while (True):
            try:
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
                    self.thread = multiprocessing.Process(target=self.serverAuth, args=(context, )).start()
                    #while (True):  
                except FileNotFoundError as e:
                    print(e)
                    print(os.getcwd())
                    self.insecure.close()
                    time.sleep(3)
            except IOError: 
                print("connection error")
                print("Client '%s' disconnected." % self.insecure)
                #Out of Server directory
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep (3)
            except ConnectionRefusedError: 
                print("Waiting for connection.....")
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep(3)
            except ConnectionResetError:
                print("Server lost a client waiting for new connection")
                #close thread and secure client connect
                #calls on server to close the insecure connection 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                self.insecure.close()
                time.sleep(3)
            except KeyboardInterrupt:
                print("Server closed")
                self.authBit = 0 
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        server = Server.threadClient.pop(i)
                        print(server)
                        self.insecure.close()
                        break
                    elif (Server.threadClient[i]['client'] == self.client):
                        server = Server.threadClient.pop(i)
                        print(server)
                        self.client.close()
                        break
                break
    
    def serverAuth(self, context):
        #insecure client is not secured client. 
        
        Server.threadClient[Server.countThread] = {'client':self.client, 'username': None, 'loggedIn': 0, 'dir': Server.dirCa}    
        print(self.thread) 
        print(os.getppid())  
        try:
            self.client = context.wrap_socket(self.insecure, server_side=True)
            cert = self.client.getpeercert()
            
            if (cert == None):
                print("Connection Failed. No Cert")
                self.client.close()
                time.sleep(3)
            elif(cert != None):
                print("Certificate Verified!")
                for i in Server.threadClient:
                    if (Server.threadClient[i]['client'] == self.insecure):
                        Server.threadClient[i]['client'] = self.client
                self.files = Server.manager.dict()
                try:
                    os.chdir("Katherine(Server)")
                    print("Inside Katherine(Server) directory!")
                    try: 
                        os.mkdir("admin")
                        os.mkdir("Katherine")
                        print("Admin user has be created!")
                        print("Katherine user has be created!")
                    except FileExistsError:
                        print("Admin user has already been created!")
                        os.chdir("admin")
                        fileList = os.listdir(os.getcwd())
                        for file in fileList:
                            if(os.path.isfile(file)):
                                timeMod = os.path.getmtime(file)
                                
                                self.files[file] = Server.manager.dict({'LastMod': timeMod, 'Write': 0, 'Read': 0, 'username': 'admin'})
                        os.chdir("..")
                        print("Katherine user has already been created!")
                        os.chdir("Katherine")
                        fileList = os.listdir(os.getcwd())
                        for file in fileList:
                            if(os.path.isfile(file)):
                                timeMod = os.path.getmtime(file)
                                self.files[file] = Server.manager.dict({'LastMod': timeMod, 'Write': 0, 'Read': 0, 'username': 'Katherine'})
                        os.chdir("..")
                    self.logIn()
                except FileNotFoundError:
                    print("New user added")
                    try: 
                        os.mkdir("admin")
                        print("Admin user has be created!")
                    except FileExistsError:
                        print("Admin user has already be created!")
                    self.logIn()
        except ConnectionError as e:
            print(e)
            print("server is not secure")
            print("connection error")
            #Out of Server directory
            print("Client '%s' disconnected." % self.client)
            #close thread and secure client connect
            #calls on server to close the insecure connection 
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    server = Server.threadClient.pop(i)
                    print(server)
            self.client.close()
            time.sleep(3)
        except ssl.SSLEOFError:
            print("Client disconnected. No Cert")
            self.authBit = 0
            self.authUser = 0
            for i in Server.threadClient:
                if (Server.threadClient[i]['client'] == self.client):
                    server = Server.threadClient.pop(i)
                    print(server)
            self.client.close()
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
                print("Authentication error! No such user exists")
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
                    print("Account Locked!")
                    if (tries == 3):
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 2 ATTEMPTS LEFT ---------\n"
                    else:
                        message = "========== USERNAME PERMISSION DENIED ==========\n--------- 1 ATTEMPT LEFT ---------\n"
                    tries -= 1
                    self.client.sendall(message.encode())
                else:
                    tries = 3
                    print("Username found!!")
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
                            print("Authentication error! No such user exists")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (F)Forgot Password\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                            self.clientResponse()
                        elif(pssWd != passwd):
                            print("Password incorrect!")
                            if (tries == 3):
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                            else:
                                message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                            tries -= 1
                            self.client.sendall(message.encode())
                        else: 
                            self.client.sendall(b"stop")
                            message = "~~~~~~~~~~~~ USER HAS BEEN SENT AUTHENTICATION CODE ON EMAIL ~~~~~~~~~~~~\nEnter code: "
                            self.client.sendall(message.encode())
                            email = Server.clientDB[self.username]['email']
                            secretKey = pyotp.random_base32()
                            messageUser = pyotp.TOTP(secretKey)
                            messageUser = messageUser.now()
                            print(messageUser)
                            self.email.login(Server.sender_email, Server.password)
                            self.email.sendmail(Server.sender_email, email, messageUser)
                            code = self.client.recv(1024).decode()
                            verifyIn = pyotp.TOTP(secretKey)
                            
                            if (verifyIn.verify(code)):
                                print("User is authenticated!!")
                                self.client.sendall(b"authenticated")
                                Server.clientDB[self.username]['login'] = datetime.datetime.now()
                                os.chdir(self.username)
                                print(os.getcwd())
                                self.authBit = 1
                                for i in Server.threadClient:
                                    if (Server.threadClient[i]['client'] == self.client):
                                        Server.threadClient[i]['username'] = self.username
                                        Server.threadClient[i]['loggedIn'] = self.authBit
                                        Server.threadClient[i]['dir'] = os.getcwd()
                                message = self.username + ": "
                                self.client.sendall(message.encode())
                                self.welcomeMessage()
                            else:
                                self.client.sendall(b"stop")
                                self.client.sendall(b"========== AUTHENTICATION CODE WRONG LOGIN FAILED ==========\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                                self.clientResponse()
                        
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
                print("Authentication error! No such account exists")
                if (tries == 3):
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                else:
                    message = ("--------- SECURITY QUESTIONS INVALID ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                tries -= 1
                self.client.sendall(message.encode())
            else:
                self.client.sendall(b"stop")
                print("Security questions passed!!")
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
            
                print("Password accepted!")
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
                        print("Password DO NOT match!")
                        if (tries == 3):
                            message = ("--------- PASSWORDS DO NOT MATCH ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                        else:
                            message = ("--------- PASSWORD DO NOT MATCH ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                        self.client.sendall(message.encode()) 
                    elif(verPass == passwd):
                        print("Password is verified.")
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
                print("Username is unique and accepted!")
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
                print("New user directory made!")
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
                fileList = os.listdir(os.getcwd())
                fileList = os.listdir(os.getcwd())
                for file in fileList:
                    if(os.path.isfile(file)):
                        timeMod = os.path.getmtime(file)
                        self.files[file] = Server.manager.dict({'LastMod': timeMod, 'Write': 0, 'Read': 0, 'username': self.username})
                os.chdir("..")
                print(thisDir)
                print(os.getcwd())
                print("Server has this user saved")
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
        message += "  _          _          _          _          _\n>(')____,  >(')____,  >(')____,  >(')____,  >(') ___,\n  (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/'\n  ~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~ artist: jgs\n\n\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                                                                                                                   
        self.client.sendall(message.encode())
        time.sleep(3)
        self.clientResponse()        
            
    def clientResponse(self): 
        message = self.client.recv(1024).decode()
        print(message)
    
        if (self.authUser == 1 and self.authBit == 1): 
            if ((message == "D") or (message == "d") or (message == "Download") or (message == "download")):
                self.clientDownload()
            elif ((message == "U" ) or  (message == "u") or (message == "Upload") or (message == "upload")): 
                self.clientUpload()
            elif ((message == "R" ) or ( message == "r") or (message == "Read") or (message == "read")): 
                self.readFile()
            elif ((message == "W" ) or ( message == "w") or (message == "Write") or (message == "write")): 
                self.writeInFile() 
            elif ((message == "M" ) or ( message == "m") or (message == "Modify") or (message == "modify")): 
                self.writeInFile() 
            elif ((message == "#" )): 
                self.userInfo() 
            elif ((message == "$" )): 
                self.updateUser() 
            elif ((message == "?" )): 
                self.serverInfo() 
            elif ((message == "%" )): 
                self.resetSecureQ() 
            elif ((message == "SOS" )): 
                self.deleteAcc() 
            elif ((message == "F" ) or  (message == "f") or (message == "File") or (message == "file")): 
                self.client.sendall(b"start")
                self.client.sendall(b"~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                self.clientResponse()
                
            elif ((message == "!" ) or  (message == "H") or (message == "h") or (message == "Home") or (message == "home")): 
                self.client.sendall(b"start")
                self.client.sendall(b"\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                self.clientResponse()
                
            elif ((message == "A" ) or  (message == "a") or (message == "Account") or (message == "account")): 
                self.client.sendall(b"start")
                self.client.sendall(b"\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           ($)Update User Information\n           (?)How to Use Server\n           (%)Reset Security Questions\n           (SOS)Delete Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                self.clientResponse()
            elif ((message == "P" ) or ( message == "p") or (message == "Print") or (message == "print")):
                self.client.sendall(b"print") 
                files = self.printServerFiles()
                self.client.sendall(b"stop") 
                if (files == 0):
                    
                    self.client.sendall(b"============ NO FILES IN SERVER ============\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                else:
                    self.client.sendall(b"\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                self.clientResponse()
            elif((message =="*")):
                self.logOut()
            elif(message == "empty"):
                if(len(message) == 0):
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                    self.clientResponse()
                else:
                    self.client.sendall(b"start")
                    time.sleep(1)
                    self.client.sendall(b"======= NOT AN OPTION =======\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                    self.clientResponse() 
        
        elif((self.authUser == 0 and self.authBit == 0) or (self.authUser == 1 and self.authBit == 0)):
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
                
            
    #logOut the user
    #They will then be asked if they would like to:
    #Login
    #Create Account
    #Exit
    def logOut(self):
        self.authUser = 0
        os.chdir("..")
        self.authBit = 0
        self.client.sendall(b"logout")
        for i in Server.threadClient:
            if (Server.threadClient[i]['username'] == self.username):
                Server.threadClient[i]['username'] = None
                Server.threadClient[i]['loggedIn'] = self.authBit
                Server.threadClient[i]['dir'] = os.getcwd()
        self.username = "Guest User"
        message = "======= "+ self.username+" Logged Out =======\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n           (C)Create Account\n           (L)Login\n           (E)Exit\n~~~~~~~~~~~~~~~~"
        self.client.sendall(message.encode())
        self.clientResponse()
        
        
# ALL FILE HANDLING FUNCTIONS

    #Prints out files for the client to choose from for Downloading.
    def printServerFiles(self):
        dir = os.getcwd()
        fileList = os.listdir(dir)
        count = 0 
        message = "======= PRINTING FILES ON " + self.username+ " SERVER =======\n"
        self.client.sendall(message.encode())
        for file in fileList:
            if (os.path.isfile(file)):
                fileName = file.encode()
                size = len(fileName)
                self.client.sendall(bin(size).encode())
                time.sleep(1)
                if(file in self.files):
                    mod = self.files[file]['LastMod']
                    mod = str(mod)
                self.client.sendall(fileName)
                self.client.sendall(b"time")
                self.client.sendall(mod.encode())
                print(fileName)
                count += 1
            else: 
                count = count
        return count   
    
    #Finds the on the machine to make sure it exists.
    #Downloading file function        
    def findFile(self, fileName):
        if (os.path.exists(fileName)):
            print("File found!")
            return True
        else:
            return False

    #Checks to make sure File is specifically a file on the Server.     
    def fileOnServer(self, fileName, fileList):
        if (self.findFile(fileName)):
            for file in fileList:
                if ((fileName == file) and (os.path.isfile(file))):
                    print("File in user Directory, User may download!")
                    return True
        else:
            return False
            
    #Client Downloads file.
    #Will print all files on the Server
    #Ask client which file they would like.
    #Checks that file is an option
    #Sends the client the file.            
    def clientDownload(self):
        dir = os.getcwd()
        print(dir)
        self.client.sendall(b"Downloading")
        time.sleep(1)
        print("Listing out files in '% s'" % dir)   
        fileList = os.listdir(dir)
        if(self.printServerFiles() == 0):
            message = "--------- FAILED: NO FILES ON "+self.username+" ACCOUNT ---------\n        (TRY TO UPLOAD FILES TO CLOUD)\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(b"NOFile")
            time.sleep(1)
            self.client.sendall(message.encode())
            self.clientResponse()
        else: 
            print("Stop printing cloud files.")
            self.client.sendall(b"stop")
            time.sleep(1)
            self.client.sendall(b"~~~~~~~~~~~~~~~~ WHAT FILE WOULD YOU LIKE TO DOWNLOAD? ~~~~~~~~~~~~~~~~\n")
            time.sleep(2)
            fileName = self.client.recv(100).decode()
            print(fileName)
            if (self.fileOnServer(fileName, fileList) == True):
                self.writeFile(fileName)
            else:
                self.client.sendall(b"start")
                time.sleep(1)
                message = "--------- FAILED: FILE "+ fileName +" NOT ON SERVER ---------\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
                
    #Client has chosen file to download from server 
    #This method checks that this file can be opened 
    #Then sends the size and the contents of the file to client
    #Checks that the client has received all the content of the file.            
    def writeFile(self, fileName):
        try:
            file = open(fileName, 'rb')
            time.sleep(1)
            self.client.sendall(fileName.encode())
            time.sleep(3)
            message = file.read()
            print("Downloading .........")
            allSent = os.path.getsize(fileName)
            allSent = bin(allSent).encode()
            self.client.sendall(allSent)
            time.sleep(1)
            print("File is '% s' " % allSent)
            self.client.sendall(message)
            file.close()
            print("User has received all data.")
            allSent = os.path.getsize(fileName)
            binaryTest = bin(allSent)
            response = self.client.recv(1024).decode()
            print(response, binaryTest)
            if (response == binaryTest):
                print("File Downloaded")
                message = "~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" +" SUCCESS: FILE "+ fileName +" DOWNLOADED " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~ \n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()         
            else: 
                print("File Not Complete!!")
                self.client.sendall(b"start")
                time.sleep(1)
                message = "--------- FAILED: FILE "+ fileName +" INCOMPLETE DOWNLOAD ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
        except IOError:
            print("I can't read " + fileName)
            self.client.sendall(b"start")
            time.sleep(1)
            message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE OPENED ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(message.encode())
            self.clientResponse()
        
    #Client would like to upload a file onto server
    #Asks client for file they would like to Upload 
    #(Most of this process takes place on client)
    #Server then creates a file with that name and writes all received data from client into file.             
    def clientUpload(self):
        dir = Server.clientDB[self.username]['dirClient']
        if (os.getcwd() != dir):
            os.chdir(dir)
        self.client.sendall(b"uploading")
        time.sleep(1)
        message = "~~~~~~~~~~~~~~~~ UPLOAD FILE TO "+ self.username+" SERVER ~~~~~~~~~~~~~~~~\nWhat file would you like to upload?"
        self.client.sendall(message.encode())
        fileName = self.client.recv(200).decode()
        if (fileName == "failed"):
            self.client.sendall(b"\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            self.clientResponse()
        else: 
            print("Client will upload " + fileName)
            if (os.path.exists(fileName)):
                print("File already on Server.\nWill over write the original file.")
                timeMod = os.path.getmtime(fileName)
                os.remove(fileName)
                if(fileName in self.files):
                    self.files[fileName]['LastMod'] = timeMod
            try: 
                file = open(fileName, 'wb')
                fileSize = self.client.recv(50).decode()
                bytes = int(fileSize, 2)
                time.sleep(1)
                #Need to account for large files and break them apart in a logical manner.          
                print(fileName + " is '%s' in size" % bytes)
                write = self.client.recv(bytes)
                count = len(write)
                while (count != bytes):
                    
                    file.write(write)
                    write = self.server.recv(bytes)
                    count += len(write)
                file.write(write)
                file.close()
                full = os.path.getsize(fileName)
                if (full == bytes):
                    if(fileName in self.files):
                        message = "~~~~~~~~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" +" SUCCESS: FILE "+ fileName +" UPDATED TO CLOUD " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~~~~~~~~"
                        print("File has been Updated")
                    else:
                        print("File has been Uploaded")
                        message = "~~~~~~~~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" +" SUCCESS: FILE "+ fileName +" UPLOADED TO CLOUD " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~~~~~~~~"
                    message += "\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    self.client.sendall(message.encode())
                    timeMod = os.path.getmtime(fileName)
                    self.files[fileName] = {'LastMod': timeMod, 'Write': 0, 'Read': 0}
                    self.clientResponse()
                else: 
                    print("Upload failed only '%s' bytes downloaded" % full)
                    if(fileName in self.files):
                        print("Not uploaded not updated")
                        uploadFail = "--------- FAILED: FILE "+ fileName +" CAN NOT UPLOADED DID NOT UPDATE ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                        self.client.sendall(uploadFail.encode())
                        self.clientResponse()
                    else:
                        os.remove(fileName)
                        uploadFail = "--------- FAILED: FILE "+ fileName +" CAN NOT UPLOADED ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                        self.client.sendall(uploadFail.encode())
                        self.clientResponse()
            except IOError:
                print("I can't open " + fileName) 
                message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE OPENED ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            
            
    def readFile(self):
        dir = os.getcwd()
        print(dir)
        self.client.sendall(b"read")
        time.sleep(1)
        print("Listing out files in '% s'" % dir)   
        fileList = os.listdir(dir)
        files = self.printServerFiles()
        if (files == 0):
            self.client.sendall(b"NOFile")
            message = "!!!!!!!!!! NO FILES TO READ ON " +  self.username + " ACCOUNT !!!!!!!!!!"
            message += "\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            self.client.sendall(message.encode())
            self.clientResponse()
        else: 
            self.client.sendall(b"stop")
            self.client.sendall(b"~~~~~~~~~~~~~~~~ WHAT FILE WOULD YOU LIKE TO READ? ~~~~~~~~~~~~~~~~\n")
            fileName = self.client.recv(1000).decode()
            here = self.fileOnServer(fileName, fileList)
            if(here == False):
                self.client.sendall(b"stop")
                message = "--------- FILE " + fileName + " IS NOT ACCESSIBLE TO " + self.username + " ---------"
                message += "\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                self.client.sendall(message.encode())
                self.clientResponse()
            else:
                message = "--------- FILE " + fileName + " CAN BE READ BY " + self.username + " ---------"
                self.client.sendall(message.encode())
                if((fileName in self.files) and (self.files[fileName]['Read'] == 1)):
                    self.client.sendall(b"stop")
                    message = "--------- FILE " + fileName + " IS NOT ACCESSIBLE TO " + self.username + " ---------"
                    message += "\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    self.client.sendall(message.encode())
                    self.clientResponse()
                else: 
                    if(fileName in self.files):
                            find = self.files[fileName]
                            find['Read'] = 1
                            find['Write'] = 1
                    try:
                        file = open(fileName, 'r')
                        time.sleep(1)
                        self.client.sendall(fileName.encode())
                        time.sleep(3)
                        allSent = os.path.getsize(fileName)
                        allSent = bin(allSent).encode()
                        self.client.sendall(allSent)
                        time.sleep(1)
                        print("File is '% s' " % allSent)
                        try:
                            read = file.read()
                        except UnicodeDecodeError:
                            self.client.sendall(b"stop")
                            message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE READ ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            self.client.sendall(message.encode())
                            self.files[fileName]['Read'] = 0
                            self.files[fileName]['Write'] = 0
                            self.clientResponse()
                        self.client.sendall(read.encode())            #file data.
                        file.close()
                        print("User has received all data.")
                        allSent = os.path.getsize(fileName)
                        binaryTest = bin(allSent)
                        response = self.client.recv(1024).decode()
                        print(response, binaryTest)
                        if (response == binaryTest):
                            print("File Downloaded")
                            message = self.client.recv(1024).decode()
                            while (message != "read"):
                                message = self.client.recv(1024).decode()
                            if (message == "read"):
                                message = "--------- FILE "+ fileName +" IS CLOSED ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                self.client.sendall(message.encode())
                                self.files[fileName]['Read'] = 0
                                self.files[fileName]['Write'] = 0
                                self.clientResponse()
                        else: 
                            print("File Not Complete!!")
                            time.sleep(1)
                            message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE READ ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            self.client.sendall(message.encode())
                            self.files[fileName]['Read'] = 0
                            self.files[fileName]['Write'] = 0
                            self.clientResponse()
                    except IOError:
                        print("I can't read " + fileName)
                        self.client.sendall(b"stop")
                        time.sleep(1)
                        message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE READ ---------\n\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                        self.client.sendall(message.encode())
                        self.files[fileName]['Read'] = 0
                        self.files[fileName]['Write'] = 0
                        self.clientResponse()

                        
    def writeInFile(self):
        dir = os.getcwd()
        print(dir)
        self.client.sendall(b"write")
        time.sleep(1)
        print("Listing out files in '% s'" % dir)   
        fileList = os.listdir(dir)
        count = 0
        while(count == 0):
            files = self.printServerFiles()
            if (files == 0):
                self.client.sendall(b"NOFile")
                message = "!!!!!!!!!! NO FILES TO MODIFY IN " +  self.username + " ACCOUNT !!!!!!!!!!"
                count = 1
            else: 
                self.client.sendall(b"stop")
                self.client.sendall(b"~~~~~~~~~~~~~~~~ WHAT FILE WOULD YOU LIKE TO MODIFY? ~~~~~~~~~~~~~~~~\n")
                fileName = self.client.recv(1000).decode()
                here = self.fileOnServer(fileName, fileList)
                if(here == True):
                    message = "--------- FILE " + fileName + " CAN BE MODIFIED BY " + self.username + " ---------\n"
                    if(fileName in self.files):
                            find = self.files[fileName]
                            find['Write'] = 1
                            try:
                                file = open(fileName, "r")
                            
                                
                                fileW = open("writeable", "w")
                                print("Temporary file Created!")
                                lines = []
                                noNum = []
                                while True:
                                    try:
                                        lineRead = file.readline()
                                        if not lineRead:
                                            break
                                        lines.append(lineRead)
                                        noNum.append(lineRead)
                                    except UnicodeDecodeError:
                                        message = "--------- FILE " + fileName + " IS NOT ACCESSIBLE TO " + self.username + " ---------\n"
                                        self.client.sendall(b"stop")
                                        message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                        self.client.sendall(message.encode())
                                        self.clientResponse()
                                        break
                                self.client.sendall(b"file")           
                                for i in range(len(lines)):
                                    
                                    fileW.write("Line:{} {}".format(i, lines[i]))
                                file.close()
                                fileW.close()
                                allSent = os.path.getsize(fileName)
                                allSent = bin(allSent).encode()
                                self.client.sendall(allSent)
                                
                                time.sleep(1)
                                amount = str(len(lines)).encode()
                                self.client.sendall(amount)
                                
                                fileW = open("writeable", 'r')
                                message = fileW.read()
                                fileW.close()
                                message += "\n"
                                self.client.sendall(message.encode())
                                
                                os.remove("writeable")
                                print("Temporary file deleted!")
                                response = self.client.recv(1024).decode()
                                time.sleep(2)
                                print("The users amount " + response + " the servers amount " +  allSent.decode())
                                if (response == allSent.decode()):
                                    message = "\n~~~~~~~~~~~~~~~~ WHAT LINES WOULD YOU LIKE TO MODIFY? ~~~~~~~~~~~~~~~~\n\n--------- INPUTS MUST BE NUMBERS 0 - NUMBER OF LINES IN FILE ---------\n\n=========== IF INPUT IS MORE THEN LINES IN FILE LINES WILL BE ADDED TO END OF FILE ===========\n"
                                    self.client.sendall(message.encode())
                                    line = self.client.recv(1024).decode()
                                    line = int(line)
                                    if(line <= len(noNum)-1):
                                        print("Line exists can modify")
                                        space = ""
                                        for char in lines[line]:
                                            if (char == " "):
                                                space += " "
                                            else: 
                                                break
                                        message = "~~~~~~~~~~~~~~~~ WHAT WOULD YOU LIKE TO MODIFY YOUR LINE TO? ~~~~~~~~~~~~~~~~\n\n=========== MAKE SURE YOUR INPUT IS EXACT TO THE INPUT INTO THE FILE ===========\n"

                                    elif(line >= len(noNum)):
                                        i = len(noNum) -1
                                        for i in range(line):
                                            if (i == line):
                                                noNum.append(" ")
                                                break
                                            else:
                                                noNum.append(" ")
                                                i += 1
                                        space = ""
                                        message = "~~~~~~~~~~~~~~~~ WHAT WOULD YOU LIKE TO ADD TO THE FILE? ~~~~~~~~~~~~~~~~\n\n=========== MAKE SURE YOUR INPUT IS EXACT TO THE INPUT INTO THE FILE ===========\n"

                                    self.client.sendall(message.encode())
                                    modify = self.client.recv(6000).decode()
                                    noNum[line] = space + modify + "\n"
                                    file = open(fileName, "w")
                                    file.writelines(noNum)
                                    file.close
                                        
                                    message = "~~~~~~~~~~~~~~~~ THIS IS YOUR MODIFIED " + fileName +" ~~~~~~~~~~~~~~~~\n"
                                    file = open(fileName, "r")
                                    message += file.read()          #file data.
                                    file.close()
                                    message += "\n"
                                    message += "\n--------- FILE "+ fileName +" IS CLOSED ---------\n"
                                    timeMod = os.path.getmtime(fileName)
                                    self.files[fileName]['LastMod'] = timeMod
                                    message += "~~~~~~~~~~~~~~~~ WOULD YOU LIKE TO MODIFY ANYTHING ELSE? ~~~~~~~~~~~~~~~~\n\n=========== (Yes or NO) ===========\n"
                                    self.client.sendall(message.encode())
                                    modify = self.client.recv(1024).decode().strip()
                                    if (modify == "yes" or modify == "Yes" or modify == "Y" or modify =="y" or modify ==" "):
                                        count = 0
                                        self.client.sendall(b"start")
                                    else:
                                        find['Write'] = 0
                                        message = "~~~~~~~~~~~~~~~~ MODIFICATION OF FILES IS DONE ~~~~~~~~~~~~~~~~\n"
                                        count = 1
                                        self.client.sendall(b"stop")
                                        message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                        self.client.sendall(message.encode())
                                        self.clientResponse()
                                else: 
                                    print("File Not Complete!!")
                                    find['Write'] = 0
                                    count = 1
                                    time.sleep(1)
                                    message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE READ THEREFORE NOT ABLE TO BE MODIFIED ---------\n"
                                    self.client.sendall(b"stop")
                                    message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                    self.client.sendall(message.encode())
                                    self.clientResponse()
                                
                            except IOError:
                                print("I can't read " + fileName)
                                count = 1
                                time.sleep(1)
                                message = "--------- FAILED: FILE "+ fileName +" CAN NOT BE MODIFIED NON READABLE FILE ---------\n"
                                find['Write'] = 0
                                self.client.sendall(b"stop")
                                message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                                self.client.sendall(message.encode())
                                self.clientResponse()
                            
                    else:
                        message = "--------- FILE " + fileName + " IS NOT ACCESSIBLE TO " + self.username + " ---------\n"
                        count = 1
                        self.client.sendall(b"stop")
                        message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                        self.client.sendall(message.encode())
                        self.clientResponse()
                else:
                    message = "--------- FILE " + fileName + " IS NOT ACCESSIBLE TO " + self.username + " ---------\n"
                    count = 1 
                    self.client.sendall(b"stop")
                    message += "\n~~~~~~~~~~~~~~~~ FILE OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (U)Upload File\n           (D)Download File\n           (R)Read File\n           (M)Modify File\n           (P)Print Files On Account\n           (&)Remove File\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                    self.client.sendall(message.encode())
                    self.clientResponse()
    


# ALL ACCOUNT SETTINGS FUNCTIONS
    
    def userInfo(self):
        self.client.sendall(b"info")
        username = self.username
        first = Server.clientDB[self.username]['first']
        last = Server.clientDB[self.username]['last']
        email = Server.clientDB[self.username]['email']
        phone = Server.clientDB[self.username]['phone']
        birthday = Server.clientDB[self.username]['birth']
        login = Server.clientDB[self.username]['login']
        
        message = "============== USERNAME ==============\n\n     "+username+"\n\n============== NAME ==============\n\n     "+ first + " " + last + "\n\n============== EMAIL ==============\n\n     "+email+"\n\n============== PHONE ==============\n\n      "+ phone + "\n\n============== BIRTHDAY ==============\n\n     "+ birthday + "\n\n============== LAST LOGIN FOR THIS USER ==============\n\n     " + str(login)
        self.client.sendall(message.encode())
        self.client.sendall(b"\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           ($)Update User Information\n           (?)How to Use Server\n           (%)Reset Security Questions\n           (SOS)Delete Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
        self.clientResponse()
    def updateUser(self):
        return 0
    def serverInfo(self):
        return 0
    #Deletes all files and directories for this account.        
    def deleteAcc(self):
        dir = Server.clientDB[self.username]['dirClient']
        if (os.getcwd() != dir):
            os.chdir(dir)
        message = "\n\n~~~~~~~~~~~~~~~~ ARE YOU SURE YOU WANT TO DELETE USER " + self.username +" ~~~~~~~~~~~~~~~~\n-------- (Y or N) ------\n"
        self.client.sendall(message.encode())
        message = self.client.recv(100).decode()
        if ( message == "Y" or message == "y" or message == "Yes" or message == "yes"):
            tries = 3
            pssWd = Server.clientDB[self.username]['passwd']
            salt = Server.clientDB[self.username]['SaltPass']
            while tries != 0:
                message = "Username: " + self.username + "Enter Password: "
                self.client.sendall(message.encode())
                #must encrypt password to get answer
                passwd = self.client.recv(1024)
                passwd = bcrypt.hashpw(passwd, salt)
                if ((pssWd != passwd) and (tries == 1)):
                    print("Authentication error! No such user exists")
                    self.client.sendall(b"stop")
                    self.client.sendall(b"stop")
                    self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                    self.clientResponse()
                elif(pssWd != passwd):
                    print("Password incorrect!")
                    if (tries == 3):
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                    else:
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                    self.client.sendall(message.encode())
                else: 
                    email = Server.clientDB[self.username]['email']
                    secretKey = pyotp.random_base32()
                    messageUser = pyotp.TOTP(secretKey)
                    messageUser = messageUser.now()
                    self.email.login(Server.sender_email, Server.password)
                    self.email.sendmail(Server.sender_email, email, messageUser)
                    message = "~~~~~~~~~~~~ USER HAS BEEN SENT AUTHENTICATION CODE ON EMAIL ~~~~~~~~~~~~\nEnter code: "
                    self.client.sendall(message.encode())
                    code = self.client.recv(1024).decode()
                    self.client.sendall(b"stop")
                    self.client.sendall(b"stop")
                    verifyIn = pyotp.TOTP(secretKey)
                    if (verifyIn.verify(code)):
                        self.client.sendall(b"~~~~~~~~~~~~~~~~ USER IS AUTHENTICATED ~~~~~~~~~~~~~~~~\n=========== ARE YOU SURE YOU WOULD LIKE TO DELETE YOUR ACCOUNT ===========\n!!!!!!!!!!! WARNING YOU WILL LOOSE ALL ACCOUNT INFORMATION AND FILES !!!!!!!!!!!\n-------- (Y or N) ------\n")
                        message = self.client.recv(1024).decode()
                        if ( message == "Y" or message == "y" or message == "Yes" or message == "yes"):
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ ACCOUNT WILL NOW BE DELETED ~~~~~~~~~~~~~~~~\n")
                        else:
                            message = "========= ACCOUNT NOT CHANGED =========\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                                                                                                                   
                            self.client.sendall(message.encode())
                            self.clientResponse()
                        fileList = os.listdir(dir)
                        value = self.printServerFiles()
                        for file in fileList:
                            os.remove(file)
                        value = self.printServerFiles()
                        if (value == 0):
                            os.chdir("..")
                            os.removedirs(self.username)
                            self.client.sendall(b"stop")
                            Server.clientDB[self.username].get()
                            self.username = "Guest User"
                            self.authUser = 0
                            self.authBit = 0
                            message = "~~~~~~~~~~~~~~~~ " + r"₍ᐢ•(ܫ)•ᐢ₎" + self.username + " USER HAS BEEN DELETED " + r'₍ᐢ•(ܫ)•ᐢ₎'+ " ~~~~~~~~~~~~~~~~"
                            message += "\n\n~~~~~~~~~~~~~~~~ OPTIONS ~~~~~~~~~~~~~~~~\n         (L)Login\n         (C)Create account\n         (E)Exit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            self.client.sendall(message.encode())
                            self.clientResponse()
                        else:
                            self.client.sendall(b"stop")
                            message = "--------- FAILED: USER "+ self.username +" CAN NOT BE DELETED ---------\n!!!!!!!!!! MAY RESULT IN LOST USER FILES !!!!!!!!!!\n         (U)Upload\n         (D)Download\n         (R)Read File\n         (M)Modify File\n           (P)Print Files On Account\n         (A)Account Settings\n         (*)Logout\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
                            self.client.sendall(message.encode())
                            self.clientResponse()
                    else: 
                        self.client.sendall(b"========== AUTHENTICATION FAILED: ACCOUNT UNCHANGED  ==========\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                  
                        self.clientResponse()
        else:
            message = "========= ACCOUNT NOT CHANGED =========\n~~~~~~~~~~~~~~~~ OPTIONS IN SERVER ~~~~~~~~~~~~~~~~\n           (F)File Options\n           (A)Account Settings\n           (*)LogOut\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"                                                                                                                   
            self.client.sendall(message.encode())
            self.clientResponse()
            
    #Reset security questions  
    #Verify Password and then this can happen.          
    def resetSecureQ(self):
            tries = 3
            pssWd = Server.clientDB[self.username]['passwd']
            salt = Server.clientDB[self.username]['SaltPass']
            #Server.clientDB.close()
            self.client.sendall(b"account")
            self.client.sendall(b"secure")
            while tries != 0:
                self.client.sendall(b"Enter Password: ")
                        #must encrypt password to get answer
                passwd = self.client.recv(1024)
                passwd = bcrypt.hashpw(passwd, salt)
                if ((pssWd != passwd) and (tries == 1)):
                    print("Authentication error! No such user exists")
                    self.username = "Guest User"
                    self.client.sendall(b"stop")
                    self.client.sendall(b"stop")
                    self.client.sendall(b"!!!PASSWORD INCORRECT!!!\n--------- 0 ATTEMPTS LEFT ---------\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           ($)Update User Information\n           (?)How to Use Server\n           (%)Reset Security Questions\n           (SOS)Delete Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                    self.authUser = 0
                    self.clientResponse()
                elif(pssWd != passwd):
                    print("Password incorrect!")
                    if (tries == 3):
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 2 ATTEMPTS LEFT ---------\n")
                    else:
                        message = ("!!!PASSWORD INCORRECT!!!\n--------- 1 ATTEMPTS LEFT ---------\n")
                        tries -= 1
                    self.client.sendall(message.encode())
                else: 
                    tries = 3
                
                    while tries != 0:
                        self.client.sendall(b"stop")
                        message = "~~~~~~~~~~~~ USER HAS BEEN SENT AUTHENTICATION CODE ON EMAIL ~~~~~~~~~~~~\nEnter code: "
                        self.client.sendall(message.encode())
                        email = Server.clientDB[self.username]['email']
                        secretKey = pyotp.random_base32()
                        messageUser = pyotp.TOTP(secretKey)
                        messageUser = messageUser.now()
                        print(messageUser)
                        self.email.login(Server.sender_email, Server.password)
                        self.email.sendmail(Server.sender_email, email, messageUser)
                        code = self.client.recv(1024).decode()
                        verifyIn = pyotp.TOTP(secretKey)
                        right = verifyIn.verify(code) 
                        if (right == False and tries == 1):
                            self.client.sendall(b"stop")
                            self.client.sendall(b"--------- VERIFICATION FAILED ---------\n=========== USER VERIFIED CANT CHANGE SECURITY QUESTIONS ===========\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           ($)Update User Information\n           (?)How to Use Server\n           (%)Reset Security Questions\n           (SOS)Delete Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                                   
                            self.clientResponse()
                        elif(right == False):
                            print("User Verification failed!")
                            if (tries == 3):
                                message = ("--------- VERIFICATION FAILED ---------\n--------- 2 ATTEMPTS LEFT ---------\n")
                            else:
                                message = ("--------- VERIFICATION FAILED ---------\n--------- 1 ATTEMPTS LEFT ---------\n")
                            tries -= 1
                            self.client.sendall(message.encode()) 
                        elif (right == True):
                    
                                
                            print("User is verified.")
                            self.client.sendall(b"secure")
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ USER ACCEPTED ~~~~~~~~~~~~~~~~\n")
                            self.client.sendall(b"======= Security Questions =======\n")
                            self.client.sendall(b"--------- Case Sensitive ---------\n")
        
                            self.client.sendall(b"What year did you graduate from High School: ")
                            message = self.client.recv(1024)
                            self.client.sendall(b"What was your mothers maiden name: ")
                            message += self.client.recv(1024)
                            self.client.sendall(b"What was your first cars make and year (Example:HONDA2012): ")
                            message += self.client.recv(1024)
                            secureQ = message 
                            self.client.sendall(b"stop")
                            self.client.sendall(b"stop")
                            self.client.sendall(b"~~~~~~~~~~~~~~~~ SECURITY QUESTIONS ACCEPTED ~~~~~~~~~~~~~~~~\n--------- SECURITY QUESTIONS UPDATED ---------\n\n~~~~~~~~~~~~~~~~ SERVER SETTINGS ~~~~~~~~~~~~~~~~\n           (#)User Account Information\n           ($)Update User Information\n           (?)How to Use Server\n           (%)Reset Security Questions\n           (SOS)Delete Account\n           (!)Home\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")                                                                                                               
                            saltQ = bcrypt.gensalt()
                            hSecure = bcrypt.hashpw(secureQ, saltQ)
                            Server.clientDB[self.username] = {'passwd': passwd, 'SaltPass':salt, 'secureQ':hSecure, 'SaltSecure': saltQ, 'lockedBit': 0}
                            self.clientResponse()                   
            
def main(): 
    s = Server(server=None, insecure = None, client=None, address=None, thread=None, files=None, authBit = 0, authUser = 0, email=None)
    s.sqlDatabase()
if __name__ == "__main__":
    main()