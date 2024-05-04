#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
# Install Ngnix if it doesn't exist
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
    sudo ufw allow 'Nginx HTTP'
fi

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo chown -R ubuntu:ubuntu /data/

sudo touch /data/web_static/releases/test/index.html
echo "<html><head><title>Test Page</title></head><body><h1>This Is A Testing Page</h1></body></html>" > /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/hbnb_static
sudo ln -s /etc/nginx/sites-available/hbnb_static /etc/nginx/sites-enabled/

sudo service nginx restart
