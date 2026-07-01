# First App

- All traffic on Port 3000

`ssh -i ~/.ssh/montezer-tech610-key.pem ubuntu@52.50.175.100`


## VM Set Up

```
sudo apt update -y
sudo apt upgrade -y
```

### Install nginx 
```
sudo apt install nginx -y
```

- ```Sudo``` = run command with root privileges 
- ```Apt``` = package manager for Ubuntu 
- ```Install``` = tells apt what to do 
- ```ngix/git/nodejs/etc``` = name of package/software you want
- ```-y``` = automatically say yes to prompts 

### Install Node JS v20

```
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs -y
```

### Get Source Code on to the VM
Options: 
- Git
- Copy ```(scp)```
- `scp -i KEY SOURCE TARGET`
- `scp -i ~/.ssh/montezer-tech610-key.pem ~/Downloads/nodejs20-sparta-test-app.zip
- Install Zip Package `sudo apt install unzip -y`
- Simply `Unzip filename` to unzip the file 

### To start App
- `npm install`
- `npm start`

### To access App
- Go Browser and type: `34.243.60.2:3000/`



## dfgdf
` sudo npm install pm2 -g`
`npm install`
`pm2 kill`
`pm2 start index.js`

### Install nginx
`sudo apt install nginx -y`

- proxy_pass http

`sudo systemctl restart nginx` - to restart a process
`sudo systemctl status nginx` - check for problems 
