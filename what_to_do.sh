#!/bin/bash

source .private_files/login.sh

SERVERS=$(cat ~/before_patch_report/servers.txt)
SCRIPT_PATH="${HOME}/before_patch_report/before_patch_check.py"
COMMAND_PATH="${HOME}/before_patch_report/commands.sh"
REMOTE_PATH="/home/${USERNAME}"
PASSWORD_PATH="${HOME}/before_patch_report/.private_files/passwd.txt"

for server in ${SERVERS}
do
        sshpass -p ${PASSWORD} scp -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${SCRIPT_PATH} ${USERNAME}@${server}:${REMOTE_PATH}
        if [ $? -ne 0 ]
        then
                echo "SCP Error in ${server}"
        fi
        sshpass -p ${PASSWORD} ssh -T -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${USERNAME}@${server} < ${COMMAND_PATH}
        if [ $? -ne 0 ]
        then
                echo "SSH Error in ${server}"
        fi
done
