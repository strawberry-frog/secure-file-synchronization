# !/bin/bash
# Sets up server machine for running this code. 
# mkdir project
# virtualenv -p /usr/bin/python3 project
# cd project
# source bin/activate

yes | pip install --upgrade pip
yes | pip install --upgrade setuptools
yes | pip install bcrypt
yes | pip install pyotp
yes | pip install maskpass
yes | pip install watchdog

#countryName = "US"
#stateName = "VA"
#localName = "Harrisonburg"
#orgName = "Katherine Server Inc."
#orgUnit = "Security"
#CN = "Server"

#password = "cookie"

touch server-extensions.txt
echo "extendedKeyUsage=serverAuth" > server-extensions.txt
touch client-extension.txt
echo "extendedKeyUsage=clientAuth" > client-extensions.txt


openssl ecparam -name prime256v1 -genkey -noout -out ca.key
openssl req -new -x509 -sha256 -key ca.key -out ca.crt

openssl ecparam -name prime256v1 -genkey -noout -out server.key

openssl req -new -sha256 -key server.key -out server.csr 

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.pem -days 1000 -sha256 -extfile server-extensions.txt

openssl ecparam -name prime256v1 -genkey -noout -out client.key

openssl req -new -sha256 -key client.key -out client.csr

openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.pem -days 1000 -sha256 -extfile client-extensions.txt
cd ..
# mkdir server
# cp ca.key ca.crt server.pem server.key server.py /server
# mkdir client
# mkdir client2
# cp ca.key ca.crt client.pem client.key client.py /client

# cp ca.key ca.crt client.pem client.key client.py /client2