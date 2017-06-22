# 操作系统实验

#### 测试运行环境
* **Python 3.x**
* **Pythonista for iOS**
* **iPad pro 12.9 (2015)**

## Experiment 1 : Process  Management

>实验目的: 加深对于进程并发执行概念的理解。实践并发进程的创建和控制方 法。观察和体验进程的动态特性。进一步理解进程生命期期间创建、 变换、撤销状态变换的过程。掌握进程控制的方法，了解父子进程间 的控制和协作关系。练习 Linux 系统中进程创建与控制有关的系统调 用的编程和调试技术。

### 实验要求

-------

1. 每个进程都执行自己独立的程序，打印自己的pid，每个父进程打印其子进程的pid
2. 每个进程都执行自己独立的程序，打印自己的pid，父进程打印其子进程的pid
3. 编写一个命令处理程序，能处理max(m,n), min(m,n)和average(m,n,l)这几个命令。（使用exec函数族）

### 代码

-------

```python
def twoson():
	print "Father's pid = " + str(os.getpid())
	p = os.fork()
	if p < 0:
		print "create child fails! "
		exit(-1)
	elif p == 0:
		print "Child 1's pid = " + str(os.getpid())
		return 0
	p1 = os.fork()
	if p1 < 0:
		print "create child fails! "
		exit(-1)
	elif p1 == 0:
		print "Child 2's pid = " + str(os.getpid())
		return 0 
	return 0
```

结果：

```
Father's pid = 37633
Child 1's pid = 37636
Child 2's pid = 37637
```

以上算法是创建了一个父进程，两个子进程。当子进程遇见return函数后，就会结束当前进程，所以相当于

```sequence
父进程->子进程1: p = os.fork()
Note over 子进程1: return 0 结束
父进程->子进程2: p1 = os.fork()
Note over 子进程2: return 0 结束
```

```python
def sonAndGson():
	p = os.fork()
	if p < 0:
		print "create son fails! "
		exit(-1)
	elif p == 0:
		print "Son's pid = " + str(os.getpid())
		p = os.fork()
		if p < 0:
			print "create Gson fails! "
			exit(-1)
		elif p == 0:
			print "Gson1's pid = " + str(os.getpid())
			return 0
		else:
			print "Father1's pid = " + str(os.getpid())
			return 0
		return 0
	else:
		print "Father's pid = " + str(os.getpid())
		return 0
	return 0
```

结果：

```
Father's pid = 37574
Son's pid = 37577
Father1's pid = 37577
Gson1's pid = 37578
```

```sequence
父进程->子进程: p = os.fork( )
子进程->孙子进程: p = os.fork( )
Note over 子进程: return 0 结束
Note over 孙子进程: return 0 结束
```

```py
# -*- coding: utf-8 -*-
import os
command = input("enter command(enter q to quit): ")
while command :
	if command == 'q':
		exit(0)
	command = command.split(' ')

	p = os.fork()
	if p < 0 :
		exit(-1)
	elif p == 0:
		if command[0] == 'max' or 'min':
			os.execlp("./" + command[0],command[0],command[1],command[2])
		elif command[0] == 'average':
			os.execlp("./" + command[0],command[0],command[1],command[2],command[3])
		else :
			print("no such command!")
	os.kill(p, 0)
	wait = os.waitpid(p,0)
	command = input("enter command: ")
```
结果：

```
enter command(enter q to quit): max 1 2
result: 2
enter command(enter q to quit): min 1 2
result: 1
enter command(enter q to quit): average 1 2 3
result: 2 
```

## Experiment 2 Processer Schema
> 实验目的: 熟悉使用各种单处理器调度的各种算法，加深对于处理机调度机制的 理解。练习模拟算法的编程技巧，锻炼分析试验数据的能力

### 实验要求
随机给出一个进程调度实例，如：

|  进程  | 到达时间   | 服务时间    |
| --- | --- | --- |
|   A |0    |3    |
|    B|2    |   6 |
|    C|  4  |    4|
|    D|    6|    5|
|    E|   8 | 2   |

模拟进程调度，给出按照算法先来先服务 FCFS、轮转 RR（q=1）、 最短进程优先 SJF、最高响应比优先 HRN 进行调度各进程的完成时 间、周转时间、带权周转时间。

### 代码

```python
# -*- coding: utf-8 -*-

class processScheduling(object):
	
	def __init__(self,path):
		self.path = path
		self.processtable = {}
		
	def readProcess(self):
		extension = self.path.split('.')[-1]
		if extension != 'process':
			print("file’s extension is not .process, please check the file!")
			exit(-1)
		processes = open(self.path,'r',encoding = 'utf-8').readlines()
		for process in processes:
			if '#' in process:
				continue
			self.processtable[process.split(' ')[0]] = [int(process.split(' ')[1]),int(process.split(' ')[2][:-1])]
		 
	def TAT(self,t,st):
		return t - st
	
	def WTAT(self,t,ts):
		return float(t)/ts
	
	def printResult (self,result):
		Result = sorted(result, key = lambda e:e[0])
		for i in Result:
			print (i[0] + "的完成时间为: " + i[1] + "，周转时间为: " + i[2] + "，带权周转时间为: " + i[3])
	
	def FCFS(self):
		time = 0
		result = []
		for x in sorted(self.processtable.keys()):
			time += self.processtable[x][1]
			tat = self.TAT(time , self.processtable[x][0])
			result.append([x ,str(time),str(tat),str(self.WTAT(tat,self.processtable[x][1]))])
		self.printResult(result)
		
	def RR(self):
		i = 0
		pro = sorted(self.processtable.keys())
		job = []
		history = []
		result = []
		for robin in range(1000):
			while robin + 1 >= self.processtable[pro[i]][0] :#该时间后一时间片是否有新的进程加入
				if pro[i] not in history:#此进程没出出现过，加入job队列
					job.append([pro[i],self.processtable[pro[i]][1]])
					history.append(pro[i])
				i += 1
				if i == len(pro):
					break
			i = 0
			if len(job) :#如果有作业
				job[0][1] -= 1#首任务执行一个时间片
				if job[0][1] == 0:#如果该任务已经执行完成
					tat = self.TAT(robin+1,self.processtable[job[0][0]][0])
					result.append([job[0][0] , str(robin + 1 ) , str(tat) , str(self.WTAT(tat,self.processtable[job[0][0]][1]) )])			
					job.pop(0)
				else:
					job.append(job[0])#如果没有完成则将作业放入队尾
					job.pop(0)
			elif robin < self.processtable[pro[-1]][0] :#如果后面还有作业
				continue
			else:
				break
		self.printResult(result)
	
	def SJF(self):#短作业优先调度
	
		pro = sorted(self.processtable.items(), key = lambda  e:e[1][0])#根据作业到达时间排序
		job = []
		time = 0
		result = []
		while pro :
			for pros in pro:
				if time >= self.processtable[pros[0]][0] and [self.processtable[pros[0]][1],pros[0]] not in job :#作业已到达，加入job队列
					job.append([self.processtable[pros[0]][1],pros[0]])
			job.sort()#根据服务时间排序，短作业优先
		
			time += job[0][0]
			tat = self.TAT(time,self.processtable[job[0][1]][0])
			result.append([job[0][1],str(time),str(tat),str(self.WTAT(tat,self.processtable[job[0][1]][1]) )])				
			pro.remove((job[0][1],self.processtable[job[0][1]]))
			job.pop(0)
		self.printResult(result)
		
	def priority(self,wTime,sTime):#计算优先权
		 return float(wTime + sTime) / sTime
	
	def DHRN(self):#抢占式动态优先权最高响应比优先算法
		time = 0
		pro = sorted(self.processtable.items(), key = lambda  e:e[1][0])
		Property = {}
		job = {}
		handle = (' ')
		result= []
		while pro:
			for pros in pro :
				if time >= self.processtable[pros[0]][0] and pros[0] not in job :
					job[pros[0]] = [self.processtable[pros[0]][1],self.processtable[pros[0]][1]]	
			for j in job:
				if handle[0] == j:
					continue
				P = priority(time , job[j][0])
				Property[j] = P	
			handle = sorted(Property.items(), key = lambda  e:e[1])[-1]
			time += 1 #self.processtable[handle[0]][1]
			job[handle[0]][1] -= 1
			if job[handle[0]][1] == 0: 
				tat = self.TAT(time,self.processtable[handle[0]][0])	
				result.append([handle[0],str(time),str(tat),str(self.WTAT(tat,self.processtable[handle[0]][1]))])		
				pro.remove((handle[0],self.processtable[handle[0]]))
				job.pop(handle[0])
				Property.pop(handle[0])
		self.printResult(result)
		
	def HRN(self):
		time = 0 
		pros = sorted(self.processtable.items() , key = lambda e:e[1][0])
		Property = {}
		jobs = {}
		result = []
		while pros:
			for pro in pros:
				if time>= self.processtable[pro[0]][0] and pro[0] not in jobs:
					jobs[pro[0]] = self.processtable[pro[0]][1]
			for job in jobs:#动态计算优先权
				P = self.priority(time - self.processtable[job][0], jobs[job])
				Property[job] = P
			handle = sorted(Property.items(), key = lambda e:e[1])[-1]#根据优先权排序
			time += jobs[handle[0]]
			tat = self.TAT(time,self.processtable[handle[0]][0])
			result.append([handle[0],str(time),str(tat),str(self.WTAT(tat,self.processtable[handle[0]][1]))] )				
			pros.remove((handle[0],self.processtable[handle[0]]))
			jobs.pop(handle[0])
			Property.clear()		 
		self.printResult(result)

if __name__ == "__main__":
	path = input('Enter the process table path :')
	process = processScheduling(path)
	process.readProcess()
	print (" - - - - - - - — - - - - - — - - - - - ")
	process.FCFS()
	print (" - - - - - - - — - - - - - — - - - - - ")
	process.RR()
	print (" - - - - - - - — - - - - - — - - - - - ")
	process.SJF()
	print (" - - - - - - - — - - - - - — - - - - - ")
	process.HRN()
	print (" - - - - - - - — - - - - - — - - - - - ")
```
### 结果

```
Enter the process table path :./process.process
 - - - - - - - — - - - - - — - - - - - 
A的完成时间为: 5，周转时间为: 5，带权周转时间为: 1.0
B的完成时间为: 11，周转时间为: 9，带权周转时间为: 1.5
C的完成时间为: 15，周转时间为: 11，带权周转时间为: 2.75
D的完成时间为: 20，周转时间为: 14，带权周转时间为: 2.8
E的完成时间为: 22，周转时间为: 14，带权周转时间为: 7.0
 - - - - - - - — - - - - - — - - - - - 
A的完成时间为: 11，周转时间为: 11，带权周转时间为: 2.2
B的完成时间为: 20，周转时间为: 18，带权周转时间为: 3.0
C的完成时间为: 19，周转时间为: 15，带权周转时间为: 3.75
D的完成时间为: 22，周转时间为: 16，带权周转时间为: 3.2
E的完成时间为: 16，周转时间为: 8，带权周转时间为: 4.0
 - - - - - - - — - - - - - — - - - - - 
A的完成时间为: 5，周转时间为: 5，带权周转时间为: 1.0
B的完成时间为: 22，周转时间为: 20，带权周转时间为: 3.3333333333333335
C的完成时间为: 9，周转时间为: 5，带权周转时间为: 1.25
D的完成时间为: 16，周转时间为: 10，带权周转时间为: 2.0
E的完成时间为: 11，周转时间为: 3，带权周转时间为: 1.5
 - - - - - - - — - - - - - — - - - - - 
A的完成时间为: 5，周转时间为: 5，带权周转时间为: 1.0
B的完成时间为: 11，周转时间为: 9，带权周转时间为: 1.5
C的完成时间为: 15，周转时间为: 11，带权周转时间为: 2.75
D的完成时间为: 22，周转时间为: 16，带权周转时间为: 3.2
E的完成时间为: 17，周转时间为: 9，带权周转时间为: 4.5
 - - - - - - - — - - - - - — - - - - - 

```


## Experiment 3 Storage Manage
>实验目的: 加深对于存储管理的了解，掌握虚拟存储器的实现原理；观察和了 解重要的页面置换算法和置换过程。练习模拟算法的编程技巧，锻炼 分析试验数据的能力

### 实验要求

1. 示例实验程序中模拟两种置换算法：LRU 算法和 FIFO 算法。

2. 给定任意序列不同的页面引用序列和任意分配页面数目，显示两种 算法的页置换过程。

3. 能统计和报告不同置换算法情况下依次淘汰的页号、缺页次数（页
错误数）和缺页率。


### 代码


```python
# -*- coding: utf-8 -*-
import time
import console
class store(object):
	def __init__(self , Amount , LRS):
		self.Amount = Amount
		self.PhysicalBlock = []
		self.LackofFrame = 0
		self.RateofLack = 0.0
		self.LRS = LRS #Logical Reference Sequence
		
	def showPB(self):
		for block in self.PhysicalBlock:
			print("|  "+str(block) + "  |")
			print(" -—--- ")
	def LRU(self):
		LackofFrame = 0.0
		for addr in self.LRS:
			time.sleep(1)
			console.clear()
			if addr not in self.PhysicalBlock:
				self.PhysicalBlock.insert(0,addr)
				if len(self.PhysicalBlock) > self.Amount :
					self.PhysicalBlock.pop(-1)
				LackofFrame += 1.0
				print("   X ")
			else:
				self.PhysicalBlock.pop(self.PhysicalBlock.index(addr))
				self.PhysicalBlock.insert(0,addr)
				print("   Y ")
			
			
			self.showPB()
		print("缺页率：" + str(LackofFrame / len(self.LRS)))
		print('缺页数：' + str(LackofFrame))
	def FIFO(self):
		LackofFrame = 0.0 
		for addr in self.LRS:
			time.sleep(1)
			console.clear()
			if addr not in self.PhysicalBlock:
				self.PhysicalBlock.insert(0,addr)
				if len(self.PhysicalBlock) > self.Amount:
					self.PhysicalBlock.pop(-1)
				LackofFrame += 1.0
				print( "   X")
			else:
				print( "   Y")
			self.showPB()
				
		print( "缺页率：" + str(LackofFrame / len(self.LRS)))
		print( '缺页数：' + str(LackofFrame))
				
				
if __name__ == "__main__":
	pages = int(input('Enter amount of pages :'))
	s = input('Enter the sequence of pages’ position separated by spaces(like 1 2 3 4 )')
	command = input('Enter method :')
	sequence = []
	for i in s:
		if i >= '0' and i <= '9':	
			sequence.append(int(i))
	s = store(pages,sequence)
	if command == 'FIFO':
		s.FIFO()
	elif command == 'LRU':
		s.LRU()
		
```

### 结果


```
3
1 2 3 4 3 4 5 3

LRU：
缺页率：0.625
缺页数：5.0

FIFO：
缺页率：0.625
缺页数：5.0

```
## Experiment 4 Disk Moving Arm
> 4.1 实验目的: 加深对于操作系统设备管理技术的了解，体验磁盘移臂调度算法的重 要性；掌握几种重要的磁盘移臂调度算法，练习模拟算法的编程技巧， 锻炼研究分析试验数据的能力

### 实验要求
1. 示例实验程序中模拟两种磁盘移臂调度算法：SSTF 算法和 SCAN算法

2. 能对两种算法给定任意序列不同的磁盘请求序列，显示响应磁盘 请求的过程。

3. 能统计和报告不同算法情况下响应请求的顺序、移臂的总量。

### 代码

```python
# -*- coding: utf-8 -*-
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


class data (object):
	def __init__ (self,start,positions):
		self.positions = positions
		self.start = start
		self.path = [self.start]
	def Findnear(self,p1):
		small = 10000
		p = p1
		for i in self.positions:
			distance = p1 - i if p1 > i else i - p1
			if small > distance :
				p = i
				small = distance
		return (p,small)
				
	def SSTF(self):
		tag = 1
		change = 0
		distance = 0 
		length = len(self.positions)
		while self.positions:
			P = self.Findnear(self.start)
			if P[0] < self.start:
				if tag > 0:
					change += 1
				tag = 0
			else:
				if tag == 0:
					change += 1
				tag = 1
			distance += P[1]
			self.start = P[0]
			self.path.append(self.start)	
			self.positions.remove(self.start)
		print('平均寻道长度：'+str(float(distance)/length))		
		print('移臂总量：' + str(change))
		
	def find(self,p1):
		pass
	
	def SCAN(self) :
		tag = 1
		change = 1
		distance = 0
		p = self.start
		length = len(self.positions)
		self.positions.sort()
		for i in self.positions:
			if i < self.start:
				continue
			else:
				distance += i - p
				p = i 
				self.path.append(p)
		self.positions.reverse()
		for i in self.positions:
			if i < self.start:
				distance += p - i
				p = i
			#self.positions.remove(i)
				self.path.append(p)
		print('平均寻道长度：'+str(float(distance)/length))		
		print('移臂总量：' + str(change))
		
		
	def drawpath(self):
		y = range(len(self.positions)+1)
		plt.clf()
		plt.plot(self.path)
		plt.ylabel("position")
		plt.show()

		
if __name__ == "__main__":
	command = input('Enter method (SCAN , SSTF , q):')
	while command != 'q' :
		origin = int(input('Enter the origin :'))
		address = input('Enter the sequence of track’s address separated by spaces(like 1 2 3 4 )')
		sequence = []
		address = address.split(' ')
		for i in address:
			if '\n' not in i:	
				sequence.append(int(i))
			else:
				sequence.append(int(i[:-1]))
		test = data(origin,sequence)
		if command == 'SSTF':
			test.SSTF()
			test.drawpath()	
		elif command == 'SCAN':
			test.SCAN()
			test.drawpath()

		command = input('Enter method (SCAN , SSTF , q):')
	print('Quit!')
```

### 结果
SCAN的结果：
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-FullSizeRender-2.jpg?iPad)
SSTF的结果：
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-FullSizeRender-3.jpg?iPad)



## Experiment 5 File Manage
>实验目的: 通过模拟文件的创建、删除操作，加深对于操作系统文件管理功能的 了解，练习模拟算法的编程技巧，锻炼研究分析试验数据的能力

### 实验要求

-------

给出一个磁盘块序列：1、2、3、……、500，初始状态所有块为空的，每块的大小为 2k。选择使用空闲表、空闲盘区链、位示图 三种算法之一来管理空闲块。对于基于块的索引分配执行以下步骤：

1. 随机生成2k-10k的文件50个，文件名为1.txt、2.txt、……、50.txt，按照上述算法存储到模拟磁盘中。


2. 删除奇数txt文件


3. 新创建5个txt名称为A.txt、B.txt、C.txt、D.txt、E.txt 大小为：7k、5k、2k、9k、3.5k，按照与（1）相同的算法存储到模拟磁盘中。

4. 给出文件A.txt、B.txt、C.txt、D.txt、E.txt的盘块存储状态和所有空闲区块的状态。

### 代码

```python
# -*- coding: utf-8 -*-
'''
file:
	filename
	size
'''
import random
import matplotlib.pyplot as plt
import console
import time
import json

class diskManager(object):
	def __init__(self,size):
		self.disk = {}
		for i in range(size):
			self.disk[str(i+1)] = {'state': 0,'filename':''}
		self.index = {}# {'filename':[[position],[needSpace]]}
		self.freeSpace = [{'first': 1,'space':500}]
		#print(self.disk)
	
	def store(self,file):
		if file['filename'] in self.index:
			print("file already exit!")
			time.sleep(1)
			console.clear()
			return False
		needSpace = int (file['size'] / 2) + 1 if file['size'] % 2 != 0 else int(file['size']/2) #计算所需块数
		emptylist = []
		positionlist = self.findSpace(needSpace) # 查找空闲的位置
		if len(positionlist) == 1:
			position = positionlist[0][0]
			number = positionlist[0][2]
			for i in range(position,position+needSpace): #存入disk
				self.disk[str(i)]['state'] = 1
				self.disk[str(i)]['filename'] = file['filename']
			
			
			self.modifyFreeSpace('a',position,needSpace,number)
			p = []
			n =[ ]
			for i in range(needSpace):
				p.append(i+position)
				n.append(1)
			self.index[file['filename']] = [[position],[needSpace]] #将文件信息存入索引表
		elif len(positionlist) > 0 :
			p = []
			n = []
			for i in range(len(positionlist) ):
				position = positionlist[i][0]
				
				needSpace = positionlist[i][1]
				number = positionlist[i][2]
				for j in range(position,position+needSpace): #存入disk
					self.disk[str(j)]['state'] = 1
					self.disk[str(j)]['filename'] = file['filename']
				p.append(position)	
				n.append(needSpace)	
				
				e = self.modifyFreeSpace('a',position,needSpace,number)
				if e >= 0 :
					 emptylist.append(e)
			self.index[file['filename']] = [p,n] #将文件信息存入索引表
		if emptylist:
			j = 0
			for i in emptylist:
				self.freeSpace.pop(i-j)
				j+=1
			
		return True
	def findSpace(self,needSpace):#返回disk中的地址和空闲表的位置
		positionlist = []
		for space in self.freeSpace:
			if space['space'] >= needSpace:
				
				positionlist.append([space['first'],needSpace,self.freeSpace.index(space)])
				return positionlist
			else:
				needSpace -= space['space']
				positionlist.append([space['first'],space['space'],self.freeSpace.index(space)])		
		print("error, file too big!")
	
	
	def modifyFreeSpace(self,method,position,needSpace,number = -1):
		empty = -1
		if method == 'a':
			if self.freeSpace[number]['space'] == needSpace:
				empty = number
			elif self.freeSpace[number]['space'] > needSpace:
				self.freeSpace[number]['first'] += needSpace
				self.freeSpace[number]['space'] -= needSpace 
			else:
				print('error!')
		elif method == 'd':
			for i in self.freeSpace:
				if i['first'] + i['space'] -1 == position - 1:
					i['space'] += needSpace
				elif position + needSpace  == i['first'] :
					i['first'] = position
					i['space'] += needSpace
			i = 0
			while (self.freeSpace[i]['first'] < position):
				i += 1
			self.freeSpace.insert(i,{"first":position,'space':needSpace})
		
		return empty
			
			
	def delete(self,filename):
		index = self.index[filename]
		position = index[0]
		needSpace = index[1]
		for i in range(len(position)):
			self.modifyFreeSpace('d',position[i],needSpace[i])
			for j in range(position[i],position[i]+ needSpace[i]):
				self.disk[str(j)]['state' ] = 0
				self.disk[str(j)]['filename'] = ''
		self.index.pop(filename)			
	
	def show(self,filename):
		if filename not in self.index:
			print("Not find file!")
			return False
		index = self.index[filename]
		position = index[0]
		needspace = index[1]
		print(filename+"存储的位置有：",end='')
		for i in range(len(position)):
			for j in range(needspace[i]):
				print(str(position[i]+j)+' ',end='')
		return	True
		
		
	def randomFile(self,amount,sizemin,sizemax,f):
		for file in range(amount):
			size = round(random.uniform(sizemin,sizemax))
			filename = str(f + file)+".txt"
			self.store({'filename':filename,'size':size})
		

def init(size):
	disk = diskManager(size)
	return disk 

def showfree(disk):
	p = 1
	size = []
	colors = []
	explode = []
	labels = []
	print("                  Free List")
	for i in disk.freeSpace:
		if i['first'] > p:
			size.append(i['first'] - p)
			size.append(i['space'])
			p = i['first']+i['space']
		else:
			size.append(0)
			size.append(i['space'])

		print('Free blocks address: '+str(i['first'])+' Free blocks amount: ' + str(i['space']))
	for i in range(1,len(size)+1):
		if i % 2 == 0:
			colors.append('white')
			explode.append(0)
			labels.append(str(size[i-1]))
		else:
			labels.append('')
			colors.append('black')
			explode.append(0)
	plt.clf()
	plt.pie(size, explode=explode, labels=labels, colors=colors,labeldistance = 1.1, shadow=False, startangle=90)
	plt.axis('equal')
	plt.text(0,1.17,"Disk Status (Black: used , White: free)",horizontalalignment ='center',fontsize = 16,bbox = {'facecolor':'0.9','alpha':0.5,'pad': 5})
	plt.text(1.2,-1.13,"Black: used\nWhite: free",horizontalalignment ='center',fontsize = 16,bbox = {'facecolor':'0.9','alpha':0.5,'pad': 5})
	
	plt.show()		
	
def page():
	print("           Welcome to disk manager!\n" + \
		  'MENU:\n'+\
		  '           1. Creat a new disk\n' +\
		  '           2. Show disk status\n'+\
		  '           3. Add a new file\n' +\
		  '           4. Create random files\n'+\
		  '			 5. Delete files\n'+\
		  '           6. Show file’s storage status\n'+\
		  '           7. Quit')
		  
def diskload():
	try :
		print('loading')

		d = open('disk.d','r')
		f = open('freespace.d','r')
		i = open('index.d','r')
		diskdata = json.load(d)
		freespace = json.load(f)
		index = json.load(i)
		disk=init(len(diskdata))
		disk.disk=diskdata
		disk.index=index
		disk.freeSpace = freespace
		d.close()
		f.close()
		i.close()
		
		return	disk
	except :
		return ''

def disksave(disk):
	d = open('disk.d','w+')
	f = open('freespace.d','w+')
	i = open('index.d','w+')
	json.dump(disk.disk,d)
	json.dump(disk.freeSpace,f)
	json.dump(disk.index,i)
	d.close()
	f.close()
	i.close()
if __name__ == "__main__":
	command = ''
	disk = diskload()
	newFileList = [{'filename':'A.txt','size':7},\
				   {'filename':'B.txt','size':5},\
				   {'filename':'C.txt','size':2},\
				   {'filename':'D.txt','size':9},\
				   {'filename':'E.txt','size':3.5}\
				   ]
	while(command != 7):
		page()
		command = int(input('Enter command number: '))
		if command == 1:
			console.clear()
			size = int(input("Enter disk size: "))
			disk = init(size)
			disksave(disk)
			print("Create success!🎉 🎊")
			time.sleep(1)
			console.clear()
		elif command ==2:
			console.clear()
			if disk == '':
				print("Please create a disk first!")
				time.sleep(1)
				console.clear()
				continue
			else:
				showfree(disk)
				command = input('Enter any key to return')
				console.clear()
		elif command == 3:
			console.clear()
			if disk == '':
				print("Please create a disk first!")
				time.sleep(1)
				console.clear()
				continue
			else:
				
				while command != 'q':
					print("There are some files. You can enter their names to add, or add a new file")
					for file in newFileList:
						print('name: ' +  file['filename']+ ' size:  '+str( file['size']))
					name = input("Enter filename: ")
					filesize = eval(input("Enter size: "))
					s = disk.store(dict(filename = name,size = filesize))
					if s :
						print("Add success!")
						disksave(disk)
						time.sleep(1)
						console.clear()
					command = input("Enter q to quit add mode , c to continue")
		elif command == 4:
			console.clear()
			if disk == '':
				print("Please create a disk first!")
				time.sleep(1)
				console.clear()
				continue
			else:
				amount = int(input("Enter amount: "))
				sizemin = int(input("Enter min size of file size: "))
				sizemax = int(input("Enter max size of file size: "))
				filename = int(input("Enter filename format: "))
				disk.randomFile(amount,sizemin,sizemax,filename)
				print("Create success!")
				disksave(disk)
				time.sleep(1)
				console.clear()
		elif command == 5:
			console.clear()
			if disk == '':
				print("Please create a disk first!")
				time.sleep(1)
				console.clear()
				continue
			else:
				for file in range(1 , 50,2):
					filename = str(file)+".txt"
					disk.delete(filename)
				print("Delete success!")
				disksave(disk)
				time.sleep(1)
				console.clear()
		elif command == 6:
			console.clear()
			if disk == '':
				print("Please create a disk first!")
				time.sleep(1)
				console.clear()
				continue
			else:
				filename = input("Enter filename: ")
				disk.show(filename)
				command = input('\nEnter any key to return')
				console.clear()
				

```
### 结果
界面：
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0431-1.PNG?iPad)
新建500个块的磁盘
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0432-1.PNG?iPad)
随机生成50个文件后的磁盘情况
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0434-1.PNG?iPad)
删除1至50之间奇数文件后的磁盘情况
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0435-1.PNG?iPad)
添加A-E.txt文件后的磁盘情况
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0436-1.PNG?iPad)

查询文件存放空间
![](http://ooiaw5slt.bkt.clouddn.com/2017-06-22-IMG_0438-1.PNG?iPad)
















