# Secure Client-Server File Sharing System

A Python client-server file sharing system built to explore secure
network communication, authentication, certificate management, password
security, and file transfer.

The application uses SSL/TLS and X.509 certificates to establish secure
communication between a client and server. Users can create accounts,
authenticate, recover passwords, and upload or download files through
the server.

## Features

-   SSL/TLS encrypted client-server communication
-   X.509 certificate authentication
-   Elliptic Curve cryptographic keys
-   Locally generated Certificate Authority
-   User account creation and authentication
-   Password complexity requirements
-   Password hashing with bcrypt
-   Hidden password entry using maskpass
-   Password recovery using security questions
-   Account lockout after repeated failed recovery attempts
-   File upload and download
-   User-specific file storage
-   Multithreaded server connections
-   Input validation and authentication controls

## Technologies

-   Python 3
-   Python sockets
-   SSL/TLS
-   OpenSSL
-   X.509 certificates
-   Elliptic Curve Cryptography
-   bcrypt
-   maskpass
-   Bash
-   Linux
-   Multithreading

## Requirements

This project was developed for Linux systems.

Python 3 and OpenSSL are required.

Create a Python virtual environment:

``` bash
mkdir ~/project
virtualenv -p /usr/bin/python3 ~/project
cd ~/project
source bin/activate
```

Update pip and setuptools:

``` bash
pip install --upgrade pip
pip install --upgrade setuptools
```

Install the server dependency:

``` bash
pip install bcrypt
```

Install the client dependency:

``` bash
pip install maskpass
```

## Project Files

The project can be run with the client and server on the same Linux
machine or on separate Linux systems.

Core files include:

``` text
client.py
server.py
client.sh
server.sh
ca.crt
```

The Bash scripts generate the cryptographic keys, certificate requests,
certificates, and other files required by the application.

Private `.key` files are intentionally not included in the repository
and should be generated locally.

## Certificate Setup

The project uses a locally created Certificate Authority and separate
certificates for the server and client.

### Server

Run:

``` bash
bash server.sh
```

During certificate creation, the server certificate must use:

``` text
Common Name: Server
Challenge Password: cookie
```

Other certificate information can be customized for your environment.

Example:

``` text
Country Name: US
State or Province: VA
Locality Name: Harrisonburg
Organization Name: KatherineServerLLC
Organizational Unit: Security
Common Name: Server
Email: your email
Challenge Password: cookie
Company Name: [blank]
```

### Client

Run:

``` bash
bash client.sh
```

During certificate creation, the client certificate must use:

``` text
Common Name: Client
Challenge Password: cookie
```

Example:

``` text
Country Name: US
State or Province: VA
Locality Name: Harrisonburg
Organization Name: KatherineServerLLC
Organizational Unit: Security
Common Name: Client
Email: your email
Challenge Password: cookie
Company Name: [blank]
```

The required Common Names and challenge password are expected by the
current implementation and should not be changed without also updating
the code.

## Manual Certificate Generation

If the Bash scripts cannot be used, the certificates can also be
generated manually with OpenSSL.

### Certificate Authority

Generate the CA private key:

``` bash
openssl ecparam -name prime256v1 -genkey -noout -out ca.key
```

Generate the CA certificate:

``` bash
openssl req -new -x509 -sha256 -key ca.key -out ca.crt
```

Recommended CA Common Name:

``` text
CA
```

### Server Certificate

Generate the server private key:

``` bash
openssl ecparam -name prime256v1 -genkey -noout -out server.key
```

Create the certificate signing request:

``` bash
openssl req -new -sha256 -key server.key -out server.csr
```

Sign the server certificate:

``` bash
openssl x509 -req -in server.csr \
-CA ca.crt \
-CAkey ca.key \
-CAcreateserial \
-out server.pem \
-days 1000 \
-sha256 \
-extfile server-extensions.txt
```

The server certificate should use:

``` text
Common Name: Server
Challenge Password: cookie
```

### Client Certificate

Generate the client private key:

``` bash
openssl ecparam -name prime256v1 -genkey -noout -out client.key
```

Create the certificate signing request:

``` bash
openssl req -new -sha256 -key client.key -out client.csr
```

Sign the client certificate:

``` bash
openssl x509 -req -in client.csr \
-CA ca.crt \
-CAkey ca.key \
-CAcreateserial \
-out client.pem \
-days 1000 \
-sha256 \
-extfile client-extensions.txt
```

The client certificate should use:

``` text
Common Name: Client
Challenge Password: cookie
```

## Running the Server

Activate the server environment:

``` bash
cd ~/server
source bin/activate
```

Start the server:

``` bash
python server.py
```

The server will initialize its directories and users and begin waiting
for client connections.

## Running the Client

In a separate terminal or Linux system:

``` bash
cd ~/client
source bin/activate
```

Start the client:

``` bash
python client.py
```

The client will establish a connection with the server and display the
main menu.

## Authentication

The initial client menu provides three primary options:

``` text
(L) Login
(C) Create Account
(E) Exit
```

Commands accept uppercase, lowercase, and supported full-word versions.

For example:

``` text
L
l
Login
login
```

## Account Creation

Selecting Create Account allows a user to register a new username.

The server checks whether the username already exists. A new account
must use a unique username.

Passwords must contain:

-   At least one lowercase letter
-   At least one uppercase letter
-   At least one number
-   At least one special character
-   At least 8 characters

Password input is hidden from view.

After creating a password, the user provides answers to three security
questions used by the password recovery system.

## Login and Account Recovery

Users authenticate with their username and password.

After repeated unsuccessful login attempts, the Forgot Password option
becomes available.

Password recovery requires the user to correctly answer the security
questions associated with the account.

If the answers are correct, the user can create a new password that
meets the password requirements.

After repeated incorrect security-question attempts, the account is
locked as a security measure.

## Authenticated User Menu

After successful authentication, the server provides:

``` text
(U) Upload File
(D) Download File
(A) Account Settings
(*) Log Out
```

The application validates commands based on the user's current location
in the menu system.

For example, login commands cannot be used while already authenticated.

## File Operations

Authenticated users can upload and download files through the server.

The server maintains user-specific directories to separate files
belonging to different accounts.

All file operations occur through the authenticated client-server
connection.

## Security Design

The project combines several security concepts:

-   SSL/TLS encrypted network communication
-   X.509 certificate authentication
-   Elliptic Curve cryptographic keys
-   Locally managed Certificate Authority
-   Password hashing
-   Password complexity enforcement
-   Hidden credential input
-   Account lockout
-   User authentication
-   Password recovery
-   Input validation
-   User-specific file storage

## Known Limitations

This project was developed as a learning project and is not intended to
be a production authentication or file-storage system.

### Multiple Client Connections

The server can accept multiple connections, but additional clients may
encounter authentication problems related to certificate paths after
directory changes.

Certificate path handling should be refactored to support multiple
clients more reliably.

### Server Connection Handling

Some client disconnects or server exceptions can require the server to
be restarted.

Thread and connection cleanup could be improved to allow the server to
recover without restarting.

### Account Settings

The Account Settings option is displayed in the authenticated menu but
is not currently implemented.

### Blank Input

Blank username, password, or security-question input can result in
repeated input loops.

Additional input validation is needed to handle empty input correctly.

## Future Improvements

-   Improve support for simultaneous clients
-   Refactor certificate and file path handling
-   Improve thread cleanup and connection handling
-   Add graceful client disconnects
-   Add stronger exception handling
-   Prevent blank-input loops
-   Complete the Account Settings functionality
-   Add structured security and server logging
-   Add automated tests
-   Improve account recovery
-   Separate configuration values from application code

## What I Learned

This project gave me hands-on experience building a network application
where networking, programming, authentication, and cryptography all had
to work together.

I worked with Python socket programming, SSL/TLS, X.509 certificates,
OpenSSL, Elliptic Curve keys, password hashing, authentication, file
handling, Linux, Bash, and multithreading.

Troubleshooting the project also gave me experience working through
problems involving certificate paths, network connections,
authentication state, working directories, and multiple client threads.

## Security Notice

Private cryptographic keys are not included in this repository. They
should be generated locally using the provided scripts or the OpenSSL
commands above.

This project was created for educational purposes and should not be used
as a production authentication or file-storage system.
