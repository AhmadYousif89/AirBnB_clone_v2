#!/usr/bin/env bash
# script that sets up web servers for the deployment of web_static
# Install Ngnix if it doesn't exist
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
sudo chown -hR ubuntu:ubuntu /data/

sudo touch /data/web_static/releases/test/index.html
echo "<html><head><title>Test Page</title></head><body><h1>This Is A Testing Page</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

sudo service nginx restart
