import subprocess as sp
import re
import time
import datetime

BETWEEN_METHODS='--------------------'

commands = {'hostname' : ['hostname', '-f'],
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

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

def get_command_output(first_command, second_command):
        #print("Sending command to the shell...")
        #print("Command 1: {0}, command 2: {1}".format(first_command, second_command))
        if(second_command == None):
                p1 = sp.Popen(first_command, stdout=sp.PIPE)

                return p1.communicate()[0].decode('utf-8')

        else:
                p1 = sp.Popen(first_command, stdout=sp.PIPE)
                p2 = sp.Popen(second_command, stdin=p1.stdout, stdout=sp.PIPE)

                p1.stdout.close()

                return p2.communicate()[0].decode('utf-8')
              
class server():

        def __init__(self):
                self.hostname = None
                self.release = None
                self.qpk = None
                self.qpk_status = None
                self.root_space = None
                self.kernel = {'kernel' : None, 'firmware' : None, 'devel' : None}
                self.repos = list()
                self.time_to_run = time.time()
                self.start_server_check()

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

                report = open("BeforePatchCheck.log", "a+")

                report.write('{0}\n'.format(BETWEEN_METHODS))
                report.write('{0}\n'.format(datetime.datetime.now()))
                report.write('Hostname: {0}\n'.format(self.hostname))
                report.write('Server release: {0}\n'.format(self.release))

                if(int(self.qpk[-4:]) < regular_expressions['qpk'][1]):
                        report.write('QPK version: {0}, needed version: {1}\n'.format(self.qpk, regular_expressions['qpk'][1]))
                        self.qpk_status = False
                else:
                        report.write('QPK version: {0}, no update needed\n'.format(self.qpk))
                        self.qpk_status = True

                if(self.root_space >= 85): report.write('Root space: {0}%, need more than 15% to patch\n'.format(abs(self.root_space-100)))
                else: report.write('Root space: {0}%\n'.format(abs(self.root_space-100)))

                if(int(self.kernel['kernel'][-3:]) < regular_expressions['kernel'][1]): report.write("Kernel: {0}, needed version: {1}\n".format(self.kernel['kernel'], regular_expressions['kernel'][1]))
                else: report.write('Kernel: {0}, no update needed\n'.format(self.kernel['kernel']))

                if(self.kernel['firmware'] == None):
                        report.write('No kernel-firmware detected\n')
                else:
                        if(int(self.kernel['firmware'][-3:]) < regular_expressions['firmware'][1]): report.write("Kernel-firmware: {0}, needed version: {1}\n".format(self.kernel['firmware'], regular_expressions['firmware'][1]))
                        else: report.write('Kernel-firmware: {0}, no update neeeded\n'.format(self.kernel['firmware']))

                if(self.kernel['devel'] == None):
                        report.write('No kernel-devel detected\n')
                else:
                        if(int(self.kernel['devel'][-3:]) < regular_expressions['devel'][1]): report.write('Kernel-devel: {0}, needed version: {1}\n'.format(self.kernel['devel'], regular_expressions['devel'][1]))
                        else: report.write('Kernel-devel: {0}, no update needed\n'.format(self.kernel['devel']))

                report.write('Repos in our scope (check for comments inside each one):\n')
                for x in range(0, len(self.repos)):
                        for y in range(0, len(self.repos[x])):
                                report.write('---{0}{1}\n'.format(commands['repos'][1], self.repos[x][y]))

                report.write('{0}\n'.format(BETWEEN_METHODS))
                report.write('It took {0:.4} seconds to run\n'.format(time.time()-self.time_to_run))
                report.close()

        def print_for_table(self):
                if(self.qpk_status):
                        print('{0:40}  {1:9}  {2}{3:3}{4}  {5:50}  {6}'.format(self.hostname, self.qpk, bcolors.OKGREEN, 'OK', bcolors.ENDC, self.release, self.time_to_run))
                else:
                        print('{0:40}  {1:9}  {2}{3:3}{4}  {5:50}  {6}'.format(self.hostname, self.qpk, bcolors.WARNING, 'OLD', bcolors.ENDC, self.release, self.time_to_run))

        def start_server_check(self):
                self.get_hostname(get_command_output(commands['hostname'], None))
                self.get_release(get_command_output(commands['release'], None))
                self.get_qpk(get_command_output(commands['qpk'][0], commands['qpk'][1]))
                self.get_root_space(get_command_output(commands['root_space'][0], commands['root_space'][1]))
                self.get_kernel(get_command_output(commands['kernel'][0], commands['kernel'][1]))
                self.get_repos(get_command_output(commands['repos'], None))
                self.make_report()
                self.print_for_table()

test_server = server()
