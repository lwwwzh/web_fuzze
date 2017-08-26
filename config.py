#coding: utf-8

class Fuzze_config:
    METHOD = 'GET'
    URL = 'http://www.ccbn.tv/?a={*}'
    PARAMS = ''
    HEADERS = {}
    DATA = ''
    
    DELAY = 1.5
    TEMPLATE = '{*}'
    
    PAYLOAD_2_FUZZE = 'union select'
    GOOD_FUZZE = 'hello_world'
    BAD_FUZZE = 'union select'