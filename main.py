import logging
import time
from threading import Thread

import paramiko

clients = ['192.168.178.33', '192.168.178.34']
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
    ssh.connect(client, username=username, password=password)
    ftp = ssh.open_sftp()
    logging.info('Transferring requirements.txt')
    ftp.put('requirements.txt', 'requirements.txt', callback=done)
    logging.info('Installing dependencies...')
    exec_command(ssh=ssh, client=client, command="sudo pip3 install -r requirements.txt", join_lines=False)
    logging.info('Disconnecting from {}'.format(client))
    ftp.close()

    logging.info('Setup complete')


def copy_code(ssh=None, client='', file=''):
    ftp = ssh.open_sftp()
    logging.info('Transferring {} to {}'.format(file, client))
    ftp.put(file, file, callback=done)
    logging.info('Transfer done')
    logging.info('Disconnecting from {}'.format(client))
    ftp.close()


if __name__ == '__main__':
    # freeze_support()
    logging.basicConfig(format='%(asctime)s %(message)s', level='INFO')
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(clients[0], username=username, password=password)
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(clients[1], username=username, password=password)
    # setup(ssh=ssh, clients=clients)
    copy_code(ssh=ssh1, file='sender.py')
    copy_code(ssh=ssh2, file='receiver.py')
    logging.info('Transferring complete')
    time.sleep(2.5)
    logging.info('Create thread 1')
    p1 = Thread(target=exec_command,
                kwargs={'ssh': ssh1,
                        'command': 'sudo python3 sender.py',
                        'join_lines': True}
                )
    logging.info('Create thread 2')
    p2 = Thread(target=exec_command,
                kwargs={'ssh': ssh2,
                        'command': 'sudo python3 receiver.py',
                        'join_lines': True}
                )
    logging.info('Starting processes')
    p1.start()
    p2.start()
    time.sleep(10)
    logging.info('Disconnecting')
    ssh1.close()
    ssh2.close()
