#!/bin/bash

USERNAME="YOUR_LINUX_USER"
SERVERS=$(cat ${HOME}/before_patch_report/servers.txt)
SCRIPT_PATH="/home/${USERNAME}/before_patch_report/before_patch_check.py"
COMMAND_PATH="/home/${USERNAME}/before_patch_report/commands.sh"
REMOTE_PATH="/home/${USERNAME}"
PASSWORD_PATH="/home/${USERNAME}/before_patch_report/passwd.txt"

for server in ${SERVERS}
do
        echo "--------------------"
        echo "Connecting to ${server}..."
        sshpass -f ${PASSWORD_PATH} scp ${SCRIPT_PATH} ${USERNAME}@${server}:${REMOTE_PATH}
        if [ $? -ne 0 ]
        then
                echo "SCP Error in ${server}"
        else
                echo "SCP Done"
        fi
        sshpass -f ${PASSWORD_PATH} ssh ${USERNAME}@${server} < ${COMMAND_PATH}
        if [ $? -ne 0 ]
        then
                echo "SSH Error in ${server}"
        else
                echo "SSH Done"
        fi
done
