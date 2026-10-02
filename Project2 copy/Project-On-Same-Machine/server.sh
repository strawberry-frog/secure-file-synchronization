# !/bin/bash
# Sets up server machine for running this code. 
mkdir /server
cp ca.key ca.crt server.py /server/
virtualenv -p /usr/bin/python3 /server
cd /server
source bin/activate
mkdir Katherine'(Server)'

yes | pip install --upgrade pip
yes | pip install --upgrade setuptools
yes | pip install bcrypt
yes | pip install pyotp

#countryName = "US"
#stateName = "VA"
#localName = "Harrisonburg"
#orgName = "Katherine Server Inc."
#orgUnit = "Security"
#CN = "Server"

#password = "cookie"

touch server-extensions.tx
echo "extendedKeyUsage=serverAuth" > server-extensions.txt

openssl ecparam -name prime256v1 -genkey -noout -out server.key

openssl req -new -sha256 -key server.key -out server.csr 

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.pem -days 1000 -sha256 -extfile server-extensions.txt
cd ..