#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
import datetime
import time

con = None

#disposition = 'ANSWERED'
try:
     
     con = psycopg2.connect(database='asterisk', user='ast_user', password='pass')
     cur = con.cursor()
     cur.execute("SELECT calldate, src, dst, disposition, billsec FROM cdr  WHERE (CAST(calldate as TEXT)  LIKE '2013-02-%' OR CAST(calldate as TEXT) LIKE '2013-01-%') AND billsec > 0 AND dst LIKE '7_____%' AND src LIKE  '1849%'")
#    cur.execute("SELECT calldate FROM tmp_2012  WHERE  billsec > 3  LIMIT 100")
     srca = cur.fetchall()
     for rec in srca:
            timer = rec[0]
      date = datetime.date.strftime(timer, "%Y-%m-%d")
#      time = timer[11:19]
            src = rec[1]
            dst = rec[2]
            dst = dst[-11:]
            dur = rec[4]
	    print "%20s %s %s %s" % (date, src, dst, dur)
#	    print rec
except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)

finally:
    if con:
        con.close()
