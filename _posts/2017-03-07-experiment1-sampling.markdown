---
layout: post
title:  "Experiments with GPIO - Continious sampling"
date:   2017-03-07
categories: raspberry_pi, gpio
---

# Continuous Sampling
A good oscilloscope is very expensive. Of course you build a digital one yourself with a Raspberry Pi, some wires and something to measure. In this experiment, I just use another Raspberry Pi to generate signals.

This oscilloscope can only handle digital signals and at a rather low frequency at that. The Python code uses wiringPi, which can sample at several MHz at the most. However, I think the main bottleneck will be the Python code itself.

One thing I will get bored of very easily is switching between Raspberries, moving cables around and logging in after restarts. So I will use the Paramiko library to SSH into the Raspberries, run the programs, collect the results and send them back to my laptop.

{% highlight python %}
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
{% highlight python %}
