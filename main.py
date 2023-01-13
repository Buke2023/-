import time
from os import system
from queue import PriorityQueue
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Node:
    def __init__(self,key=None,next=None):
        self.key=key
        self.next=next

class SingleLinkedList:
    def __init__(self):
        self.head=None
        self.tail=None
        self.size=0

    def append(self,value):
        tmp=Node(value)
        if not self.head:
            self.head=tmp
            self.tail=tmp
        else:
            self.tail.next=tmp
            self.tail=tmp
        self.size+=1
    
    def delete(self,index):
        if index<0 or index>=self.size:
            print("invalid index")
        elif index==0:
            self.head=self.head.next
            if self.size==1:
                self.tail=None
        else:
            p=self.head
            for i in range(index-1):
                p=p.next
            
            if index==self.size-1:
                self.tail=p
            p.next=p.next.next
        self.size-=1
    
    
    
    def insert(self,index,value):
        if index<0 or index>self.size:
            print("invalid index")
        tmp=Node(value)
        self.size+=1
        if index==0:
            tmp.next=self.head
            self.head=tmp
        else:
            p=self.head
            for i in range(index-1):
                p=p.next
            tmp.next=p.next
            p.next=tmp
    
    def __getitem__(self,index):
        if index<0 or index>self.size:
            print("invalid index")
        p=self.head
        for i in range(index):
            p=p.next
        return p

    def __len__(self):
        return self.size
    


class minHeap:
    def __init__(self,linkList=SingleLinkedList()):
        self.list=linkList
    
    def isEmpty(self):
        return self.list.size==0

    def getParentIndex(self,curIndex):
        return (curIndex-1)//2

    def getLeftChildIndex(self,curIndex):
        return 2*curIndex+1

    def getRightChildIndex(self,curIndex):
        return 2*curIndex+2

    def push(self,value):
        self.list.append(value)
        cur_index=len(self.list)-1
        while cur_index>0:
            parent_index=(cur_index-1)//2
            if self.list[parent_index].key>self.list[cur_index].key:
                self.list[parent_index].key,self.list[cur_index].key=self.list[cur_index].key,self.list[parent_index].key
                cur_index=parent_index
            else:
                break

    def pop(self):
        if len(self.list)==0:
            return None
        # if len(self.list)==1:
        #     tmp=self.list.head.key
        #     self.list.delete(0)
        #     return tmp
        min_res=self.list.head.key              #保存最后的值
        self.list.head.key=self.list.tail.key #移到堆顶
        self.list.delete(self.list.size-1)   #删除末尾
        i=0
        min_index=0
        while True:
            left=self.getLeftChildIndex(i)
            right=self.getRightChildIndex(i)
            if left>=self.list.size:
                break
            if right>=self.list.size or self.list[left].key<self.list[right].key:
                min_index=left
            else:
                min_index=right
            if self.list[i].key>self.list[min_index].key:
                self.list[i].key,self.list[min_index].key=self.list[min_index].key,self.list[i].key
                i=min_index
            else:
                break
        return min_res

def HeapGraph(H=minHeap()):
    f=open("graph.dot","w")
    f.write("digraph graphname{\n dpi=300;\n")
    p=H.list.head
    for i in range(H.list.size):
        f.write("{}[label={}];\n".format(i,p.key))
        p=p.next
        if H.getRightChildIndex(i)<H.list.size:
            f.write("{}->{};\n".format(i,H.getRightChildIndex(i)))
        if H.getLeftChildIndex(i)<H.list.size:
            f.write("{}->{};\n".format(i,H.getLeftChildIndex(i)))
    f.write("}\n");
    f.close()

def benchMark():
    data_size=[50,100,200,300,500,1000,2000,5000,10000]
    f=open("time.csv","w")
    f.write("n,time\n")
    for n in data_size:
        H=minHeap()
        Q=PriorityQueue()
        start=time.time()
        for i in range(n):
            H.push(np.random.randint(0,100000))
        while not H.isEmpty():
            H.pop()
        end=time.time()
        print((end-start)*1000,"ms")
        f.write("{},{}\n".format(n,(end-start)*100))
    f.close()
    data=pd.read_csv("time.csv")
    plt.plot(data['n'],data['time'])
    plt.xlabel('data size')
    plt.ylabel('cost time')
    plt.show()


# 测试部分 
H=minHeap()
Q=PriorityQueue()
for i in range(40):
    a=np.random.randint(0,1000)
    Q.put(a)
    H.push(a)

flag=1
while not Q.empty:
    m=Q.get()
    n=H.pop()
    if(m!=n):
        flag=0
        break

print("finish check:",flag)
HeapGraph(H) # draw Tree 
system(".\\bin\\dot graph.dot -Tpng -o Tree.png")
system("Tree.png")

benchMark()



