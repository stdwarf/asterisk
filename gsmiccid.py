#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import datetime

#import gevent
#from gevent import monkey; monkey.patch_all()
import os,sys,re,paramiko,time
from paramiko import SSHClient
from paramiko import AutoAddPolicy

user = 'root'
passwd = 'passWord'
port = 22
hosts = ('IP','IP2','IP')
remotepath='/var/lib/asterisk/scripts/iccid.txt'
localpath=()
cmd = "/bin/sh //var/lib/asterisk/scripts/geticcid.sh"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(AutoAddPolicy())
q="'"

for host in hosts: 
    try:
  ssh.connect(host, port=22, username="root", password='passWord')
  print "connected.."
	print "creating local file on " + host
	ssh.exec_command(cmd)
	time.sleep(3)
    except:
	print "Error connecting to host " + host
	ssh.close()

for host in hosts: 
    try:
	localpath='/var/lib/asterisk/scripts/iccid.txt.'+host
	transport = paramiko.Transport((host, 22))
	print 'get '+ localpath + ' from '+ host
	transport.connect(username="root", password='passWord')
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get(remotepath, localpath)
	time.sleep(3)
	sftp.close()
	transport.close()
    except:
	print "Error sftp from host " + host

con = None

#disposition = 'ANSWERED'

try:
    con = psycopg2.connect(database='gsm', user='asterisk', password='passWord2')
    cur = con.cursor()
    for host in hosts:
	localpath='/var/lib/asterisk/scripts/iccid.txt.'+host
	with open(localpath) as inf:
	    line_words = (line.split(' ') for line in inf)
	    for words in line_words:
#		print words
		iccid = words[2]
	        gsmchan = words[1]
		gsmgate = words[0]
	 	cur.execute("UPDATE gsmsms SET iccid=" + q + iccid + q + " WHERE gsmchan=" + q + gsmchan + q + " AND gsmgate=" + q + gsmgate + q )
		print "UPDATE gsmsms SET iccid=" + q + iccid + q + " WHERE gsmchan=" + q + gsmchan + q + " AND gsmgate=" + q + gsmgate + q
#		cur.execute("INSERT INTO gsmsms (gsmgate, gsmchan, iccid) VALUES (%s, %s, %s);" % (q + gsmgate + q, q + gsmchan + q, q + iccid + q))
#		print "INSERT INTO gsmsms (gsmgate, gsmchan, iccid) VALUES (%s, %s, %s)" % (q + gsmgate + q, q + gsmchan + q, q + iccid + q)
        con.commit()

except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
    
    
finally:
    
    if con:
        con.close()
