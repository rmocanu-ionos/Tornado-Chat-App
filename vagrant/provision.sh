#!/bin/bash

apt-get update
apt-get install -y python python-dev python-pip nodejs npm
apt-get install -y libcurl4-openssl-dev libssl-dev

ln -s /usr/bin/nodejs /usr/bin/node
ln -s /opt/dev/avmess/bin/avmess /usr/bin/avmess

# install MySQL server
echo "mysql-server mysql-server/root_password password root" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password root" | sudo debconf-set-selections
apt-get install -y mysql-server mysql-client MySQL-python
mysql_secure_installation

# configure mysql
mysql -uroot -proot -e "CREATE DATABASE avmess /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -uroot -proot -e "CREATE USER avmess@localhost IDENTIFIED BY 'avmess';"
mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON avmess.* TO 'avmess'@'localhost';"
mysql -uroot -proot -e "FLUSH PRIVILEGES;"

# install python dependencies
cd /opt/dev/avmess
pip install -r requirements.txt

# install node dependencies
cd /opt/dev/avmess/web
npm install

AVMESS_PATH="/opt/dev/avmess"
export PYTHONPATH=$AVMESS_PATH:$PYTHONPATH
export AVMESS_WEB_DIR=$AVMESS_PATH/web
echo "export PYTHONPATH=$AVMESS_PATH:$PYTHONPATH" >> /etc/environment
echo "export AVMESS_WEB_DIR=$AVMESS_PATH/web" >> /etc/environment
