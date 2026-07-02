# Deploying Apps

1. Create the instance
    - What type of instance? * (Size / OS)
    - Key pairs 
    - Configure a security group *
        - SSH on isolated IP Address
        - HTTP (80) all? 
        - Other ports? *
2. Copy across source code (e.g using `scp`) and deployment script maybe? 
3. SSH into VM 
4. (Change permissions on script if needed)
5. Run deployment script!
    1. Check for updates and install them
   2. Install any dependancies *
        - Packages needed for other steps in the automation 
        - Packages / Software needed to run the app 
   3. Start / launch the application 
   4. Configure nginx as a reverse proxy / port forwarding
   5. Restart nginx 