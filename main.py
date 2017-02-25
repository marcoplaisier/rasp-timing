import logging
from threading import Thread

import paramiko
from multiprocessing import Process

from multiprocessing import freeze_support

import time

clients = ['192.168.178.33', '192.168.178.34']
username = 'pi'
password = 'raspberry'


def done(bytes_done, bytes_to_go):
    logging.info('Sent: {} bytes. Total: {} bytes'.format(bytes_done, bytes_to_go))


def exec_command(ssh=None, client='', command='', join_lines=False):
    logging.info('Attempting to {} on {}'.format(command, client))
    ssh.connect(client, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    if join_lines:
        stdout_text = client + ':' + ''.join(stdout.readlines())
        logging.info(stdout_text)
        stderr_text = client + ':' + ''.join(stderr.readlines())
        logging.info(stderr_text)
    else:
        for line in stdout.readlines():
            logging.info(client + ':' + line.rstrip())
        for line in stderr.readlines():
            logging.info(client + ':' + line.rstrip())
    logging.info('Disconnecting from {}'.format(client))
    ssh.close()


def setup(ssh=None, clients=[]):
    for client in clients:
        logging.info("Connecting to {}".format(client))
        ssh.connect(client, username=username, password=password)
        ftp = ssh.open_sftp()
        logging.info('Transferring requirements.txt')
        ftp.put('requirements.txt', 'requirements.txt', callback=done)
        logging.info('Installing dependencies...')
        exec_command(ssh=ssh, client=client, command="sudo pip3 install -r requirements.txt", join_lines=False)
        logging.info('Disconnecting from {}'.format(client))
        ftp.close()
        ssh.close()

    logging.info('Setup complete')


def copy_code(ssh=None, client='', file=''):
    ssh.connect(client, username=username, password=password)
    ftp = ssh.open_sftp()
    logging.info('Transferring {} to {}'.format(file, client))
    ftp.put(file, file, callback=done)
    logging.info('Transfer done')
    logging.info('Disconnecting from {}'.format(client))
    ftp.close()
    ssh.close()


if __name__ == '__main__':
    freeze_support()
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    ssh1 = paramiko.SSHClient()
    ssh2 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # setup(ssh=ssh, clients=clients)
    copy_code(ssh=ssh1, client=clients[0], file='sender.py')
    copy_code(ssh=ssh2, client=clients[1], file='receiver.py')
    logging.info('Transferring complete')
    time.sleep(5)
    logging.info('Create thread 1')
    p1 = Thread(target=exec_command,
                kwargs={'ssh': ssh1,
                        'client': clients[0],
                        'command': 'sudo python3 sender.py',
                        'join_lines': True}
                )
    logging.info('Create thread 2')
    p2 = Thread(target=exec_command,
                kwargs={'ssh': ssh2,
                        'client': clients[1],
                        'command': 'sudo python3 receiver.py',
                        'join_lines': True}
                )
    logging.info('Starting processes')
    p1.start()
    p2.start()

