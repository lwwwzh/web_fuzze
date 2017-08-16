
from fuzzer import Web_fuzzer

fu = Web_fuzzer(method='get')

print fu.method

fu.get_fuzze_res('method', ['fuck','123'])
