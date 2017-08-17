#coding=utf-8

import copy
import time
import re

from requests import Request, Session

class Requests_fuzzer(object):
    
    FUZZE_TARGET  = ('method', 'url', 'params', 'headers', 'data')
    
    def __init__(self, method = None, url = None, params = None, headers = None, data = None, delay=1.5, template = '{*}'):
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.data = data
        
        self.delay = delay
        self.template = template
    
    def get_fuzze_res(self, target, fuzze_word_list):
        if target in Requests_fuzzer.FUZZE_TARGET:            
            raw_value = getattr(self, target)
            tmp = copy.deepcopy(self)
            
            for word in fuzze_word_list:
                changed, _2_change = self.__fuzze(raw_value, word)
                
                if changed:
                    setattr(tmp, target, _2_change)
                    
                    yield tmp.__send_request()
                    time.sleep(self.__delay)
                
    def __send_request(self):
        session = Session()
        req = Request(method=self.method, url=self.url, headers=self.headers, data=self.data, 
                      params=self.params)        
        prep = session.prepare_request(req)
        
        is_delay = False        
        try:
            res = session.send(prep)
        except Exception, e:
            is_delay = True
            res = None
                
        return res, is_delay
    
    def __fuzze(self, raw, fuzze_item):
        res = raw        
        if isinstance(raw, basestring):
            res = raw.replace(self.__template, fuzze_item)     
            
        elif isinstance(raw, dict):
            res = {}            
            for key, value in raw.iteritems():
                key = key.replace(self.__template, fuzze_item)
                value = value.replace(self.__template, fuzze_item)
                res[key] = value
                
        elif isinstance(raw, (tuple, list)):
            res  = []
            for item in  raw:
                item = item.replace(self.__template, fuzze_item)
                res.append(item)
        
        changed = False
        if res != raw:
            changed = True
        
        return changed, res
    
    @property
    def method(self):
        return self.__method
    
    @method.setter
    def method(self, value):
        self.__method = value
    
    @property
    def url(self):
        return self.__url
    
    @url.setter
    def url(self, value):
        self.__url = value
    
    @property    
    def params(self):
        return self.__params
    
    @params.setter
    def params(self, value):
        self.__params = value
    
    @property
    def headers(self):
        return self.__headers
    
    @headers.setter
    def headers(self, value):
        self.__headers = value
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, value):
        self.__data = value
    
    @property    
    def delay(self):
        return self.__delay
    
    @delay.setter
    def delay(self, value):
        self.__delay = value
        
    @property
    def template(self):
        return self.__template
    
    @template.setter
    def template(self, value):
        self.__template = value
 

    VALID_PARAM = ('123', 'okff', '1ok2')
    INVALID_PARAM = ('union select',)
     
    



class Base_caler(object):
    
    CAL_DIMENSION = ('status', 'length', 'title', 'delay', 'invalid_keyword')
    
    TITLE_PATTERN = re.compile(r'<title>(.*?)</title>')
    INVALID_KEYWORLD = (u'造成安全威胁', u'疑似黑客攻击', u'创宇盾', u'不合法参数', u'D盾', u'提交的内容包含危险')    
    
    
    def deal_res(self, res, is_delay):        
        result = {}
        
        result['status'] = res.status_code
        result['length'] = len(res.text)
        result['title'] = self.TITLE_PATTERN.findall(res.text)[0]
        result['delay'] = is_delay
        
        is_valid = True
        for invalid_word in self.INVALID_KEYWORLD:
            if invalid_word in res.text:
                is_valid = False
                break            
        result[invalid_keyword] = is_valid
        
        return result
    
    def study(self, req_type, res, is_delay):
        pass
    
    def cal_res(self, res, is_delay):
        pass
        