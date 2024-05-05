#!/usr/bin/env bash
# This script is setting up prefered directory to hold static files

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/

# Remove the default Nginx configuration
sudo rm -f /etc/nginx/sites-enabled/custom_conf

# Update Nginx configuration
sudo tee /etc/nginx/sites-available/custom_config <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }

    error_page 404 /404.html;

    location /404.html {
        root /var/www/html;
        internal;
    }

    location / {
        root /var/www/html;
        index index.html index.htm;
    }
}
EOF

# Enable the new Nginx site configuration
sudo ln -sf /etc/nginx/sites-available/custom_config /etc/nginx/sites-enabled/

# Restart Nginx
sudo systemctl restart nginx

exit 0
