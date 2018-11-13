import subprocess as sp
import re
import time

BETWEEN_METHODS="--------------------"
KERNEL_ACTUAL_REGEX="kernel-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}"
KERNEL_FIRMWARE_ACTUAL_REGEX="kernel-tools-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}"
KERNEL_DEVEL_ACTUAL_REGEX="kernel-headers-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}"
KERNEL_ACTUAL_VERSION=754
KERNEL_FIRMWARE_ACTUAL_VERSION=754
KERNEL_DEVEL_ACTUAL_VERSION=999

def checking_server_release():
        print("Checking the server release...")
        SEPARATOR_LOCATION=13
        first_for_release_check = ['/bin/cat', '/etc/os-release']
        second_for_release_check = ['/bin/grep', 'PRETTY_NAME']

        redhat_string = "red hat"
        centos_string = "centos"
        ubuntu_string = "ubuntu"

        p1 = sp.Popen(first_for_release_check, stdout=sp.PIPE)
        p2 = sp.Popen(second_for_release_check, stdin=p1.stdout, stdout=sp.PIPE)

        p1.stdout.close()

        release = p2.communicate()[0].decode('utf-8')

        if(re.search(redhat_string, release, re.I) or re.search(centos_string, release, re.I)): print("OK_TO_PATCH: Release is in scope: {0}.".format(release[SEPARATOR_LOCATION:-2]))
        else: print("CANT_PATCH: Release isn't in scope: {0}.".format(release[SEPARATOR_LOCATION:-2]))

        p2.stdout.close()

def checking_for_root_space():
        print("Checking if /root has more than 20% space available...")
        first_for_root_check = ['/bin/df', '/']
        second_for_root_check = ['/usr/bin/awk', 'NR==2 {print $5}']

        p1 = sp.Popen(first_for_root_check, stdout=sp.PIPE)
        # stdin of p2, will be the p1.stdout
        p2 = sp.Popen(second_for_root_check, stdin=p1.stdout, stdout=sp.PIPE)

        # Closing p1.stdout so p2.stdin can receive it properly
        p1.stdout.close()

        # Access to communicate()[0] because is stdout, comminucate()[1] is stdeer, it returns a tuple
        # communicate() returns (stdout, stderr)
        root_space = p2.communicate()[0].decode('utf-8')

        if(root_space[:3] == '100'): print("CANT_PATCH: Root (/) has {0}% space left, need more than 20%.".format(int(root_space[:3]) - 100))
        elif(int(root_space[:2]) >= 80): print("CANT_PATCH: Root (/) has {0}% space left, need more than 20%.".format(abs(int(root_space[:2]) - 100)))
        else: print("OK_TO_PATCH: Root (/) has {0}% space left.".format(abs(int(root_space[:2]) - 100)))

        p2.stdout.close()
        
def checking_for_kernel_versions():
        print("Checking which kernel versions are needed...")
        first_for_kernel_check = ['/usr/bin/rpm', '-qa']
        second_for_kernel_check = ['/usr/bin/sort', '-r']
        third_for_kernel_check =['/usr/bin/awk', '/^kernel-[0-9]\.*/ {print $1; exit}']

        p1 = sp.Popen(first_for_kernel_check, stdout=sp.PIPE)
        p2 = sp.Popen(second_for_kernel_check, stdin=p1.stdout, stdout=sp.PIPE)

        p1.stdout.close()

        first_output = p2.communicate()[0].decode('utf-8')

        kernel_string = re.search(KERNEL_ACTUAL_REGEX, first_output)
        kernel_version = int(first_output[kernel_string.end()-3:kernel_string.end()])

        kernel_firmware_string = re.search(KERNEL_FIRMWARE_ACTUAL_REGEX, first_output)
        kernel_firmware_version = int(first_output[kernel_firmware_string.end()-3:kernel_firmware_string.end()])

        kernel_devel_string = re.search(KERNEL_DEVEL_ACTUAL_REGEX, first_output)
        kernel_devel_version = int(first_output[kernel_devel_string.end()-3:kernel_devel_string.end()])

        print("Actual kernel installed: {0}.".format(first_output[kernel_string.start():kernel_string.end()]))

        if(kernel_version < KERNEL_ACTUAL_VERSION): print("NEED KERNEL UPDATE: Actual: {0}, Needed: {1}.".format(kernel_version, KERNEL_ACTUAL_VERSION))
        else: print("NO KERNEL UPDATE NEEDED:  Actual: {0}, Needed: {1}.".format(kernel_version, KERNEL_ACTUAL_VERSION))

        print("Actual kernel-firmware installed: {0}.".format(first_output[kernel_firmware_string.start():kernel_firmware_string.end()]))

        if(kernel_firmware_version < KERNEL_FIRMWARE_ACTUAL_VERSION): print("NEED KERNEL FIRMWARE UPDATE: Actual: {0}, Needed: {1}.".format(kernel_firmware_version, KERNEL_FIRMWARE_ACTUAL_VERSION))
        else: print("NO KERNEL FIRMWARE UPDATE NEEDED: Actual: {0}, Needed: {1}.".format(kernel_firmware_version, KERNEL_FIRMWARE_ACTUAL_VERSION))

        print("Actual kernel-devel installed: {0}.".format(first_output[kernel_devel_string.start():kernel_devel_string.end()]))

        if(kernel_devel_version < KERNEL_DEVEL_ACTUAL_VERSION): print("NEED KERNEL DEVEL UPDATE: Actual: {0}, Needed: {1}.".format(kernel_devel_version, KERNEL_DEVEL_ACTUAL_VERSION))
        else: print("NO KERNEL DEVEL UPDATE NEEDED: Actual: {0}, Needed: {1}.".format(kernel_devel_version, KERNEL_DEVEL_ACTUAL_VERSION))

        p2.stdout.close()    
        
def start_script():
        print(BETWEEN_METHODS)
        start_time = time.time()
        print("STARTED AT: {0}.".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))))

        print(BETWEEN_METHODS)
        checking_server_release()

        print(BETWEEN_METHODS)
        checking_for_root_space()

        print(BETWEEN_METHODS)
        checking_for_kernel_versions()

        print(BETWEEN_METHODS)
        finish_time = time.time()
        print("FINISHED AT: {0}.".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(finish_time))))
        finish_time -= start_time
        print("It took {0:.4f} seconds to run.".format(finish_time))
        print(BETWEEN_METHODS)

start_script()        
