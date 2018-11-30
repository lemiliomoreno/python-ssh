# python-ssh
SSH connection to retrieve server information with Python and Bash

### Development
To retrieve the project and work from another host:
```
$ git clone https://github.com/lemiliomoreno/python-ssh.git
```
When doing this, you will still need to create the *passwd.txt* and *servers.txt* files.

### Creating files and directories needed
To start working with this script, you will need first to copy the source files and directories for the script to work, for that, we should use the following commands from 'itxadmin':
```
$ mkdir ~/before_patch_report
$ pbrun bash
# cp /home/morenodl/before_patch_report/before_patch_check.py /home/morenodl/before_patch_report/commands.sh /home/morenodl/before_patch_report/what_to_do.sh ~/before_patch_report/
# exit
```
If you got a problem with the permissions, you can change to root, use the ```cp``` command and then change to normal user.

Then we should create the *servers.txt* and *login.sh*, I recommend saving *login.sh* in a hidden folder:
```
$ touch ~/before_patch_report/servers.txt
$ mkdir ~/before_patch_report/.private_files
$ touch ~/before_patch_report/.private_files/login.sh
```
Running these commands, we should got the following directories:
```
before_patch_report/
├── before_patch_check.py   # Script to run in the server
├── commands.sh             # Commands that are going to run thru SSH
├── .private_files
│   └── login.sh            # Password of your account (may change when private key supported)
├── servers.txt             # List of servers to check
└── what_to_do.sh           # Configuration of SSH connection and username 
```
### Configuration files
When all the files are created, we need to change the configuration file *login.sh* in order to start working with the script, we should open it:
```
$ vim ~/before_patch_report/.private_files/login.shh
```
We will see the following variables:
```
USERNAME="username"
PASSWORD="password"
```
In this file you will change these two variables so they match with your Linux account credentials.

You should change the permissions of that file so it cannot be accessed by other users:
```
$ chmod 400 ~/before_patch_report/.private_files/login.sh
```

**NOTE**: If you want to store the login.sh file in another place, you should modify the file *what_to_do.sh*:
```
source YOUR_LOGIN.SH_PATH   # This is without quotes
```

Next, you should put the list of servers that are going to be checked in *servers.txt*:
```
$ vim ~/before_patch_report/servers.txt
```
Add them like this:
```
server1.hostname.com
server2.hostname.com
server3.hostname.com
server4.hostname.com
```
and save the file.

Before running the script, make sure you have the files *commands.sh* and *what_to_do.sh* in executable mode, if not:
```
$ chmod 750 ~/before_patch_report/commands.sh ~/before_patch_report/what_to_do.sh
```
### Running the script
To run the script, you should only run the following commands:
```
$ cd ~
$ ./before_patch_report/what_to_do.sh
```
This will create a file called:
> BeforePatchReport.log

this is going to be stored in the server checked, it saves the server information.

Where you run the script (itxadmin) it will output like this:
```
server1.hostname.com  qpk20xxxx Release
server2.hostname.com  qpk20xxxx Release
server3.hostname.com  qpk20xxxx Release
server4.hostname.com  qpk20xxxx Release
```
