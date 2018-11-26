import subprocess as sp
import re
import time

BETWEEN_METHODS='--------------------'

commands = {'hostname' : 'hostname',
                'release' : ['/bin/cat', '/etc/redhat-release'],
                'qpk' : [['/bin/rpm', '-qa'], ['/bin/sort', '-r']],
                'root_space' : [['/bin/df', '/'], ['/usr/bin/awk', 'NR==2 {print $5}']],
                'kernel' : [['/bin/rpm', '-qa'], ['/bin/sort', '-r']],
                'repos' : ['/bin/ls', '/etc/yum.repos.d/']
                }

regular_expressions = {'kernel' : ['kernel-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'firmware' : ['kernel-firmware-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'devel' : ['kernel-devel-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
                        'qpk' : ['qpk20[0-9]{4}', 1811]
                        }

release_strings = {'redhat' : 'red hat', 'centos' : 'centos', 'ubuntu' : 'ubuntu', 'fedora' : 'fedora'}

repos_strings = {'linxcoe' : 'linuxcoe-.*\.repo', 'hpit' : 'hpit-.*\.repo', 'btdt' : 'btdt-.*\.repo', 'epel' : 'epel.repo', 'rhel' : 'rhel-.*\.repo'}

class server():

        def __init__(self):
                self.hostname = None
                self.release = None
                self.qpk = None
                self.root_space = None
                self.kernel = {'kernel' : None, 'firmware' : None, 'devel' : None}
                self.repos = list()
                self.start_server_check()

        def get_command_output(self, first_command, second_command):
                print("Sending command to the shell...")
                print("Command 1: {0}, command 2: {1}".format(first_command, second_command))
                if(second_command == None):
                        p1 = sp.Popen(first_command, stdout=sp.PIPE)

                        return p1.communicate()[0].decode('utf-8')
                 else:
                        p1 = sp.Popen(first_command, stdout=sp.PIPE)
                        p2 = sp.Popen(second_command, stdin=p1.stdout, stdout=sp.PIPE)

                        p1.stdout.close()

                        return p2.communicate()[0].decode('utf-8')

        def get_hostname(self, output):
                self.hostname = output[:-1]

        def get_release(self, output):
                for regex in release_strings:
                        if(re.search(release_strings[regex], output, re.I)):
                                self.release = output[:-1]
                                break
                        else: self.release = "Release not in scope: " + output[:-1]

        def get_qpk(self, output):
                location = re.search(regular_expressions['qpk'][0], output)
                self.qpk = output[location.start():location.end()]

        def get_root_space(self, output):
                if(output[:3] == '100'): self.root_space = 100
                elif(output[1] == '%'): self.root_space = int(output[:1])
                else: self.root_space = int(output[:2])

        def get_kernel(self, output):
                location = re.search(regular_expressions['kernel'][0], output)
                self.kernel['kernel'] = output[location.start():location.end()]

                location = re.search(regular_expressions['firmware'][0], output)
                if(location != None):
                        self.kernel['firmware'] = output[location.start():location.end()]
                else:
                        self.kernel['firmware'] = None

                location = re.search(regular_expressions['devel'][0], output)
                if(location != None):
                        self.kernel['devel'] = output[location.start():location.end()]
                else:
                        self.kernel['firmware'] = None       
                        
        def get_repos(self, output):
                for regex in repos_strings:
                        self.repos.append(re.findall(repos_strings[regex], output, re.I))

        def make_report(self):
                print(BETWEEN_METHODS)

                print('Hostname: {0}'.format(self.hostname))

                print('Server release: {0}'.format(self.release))

                if(int(self.qpk[-4:]) < regular_expressions['qpk'][1]): print('QPK version: {0}, needed version: {1}'.format(self.qpk, regular_expressions['qpk'][1]))
                else: print('QPK version: {0}, no update needed'.format(self.qpk))

                if(self.root_space >= 85): print('Root space: {0}%, need more than 15% to patch'.format(abs(self.root_space-100)))
                else: print('Root space: {0}%'.format(abs(self.root_space-100)))

                if(int(self.kernel['kernel'][-3:]) < regular_expressions['kernel'][1]): print("Kernel: {0}, needed version: {1}".format(self.kernel['kernel'], regular_expressions['kernel'][1]))
                else: print('Kernel: {0}, no update needed'.format(self.kernel['kernel']))

                if(self.kernel['firmware'] == None):
                        print('No kernel-firmware detected')
                else:
                        if(int(self.kernel['firmware'][-3:]) < regular_expressions['firmware'][1]): print("Kernel-firmware: {0}, needed version: {1}".format(self.kernel['firmware'], regular_expressions['firmware'][1]))
                        else: print('Kernel-firmware: {0}, no update neeeded'.format(self.kernel['firmware']))

                if(self.kernel['devel'] == None):
                        print('No kernel-devel detected')
                else:
                        if(int(self.kernel['devel'][-3:]) < regular_expressions['devel'][1]): print('Kernel-devel: {0}, needed version: {1}'.format(self.kernel['devel'], regular_expressions['devel'][1]))
                        else: print('Kernel-devel: {0}, no update needed'.format(self.kernel['devel']))

                print('Repos in our scope (check for comments inside each one):')
                for x in range(0, len(self.repos)):
                        for y in range(0, len(self.repos[x])):
                                print('---{0}{1}'.format(commands['repos'][1], self.repos[x][y]))

                print(BETWEEN_METHODS)          

        def start_server_check(self):
                time_to_run = time.time()
                self.get_hostname(self.get_command_output(commands['hostname'], None))
                self.get_release(self.get_command_output(commands['release'], None))
                self.get_qpk(self.get_command_output(commands['qpk'][0], commands['qpk'][1]))
                self.get_root_space(self.get_command_output(commands['root_space'][0], commands['root_space'][1]))
                self.get_kernel(self.get_command_output(commands['kernel'][0], commands['kernel'][1]))
                self.get_repos(self.get_command_output(commands['repos'], None))
                self.make_report()
                print('It took {0:.4} seconds to run'.format(time.time()-time_to_run))

test_server = server()
