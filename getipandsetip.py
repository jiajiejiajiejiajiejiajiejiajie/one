import os
import time

import requests
import re
class getip_and_setip():
    last_ip='0.0.0.0'
    def getip(self):
        res=requests.get('https://2023.ip138.com/',headers={'Host':'2023.ip138.com',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'sec-ch-ua':'"GoogleChrome";v="117","Not;A=Brand";v="8","Chromium";v="117"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':'"Windows"',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/117.0.0.0Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-User':'?1',
    'Sec-Fetch-Dest':'document',
    'Accept-Encoding':'gzip,deflate,br',
    'Accept-Language':'zh-CN,zh;q=0.9,de;q=0.8'
        })
        # print(res.text)
        r=re.findall(r'''<title>您的IP地址是：(.*)</title>''',res.text)
        if r:
            return (r[0])
        return None
    def getip2(self):
        res=requests.get("https://qifu-api.baidubce.com/ip/local/geo/v1/district?")
        # print(res.json())
        r=res.json().get('ip',None)
        return r
    def setip(self,ip):
        if(not ip):
            print('获取IP失败')
            return
        if (ip==self.last_ip):
            print('IP不变')
            return
        print(ip,self.last_ip)
        with open('testurl.txt','w') as f:
            f.write('''http://{}:3000'''.format(ip))
            f.close()
            print('保存成功')
            self.last_ip=ip
            os.system("git add testurl.txt | git commit -m '说明'  |git push")

if __name__ == '__main__':
    gas = getip_and_setip()
    while True:
        ip=gas.getip2()
        if not ip:
            print('获取138ip')
            ip = gas.getip()
        gas.setip(ip)
        time.sleep(6)
