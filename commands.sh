#!/bin/bash

python ${HOME}/before_patch_check.py > ${HOME}/Before_Patch_Check.txt
cat ${HOME}/Before_Patch_Check.txt
rm ${HOME}/before_patch_check.py
