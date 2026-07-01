# TicTacToe App with PM2 and Nginx Reverse Proxy

## 1. Launch Instance

* Once the instance is launched on AWS EC2, choose `myip` for source in the inbound rules for SSH port `22`.
* Add another inbound rule for HTTP:

```text
HTTP | Port 80 | Source 0.0.0.0/0
```

* Since Nginx will act as a reverse proxy, port `3000` does not need to be publicly open anymore.
* The app will still run on port `3000` inside the VM, but users will access it through port `80`.

```text
Browser → EC2 Public IP on port 80 → Nginx → Node app on localhost:3000
```

## 2. VM Launch

* If not done, ensure the instance key is copied into the `.ssh` folder on the main PC:

```bash
cp ~/Downloads/montezer-tech610-key.pem ~/.ssh/
```

* Then change permissions on the key file:

```bash
chmod 400 ~/.ssh/montezer-tech610-key.pem
```

* SSH into the Ubuntu EC2 instance:

```bash
ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@currentpublicid
```

Example:

```bash
ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@108.132.7.162
```

## 3. Get Source Code onto the VM

* The TicTacToe zip file needs to be copied from the main PC to the Ubuntu VM.
* Exit back to Git Bash on the main PC:

```bash
exit
```

* Copy the source code into the VM using `scp`.

General format:

```bash
scp -i KEY SOURCE TARGET
```

Example:

```bash
scp -i ~/.ssh/montezer-tech610-key.pem ~/Downloads/nodejs20-sparta-tictactoe-v1-2.zip ubuntu@currentpublicid:~/
```

Real example:

```bash
scp -i ~/.ssh/montezer-tech610-key.pem ~/Downloads/nodejs20-sparta-tictactoe-v1-2.zip ubuntu@108.132.7.162:~/
```

* The `:~/` at the end means copy the file into the Ubuntu user’s home directory.

## 4. Log Back into Ubuntu

* SSH back into the Ubuntu VM:

```bash
ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@currentpublicid
```

Example:

```bash
ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@108.132.7.162
```

* Use `ls` to check that the zip file was copied successfully:

```bash
ls
```

Expected file:

```text
nodejs20-sparta-tictactoe-v1-2.zip
```

## 5. Create the Bash Script in Ubuntu

* Create a script called `deploy.sh`:

```bash
nano deploy.sh
```

* Add the following script:

```bash
#!/bin/bash

# ==========================
# TicTacToe VM Setup Script
# PM2 + Nginx Reverse Proxy
# Run this inside Ubuntu EC2
# ==========================

ZIP_NAME="nodejs20-sparta-tictactoe-v1-2.zip"

echo "Updating Ubuntu..."
sudo apt update -y
sudo apt upgrade -y

echo "Installing Node.js 20, unzip, and Nginx..."
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs unzip nginx -y

echo "Checking Node and npm versions..."
node -v
npm -v

echo "Unzipping app..."
unzip -o $ZIP_NAME

echo "Moving into app folder..."
cd ~/app

echo "Installing app dependencies..."
npm install

echo "Installing PM2 globally..."
sudo npm install -g pm2

echo "Starting app with PM2..."
pm2 kill
pm2 start index.js

echo "Saving PM2 process list..."
pm2 save

echo "Configuring Nginx reverse proxy..."
sudo sed -i 's|try_files $uri $uri/ =404;|proxy_pass http://localhost:3000;\n        proxy_set_header Host $host;\n        proxy_set_header X-Real-IP $remote_addr;|' /etc/nginx/sites-available/default

echo "Testing Nginx config..."
sudo nginx -t

echo "Restarting and enabling Nginx..."
sudo systemctl restart nginx
sudo systemctl enable nginx

echo "Deployment complete!"
echo "Visit your EC2 public IP in the browser."
```

## 6. Make the Script Executable

* Change the file permissions so the script can be run:

```bash
chmod +x deploy.sh
```

* Run the script:

```bash
./deploy.sh
```

## 7. What the Script Does

The script automates the VM setup by:

```text
1. Updating Ubuntu
2. Installing Node.js v20
3. Installing unzip
4. Installing Nginx
5. Unzipping the TicTacToe app
6. Entering the app folder
7. Running npm install
8. Installing PM2
9. Starting the app with PM2
10. Configuring Nginx as a reverse proxy
11. Restarting Nginx
```

## 8. To Access the App

* Go to the browser and type the EC2 public IPv4 address:

```text
http://108.132.7.162
```

* You should no longer need to type `:3000`.

Old way:

```text
http://108.132.7.162:3000
```

New way with Nginx:

```text
http://108.132.7.162
```

## 9. Useful PM2 Commands

* Check running apps:

```bash
pm2 status
```

* View logs:

```bash
pm2 logs
```

* Restart the app:

```bash
pm2 restart index
```

* Stop the app:

```bash
pm2 stop index
```

* Stop all PM2 processes:

```bash
pm2 kill
```

## 10. Important Reminder

* If the EC2 instance is stopped and started again, the public IPv4 address may change.
* If SSH or the app stops working, check the current Public IPv4 address in the EC2 console and update the commands.
* If the instance is terminated, the Ubuntu server is deleted and the setup must be repeated.
* The source code zip and script should be kept on the main PC or in GitHub so they can be reused on a clean VM.

## 11. What Would Stay the Same for Another App?

If deploying a different application, these parts would probably stay the same:

```text
SSH into EC2
Copy files using scp
Run apt update and apt upgrade
Install required packages
Use PM2 for Node.js apps
Use Nginx as a reverse proxy
Use security group rules for SSH and HTTP
```

## 12. What Might Change for Another App?

These parts might change depending on the application:

```text
Zip file name
App folder name
Start file, for example index.js or server.js
App port, for example 3000, 5000, or 8000
Runtime, for example Node.js, Python, or Java
Install command, for example npm install or pip install
Start command, for example pm2 start index.js or python app.py
Nginx proxy_pass port
```
