#coding: utf-8

import sys
import codecs

from res_evaluator import Res_evaluator
from fuzze_sender import Requests_fuzzer
from fuzze_script import payload_fuzzer
from config import Fuzze_config

METHOD = Fuzze_config.METHOD
URL = Fuzze_config.URL
PARAMS = Fuzze_config.PARAMS
HEADERS = Fuzze_config.HEADERS
DATA = Fuzze_config.DATA

DELAY = Fuzze_config.DELAY
TEMPLATE = Fuzze_config.TEMPLATE

PAYLOAD_2_FUZZE = Fuzze_config.PAYLOAD_2_FUZZE
GOOD_FUZZE = Fuzze_config.GOOD_FUZZE
BAD_FUZZE = Fuzze_config.BAD_FUZZE

class Waf_evaluator(Res_evaluator):
    
    def __init__(self, req_fuzzer, good_fuzze, bad_fuzze):
        good_res, is_delay = req_fuzzer.fuzze_by_template(good_fuzze).next()
        self.__good_res_weight = self.cal_weight(good_res, is_delay)
        
        bad_res, is_delay = req_fuzzer.fuzze_by_template(bad_fuzze).next()
        self.__bad_res_weight = self.cal_weight(bad_res, is_delay)
        
    def evaluate_res(self, res, *other_args):
        weight = self.cal_weight(res, other_args)
        good_weight = self.is_like(weight, self.__good_res_weight)
        bad_weight = self.is_like(weight, self.__bad_res_weight)
        
        if bad_weight < 0.5 < good_weight:
            res_type = 'good'
        elif good_weight < 0.5 < bad_weight:
            #bad
            res_type = 'bad'
        else:
            res_type = 'other'
        
        return res_type, good_weight, bad_weight

def start_fuzze():
    fuzzer = Requests_fuzzer(method=METHOD, url=URL, params=PARAMS, data=DATA, delay=DELAY, template=TEMPLATE)
    evaluator = Waf_evaluator(fuzzer, GOOD_FUZZE, BAD_FUZZE)
    
    fuzze_word_list = payload_fuzzer.fuzz_by_all_script(PAYLOAD_2_FUZZE) 
    with codecs.open('out.tsv', 'w') as fout:
        fout.write('fuzze_word\tfuzze_script\tevaluate_type\tgood_fuzze_percent\tbad_fuzze_percent\n')
        
        for fuzze_word, detail in fuzze_word_list.iteritems():    
            for res, is_delay in fuzzer.fuzze_by_template(fuzze_word):
                print '[*]running:   %s' % fuzze_word
                result, good_like, bad_like = evaluator.evaluate_res(res, is_delay)
                
                fout.write('%s\t%s\t%s\t%f\t%f\n' % (fuzze_word, detail, result, good_like, bad_like))
         
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    print '[*]start'
    
    start_fuzze()
    
    print '[*]ok'
    