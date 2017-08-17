#!/bin/bash
nginx_url="ftp://192.168.52.1/nginx-1.8.0.tar.gz"
yum -y install perl-ExtUtils-Embed perl-CPAN gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel  &>/dev/null
#install_m264() {
#tar xf nginx_mod_h264_streaming-2.2.7.tar.gz -C /usr/local/
#sed -i '158,161s@^@//@g' /usr/local/nginx_mod_h264_streaming-2.2.7/src/ngx_http_streaming_module.c
#}
useradd nginx -s /sbin/nologin
wget -q $nginx_url
tar xf nginx-1.8.0.tar.gz
rm -f nginx-1.8.0.tar.gz
cd nginx-1.8.0
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module \
--with-http_gzip_static_module --with-http_dav_module --with-http_addition_module --with-http_realip_module \
--with-http_flv_module --with-http_mp4_module --with-http_ssl_module --with-http_perl_module --with-debug \
--with-http_perl_module --with-ld-opt="-Wl,-E"  &>/dev/null
#--with-stream TCP反向代理
#--add-module=/usr/local/nginx_mod_h264_streaming-2.2.7
make            &>/dev/null
make install    &>/dev/null
sed -i '116a\include vhosts/*.conf;' /usr/local/nginx/conf/nginx.conf
mkdir /usr/local/nginx/conf/vhosts
