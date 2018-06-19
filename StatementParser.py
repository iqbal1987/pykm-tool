import re
import collections
from callError import error
class SParser:
    s=None
    # Keywords
    k1=['is-a','is','has', 'consists-of', 'comprises']
    k2=['sub-component-of', 'connected-to','related-to',
        'property', 'function', 'attribute']
    c1=['and','which','with','whose']
    k=[] # user given k

    # Keyword associations

    # Delimiter
    delimiter=';'

    s_hints={0:'Statement omitted.',
             1:'Statements should not start with a keyword.\n',
             2:'Start with an object name or property name.\n',
             }
    
    # dummy input
    a='FESS is-a Thing; FESS has property energyCapacity[E];'
    c='rotor is-a sub-component-of FESS and is related-to motor'
    #  id     k1     k2             id   c1  k1     k2       id
    c2='magnet is-a sub-component-of rotor whose thickness[tm,val] is connected-to elecLoss'
    b='FESS is-a Thing'
    #s=re.match('(P<first_name>\w+) (P<last_name>\w+)',b)
    #print(s)

    # REGEX specifications
    tspec=[('ID', r'[A-Z-a-z]+'),('newline', r'\n'),('PROP',r'[A-Z-a-z=$\{\}\\\[?(*\d+.\d+)\]]+'),('PROPt',r'\[?type=(\w+)')]
    # Explanation   capture text         newline              include text,$,{,},\ capture between (if \[? exists) [anything,dnumbers,decimalPt,dnumbers]
    # Create named groups
    tregx='|'.join('(?P<%s>%s)' % pair for pair in tspec)
    #print(tregx)
    #mo=re.finditer(tregx,c)
    ha=[]

    
    def __init__(self,k=[],delimiter=';'):
        self.k.append(k)
        self.delimiter=delimiter
        self.addKeys=[]
        self.addPropClass=[]
        self.codeStyle='og'

    def delimit(self,s,delimiter=';'):
        ds=re.split(delimiter,s)
        return [i.strip() for i in ds if not (i=='' or i==' ')]
        
    def parse(self,s,k=None):
        ds=self.delimit(s)
        print(ds)
        sk=self.splitKeyword(ds)
        print(sk)
    
    def splitKeyword(self,s):
        skk= [self.delimit(st,delimiter='|'.join(self.fl)) for st in s]
        return skk
    
    def tokens(self,s):
        d=self.delimit(s)
        t=[self.delimit(i,'\s') for i in d]
        return t
    
    def keywords_SVO(self,s):
        print(s[0])
        #a=re.finditer('?P<name>\[A-Za-z]+\sis-a\s',s[0])
        #print(a)
        #return a
        
    def genToken(self,a=None,delimitBool=False):
        if not(a==None):
            if not delimitBool:
                self.a=a
            else:
                self.a=self.delimit(a)

    # text parsing
        Token=collections.namedtuple('Token',['typ','value','level'])
        y={}
        p=[]
        for i in range(len(self.a)):
            p=[]
            #print(self.a[i][0])
            if not self.a[i][0]=='%':
                for mo in re.finditer(self.tregx,self.a[i]):
                    k=mo.lastgroup
                    v=mo.group(k)
                    #print(v)
                    if k=='ID':
                        k=v
                    if v in self.k1:
                       level='k1'
                       k='k'
                    elif v in self.k2:
                       level='k2'
                    elif v in self.c1:
                       level='c1'
                    else:
                       level=0
                    if k=='PROP':
                        level=1
                    p.append(Token(k,v,level))
            else:
                    p.append(Token('COMMENT',self.a[i],'COMMENT'))
            y.update({i:p})    
        #[print(y[yy]) for yy in y]
        #print([p.level for yy in y for p in y[yy]])
        #print(y)
        
        # some sanity check for statments: grammer rules
        scnt=1
        tobedel=[]
        for w in y:
            if not(y[w][0].typ=='COMMENT'):
                if not(y[w][0].level==0): # not boolean, just a zero char.
                    tobedel.append(w)    
                    print('StatmentParser: Check statement %s. ' % str(scnt) +
                          self.s_hints[1]+self.s_hints[2]+self.s_hints[0])
                scnt+=1
        # Delete statements
        for ww in tobedel: del y[ww]
        return y
        
    def hashDefParser(self,a=None,delimitBool=False):
        if not(a==None):
            if not delimitBool:
                self.ha=a
            else:
                self.ha=self.delimit(a)
        # templates         
        # #def key <keyname>
        # #def propClass <property classsification> implemented:geom,chem,mech,
        # #def fileType <gv> default:ontograph
        s=self.ha
        mh=re.search(r'^#def',s)
        if mh:
            m=re.search(r'#def\s(?P<typ>.*?)\s(?P<param>.*)',s)
            #print(m.groupdict())

        if re.search(r',',m.groupdict()['param']): # if comma is found 
            newParams=m.groupdict()['param'].split(',')
            newParams=[i.strip() for i in newParams]
        else:
            newParams=m.groupdict()['param'].strip()
        #print(newParams)
        # Assign types and params
        if m.groupdict()['typ']=='key':
            self.addKeys=newParams
        elif m.groupdict()['typ']=='propClass':
            self.addPropClass=newParams
        elif m.groupdict()['typ']=='fileType':
            if len(newParams[0])==1:
                # only one param exists
                np=True
            else:
                # may be more than one exists
                np=False
                
            if np:
                self.codeStyle=newParams # possibility for error when used commans mistakenly
            else:
                self.codeStyle=newParams[0]
                print('fileType #def declaration should have only one parameter! First one used.')
        else:
            print('Undefined #def '+m.groupdict()['typ']+' is ommitted.')
            

if __name__=="__main__":
    
    a='FESS is-a Thing; %has property bla; FESS has property energyCapacity[E];'
    sp=SParser(k=['comprises'])
    """
    sp.parse(a)
    t=sp.tokens(a)
    print(t)
    print(sp.keywords_SVO(t))
    """
    sp.genToken(a,True)
    sp.hashDefParser('#def filType gv')

    
        
