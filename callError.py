import inspect
def error(txt=None,n=None):     
    c=inspect.currentframe()
    #print(c)
    calfr=inspect.getouterframes(c,4)
    #print(calfr[1][3])
    #print(len(calfr))
    func=[f[3] for f in calfr]
    filePath=[f[1] for f in calfr]

    if not txt==None:
        print(txt)
        printErrorStack(func,filePath)
        
    return(str(calfr[1][3]))
    
def printErrorStack(func,filePath):
    s='{:-^20} : {}'
    a=[]
    print('-'*72)
    print('Function Stack')
    print('-'*72)
    for i,j in zip(func,filePath):
        a.append(s.format(str(i),str(j)))
    print('\n'.join(a[1:])) # dont show the callError function call. it is implicit.
    #print(i+':\t '+j)
