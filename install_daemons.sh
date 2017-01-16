#!/bin/bash

#git clone https://git.postgresql.org/git/postgresql.git
#cd postgresql
#./configure --prefix=$1
#make
#make install

#cd ..

curl -o httpd-2.4.25.tar.gz http://mirrors.koehn.com/apache//httpd/httpd-2.4.25.tar.gz
tar -xvzf httpd-2.4.25.tar.gz
cd httpd-2.4.25
./configure --prefix=$1
make
make install
# TODO: need to configure for port 8080

cd ..
