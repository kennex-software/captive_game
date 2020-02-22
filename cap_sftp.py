#! python 3
# kennex
# 

import pysftp

hostname = 'access795410207.webspace-data.io'
username = 'u98326309-captive'
password = 'e11r0c%G5ig!tD8AV'
port = 22

cnopts = pysftp.CnOpts()
#cnopts.hostkeys = None

with pysftp.Connection(host=hostname, port=port, username=username, password=password) as sftp:
    print('connection established')

    sftp.mkdir('niceee')
    dir = sftp.listdir()

    print(dir)



