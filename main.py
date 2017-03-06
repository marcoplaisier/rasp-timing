import logging
import time
from threading import Thread

import paramiko

clients = ['192.168.178.37']
username = 'pi'
password = 'raspberry'


def done(bytes_done, bytes_to_go):
    logging.info('Sent: {} bytes. Total: {} bytes'.format(bytes_done, bytes_to_go))


def exec_command(ssh=None, command='', join_lines=False):
    logging.info('Attempting to {}'.format(command))
    stdin, stdout, stderr = ssh.exec_command(command)
    if join_lines:
        stdout_text = ''.join(stdout.readlines())
        logging.info(stdout_text)
        stderr_text = ''.join(stderr.readlines())
        logging.info(stderr_text)
    else:
        for line in stdout.readlines():
            logging.info(line.rstrip())
        for line in stderr.readlines():
            logging.info(line.rstrip())
    logging.info('Command {} done'.format(command))

def setup(ssh=None, client=''):
    logging.info("Connecting to {}".format(client))
    logging.info("Installing wiringPi...")
    exec_command(ssh=ssh1, command='git clone git://git.drogon.net/wiringPi')
    exec_command(ssh=ssh1, command='cd /home/pi/wiringPi; sudo /bin/bash build')
    logging.info("Installing wiringPi done")
    ftp = ssh.open_sftp()
    logging.info('Transferring requirements.txt')
    ftp.put('requirements.txt', 'requirements.txt', callback=done)
    logging.info('Installing dependencies...')
    exec_command(ssh=ssh, command="sudo pip3 install -r requirements.txt", join_lines=False)
    logging.info('Disconnecting from {}'.format(client))
    ftp.close()
    logging.info('Setup complete')


def copy_code(ssh=None, file=''):
    ftp = ssh.open_sftp()
    logging.info('Transferring {}'.format(file))
    ftp.put(file, file, callback=done)
    logging.info('Transfer done')
    logging.info('Disconnecting FTP')
    ftp.close()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(clients[0], username=username, password=password)
    # setup(ssh=ssh1, client=clients[0])
    copy_code(ssh1, file='test_print.py')
    # exec_command(ssh=ssh1, command='sudo python3 test_print.py', join_lines=True)