# HackTactic
Software tool for a purple team that allows:  

    Deploying infrastructures  
    Launching attacks against them  
    Viewing attack results in ELK (from Suricata)
##################################################SETTINGS##################################################    
Create a database in PostgreSQL according to the config.py file in the backend section.
Change to your own PostgreSQL database credentials. 
Example: SQLALCHEMY_DATABASE_URI = 'postgresql://login:password@localhost:5433/attackbase'
- Make the deploy.sh and start-stop.sh scripts executable — use the command: chmod +x script_name
- Run the deploy.sh script — it will check and install dependencies required to run the software tool. 
- Run the start-stop.sh script — follow its instructions to start or stop the software tool. 
     
⚠️ IMPORTANT!  All scripts must be run by a user with root privileges . Also, the images folder must contain prepared virtual machine images! 
##################################################SETTINGS##################################################  



##################################################WORK EXAMPLES##################################################  
















##################################################WORK EXAMPLES##################################################  
