# TicTacToe App 

## 1. Launch Instance 
- Once the instance is launched on AWS EC2, choose `myip` for source, in the inbound rules for SSH port `22`. 
- Another rule would be to add a custom TCP with port range `3000` and source can be empty. 

## 2. VM Launch
- If not done, ensure instance key is copied into the .ssh folder using `cp ~/Downloads/montezer-tech610-key.pem`
- Then change permissions to `chmod 400 ~/.ssh/montezer-tech610-key.pem ubuntu@currentpublicid`

## 3. VM Set Up
- `sudo apt update -y`
- `sudo apt upgrade -y`

### Install Node JS v20

```
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs -y
```

### Get Source Code on to the VM
- `exit` back into bash
- We are now going to copy the source code into our VM using `scp`
- - `scp -i KEY SOURCE TARGET`
- `scp -i ~/.ssh/montezer-tech610-key.pem ~/Downloads/nodejs20-sparta-tictactoe-v1-2.zip ubuntu@currentpublicid:~
nodejs20-sparta-tictactoe-v1-2.zip`
- `:~` this above represents the home directory in ubuntu

### Unzip Source Code in VM
- Then log back into Ubuntu: `ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@34.250.43.45(currentpublicid)`
- `ls` in home directory to ensure `scp` worked and the source code has been transferred. 
- - Install Zip Package `sudo apt install unzip -y`
- - Simply `unzip filename` to unzip the file 
- `cd` into `app`

### To start App
- `npm install`
- `npm start`

### To access App
- Go Browser and type: `34.250.43.45:3000/`

## Important Reminder
- If the EC2 instance is stopped and started again, the public IPv4 address may change. If SSH or the app stops working, check the current Public IPv4 address in the EC2 console and update the commands.



