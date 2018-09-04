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

#data1 = ('crm_hostserver','crm_hostserver01') 

data1 = ('10.10.3.108','10.10.3.109','10.10.3.102','10.10.2.21','10.10.2.23','10.10.2.24','10.10.3.107','10.10.2.22','10.10.3.10')
data2 = ('10.10.2.25','10.10.2.27','10.10.2.29','10.10.2.31','10.10.8.6','10.10.8.2')
data3 = ('10.10.8.8','10.10.3.18','10.10.2.19','10.10.3.20','10.10.3.21','10.10.2.10','10.10.3.201','10.10.8.4','10.10.3.11','10.10.2.12','10.10.3.12')
data4 = ('10.10.3.103','10.10.3.106','10.10.8.5','10.10.8.62','10.10.3.13','10.10.3.202','10.10.2.14','10.10.3.14','10.10.3.15','10.10.3.23','10.10.3.25')
data5 = ('10.10.3.28','10.10.8.60','10.10.8.61','10.10.2.19','10.10.2.16','10.10.2.17','10.10.3.17','10.10.2.15','10.10.3.22')
data6 = ('10.10.2.26','10.10.2.28','10.10.2.30','10.10.2.32','10.10.8.7','10.10.2.35','10.10.8.3')
def check():
    i = 0
    while i < 6:
        #print(i)
        host = 'crm_hostserver0%s'%(i)
        #print(host)
        if host == "crm_hostserver00":
            host = "crm_hostserver"
            for ip in data1:
                #print(ip)
                exec_sql(host,ip)
        elif host == "crm_hostserver01":
            for ip in data2:
                #print(ip)
                exec_sql(host,ip)
        elif host == "crm_hostserver02":
            for ip in data3:
                exec_sql(host,ip)
        elif host == "crm_hostserver03":
            for ip in data4:
                exec_sql(host,ip)
        elif host == "crm_hostserver04":
            for ip in data5:
                exec_sql(host,ip)
        else:
            for ip in data6:
                exec_sql(host,ip)
        i +=1

def exec_sql(host,ip):
     conn = pymysql.connect(host="10.10.3.201",port=3306,user="root", passwd="emFiYml4MTIzNDU2Cg==",db="crm_serverhosts",charset="utf8")
     print(host)
     print(ip)
     cmd=r'ping -c 1 %s > /dev/null && h=$? && echo $h'%(ip)
     status = os.system(cmd)
     print(status)
     value=0
     if status == value:
         up = "signed"
         mysql_cmd01="""SELECT status from %s where host='%s'"""%(host,ip)
         cur = conn.cursor()
         cur.execute(mysql_cmd01)
         result01 = cur.fetchall()[0][0]
         if up != result01:
             sql01="""UPDATE %s SET status='%s' WHERE host='%s'"""%(host,up,ip)
             print(sql01)
             cur.execute(sql01)
             conn.commit()
         else:
             pass
     else:
         down = "unregistered"
         print(down)
         mysql_cmd02="""SELECT status from %s where host='%s'"""%(host,ip)
         cur = conn.cursor()
         cur.execute(mysql_cmd02)
         result02 = cur.fetchall()[0][0]
         if down != result02:
             sql02="""UPDATE %s SET status='%s' WHERE host='%s'"""%(host,down,ip)
             print(sql02)
             cur.execute(sql02)
             conn.commit()
         else:
              pass
     cur.close()
     conn.close()

if __name__=='__main__':
    check()
