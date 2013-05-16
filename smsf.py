#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,re,sqlite,datetime
import smtplib
from smtplib import SMTP
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import parseaddr, formataddr



q="'"
# файл генерируемый для учета iccid sim карт
localpath='/var/lib/asterisk/scripts/iccid.txt'

smscmdre = re.compile(r'.{0,}p(?P<pin>\d{1,})#(?P<exten>\d{1,})#.{0,}')
inboxdir = '/var/spool/asterisk/smsincoming/'

# база данных смс
conn = sqlite.connect('/var/log/asterisk/polygator-sms.db',autocommit=True)
c = conn.cursor()

#данные для писем
emailbody = """SMS FROM: %s\r\nSENT: %s\r\n\r\n%s """ 
sent_from = 'root@gsm.lc'
sent_to =  'user@domain.lc'
server="mail1.domain.lc"


# функция отправки письма
def send_email(sender, recipient, subject, body):
    header_charset = 'UTF-8'
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            body.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    sender_name, sender_addr = parseaddr(sender)
    recipient_name, recipient_addr = parseaddr(recipient)

    sender_name = str(Header(unicode(sender_name), header_charset))
    recipient_name = str(Header(unicode(recipient_name), header_charset))

    sender_addr = sender_addr.encode('ascii')
    recipient_addr = recipient_addr.encode('ascii')

    msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
    msg['From'] = formataddr((sender_name, sender_addr))
    msg['To'] = formataddr((recipient_name, recipient_addr))
    msg['Subject'] = Header(unicode(subject), header_charset)

    smtp = smtplib.SMTP("msmail1.polo.lc")
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.close()


def escaper(string,symbols):
 for symbol in symbols: string = string.replace(symbol,'')
 return string





#with open(localpath) as inf:

# парсим файл 
fl = open(localpath,"r")
for line in fl.xreadlines():
    words = (line.split(' '))
    iccid = words[2]
    chan = words[1]
    f = float(iccid)
    if f == 0:
        continue
    else: 
        tablename = iccid.rstrip() + "-inbox" 
        #print tablename
# заходим в базу, получаем считываем данные
  c.execute("select msgid,oaname,sent,partid,part,partof,content from %s"  % (q + tablename + q) )
	data = c.fetchall()
	smshash = {}
	for row in data:
    	    if row[0] in smshash:
		smshash[row[0]].append(list(row))
	    else: 
		smshash[row[0]] = [ list( row ) ]
	smslist = []
	for smskey in smshash.keys():
	    if smshash[smskey][0][5] == len(smshash[smskey]):
    		smsmp = sorted(smshash[smskey], key = lambda node: node[4])
    		smslist.append( smsmp )
	for smsmp in smslist:
	    smsid = smsmp[0][0]
	    sender = smsmp[0][1]
	    sendtime = datetime.datetime.fromtimestamp(int(smsmp[0][2]))
	    smstext = ''
	    for x in smsmp: 
    		smstext+=escaper(x[6].decode('utf-8'),'\r\n')
    		#print smstext
    	        #print sender
    		#print sendtime

	    emailbody = """SMS FROM: %s\r\nSENT: %s\r\n\r\n%s """
    	    try:
#	    send_email("%s",'user@domain.lc', "%s", "%s" % (sender, sendtime, smstext) )
		send_email('%s<root@domain.lc>' % os.uname()[1], [' user@domain.lc ', ' user2@domain.lc '], iccid, emailbody % (sender, sendtime, smstext) )
    		#print 'Email sent'
	    except: 
		continue
	    try:
    		c.execute("delete from '%s' where msgid=%s;" % ( tablename, str(smsid) ) )
	    except: 
	        continue
	    try:
    		os.unlink( os.path.join(inboxdir,sms) )
    		
	    except: 
    		continue
    #print (' script DONE')
