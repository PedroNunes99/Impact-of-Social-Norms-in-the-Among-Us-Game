import pygame
from random import choices
from settings import *
from copy import deepcopy


# Predicates

def isAdmin(layout, i, j):
	return layout[i][j] == 'A'

def isAdmin_task(layout, i, j):
	return layout[i][j] == 'a'

def isStorage(layout, i, j):
	return layout[i][j] == 'S'

def isStorage_task(layout, i, j):
	return layout[i][j] == 's'

def isShield(layout, i, j):
	return layout[i][j] == 'D'

def isShield_task(layout, i, j):
	return layout[i][j] == 'd'

def isNavigation(layout, i, j):
	return layout[i][j] == 'N'

def isNavigation_task(layout, i, j):
	return layout[i][j] == 'n'

def isWeapons(layout, i, j):
	return layout[i][j] == 'P'

def isWeapons_task(layout, i, j):
	return layout[i][j] == 'p'

def isMedBay(layout,i,j):
	return layout[i][j] == 'G'

def isMedBay_task(layout,i,j):
	return layout[i][j] == 'g'

def isReactorEngine_task(layout,i,j):
	return layout[i][j] == 'r'

def isReactorEngine(layout,i,j):
	return layout[i][j] == 'R'

def isEletrical_task(layout,i,j):
	return layout[i][j] == 'e'

def isEletrical(layout,i,j):
	return layout[i][j] == 'E'

def isCafetaria(layout, i, j):
	return layout[i][j] == 'C'

def isCafetaria_task(layout, i, j):
	return layout[i][j] == 'c'

def isWall(layout, i, j):
	return layout[i][j] == 'W'

def validMove(layout, i, j):
	return not isWall(layout,i,j)


# Auxiliar

def getLayout(file):
	if(file is None): f = open('amongUS.txt', 'r').read()
	else: f = open(file, 'r').read()
	p = []
	p = [item.split() for item in f.split('\n')[:-1]]
	return p

def getCafetaria_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'c' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'c'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])
	
	return task

def getEletrical_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'e' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'e'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])
	return task

def getReactorEngine_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'r' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'r'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getMedBay_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'g' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'g'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getWeapons_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'p' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'p'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getNavigation_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'n' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'n'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getShield_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'd' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'd'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getStorage_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 's' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 's'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task

def getAdmin_task(layout):
	task = []
	for index, row in enumerate(layout):
		if 'a' in row:
			aux = 0
			indexes = []
			for i in range(len(row)):
				if (row[i] == 'a'):
					aux+=1
					indexes.append(i)
			for i in range(aux):
				task.append([index,indexes[i]])

	return task