#!/usr/bin/env bash
# This script is setting up prefered directory to hold static files

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo echo "Holberton School" > /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu /data/
sudo chgrp -R ubuntu /data/

printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
    }

    location /redirect_me {
	return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
# test nginx 
# sudo nginx -t
# restart nginx
sudo service nginx restart
