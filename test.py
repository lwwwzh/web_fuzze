#coding=utf-8

from requests import Request, Session

class requests_fuzzer(object):
    FUZZE_TARGET  = ('method', 'url', 'params', 'headers', 'data')
    
    def __init__(self, method = None, url = None, params = None, headers = None, data = None):
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.data = data
    
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
    
    def fuzze_request(self, fuzze_list, target=None):
        for fuzze_item in fuzze_list:
            
            target_list = self.FUZZE_TARGET
            if target :
                target_list = target
                
            for fuzze_target in target_list:                    
                for fuzze_item in fuzze_list:
                
                    req = Request(method=self.__method, url=self.__url, headers=self.__headers, 
                                  data=self.__data, params=self.__params)
            
        
            yield req
        
    
    