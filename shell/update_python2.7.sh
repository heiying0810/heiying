#!/bin/bash
##将Centos-6.5 的Python环境更新2.7

python_url="ftp://192.168.52.1/Python-2.7.10.tar.xz"
pip_url="ftp://192.168.52.1/pip-7.1.0.tar.gz"
setuptools_url="ftp://192.168.52.1/setuptools-18.0.1.tar.gz"
##安装基础依赖环境
yum -y install gcc gcc-c++ unzip ncurses-devel sqlite-devel bzip2 bzip2-devel \
gdbm-devel readline-devel zlib-devel xz openssl-devel
##update Python 2.7
wget $python_url
tar xf Python-2.7.10.tar.xz
cd Python-2.7.10
./configure --prefix=/usr/local/python27
make && make install
cd ..
mv /usr/bin/python /usr/bin/python_old
ln -sf /usr/local/python27/bin/python /usr/bin/
sed -i 's;#!/usr/bin/python;#!/usr/bin/python2.6;' /usr/bin/yum
rm -rf Python-2.7.10*
echo 'PATH=$PATH:/usr/local/python27/bin' >> /etc/profile
source /etc/profile
#install setuptools
wget $setuptools_url
tar xf setuptools-18.0.1.tar.gz
cd setuptools-18.0.1
python setup.py install
cd ..
rm -rf setuptools-18.0.1*
#install pip
wget $pip_url
tar xf pip-7.1.0.tar.gz
cd pip-7.1.0
python setup.py install
cd ..
rm -rf pip-7.1.0*
mkdir ~/.pip
cat > ~/.pip/pip.conf <<-EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
EOF
pip install --upgrade pip
