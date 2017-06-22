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
