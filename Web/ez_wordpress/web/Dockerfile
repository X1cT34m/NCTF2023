FROM php:7.4-apache

COPY ./html.tar.gz /var/www/

RUN cd /var/www/ && \
    tar -zxvf html.tar.gz && \
    rm -rf html.tar.gz

RUN docker-php-ext-install mysqli && \
    chown -R www-data:www-data /var/www/html && \
    echo nctf{insecure_wordpress_core_deserialization_BWxMCmos0pzTcNFw} > /flag && \
    chmod 400 /flag && \
    chmod 4755 /bin/date

USER www-data