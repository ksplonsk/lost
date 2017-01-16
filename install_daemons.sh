#!/bin/bash

git clone https://git.postgresql.org/git/postgresql.git
cd postgresql
./configure --prefix=$1/postgresql
make
make install

cd ..

curl -o httpd-2.4.25.tar.gz http://mirrors.koehn.com/apache//httpd/httpd-2.4.25.tar.gz
tar -xvzf httpd-2.4.25.tar.gz
cd httpd-2.4.25
./configure --prefix=$1/apache2
make
make install
sed -i -- 's/Listen 80/Listen 8080/g' $1/apache2/conf/httpd.conf

cd ..
