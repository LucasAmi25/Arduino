import sys
f = open(sys.argv[1])



file=f.readlines()
time=0
signal=0
diffSign=''
count=1
tab=[]
value=[]

def supprErreur():
    f1 = open(sys.argv[1])
    
    file1=f1.readlines()
    boolean=False
    string=''
    for l in file1:
        if l.split(',')[0]=='0' or l.split(',')[0]=='33':
            boolean=True
        if boolean and ',' in l:
            string+=l
    f2=open(sys.argv[1],'w+')
    f2.write(string)
supprErreur()
for l in file[1:]:
    print(l)
    if int(l.split(',')[1])>=600  and diffSign=='-':
        diffSign='+'
        diff=int(l.split(',')[0])-time
        time=int(l.split(',')[0])
        
        tab.append(60/(diff/1000))
    elif int(l.split(',')[1])<=600 and diffSign=='+':
        diffSign='-'
    elif diffSign=='':
        if int(l.split(',')[1])<=600:
            diffSign='-'
            
        else :
            diffSign='+'
        diff=int(l.split(',')[0])-time
        time=int(l.split(',')[0])
    value.append(int(l.split(',')[0]))
tab=tab[1:-1] #enlever le premier et dernier pique
value.sort()
print(sum(tab)/len(tab),value[int(len(value)//2)],len(tab))  

