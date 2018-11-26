#!/bin/bash

USERNAME="morenodl"
SERVERS=$(cat ${HOME}/before_patch_report/servers.txt)
SCRIPT_PATH="/home/${USERNAME}/before_patch_report/before_patch_check.py"
COMMAND_PATH="/home/${USERNAME}/before_patch_report/commands.sh"
REMOTE_PATH="/home/${USERNAME}"

for server in ${SERVERS}
do
        echo "--------------------"
        echo "Connecting to ${server}..."
        scp ${SCRIPT_PATH} ${USERNAME}@${server}:${REMOTE_PATH}
        ssh ${USERNAME}@${server} < ${COMMAND_PATH}
done
