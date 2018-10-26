#/bin/bash

UNIQUE_NAME=$1
PRE_KEY_PREFIX="pre_key_"
PEM_EXTENSION=".pem"
UNIQUE_PRE_KEY=$PRE_KEY_PREFIX$UNIQUE_NAME$PEM_EXTENSION

PUBLIC_PREFIX="public_"
PRIVATE_PREFIX="private_"

UNIQUE_PUBLIC_KEY=$PUBLIC_PREFIX$UNIQUE_NAME$PEM_EXTENSION
UNIQUE_PRIVATE_KEY=$PRIVATE_PREFIX$UNIQUE_NAME$PEM_EXTENSION

#Generate private key 
openssl genrsa -out $UNIQUE_PRE_KEY 2048

#Get public key
openssl rsa -in $UNIQUE_PRE_KEY -pubout > $UNIQUE_PUBLIC_KEY

#change the private key to pkcs8 specification
openssl pkcs8 -topk8 -inform PEM -outform PEM -in $UNIQUE_PRE_KEY -out $UNIQUE_PRIVATE_KEY -nocrypt

#delete pre_key
rm $UNIQUE_PRE_KEY

mv $UNIQUE_PUBLIC_KEY public_keys/

mv $UNIQUE_PRIVATE_KEY private_keys/

