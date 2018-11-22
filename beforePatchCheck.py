# For Popen() and communicate()
import subprocess as sp
# For the REGEX comparison
import re
# To calculate the time it take to run the full script
import time

BETWEEN_METHODS='--------------------'

# This are the commands that are we going to use with the method 'get_command_output'
# If it only has one value, the second parameter when calling the method, MUST be None
commands = {'release' : ['/bin/cat', '/etc/redhat-release'],
		'qpk' : [['/usr/bin/rpm', '-qa'], ['sort', '-r']],
		'root_space' : [['/bin/df', '/'], ['/usr/bin/awk', 'NR==2 {print $5}']],
		'kernel' : [['/usr/bin/rpm', '-qa'], ['/usr/bin/sort', '-r']],
		'repos' : ['/usr/bin/ls', '/etc/yum.repos.d/']
		}

# This are the regular expressions that we are going to use to compare with the output, 
# the variable 'regular_expressions' has a key, that is referenced with the method that
# is going to use, and the values:
# [0] -> regular expressions to use and compare with the output of the command 
# [1] -> version to compare with the output of the command
regular_expressions = {'kernel' : ['kernel-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
			'firmware' : ['kernel-tools-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
			'devel' : ['kernel-headers-[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}-[0-9]{1,3}', 754],
			'qpk' : ['glibc', 1811]
			#'qpk' : ['qpk20[0-9]{4}', '1811']
			}

# Release strings, are going to be used in 'get_release' to compare it with the actual release
release_strings = {'redhat' : 'red hat', 'centos' : 'centos', 'ubuntu' : 'ubuntu', 'fedora' : 'fedora'}

# This REGEX are going to be used to look for the repos that are in our scope, 
# in '/etc/yum.repos.d
repos_strings = {'linxcoe' : 'redhat.*\.repo', 'hpit' : 'hpit'}

class server():
	# Constructor of the class, all initialize in None
	def __init__(self):
		self.release = None
		self.qpk = None
		self.root_space = None
		self.kernel = {'kernel' : None, 'firmware' : None, 'devel' : None}
		self.repos = list()
		self.start_server_check()

	# This is going to send the commands to the shell, if the second command
	# is None, it will only going to execute the first command and return output,
	# if is True, it will execute both commands and return the output
	# The output is using decode('utf-8') so we can read the binary output
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
					  
	# It will iterate between the releases allowed in 'release_string' dictionary
	def get_release(self, output):
		for item in release_strings:
			if(re.search(release_strings[item], output, re.I)): 
				self.release = output[:-1]
				break
			else: self.release = "Release not in scope: " + output[:-1]
	
	# It will return the qpk version, with start() and end() we prevent unnecessary text
	# to be stored in self.qpk
	def get_qpk(self, output):
		location = re.search(regular_expressions['qpk'][0], output)
		self.qpk = output[location.start():location.end()]

	# If the root_space is 100%, it will return an integer 100, if not, it will only cast
	# the string to integer and return it
	def get_root_space(self, output):
		if(output[:3] == '100'): self.root_space = 100
		else: self.root_space = int(output[:2])

	def get_kernel(self, output):
		location = re.search(regular_expressions['kernel'][0], output)
		self.kernel['kernel'] = output[location.start():location.end()]

		location = re.search(regular_expressions['firmware'][0], output)
		self.kernel['firmware'] = output[location.start():location.end()]

		location = re.search(regular_expressions['devel'][0], output)
		self.kernel['devel'] = output[location.start():location.end()]

	# It will iterate between the repos allowed in 'repos_strings', and return them as
	# a string
	def get_repos(self, output):
		for regex in repos_strings:
			self.repos.append(re.findall(repos_strings[regex], output, re.I))

	def make_report(self):
		print(BETWEEN_METHODS)

		print('Server release: {0}'.format(self.release))
		print('QPK version: {0}'.format(self.qpk))

		# It will compare the root_space and return the space left, that's why we use abs()
		if(self.root_space >= 85): print('Root space: {0}%, need more than 15% to patch'.format(abs(self.root_space-100)))
		else: print('Root space: {0}%'.format(abs(self.root_space-100)))

		# It will compare the version of the kernel with the las 3 numbers of the string,
		# for example, we got kernel-3.10.0-957, it will compare only the 957, that's why
		# we use an array with [-3:]
		if(int(self.kernel['kernel'][-3:]) < regular_expressions['kernel'][1]): print("Kernel: {0}, needed version: {1}".format(self.kernel['kernel'], regular_expressions['kernel'][1]))
		else: print('Kernel: {0}, no update needed'.format(self.kernel['kernel']))

		if(int(self.kernel['firmware'][-3:]) < regular_expressions['firmware'][1]): print("Kernel-firmware: {0}, needed version: {1}".format(self.kernel['firmware'], regular_expressions['firmware'][1]))
		else: print('Kernel-firmware: {0}, no update neeeded'.format(self.kernel['firmware']))

		if(int(self.kernel['devel'][-3:]) < regular_expressions['devel'][1]): print('Kernel-devel: {0}, needed version: {1}'.format(self.kernel['devel'], regular_expressions['devel'][1]))
		else: print('Kernel-devel: {0}, no update needed'.format(self.kernel['devel']))

		# It will print the repos in our scope allowed by 'repos_strings', it's iterating in 
		# two for loops, because when we use append, it store it like:
		# a = [1, 2, 3]
		# a.append([4, 5, 6])
		# print(a) -> [1, 2, 3, [4, 5, 6]]
		print('Repos in our scope (check for comments inside each one):')
		for x in range(0, len(self.repos)): 
			for y in range(0, len(self.repos[x])): 
				print('---{0}{1}'.format(commands['repos'][1], self.repos[x][y]))
				
		print(BETWEEN_METHODS)

	def start_server_check(self):
		time_to_run = time.time()
		self.get_release(self.get_command_output(commands['release'], None))
		self.get_qpk(self.get_command_output(commands['qpk'][0], commands['qpk'][1]))
		self.get_root_space(self.get_command_output(commands['root_space'][0], commands['root_space'][1]))
		self.get_kernel(self.get_command_output(commands['kernel'][0], commands['kernel'][1]))
		self.get_repos(self.get_command_output(commands['repos'], None))	
		self.make_report()
		print('It took {0:.4} seconds to run'.format(time.time()-time_to_run))

test_server = server()
