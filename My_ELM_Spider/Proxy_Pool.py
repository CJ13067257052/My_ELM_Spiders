import random


class ProxyPool(object):
    def the_proxy(self):
        proxy = []
        with open('D:/2_文件存档/3_Scrapy/Proxy_Ip_Pool/data2.json') as f:
            for i in f:
                if i[11:-3]:
                    proxy.append(i[11:-3])
        return random.choice(proxy)

    def choice(self):
        return self.the_proxy()