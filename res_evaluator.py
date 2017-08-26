#coding: utf-8

import re

class Base_evaluator(object):

    DIMENSION_WEIGHT = {}
    CAL_TOTAL_WEIGHT = 10
    
    def cal_weight(self, res, *other_args):           
        result = {}
        
        dimension_list = self.DIMENSION_WEIGHT.keys()
        for dimension in dimension_list:
            meth = getattr(self, 'cal_%s' % dimension)
            result[dimension] = meth(res, other_args)
            
        return result
    
    def is_like(self, res_1, res_2):
        result = 0
        
        dimension_list = self.DIMENSION_WEIGHT.keys()
        for dimension in dimension_list:
            var_1 = res_1[dimension]
            var_2 = res_2[dimension]
            
            cal_meth = getattr(self, 'is_like_%s' % dimension)            
            result = result + cal_meth(var_1, var_2) * self.DIMENSION_WEIGHT[dimension]
        
        result = float(result) / self.CAL_TOTAL_WEIGHT
        if result > 1:
            result = 1
        return result

        
class Res_evaluator(Base_evaluator):

    TITLE_PATTERN = re.compile(r'<title>(.*?)</title>')
    INVALID_KEYWORLD = (u'造成安全威胁', u'疑似黑客攻击', u'创宇盾', u'不合法参数', u'D盾', u'提交的内容包含危险')    

    VALID_PARAM = ('123', 'okff', '1ok2')
    INVALID_PARAM = ('union select',)

    DIMENSION_WEIGHT = {
        'status': 3,
        'length': 3,
        'title': 3,
        'delay': 1,
        'invalid_keyword': 5,
    }
    
    def cal_status(self, res, *is_delay):
        return res.status_code
    
    def is_like_status(self, status_1, status_2):
        status_1 = int(status_1)
        status_2 = int(status_2)
        
        if status_1 == status_2:
            return 1
        elif -10 < status_1 - status_2 < 10:
            return abs(status_1-status_2)/10.0
        else:
            return 0
    
    def cal_length(self, res, *is_delay):
        return len(res.text)
    
    def is_like_length(self, length_1, length_2):
        if length_1 < length_2:
            length_1, length_2 = length_2, length_1
        
        if length_1 == length_2 :
            return 1
        elif length_1*0.85 < length_2 :
            return float(length_2) / length_1
        else:
            return 0
    
    def cal_title(self, res, *is_delay):
        try:
            result = self.TITLE_PATTERN.findall(res.text)[0]
        except:
            result = None
            
        return result
    
    def is_like_title(self, title_1, title_2):
        if title_1 == title_2:
            return 1
        else:
            return 0
    
    def cal_delay(self, res, *is_delay):
        try:
            return is_delay[0][0]            
        except:
            return False
    
    def is_like_delay(self, delay_1, delay_2):
        if delay_1 == delay_2:
            return 1
        else:
            return 0    
    
    def cal_invalid_keyword(self, res, *is_delay):
        result = None
        
        for invalid_word in self.INVALID_KEYWORLD:
            if invalid_word in res.text:
                result = invalid_word
                break            
        
        return result
    
    def is_like_invalid_keyword(self, invalid_word_1, invalid_word_2):
        if invalid_word_1 and invalid_word_1 == invalid_word_2:
            return 1
        else:
            return 0    

def test():
    cal = Res_evaluator()
    
    import requests
    import time
    
    url = 'http://www.bp.gov.cn/news/?id=56172'
    _headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    }
    
    res1 = requests.get('%s' % url, headers=_headers)
    print res1.request.headers
    #print res1.text
    
    time.sleep(1)
    res3 = requests.get('%s&b=113' % url, headers=_headers)    
    
    time.sleep(1)
    res2 = requests.get('%s&a=union select' % url, headers=_headers)

    dw_1 = cal.cal_weight(res1)
    dw_2 = cal.cal_weight(res2, False)
    dw_3 = cal.cal_weight(res3, False)
    print dw_1
    print dw_2
    print dw_3
    print '1,3', cal.is_like(dw_1, dw_3)
    print '1,2', cal.is_like(dw_1, dw_2)
    print '2,3', cal.is_like(dw_2, dw_3)
    
if __name__ == '__main__':
    test()