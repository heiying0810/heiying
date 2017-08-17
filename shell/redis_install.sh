#!/bin/bash

url="ftp://192.168.52.1/redis-3.0.1.tar.gz"
init_url="ftp://192.168.52.1/script/redis-server"
##安装redis
cd ~
wget $url
tar xf redis-3.0.1.tar.gz
cd redis-3.0.1
make
cd src ;make install
mkdir -p /usr/local/redis/{etc,bin,var}
mv ../redis.conf /usr/local/redis/etc
sed -i 's#pidfile.*$#pidfile /var/run/redis.pid#' /usr/local/redis/etc/redis.conf
sed -i 's#logfile.*$#logfile /usr/local/redis/var/redis.log#' /usr/local/redis/etc/redis.conf
sed -i 's#^dir.*$#dir /usr/local/redis/var/#' /usr/local/redis/etc/redis.conf
sed -i 's#daemonize no#daemonize yes#' /usr/local/redis/etc/redis.conf
mv ./{mkreleasehdr.sh,redis-benchmark,redis-check-aof,redis-check-dump,redis-cli,redis-server,redis-sentinel} /usr/local/redis/bin/
cd ~;rm -rf redis-3.0.1*
##添加启动文件
wget $init_url
mv redis-server /etc/init.d/
chmod +x /etc/init.d/redis-server
chkconfig --add redis-server
chkconfig redis-server
