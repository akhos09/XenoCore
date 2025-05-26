#!/bin/bash
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install apache2 php mysql-server php-mbstring php-zip php-gd php-json php-curl openssl libapache2-mod-php php-mysql -y
sudo reboot
sudo tee /etc/php/8.3/apache2/php.ini > /dev/null << 'EOF'
display_errors = On
display_startup_errors = On
error_reporting = E_ALL
log_errors = On
error_log = /var/log/php_errors.log
memory_limit = 256M
max_execution_time = 300
upload_max_filesize = 64M
post_max_size = 64M
extension=curl
extension=mbstring
extension=mysqli
extension=openssl
extension=pdo_mysql
extension=gd
date.timezone = Europe/Madrid
opcache.enable = 0
default_charset="ES"
EOF
sudo systemctl restart apache2
echo "<?php phpinfo ();?>" > /var/www/html/version.php
sudo loadkeys es
