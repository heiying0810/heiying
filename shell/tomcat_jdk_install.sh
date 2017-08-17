#!/bin/bash
#安装JDK和TOMCAT
tomcat_url="ftp://192.168.52.1/apache-tomcat-7.0.52.tar.gz"
jdk_url="ftp://192.168.52.1/jdk-7u51-linux-x64.tar.gz"

wget $jdk_url >/dev/null 2>&1
tar -xf jdk-7u51-linux-x64.tar.gz -C /usr/local/
rm -f jdk-7u51-linux-x64.tar.gz
mv /usr/local/{jdk1.7.0_51,jdk}
echo 'JAVA_HOME=/usr/local/jdk' >> /etc/profile
echo 'PATH=$JAVA_HOME/bin:$PATH' >> /etc/profile
echo 'CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar' >> /etc/profile
echo 'export JAVA_HOME' >> /etc/profile
echo 'export PATH' >> /etc/profile
echo 'export CLASSPATH' >> /etc/profile
source /etc/profile

wget $tomcat_url >/dev/null 2>&1
tar -xf apache-tomcat-7.0.52.tar.gz -C /usr/local/
rm -f apache-tomcat-7.0.52.tar.gz
cd /usr/local/
mv apache-tomcat-7.0.52 tomcat
rm -rf /usr/local/tomcat/webapps/*
rm -f tomcat/{LICENSE,NOTICE,RELEASE-NOTES,RUNNING.txt}
