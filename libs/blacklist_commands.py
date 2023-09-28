harmful_prompts = [
  'rename',  # Existing commands
  'delete',
  'remove',
  'shutdown',
  'reboot',
  'format',
  'halt',
  'poweroff',
  'remove file',
  'remove folder',
  'remove directory',
  'delete file',
  'delete folder',
  'delete directory',
  'rename file',
  'rename folder',
  'rename directory',
  'move file',
  'move folder',
  'move directory',
  'replace file',
  'replace folder',
  'replace directory',
  'exit',  # Additional harmful prompts
  'quit',
  'vanish',
  'null',
  'void',
  'wipe',
  'erase',
  'obliterate',
  'discard',
  'purge',
  'exterminate',
  'terminate',
  'expunge',
  'eliminate',
  'kill file',
  'kill folder',
  'kill directory',
  'destroy file',
  'destroy folder',
  'destroy directory',
  'nullify file',
  'nullify folder',
  'nullify directory',
  'void file',
  'void folder',
  'void directory',
  'change file',
  'change folder',
  'change directory',
  'shift file',
  'shift folder',
  'shift directory',
   # Standalone commands
  'remove', 
  'delete',
  'rename',
  'move',
  'replace',
  'kill',
  'destroy',
  'nullify',
  'void',
  'change',
  'shift',
   # Blacklisted files
  'bardcode_interpreter.py', 
  'bardcoder.py',
  'bardcoder_lib.py',
  'bardcoder',
  'bardcoder_lib',
  'bardcode_interpreter',
  'blacklist_commands.py',
  'blacklist_commands',
  'requirements.txt',
  'clear_cache.sh',
  'code_runner.sh'
]

harmful_commands_python = [
    # Existing commands
  'cut',
  'dig',
  'kedit',
  'ftp',
  'iwconfig',
  'pkill',
  'whois',
  'scp',
  'chgrp',
  'nc',
  'traceroute',
  'pgrep',
  'mv',
  'move',
  'replace',
  'chdir',
  'rename',
  'kate',
  'arp',
  'route',
  'host',
  'curl',
  'ncat.openbsd',
  'nmap',
  'ncat.traditional',
  'htop',
  'ls',
  'netstat',
  'ping',
  'sudo',
  'cd',
  'mousepad',
  'wireshark',
  'wget',
  'chown',
  'ps',
  'tcpdump',
  'grep',
  'netcat',
  'nc.openbsd',
  'mkdir',
  'cp',
  'mac',
  'nslookup',
  'sftp',
  'top',
  'format',
  'ifconfig',
  'nc.traditional',
  'ip',
  'nano',
  'ssh',
  'chmod',
  'vim',
  'kill',
  'rm',
  'ss',
  'restart',
  'telnet',
  'kwrite',
  'cat',
  'ncat',
  'rsync',
  'delete',
  'deleted',
  'remove',
  'shutdown',
  'reboot',
  'append',
  'appended',
  'remove',
  'removed',
  'rmdir',
  'rmtree',
  'shutil.rmtree',
  'subprocess.call',
  'eval',
  'exec',
  'unlink',
  'pathlib.unlink',
  '_exit',
  'abort',
  'kill',
  'fork',
  'execl',
  'execle',
  'execlp',
  'execlpe',
  'execv',
  'execve',
  'execvp',
  'execvpe',
  'popen',
  'popen2',
  'popen3',
  'popen4',
  'startfile',
  'spawnl',
  'spawnle',
  'spawnlp',
  'spawnlpe',
  'spawnv',
  'spawnve',
  'spawnvp',
  'spawnvpe',
  'write(\"\")',
  'write(\'\')',
  'write(NULL)',
  'write(0)',
  'os.remove',
  'os.rmdir',
  'os.removedirs',
  'os.unlink',
  'os.rename',
  'os.renames',
  'os.system',
  'os.chdir',
  'os.mkdir',
  'os.makedirs',
  # Blacklisted files
  'bardcode_interpreter.py',  
  'bardcoder.py',
  'bardcoder_lib.py',
  'bardcoder',
  'bardcoder_lib',
  'bardcode_interpreter',
  'blacklist_commands.py',
  'blacklist_commands',
  'requirements.txt',
  'clear_cache.sh',
  'code_runner.sh'
  'dd',  # Additional shell commands  # Can be used to write and backup raw disk images
  'gksudo',  # Graphical sudo
  'lshw',  # Can reveal hardware details
  'lspci',  # Can reveal PCI devices
  'lsusb',  # Can reveal USB devices
  'dmidecode',  # Can reveal system details
  'hdparm',  # Can change hard drive settings
  'iptables',  # Can manipulate network traffic rules
  'passwd',  # Can change user passwords
  'useradd',
  'userdel',
  'adduser',
  'deluser',  # Can manipulate user accounts
  'gpasswd',  # Can change group passwords
  'groupadd',
  'groupdel',
  'addgroup',
  'delgroup',  # Can manipulate group accounts
  'crontab',  # Can schedule tasks
  'mount',
  'umount',  # Can mount and unmount file systems
  'nohup',  # Can keep processes running after their parent process ends
  'reboot',
  'halt',
  'poweroff',  # Can shutdown or reboot the system
  'su',
  'sudo',  # Can run commands as other users
  'chsh',  # Can change the default shell
  'chfn',  # Can change the user's full name
  'chage',  # Can change password expiry
  'chpasswd',  # Can change passwords
  'chroot',  # Can change the root directory
  'chrt',  # Can change process scheduling
  'crontab',  # Can schedule tasks
  'date',  # Can change the system date and time
  'dd',  # Can write and backup raw disk images
  'dmesg',  # Can show kernel messages
  'fdisk',  # Can manipulate disk partitions
  'fsck',  # Can check and repair file systems
  'fuser',  # Can show which processes are using a file
  'hdparm',  # Can change hard drive settings
  'kill',  # Can send signals to processes
  'killall',  # Can send signals to processes by name
  'last',  # Can show recent logins
  'lastlog',  # Can show recent logins
  'lsof',  # Can show which files are open by which processes
  'lsusb',  # Can show USB devices
  'lspci',  # Can show PCI devices
  'lsmod',  # Can show kernel modules
  'modinfo',  # Can show kernel module details
  'modprobe',  # Can load and unload kernel modules
  'mount',  # Can mount file systems
  'netstat',  # Can show network statistics
  'nice',  # Can change process priority
  'pstree',  # Can show running processes as a tree
  'pickle',  # Can execute arbitrary code during unpickling
  'os.popen',  # Can be used to execute shell commands
  'os.startfile',  # Can be used to start a file with its associated application
  'os.exec*',  # Any function starting with 'os.exec' can be used to execute different programs
  'os.spawn*',  # Any function starting with 'os.spawn' can be used to spawn new process using os-level commands
  'os.fork',  # Can be used to create new processes
  'os.kill',  # Can be used to send signals to processes
  'socket',  # Can be used to create network connections
  'ctypes',  # Can be used to call C functions in Python programs
  'gc.get_objects',  # Can be used to inspect objects currently in memory
  'os.setuid',  # Can be used to set the current process's user id
  'os.setgid',  # Can be used to set the current process's group id
  'os.chroot',  # Can be used to change the root directory of the current process
  'os.chmod',  # Can be used to change file permissions
  'os.chown',  # Can be used to change file ownership
  'os.chflags',  # Can be used to change file flags
  'os.chroot',  # Can be used to change the root directory of the current process
  'os.seteuid',  # Can be used to set the current process's effective user id
  'os.setegid',  # Can be used to set the current process's effective group id
  'os.setreuid',  # Can be used to set the current process's real and effective user id
  'os.setregid',  # Can be used to set the current process's real and effective group id
  'os.setresuid',  # Can be used to set the current process's real, effective, and saved user id
]

harmful_commands_cpp = [
  "remove",  # Existing commands
  "std::remove",
  "remove_all",
  "ilesystem::remove_all",
  "filesystem::remove",
  "rename",
  "std::rename",
  "filesystem::rename",
  "std::system",
  "abort",
  "std::abort",
  "exit",
  "std::exit",
  "move",
  "std::move",
  "filesystem::move",
  "std::ofstream",
  "std::quick_exit",
  "ios::app",
  "trunc",
  "ios::trunc",
  "std::ios::app",
  "std::ios::trunc",
  "std::filesystem::remove",
  "std::_Exit",
  "fp << NULL",
  'fp << "" <<',
  "file << NULL",
  'file << "" <<',
  "std::system_clock::now().time_since_epoch().count()",
  "std::chrono::system_clock::now().time_since_epoch().count()",
  "std::system(\"rm -rf",
  "std::system(\"format",
  "std::system(\"curl",
  "system",  # Additional commands # Executes an shell command
  "popen",  # Can open a process by creating apipe, forking, and invoking the shell
  "_popen",  # Windows version of popen
  "WinExec",  # Can run a command
  "ShellExecute",  # Can run a command
  "fork",  # Can be used to create new processes
  "execl",
  "execlp",
  "execle",
  "execv",
  "execvp",
  "execvpe",  # Can be used to execute different programs
  "spawnl",
  "spawnlp",
  "spawnle",
  "spawnv",
  "spawnvp",
  "spawnvpe",  # Can be used to spawn new process using os-level commands
  "kill",  # Can be used to send signals to processes
  "raise",  # Can be used to send a signal to the current process
  "socket",  # Can be used to create network connections
  "setuid",  # Can be used to set the current process's user id
  "setgid",  # Can be used to set the current process's group id
  "chroot",  # Can be used to change the root directory of the current process
]


# define method to get the list of harmful prompts
def get_harmful_prompts():
  return harmful_prompts


# define method to get the list of harmful commands for python
def get_harmful_commands_python():
  return harmful_commands_python


# define method to get the list of harmful commands for cpp
def get_harmful_commands_cpp():
  return harmful_commands_cpp
