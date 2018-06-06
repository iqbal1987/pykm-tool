import re
class SParser:
    s=None
    fl=['is-a','is','has','with', 'and', 'consists-of', 'comprises']
    sl=['sub-component-of', 'connected-to',
        'property', 'function', 'attribute']
    k=[]
    delimiter=';'
    
    def __init__(self,k=[],delimiter=';'):
        self.k.append(k)
        self.delimiter=delimiter

    def delimit(self,s,delimiter=';'):
        ds=re.split(delimiter,s)
        return [i.strip() for i in ds if not i=='']
        
    def parse(self,s,k=None):
        ds=self.delimit(s)
        print(ds)
        sk=self.splitKeyword(ds)
        print(sk)
    
    def splitKeyword(self,s):
        skk= [self.delimit(st,delimiter='|'.join(self.fl)) for st in s]
        return skk

if __name__=="__main__":
    a='FESS is-a Thing; FESS has property energyCapacity[E];'
    sp=SParser(k=['comprises'])
    sp.parse(a)
        
