#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'xuliwei'
from pymysql import Connect
import pymysql
import os
import sys
import time
import datetime
import shutil
import unidecode
import subprocess

data = ('10.10.3.108','10.10.3.109','10.10.3.102','10.10.2.21','10.10.2.23','10.10.2.24','10.10.3.107','10.10.2.22','10.10.3.10')

def check():
    conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
    for ip in data:
        #print(ip)
        cmd=r'ping -c 1 %s > /dev/null && h=$? && echo $h'%(ip)
        #print(cmd)
        status = os.system(cmd)
        value=0
        if status == value:
            up = "signed"
            #print(up)
            #conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
            mysql_cmd01="""SELECT status from crm_hostserver where host='%s'"""%(ip)
            #print(mysql_cmd01)
            cur = conn.cursor()
            #print("==================")
            cur.execute(mysql_cmd01)
            result01 = cur.fetchall()[0][0]
            #print(result01)
            #print('connect successful')
            if up != result01:
                sql01="""UPDATE crm_hostserver SET status='%s' WHERE host='%s'"""%(up,ip)
                print(sql01)
                cur.execute(sql01)
                conn.commit()
                print(result01)
            else:
                pass
            #cur.close()
            #conn.close()
            #print("==================")
        else:
            down = "unregistered"
            #print(down)
            #conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
            mysql_cmd02="""SELECT status from crm_hostserver where host='%s'"""%(ip)
            #print(mysql_cmd02)
            cur = conn.cursor()
            #print("==================")
            cur.execute(mysql_cmd02)
            result02 = cur.fetchall()[0][0]
            #print(result02)
            #print('connect successful')
            if down != result02:
                sql02="""UPDATE crm_hostserver SET status='%s' WHERE host='%s'"""%(down,ip)
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
