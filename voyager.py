from pprint import pprint
import requests
import json
import pandas as pd
import csv
import urllib3
import schedule
import ast
import sys
import time
import http.client
import re
import urllib.request
import threading
from devicecontrol.voyager import Voyager
import http.client
import re
import urllib.request
import pymongo
import numpy as np





lst = ['date']
for k in range(1,9):
    cols = ['channel%d'%k]
    lst = lst + cols
f_voyager = open('voyager.csv', mode='a',encoding='utf-8',newline='')
csv_writer = csv.writer(f_voyager)
csv_writer.writerow(lst)
f_voyager.close()

def run_voyager():
    _headers = {
            "Content-type": "application/json"
            # "Accept": "application/json",
            # 'Cache-Control': 'no-cache'
    }
    device_list = ("voyager1", "voyager2")
    device_auth_dict = {
        "voyager1": ("cumulus", "CumulusLinux!"),
        "voyager2": ("cumulus", "CumulusLinux!"),
    }
    device_ip_dict = {"voyager1": "10.68.100.200", "voyager2": "10.68.100.201"}
    device_type_dict = {"voyager1": "voyager", "voyager2": "voyager"}
    device_url_dict = {
        "voyager1": "https://10.68.100.200:8080/nclu/v1/rpc",
        "voyager2": "https://10.68.100.201:8080/nclu/v1/rpc",
    }

    voyager1 = Voyager("voyager1", "10.68.100.200")
    voyager2 = Voyager("voyager2", "10.68.100.201")

    data1 = voyager1.show_transponder()
    data2 = voyager2.show_transponder()
    v1 = data1[0]
    v1_dict = json.loads(v1)
    v2 = data2[0]
    v2_dict = json.loads(v2)

    gsp = [None]*8
    m = [None]*8
    opt = [None]*8
    copt = [None]*8
    lf = [None]*8
    cipt = [None]*8
    ber = [None]*8
    osnr = [None]*8
    cd = [None]*8

    data = []
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())#system time
    now_time = [date]
    data = now_time + data

    for i in range(0,8):
        if i in range(0,4):
            gsp[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['grid_spacing']
            m[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['modulation']
            opt[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['output_power']
            copt[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['current_output_power']
            lf[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['laser_frequency']
            cipt[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['current_input_power']
            ber[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['current_ber']
            osnr[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['current_osnr']
            cd[i] = v1_dict['modules'][(i<=1)+0]['network_interfaces'][i%2]['current_cd']
        if i in range(4,8):
            gsp[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['grid_spacing']
            m[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['modulation']
            opt[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['output_power']
            copt[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['current_output_power']
            lf[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['laser_frequency']
            cipt[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['current_input_power']
            ber[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['current_ber']
            osnr[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['current_osnr']
            cd[i] = v2_dict['modules'][(i<=5)+0]['network_interfaces'][i%2]['current_cd']


        BER = [ber[i]] 

        data = data + BER

        i = i+1

    print(data)

    f = open('voyager.csv', mode='a',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(data)

    return data


if __name__ == '__main__':
       
    schedule.every(5).seconds.do(run_voyager)

    while True:
        schedule.run_pending() 