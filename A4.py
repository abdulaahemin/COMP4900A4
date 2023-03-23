import random
    
def calc(c,n):
    return 1/(1+(((c[0]/c[1])**n)*((c[0]-(1-c[0]))/(c[1]-(1-c[1])))*(((c[1]**n)-((1-c[1])**n))/((c[0]**n)-((1-c[0])**n)))))
    
def beta(action,c):
    if  random.random() < c[action]:
        return 1
    else: 
        return 0
    
def binarySearch(low, high,c,prev):
    if low > high:
        return prev
    mid = int((low + high)/2)
    acc=calc(c,mid)
    acc=acc// 0.01 / 100
    if acc==0.95:
        return mid
    elif 0.95 >acc:    
        prev=mid
        return binarySearch(mid + 1, high,c,prev)
    else :     
        prev=mid                 
        return binarySearch(low, mid - 1,c,prev) 
           
def binarySearchLRI(low, high,c):
    if low > high:
        return False
    kr = (low + high)/2
    acc,steps=lri(c,kr)
    acc=acc // 0.01 / 100
    if acc==0.95:
        return kr,acc,steps
    elif 0.95 >acc:
        return binarySearchLRI(kr, high,c)
    else :               
        return binarySearchLRI(low, kr,c) 

def tsetlin(n,state,c):
    action1_counter=0
    for i in range(100):
        for j in range(11000):   
            if state<=n:
                action=0
                if j>=10000:
                    action1_counter+=1
            else: 
                action=1
            res=beta(action,c)
            if res==0:
                if state!=1 and state!=n+1:
                    state=state-1
            else:
                if state==n:
                    state=2*n
                elif state==2*n:
                    state=n
                else:
                    state=state+1
    return action1_counter/100000

def krylov(n,state,c):
    action1_counter=0
    for i in range(100):
        for j in range(11000):   
            if state<=n:
                action=0
                if j>=10000:
                    action1_counter+=1
            else: 
                action=1
            res=beta(action,c)
            if res==0:
                if state!=1 and state!=n+1:
                    state=state-1
            else:
                if  random.random() < 0.5:
                    if state!=1 and state!=n+1:
                        state=state-1
                else:
                    if state==n:
                        state=2*n
                    elif state==2*n:
                        state=n
                    else:
                        state=state+1
    return action1_counter/100000

def lri(c,kr):
    count=[0,0]
    steps=0
    for i in range(1000):
        pr=[0.5,0.5]
        while pr[0]<0.99 and pr[1]<0.99:
            if random.random() < pr[0]:
                action=0
            else:
                action=1
            steps+=1
            res=beta(action,c)
            if res==0 and action==0:
                pr[1]=kr*pr[1]
                pr[0]=1-pr[1]
            elif res==0 and action==1:
                pr[0]=kr*pr[0]
                pr[1]=1-pr[0]
        count[pr.index(max(pr))]+=1
    return  count[0]/1000,steps/1000

for i in range(7):
    c=[0.05+i*0.1,0.7]
    n=binarySearch(1, 100,c,0)
    print(c,"Number of states required: ",n," Exact accuracy:",calc(c,n)," Simulated: ",tsetlin(n,2*n,c))
    
#compare tsetlin to kylov
c=[0.98,0.99]
c_2=[c[0]/2,c[1]/2]
n=6
print("Exact accuracy: ",calc(c_2,n))
print("Tsetlin with c=",c_2," ",tsetlin(n,n,c_2))
print("Krylov with c=",c," ",krylov(n,n,c))
        

for i in range(7):
    c=[0.05+i*0.1,0.7]
    kr,x,steps=binarySearchLRI(0.01,0.99,c)
    print(c,"lamda=",1-kr," accuracy:",x," steps: ",steps)
