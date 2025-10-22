FROM httpd:2.4-alpine

RUN apk update && apk add python3

# Enable CGI module and configure Apache to run CGI scripts with .py extension
RUN sed -i 's/#LoadModule cgid_module/LoadModule cgid_module/g' /usr/local/apache2/conf/httpd.conf
RUN sed -i 's/#AddHandler cgi-script .cgi/AddHandler cgi-script .py/g' /usr/local/apache2/conf/httpd.conf

RUN mkdir /usr/local/apache2/htdocs/static

COPY index.html /usr/local/apache2/htdocs
COPY --chmod=755 upload.py /usr/local/apache2/cgi-bin

# Make web user accessible
RUN chown -R www-data:www-data /usr/local/apache2/

COPY run.sh /

# Expose HTTP port
EXPOSE 80

cMD ["sh", "/run.sh"]

