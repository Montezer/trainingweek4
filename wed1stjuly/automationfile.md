## Option 1: Bash script on the VM

```
#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh

sudo apt install nodejs unzip -y

node -v
npm -v

unzip nodejs20-sparta-tictactoe-v1-2.zip

cd app

npm install
npm start
 
```
- Save it as `setup.sh` - Makes this script executable 
- Run it as `chmod +x setup.sh` - Runs script in current folder with `./` meaning look in the current directory


## Option 2: Bash Script in main PC to do everything for you

```
#!/bin/bash

# ==========================
# TicTacToe EC2 Deploy Script
# ==========================

# Change to current EC2 public IPv4 address
EC2_IP="108.132.7.162"

# EC2 username for Ubuntu
EC2_USER="ubuntu"

# Path to your private key 
KEY="$HOME/.ssh/montezer-tech610-key.pem"

# Path to TicTacToe zip file
ZIP_FILE="$HOME/Downloads/nodejs20-sparta-tictactoe-v1-2.zip"

# Name of the zip file after copying to Ubuntu
ZIP_NAME="nodejs20-sparta-tictactoe-v1-2.zip"

echo "Fixing key permissions..."
chmod 400 "$KEY"

echo "Copying TicTacToe zip file to EC2..."
scp -i "$KEY" "$ZIP_FILE" "$EC2_USER@$EC2_IP:~/"

echo "Connecting to EC2 and setting up the app..."
ssh -i "$KEY" "$EC2_USER@$EC2_IP" << EOF

echo "Updating Ubuntu..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing Node.js 20..."
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs unzip -y

echo "Checking Node and npm versions..."
node -v
npm -v

echo "Unzipping app..."
unzip -o $ZIP_NAME

echo "Going into app folder..."
cd ~/app

echo "Installing npm dependencies..."
npm install

echo "Starting TicTacToe app..."
npm start

EOF

```