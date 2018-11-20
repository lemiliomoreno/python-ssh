#!/bin/bash

OUTPUT=$(python /home/emilio/python_devel/beforePatchingCheck/before_patch_report.py)
DATE=$(date)
SUBJECT="Before patching report ${DATE}"
FROM="lemiliomoreno@gmail.com"
RECIPIENTS="my_email@company.com"

MAIL="subject:${SUBJECT}\nfrom:${FROM}\n${OUTPUT}"

echo -e "${MAIL}" | sendmail ${RECIPIENTS}

if [ $? -ne 0 ]; then
        echo "Error sending message, /var/log/maillog:"
        tail -n 10 /var/log/maillog
else
        echo "Message sent."
fi
