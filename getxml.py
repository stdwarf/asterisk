#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import psycopg2
import datetime

import smtplib
import base64
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

#import gevent
#from gevent import monkey; monkey.patch_all()
import os,sys,re,paramiko,time
from paramiko import SSHClient
from paramiko import AutoAddPolicy

d=datetime.datetime.now()
date=datetime.datetime.strftime(d,"%Y-%m-%d")
user = 'root'
passwd = 'XXXXX'
port = 22
host = ('127.0.0.1')
remotepath='/tmp/format.xls'
localpath='/var/lib/asterisk/agi-bin/Monitoring_Voip/format_'+ date + '.xls'
cmd = "/bin/sleep3 ; /var/lib/asterisk/scripts/analizeUT.py; /bin/sleep 3"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
q="'"

 
try:
    ssh.connect(host, port=22, username="root", password='XXXXX')
    print "connected.."
    print "generating EXCEL " + host
    ssh.exec_command(cmd)
    time.sleep(10)
except:
  print "Error connecting to host " + host
  ssh.close()
	
try:
#    localpath='/var/lib/asterisk/scripts/iccid.txt.'+host
    transport = paramiko.Transport((host, 22))
    print 'get '+ localpath + ' from '+ host
    transport.connect(username="root", password='XXXXXXX')
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remotepath, localpath)
    time.sleep(1)
    sftp.close()
    transport.close()
except:
    print "Error sftp from host " + host
    con = None




#-------------------------------------------------------------------------------
sent_from = 'root@pbx-ng'
sent_to = 'XXXXX@YYYYY.lc'
f=localpath
s='Мониторинг группы телефонии 1'

#subject = s.decode('cp1251').encode('utf-8')
subject = s
print type(s),subject

t='Результаты мониторинга смотрите во вложении'
#text= t.decode('cp1251').encode('utf-8')
text= t
print type(s),text
server="msmail1.domain.lc"

#def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
#    assert type(send_to)==list
#    assert type(files)==list

    

msg = MIMEMultipart()
msg['From'] = sent_from
msg['To'] = sent_to
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = subject.decode('utf-8')
        
msg.attach( MIMEText(text))
part = MIMEBase('application', "octet-stream")
part.set_payload( open(f,"rb").read() )
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
msg.attach(part)

smtp = smtplib.SMTP(server)
smtp.sendmail(sent_from, sent_to, msg.as_string())
smtp.close()


#=-------------------------------------------------------------------------------
