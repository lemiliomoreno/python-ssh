import subprocess as sp
import re
import time

BETWEEN_METHODS='--------------------'

commands = {'release' : [['/bin/cat', '/etc/os-release'], ['/bin/grep', 'PRETTY_NAME']],
            'qpk' : [['/usr/bin/rpm', '-qa'], ['sort', '-r']],
            'root_space' : [['/bin/df', '/'], ['/usr/bin/awk', 'NR==2 {print $5}']],
            'kernel' : [['/usr/bin/rpm', '-qa'], ['/usr/bin/sort', '-r']]
            }

regular_expressions = {'kernel' : ['kernel-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'firmware' : ['kernel-tools-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'devel' : ['kernel-headers-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'qpk' : ['qpk20[0-9]{4}', 1811]
                        }

release_strings = {'redhat' : 'red hat', 'centos' : 'centos', 'ubuntu' : 'ubuntu', 'fedora' : 'fedora'}

class server():

        def __init__(self):
                self.release = None
                self.qpk = None
                self.root_space = None
                self.kernel = {'kernel' : None, 'firmware' : None, 'devel' : None}

        def get_command_output(self, first_command, second_command):
                print("Sending command to the shell...")
                print("Command 1: {0}, command 2: {1}".format(first_command, second_command))

                p1 = sp.Popen(first_command, stdout=sp.PIPE)
                p2 = sp.Popen(second_command, stdin=p1.stdout, stdout=sp.PIPE)

                p1.stdout.close()

                output = p2.communicate()[0].decode('utf-8')

                return output

        def get_release(self, output):
                SEPARATOR_LOCATION=13
                if(re.search(release_strings['redhat'], output, re.I) or re.search(release_strings['centos'], output, re.I)): self.release = output[SEPARATOR_LOCATION:-2]
                else: self.release = False

        def start_server_check(self):
                self.get_release(self.get_command_output(commands['release'][0], commands['release'][1]))




a = server()
print(a.release, a.qpk, a.root_space, a.kernel)
a.start_server_check()
print(a.release, a.qpk, a.root_space, a.kernel)
