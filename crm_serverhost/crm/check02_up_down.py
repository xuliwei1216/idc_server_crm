#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#mysqldb
from pymysql import Connect
import pymysql
import os
import sys
import time
import datetime
import shutil
import unidecode
import subprocess

data = ('10.10.2.25','10.10.2.27','10.10.2.29','10.10.2.31','10.10.8.6','10.10.8.2')

def check():
    for ip in data:
        #print(ip)
        cmd=r'ping -c 2 %s > /dev/null && h=$? && echo $h'%(ip)
        #print(cmd)
        status = os.system(cmd)
        value=0
        if status == value:
            up = "signed"
            #print(up)
            conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
            mysql_cmd01="""SELECT status from crm_hostserver01 where host='%s'"""%(ip)
            #print(mysql_cmd01)
            cur = conn.cursor()
            #print("==================")
            cur.execute(mysql_cmd01)
            result01 = cur.fetchall()[0][0]
            #print(result01)
            #print('connect successful')
            if up != result01:
                sql01="""UPDATE crm_hostserver01 SET status='%s' WHERE host='%s'"""%(up,ip)
                #print(sql01)
                cur.execute(sql01)
                conn.commit()
                #print(result01)
            else:
                pass
            cur.close()
            conn.close()
            #print("==================")
        else:
            down = "unregistered"
            #print(down)
            conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
            mysql_cmd02="""SELECT status from crm_hostserver01 where host='%s'"""%(ip)
            #print(mysql_cmd02)
            cur = conn.cursor()
            #print("==================")
            cur.execute(mysql_cmd02)
            result02 = cur.fetchall()[0][0]
            #print(result02)
            #print('connect successful')
            if down != result02:
                sql02="""UPDATE crm_hostserver01 SET status='%s' WHERE host='%s'"""%(down,ip)
                #print(sql02)
                cur.execute(sql02)
                conn.commit()
                #print(result02)
            else:
                pass
            cur.close()
            conn.close()

if __name__=='__main__':
    check()
