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
		
	
