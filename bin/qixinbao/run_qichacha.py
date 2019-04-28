#!/usr/bin/python
# coding:utf-8

"""
Author:honel521
Email:546501664@qq.com
===========================================
CopyRight
===========================================
"""
import random
import time
import os
import sys
import json
import multiprocessing

cur_dir = os.path.split(os.path.realpath(__file__))[0]
sys.path.append("%s/../.." % cur_dir)
from src.qichacha import Qcc


def target(name, arvg1):
    qcc = Qcc("http://www.qichacha.com/search?key={}", name, proxies=[
        "http://honel521:538ad8-385c51-b63230-0482e5-cfd54a@megaproxy.rotating.proxyrack.net:222"])
    dic = qcc.get_index()
    with open(arvg1+'.txt', "a") as f:
        f.write(json.dumps(dic, ensure_ascii=False) + "\n")


def run(arvg1):
    pool = multiprocessing.Pool(4)
    for index, one in enumerate(open(arvg1+'.json', encoding='utf-8')):
        dic = eval(one)
        name = dic['entName']
        pool.apply_async(target, args=(name, arvg1))
    pool.close()
    pool.join()


if __name__ == '__main__':
    run(sys.argv[1])
