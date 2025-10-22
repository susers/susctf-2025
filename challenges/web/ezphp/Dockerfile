FROM php:7.3-fpm-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add --update --no-cache tar nginx mysql mysql-client bash

# 复制nginx+mysql配置文件
COPY ./config/nginx.conf /etc/nginx/nginx.conf

# 复制web项目源码
COPY src /var/www/html
COPY flag /flag

RUN chmod 777 /flag
# 重新设置源码路径的用户所有权
RUN chown -R www-data:www-data /var/www/html

# 复制数据库配置文件
# 拷贝容器入口点脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 设置shell的工作目录
WORKDIR /var/www/html

# [可选]指定对外暴露端口，对于GZCTF等平台，强制EXPOSE可能会造成非预期端口泄露，请酌情启用
EXPOSE 80

# 设置nginx日志保存目录
VOLUME ["/var/log/nginx"]

# 设置容器入口点
ENTRYPOINT [ "/docker-entrypoint.sh" ]