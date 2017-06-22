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
