#!/usr/bin/env bash
# This script is setting up prefered directory to hold static files

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Create Nginx configuration file
sudo tee /etc/nginx/sites-available/server_config <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://github.com/ezechielkiregha;
    }

    error_page 404 /404.html;
    location /404 {
        root /var/www/html;
        internal;
    }
}
EOF

# Enable the new Nginx site configuration
sudo ln -sf /etc/nginx/sites-available/server_config /etc/nginx/sites-enabled/

# Remove the default Nginx configuration
sudo rm -f /etc/nginx/sites-enabled/default

# Change ownership of /data/
sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu:ubuntu /data/

# Restart Nginx
sudo systemctl restart nginx
