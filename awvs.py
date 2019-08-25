# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')

requests.packages.urllib3.disable_warnings()
tarurl = "https://awvs:port/"
apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


headers = {'Host':'ip:port',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           "X-Auth":apikey,
           "content-type": "application/json"}

def addtask(url=''):
    url = url.strip()
    data = {"address":url,"description":url,"criticality":"10"}
    try:
        response = requests.post(tarurl+"/api/v1/targets",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        print('add_tesk.....')
        print(result)
        print('target_id: '+result['target_id'])
        return result['target_id']
    except Exception as e:
        print(str(e))
        return

def startscan(task_id):
    data = {"target_id":task_id,"profile_id":"11111111-1111-1111-1111-111111111111","schedule": {"disable": False,"start_date":None,"time_sensitive": False}}
    try:
        response = requests.post(tarurl+"/api/v1/scans",data=json.dumps(data),headers=headers,timeout=30,verify=False)
        result = response.headers
        print('start_scan....')
        print(result)
        scan_id = result['Location'].split('/')[4]
        return scan_id
    except Exception as e:
        print(str(e))
        return

def get_scan_session(scan_id):
    try:
        response = requests.get(tarurl+"/api/v1/scans/"+scan_id,headers=headers,timeout=30,verify=False)
        result = json.loads(response.content)
        print('get_scan_sessoion...')
        print(result)
        scan_session_id = result['current_session']['scan_session_id']
        print('scan_session_id: '+scan_session_id)
        return scan_session_id
    except Exception as e:
        print(str(e))
        return

def get_scan_gk(scan_id,scan_session_id):
    try:
        response = requests.get(tarurl+"/api/v1/scans/"+scan_id+'/results/'+scan_session_id+'/statistics',headers=headers,timeout=60,verify=False)
        result = json.loads(response.content)
        print('get_scan_gk...')
        print(result)
        print('获取扫描概况包括状态: .............')
        print('status: '+result['status'])
        return result
    except:
        time.sleep(30)
        return "notcompleted"


def get_report_url(scan_id):
    data = {"template_id":"11111111-1111-1111-1111-111111111112","source":{"list_type":"scans","id_list":[scan_id]}}
    try:
        response = requests.post(tarurl+"/api/v1/reports",data=json.dumps(data),headers=headers,timeout=60,verify=False)
        result = response.headers
        print(result)
        report = result['Location'].replace('/api/v1/reports/','/reports/download/')
        print(report)
        return tarurl.rstrip('/')+report+'.html'
    except Exception as e:
        print(str(e))
        return ""

def down_report(url):
    r = requests.get(url, verify=False)
    with open("report.html", "wb") as code:
        code.write(r.content)

def scan(url):
    target_id = addtask(url)
    scan_id = startscan(target_id)
    time.sleep(2)
    scan_session_id = get_scan_session(scan_id)

    gk = get_scan_gk(scan_id,scan_session_id)
    while gk['status'] !='completed':
        if gk['status'] == 'failed':
            break
        time.sleep(60)
        try:
            gk = get_scan_gk(scan_id,scan_session_id)
            print('没有完成扫描: status: '+gk['status'])
        except:
            pass
    print('完成扫描........')
    print('获取报告')
    report_url = get_report_url(scan_id)
    print('报告地址: '+report_url)
    #down_report(report_url)
    print('报告保存完成....')
    return  report_url

def get_url_list(filename):
    url_list = []
    try:
        f = open(filename, 'r')
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            url_list.append(line)
        return url_list
    except:
        print("[-][Error]: Get url.txt failed!")
        sys.exit("Exit!")

if __name__ == '__main__':
    url_list = get_url_list('url.txt')
    for url in url_list:
        report_url = scan(url)
        if report_url == "":
            report_url = scan(url)
