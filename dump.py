"""
# multilevel dict and nodes
a={'p':{'1':11,'2' :22},
   'f':{'3':33,'4':44,'5':55}
   }
print(a['p'])
a['f']['5']=89
print(a['f'].keys())
b={'p':{},
   'f':{}
   }
from node import Node

n=[Node(str(i)) for i in range(10)]
print([str(j) for j in n])
n[0].addProp('yolo')
print(n[0].getProp())
"""
# text parsing
import re
import collections
a='FESS is-a Thing; FESS has property energyCapacity[E];'
c='rotor is-a sub-component-of FESS and is related-to motor'
#  id     k1     k2             id   c1  k1     k2       id
c2='magnet is-a sub-component-of rotor whose thickness[tm,val] is conneted-to elecLoss'
b='FESS is-a Thing'
#s=re.match('(P<first_name>\w+) (P<last_name>\w+)',b)
#print(s)

k1=['is-a','is','has', 'consists-of', 'comprises']
k2=['sub-component-of', 'connected-to','related-to',
        'property', 'function', 'attribute']
c1=['and','which','with','whose']
tspec=[('ID', r'[A-Z-a-z\[\w+\]]+'),('newline', r'\n')]
tregx='|'.join('(?P<%s>%s)' % pair for pair in tspec)
print(tregx)
Token=collections.namedtuple('Token',['typ','value','level'])
#mo=re.finditer(tregx,c)
y=[]

for mo in re.finditer(tregx,c2):
    k=mo.lastgroup
    v=mo.group(k)
    #print(k)
    if k=='ID':
        k=v       
        if v in k1:
           level='k1'
        elif v in k2:
            level='k2'
        elif v in c1:
            level='c1'
        else:
            level=0
    y.append(Token(k,v,level))
print(y)
