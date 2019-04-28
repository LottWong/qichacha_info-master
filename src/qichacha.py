#!/usr/bin/python
# coding:utf-8

"""
Author:honel521
Email:546501664@qq.com
===========================================
CopyRight:
===========================================
"""
import os
import sys
import json
import time
import logging
from bs4 import BeautifulSoup
from SpiderTool import Request

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/.." % cur_dir)


class Qcc(object):
    def __init__(self, url, company, proxies=[]):
        self.url = url.format(company)
        self.spider = Request.Request(proxies=[])
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        }

    def get_detailList(self):
        '多个数据'
        home_html = self.spider.get(self.url, headers=self.header)
        for detail_url, name in self.parser_home_html(home_html.text):
            detail_html = self.spider.get(detail_url, headers=self.header)
            self.parser_firm_html(detail_html.text, name)


    def parser_home_html(self, html):
        '解析多个数据'
        soup = BeautifulSoup(html, 'lxml')
        try:
            for i in soup.find('section', id='searchlist').find('tbody').find_all('tr'):
                try:
                    print(i.find('a', 'ma_h1').get_text())
                    yield 'http://www.qichacha.com' + i.find('a', 'ma_h1')['href'], i.find('a', 'ma_h1').get_text()
                except:
                    print(i.find('a', 'ma_h1').get_text(),
                          i.find('span', 'nstatus text-warning m-l-xs').get_text().strip())
        except:
            print('没有查到该公司')


    def get_index(self):
        '取一条'
        html = self.spider.get(self.url, headers=self.header)
        soup = BeautifulSoup(html.text, 'lxml')
        tr = soup.find('section', id='searchlist').find('tbody').find_all('tr')[0]
        name = tr.find('a', 'ma_h1').get_text()
        firm_url = 'http://www.qichacha.com' + tr.find('a', 'ma_h1')['href']
        own_url = firm_url.replace("firm","own")
        firm_html = self.spider.get(firm_url, headers=self.header)
        own_html = self.spider.get(own_url, headers=self.header)

        '返回的数据'
        return_dic = {}
        return_dic['name'] = name
        self.parser_own_html(own_html.text, return_dic)
        self.parser_firm_html(firm_html.text, return_dic)
        return return_dic

    def parser_firm_html(self, html, dic):
        '''解析firm页信息'''
        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('tr')
        # legalPersonName 
        try:
            dic['legalPersonName'] = soup.find('a', 'bname').get_text()
        except:
            dic['legalPersonName'] = ''

        # regLocation 
        try:
            dic['regLocation'] = content[9].find_all(
                'td')[1].get_text().strip().split('查看地图')[0].strip()
        except:
            dic['regLocation'] = ''

        # regManager 
        try:
            dic['regManager'] = content[5].find_all(
                'td')[3].get_text().strip()
        except:
            dic['regManager'] = ''

        return dic

    def parser_own_html(self, html, dic):
        '''解析own页信息'''
        soup = BeautifulSoup(html, 'lxml')
        # contact 
        try:
            dic['contact'] = soup.find('div', 'dcontent').find_all('div')[0].find('span','fc').find_all('span')[1].get_text().strip()
        except:
            dic['contact'] = ''
        return dic


def test():
    """unittest"""
    qcc = Qcc("http://www.qichacha.com/search?key={}", "腾讯")
    dic = qcc.get_index()
    print(dic)


if __name__ == '__main__':
    test()
