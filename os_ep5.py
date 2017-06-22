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
				
	
