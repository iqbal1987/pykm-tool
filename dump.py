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
