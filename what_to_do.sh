#!/bin/bash

USERNAME="x-lmorenoduran"
SERVERS=$(cat /home/morenodl/before_patch_report/servers.txt)
SCRIPT_PATH="/home/morenodl/before_patch_report/before_patch_check.py"
COMMAND_PATH="/home/morenodl/before_patch_report/commands.sh"
REMOTE_PATH="/home/${USERNAME}"
PASSWORD_PATH="/home/morenodl/before_patch_report/passwd.txt"

for server in ${SERVERS}
do
        sshpass -f ${PASSWORD_PATH} scp -o StrictHostKeyChecking=no ${SCRIPT_PATH} ${USERNAME}@${server}:${REMOTE_PATH}
        if [ $? -ne 0 ]
        then
                echo "SCP Error in ${server}"
        fi
        sshpass -f ${PASSWORD_PATH} ssh -T -o StrictHostKeyChecking=no ${USERNAME}@${server} < ${COMMAND_PATH}
        if [ $? -ne 0 ]
        then
                echo "SSH Error in ${server}"
        fi
done
