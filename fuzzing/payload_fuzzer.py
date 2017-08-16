#!/usr/bin/env python

import glob
import os

SCRIPT_DIR = ('sqlmap_tamper', )

def fuzz_by_all_script(payload):
    payload = payload if payload else ''
    res = {payload: 'raw'}    
        
    for script_dir in SCRIPT_DIR:
        fuzzer_list = glob.glob(r'fuzzing\%s\*_fuzzer.py' % script_dir)  
        
        for fuzzer in fuzzer_list:
            fuzzer = '%s.%s' % (script_dir, os.path.basename(fuzzer).split('.')[0])
            module = __import__('fuzzing.%s' % fuzzer, fromlist=True)
            
            func = getattr(module, 'fuzz')
            _ = func(payload)
            if not res.has_key(_):
                res[_] = fuzzer
    
    return res