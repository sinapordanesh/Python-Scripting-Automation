# Copyright (C) 2023 BLACK HAT PYTHON, Modified By Saman Pordanesh

import paramiko

"""
    makes a connection to an SSH server and runs a single command.
"""
def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
    # set the policyto accept the SSH key for the SSH server we’re connecting to
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    # run the command 3 that we passed in the call to the ssh_command function.
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    # if the command produced output -> print each line of the output
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    # use it to get the username/password from the current environment
    import getpass
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ') or '192.168.1.203'
    port = input('Enter port or <CR>: ') or 2222
    cmd = input('Enter command or <CR>: ') or 'id'
    # run and send requestd variables to be executed
    ssh_command(ip, port, user, password, cmd)