FROM php:8.4-apache

# 制作者信息
LABEL auther_template="CTF-Archives"

# Apache 初始化
RUN a2enmod rewrite

# 安装必要的软件包
RUN apt update && \
    apt install -y default-mysql-client default-mysql-server wget unzip

# 配置mysql
RUN docker-php-source extract && \
    docker-php-ext-install pdo_mysql mysqli && \
    docker-php-source delete && \
    mysql_install_db --user=mysql --datadir=/var/lib/mysql

# 复制mysql配置文件
COPY ./config/docker-php-ext-mysqli.ini /usr/local/etc/php/conf.d
COPY ./config/docker-php-ext-pdo_mysql.ini /usr/local/etc/php/conf.d

# 复制web项目源码
RUN wget -O xinhu.zip "http://www.rockoa.com/index.php?a=down&id=297" && unzip -d xinhu xinhu.zip
RUN mv xinhu/* /var/www/html && rm /var/www/html/webmain/webmainConfig.php1
COPY ./config/webmainConfig.php /var/www/html/webmain

# 重新设置源码路径的用户所有权
RUN chown -R www-data:www-data /var/www/html

# 复制数据库配置文件
COPY ./data/db.sql /var/db.sql

# 拷贝容器入口点脚本
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# 配置数据库数据
RUN echo "[mysqld]\nsql_mode='ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'\n" > /etc/mysql/conf.d/sql_mode.cnf \
    && echo "default-character-set=utf8" >> /etc/mysql/conf.d/mysql.cnf
RUN sh -c 'mysqld_safe &' \
    && sleep 5s \
    && mysqladmin -uroot password 'seu@susctf@2025' \
    && mysql -e "source /var/db.sql;" -uroot -p'seu@susctf@2025' \
    && mysql -uroot -p'seu@susctf@2025' rockxinhu < /var/www/html/webmain/install/rockxinhu.sql

# 设置shell的工作目录
WORKDIR /var/www/html

EXPOSE 80

# 设置容器入口点
ENTRYPOINT [ "/docker-entrypoint.sh" ]
