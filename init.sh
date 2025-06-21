#!/bin/bash

# Create a symlink to the .env file
sudo mkdir -p /var/www/api.peterrauscher.com/.well-known
sudo ln -sf $HOME/api.peterrauscher.com/openapi.json /var/www/api.peterrauscher.com/openapi.json
sudo ln -sf $HOME/api.peterrauscher.com/.well-known/mcp.json /var/www/api.peterrauscher.com/.well-known/mcp.json
sudo ln -sf $HOME/api.peterrauscher.com/nginx.conf/etc/nginx/sites-enabled/api.peterrauscher.com
