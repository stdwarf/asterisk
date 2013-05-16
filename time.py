#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
from datetime import datetime
import time

con = None
price_con = 0.04
price_msk = 2
price_spb = 1.2

#disposition = 'ANSWERED'

try:

    con = psycopg2.connect(database='cdr2', user='asterisk')
    cur = con.cursor()
    cur.execute("SELECT calldate, src, dst,  disposition, billsec FROM tmp_2012  WHERE  billsec > 3  AND src != 'gsmSeven' LIMIT 1000")
#    cur.execute("SELECT calldate FROM tmp_2012  WHERE  billsec > 3  LIMIT 100")
    srca = cur.fetchall()
    for rec in srca:
        timer = rec[0]
        timer =timer.strftime("%Y-%m-%d %H:%M:%S+0400")
        timer = datetime.strptime(timer, "%Y-%m-%d %H:%M:%S+0400")
        date = timer.strftime('%d-%m-%Y')
        time = timer.strftime('%H-%M-%S')
        src = rec[1]
        client_code = src[:4]
        client_num = src[-4:]
        dst = rec[2]
        dst = dst[-9:]
        interval = rec[4]
        price = float(interval)
        price = (price*(float(price_msk)/60)) + price_con
        print "%10s %8s %4s %4s %10s %3s %s" % (date, time, client_code, client_num, dst, interval, price)
#       print "%s" % (timer)
except psycopg2.DatabaseError, e:
    print 'Error %s' % e
    sys.exit(1)


finally:
    if con:
        con.close()
