#coding: utf-8

import copy
import time

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
    
    def fuzze_by_template(self, fuzze_word_list):
        for target in Requests_fuzzer.FUZZE_TARGET:
            for res in self.get_fuzze_res(target, fuzze_word_list):
                yield res
    
    def get_fuzze_res(self, target, fuzze_word_list):
        if target in Requests_fuzzer.FUZZE_TARGET:            
            raw_value = getattr(self, target)            
            if isinstance(fuzze_word_list, basestring):
                fuzze_word_list = [fuzze_word_list, ]
            
            for word in fuzze_word_list:
                is_changed, word_changed = self.__fuzze(raw_value, word)
                
                if is_changed:
                    tmp = copy.deepcopy(self)
                    setattr(tmp, target, word_changed)                    
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
 