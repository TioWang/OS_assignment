# -*- coding: utf-8 -*-
import os

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

i = sonAndGson()
