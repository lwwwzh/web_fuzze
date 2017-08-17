#coding=utf-8

import copy

from fuzzer import Requests_fuzzer

fzzr = Requests_fuzzer(method='get', url='http://www.baidu.com', params='a={*}&b=123')

for res in fzzr.get_fuzze_res('params', ['1', '2', '3']):
    print res.request.url
