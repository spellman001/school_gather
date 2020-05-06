# -*- encoding: utf-8 -*-"
'''
@Descripttion: 
@version: 
@Author: small_fafa
@Date: 2020-05-06 18:39:52
@LastEditors: small_fafa
@LastEditTime: 2020-05-06 22:30:32
'''
import requests, sys
from bs4 import BeautifulSoup

def filter_website(func):
    def _func1(*args, **kwargs):
        data = func(*args)
        tmp = []
        for i in data:
            if len(i[2]) != 0:
                tmp.append([str(x).strip() for x in i])
        
        return tmp
    
    return _func1


class pinyinconvert:
    
    def __init__(self, word):
        self.app_key = "3F21038EDDB73C2FABBE1A88A70C77EF"
        self.word = word
        self.base_url = "http://hn216.api.yesapi.cn/?&s=Ext.Pinyin.Convert"
    
    def _url(self):
        url = "{}&app_key={}&text={}".format(
            self.base_url,
            self.app_key,
            self.word
        )
        return url
    
    def to(self):
        req = requests.get(url=self._url())
        json_data = req.json()
        if json_data['ret'] == 200:
            return json_data['data']['pinyin'].replace(' ', '')


class school:

    def __init__(self, subdomain):
        self.url = "http://{}.xuexiaodaquan.com/".format(subdomain)
        self.school_type = [
                                'youeryuan', 'xiaoxue',
                                'chuzhong', 'gaozhong',
                                'daxue', 'chengrenjiaoyu',
                                'peixunjigou'
                            ]

    def _request(self, url):
        req = requests.get(url)
        req.encoding='gbk'
        soup = BeautifulSoup(req.text, 'lxml')
        return soup
    
    def obtain_last_page(self, soup):
        try:
            a_value = soup.find(name='a', attrs={'class':'last'})['href']
            page_num = a_value.split('/')[-1].split('.')[0][2:]
            return int(page_num)
        except TypeError:
            return 2


    def obtain_school_info(self, soup):
        s_list = []
        info_div = soup.find(name='div', attrs={'class': 'list-xx clearfix'})
        uls = info_div.find_all(name='ul')
        school_names = info_div.find_all(name='p')
        for ul in uls:
            school_name = school_names[uls.index(ul)].a.text
            tmp = [i.span.text for i in ul.find_all(name="li")]
            tmp.append(school_name)
            s_list.append(tmp)

        return s_list

    def obtain_urls(self):
        tmp = []
        for type in self.school_type:
            base_url = "{}{}/".format(
                self.url,
                type
            )
            soup = self._request(base_url)
            last_page = self.obtain_last_page(soup)
            for i in range(1, last_page):
                if i == 1:
                    tmp.append(base_url)
                else:
                    url = "{}pn{}.html".format(base_url, i)
                    tmp.append(url)
        
        return tmp

    @filter_website
    def main(self):
        tmp = []
        urls = self.obtain_urls()
        for url in urls:
            soup = self._request(url)
            tmp += self.obtain_school_info(soup)
            
        return tmp
                    
    

if __name__ == "__main__":
    print("这脚本跑一到两次, 出现NoneType ,就差不多被封IP了 请自行注意 -_-!" + "\r\n")
    region = sys.argv[1]
    subdomain = pinyinconvert(region).to()
    s = school(subdomain)
    r = s.main()
    for i in r:
        i.reverse()
        print('-'.join(i))
    print('\r\n')
    print("total: {}".format(len(r)))