#git clone https://git.postgresql.org/git/postgresql.git
#cd postgresql
#./configure 
#make
#make install
curl http://mirrors.koehn.com/apache//httpd/httpd-2.4.25.tar.gz > httpd-2.4.25.tar.gz
tar -xvzf httpd-2.4.25.tar.gz
cd httpd-2.4.25
./configure --prefix=~/apache2
make
make install
# TODO: need to configure for port 8080