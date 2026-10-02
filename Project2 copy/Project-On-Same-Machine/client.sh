# !/bin/bash
# Client set up 
mkdir /client
cp ca.key ca.crt client.py /client/
virtualenv -p /usr/bin/python3 /client
cd /client
source bin/activate

yes | pip install --upgrade pip
yes | pip install --upgrade setuptools
yes | pip install maskpass

#countryName = "US"
#stateName = "VA"
#localName = "Harrisonburg"
#orgName = "Katherine Server Inc."
#orgUnit = "Security"
#CN = "Client"

#password = "cookie"

touch client-extensions.txt
echo "extendedKeyUsage=clientAuth" > client-extensions.txt
openssl ecparam -name prime256v1 -genkey -noout -out client.key
openssl req -new -sha256 -key client.key -out client.csr

openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.pem -days 1000 -sha256 -extfile client-extensions.txt
