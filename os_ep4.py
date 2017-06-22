# -*- coding: utf-8 -*-
import turtle
#turtle.setup(500,300)
#turtle.pendown()
#turtle.fd(200)
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
