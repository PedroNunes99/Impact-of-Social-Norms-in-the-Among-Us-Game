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
	return layout[i][j] == 'R'

def isReactorEngine(layout,i,j):
	return layout[i][j] == 'r'

def isEletrical_task(layout,i,j):
	return layout[i][j] == 'E'

def isEletrical(layout,i,j):
	return layout[i][j] == 'e'

def isCafetaria(layout, i, j):
	return layout[i][j] == 'C'

def isCafetaria_task(layout, i, j):
	return layout[i][j] == 'c'

def isFire(layout, i, j):
	return layout[i][j] == 'F'

def isSmoke(layout, i, j):
	return layout[i][j] == 'S'

def isWall(layout, i, j):
	return layout[i][j] == 'W'

def isExit(layout, i, j):
	return layout[i][j] == 'E'

def isAlarm(layout, i, j):
	return layout[i][j] == 'A'

def validPropagation(layout, i, j):
	return not isWall(layout,i,j) and not isFire(layout,i,j) and not isSmoke(layout,i,j) and not isExit(layout,i,j)


# Auxiliar

def getLayout(file):
	if(file is None): f = open('amongUS.txt', 'r').read()
	else: f = open(file, 'r').read()
	p = []
	p = [item.split() for item in f.split('\n')[:-1]]
	return p

#def getExitsPos(layout):
	#return [ [index, row.index('E')] for index, row in enumerate(layout) if 'E' in row]