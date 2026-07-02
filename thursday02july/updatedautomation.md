# Tic Tac Toe Automation 

```
#!/bin/bash

# TicTacToe VM Setup Script
# PM2 + Nginx Reverse Proxy
# Run inside Ubuntu EC2

ZIP_NAME="nodejs20-sparta-tictactoe-v1-2.zip"

sudo apt update -y
sudo apt upgrade -y

curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs unzip nginx -y

node -v
npm -v

unzip -o $ZIP_NAME

cd ~/app

npm install

sudo npm install -g pm2

pm2 kill
pm2 start index.js

pm2 save

sudo sed -i 's|try_files $uri $uri/ =404;|proxy_pass http://localhost:3000;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;|' /etc/nginx/sites-available/default

sudo nginx -t

sudo systemctl restart nginx
sudo systemctl enable nginx
```