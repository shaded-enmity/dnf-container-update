#!/bin/bash
# open("/etc/hosts", O_RDONLY|O_CLOEXEC)  = 8

# open("/etc/localtime", O_RDONLY|O_CLOEXEC) = 9

# open("/etc/crypto-policies/back-ends/openssl.config", O_RDONLY) = 9
# open("/etc/pki/tls/certs/ca-bundle.crt", O_RDONLY) = 9

# open("/etc/hosts", O_RDONLY|O_CLOEXEC)  = 9
# open("/etc/crypto-policies/back-ends/openssl.config", O_RDONLY) = 10
# open("/etc/pki/tls/certs/ca-bundle.crt", O_RDONLY) = 10

DEST=${1:-chroot}

mkdir -p ${DEST}/etc/crypto-policies/back-ends
mkdir -p ${DEST}/etc/pki/tls/certs

cp /etc/hosts ${DEST}/etc/hosts
cp /etc/crypto-policies/back-ends/openssl.config ${DEST}/etc/crypto-policies/back-ends/openssl.config
cp /etc/pki/tls/certs/ca-bundle.crt ${DEST}/etc/pki/tls/certs/ca-bundle.crt
