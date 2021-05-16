# Sprites

from auxiliary import getLayout, isWall
import pygame
import random
from random import choices
import numpy as np
from settings import *
from auxiliary import *
import heapq
import math


class Agent(pygame.sprite.Sprite):
    def __init__(self, identifier, layout, starting_room, communicates):
        pygame.sprite.Sprite.__init__(self)
        self.id           = identifier
        self.font = pygame.font.SysFont("freesansbold", 16)
        self.textSurf = self.font.render(str(self.id), 1, WHITE,DARKRED)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.image.blit(self.textSurf, [2, 0])

        self.rect = self.image.get_rect()

        self.communicates = communicates
        self.layout       = layout
        self.plan         = []
        self.reconsider   = False
        self.dead         = False
        self.range        = VIS_RANGE
        self.volume       = VOL_RANGE

        pos = random.choice(starting_room) #randomly chooses a position from cafetaria to spawn
            
        self.x = pos[0]
        self.y = pos[1]

        self.new_x = -1
        self.new_y = -1

        self.draw  = False

    def setSettings(self,font,id_color,background_color,pos_x,pos_y):
        self.font = pygame.font.SysFont("freesansbold", 16)
        self.textSurf = self.font.render(str(self.id), 1, id_color,background_color)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(background_color)
        self.image.blit(self.textSurf, [pos_x, pos_y])

    def getPosition(self):
        return [self.x, self.y]

    def getNewPosition(self):
        return [self.new_x, self.new_y]
    
    def getID(self):
        return self.id
    
    def getLayout(self):
        return self.layout

    def getVolume(self):
        return self.volume

    def setColor(self, color):
        self.image.fill(color)
    
    def setRange(self, new_range):
        self.range = new_range
    
    def setVolume(self, new_volume):
        self.volume =  new_volume
        
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def die(self):
        self.dead = True

    def isDead(self):
        return self.dead

    def isCommunicative(self):
        return self.communicates

    def update(self, all_agents, agents_positions):

        if (not self.dead):
            if (len(self.plan)>0):
                self.new_x = (self.plan[0][0])
                self.new_y = (self.plan[0][1])
                
                for agent in all_agents:
                    if not agent.isDead() and agent.getPosition() == [self.new_x, self.new_y] and not agent.getNewPosition() == [self.x, self.y] and self.draw:
                        return 

                self.move(dx = (self.new_x - self.x), dy = (self.new_y - self.y))
                agents_positions[self.getID()] = self.getPosition()
                self.plan        = self.plan[1:]
                self.rect.x  = self.x * TILESIZE 
                self.rect.y  = self.y * TILESIZE

        else:
            self.rect.x  = self.x * TILESIZE 
            self.rect.y  = self.y * TILESIZE
         

    def receiveMessage(self, message):
        for i in range(len(message)):
            for j in range(len(message[i])):
                if (self.layout[i][j] != message[i][j]):
                    self.danger       = True
                    self.reconsider   = True
                    self.layout[i][j] = message[i][j]

    def percept(self, layout):
        x0 = self.x-self.range
        y0 = self.y-self.range
        x1 = self.x+self.range
        y1 = self.y+self.range
        self.reconsider = False
        if (x0 < 0):
            x0 = 0
        if (y0 < 0):
            y0 = 0
        if (x1 > len(layout)-1):
            x1 = len(layout)-1
        if (y1 > len(layout[0])-1):
            y1 = len(layout[0])-1
        for i in range(x0, x1+1):
            for j in range(y0, y1+1):
                if (self.layout[i][j] != layout[i][j]):
                    self.reconsider   = True
                    self.layout[i][j] = layout[i][j]

    def moveRandom(self):
        row  = [-1, 0, 0, 1]
        col  = [0, -1, 1, 0]
        move = [True, False]
        prob = [1/self.id, 1-(1/self.id)]
        if (choices(move, prob)):
            i = random.randrange(0, 4)
            x = self.x + row[i]
            y = self.y + col[i]
            if (not isWall(self.layout,x,y)):
                return [[x, y]]
        return [[self.x, self.y]]


    def Dijkstra(self, dests): #TODO change to receive position!!!!!!
        source  = [self.x, self.y]

        if (source in dests):
            return [source]

        row = [-1, 0, 0, 1]
        col = [0, -1, 1, 0]

        queue   = []
        my_dest = []
        visited = []
        parents  = dict()
        distance = dict()
        enqueued = dict()

        # Initialize stuff
        for i in range(len(self.layout)):
            visit = []
            for j in range(len(self.layout)):
                visit.append(0)
                parents[(i,j)]  = None
                distance[(i,j)] = math.inf
                enqueued[(i,j)] = None
            visited.append(visit)

        queue = [[0, source[0], source[1]]]
        heapq.heapify(queue)
        distance[tuple(source)] = 0
        enqueued[tuple(source)] = True
        visited [source[0]][source[1]] = 1

        while (len(queue) > 0):
            
            cur    = heapq.heappop(queue)
            parent = (cur[1], cur[2])
            if (not enqueued[parent]):
                continue

            enqueued[parent] = False

            if(list(parent) in dests): 
                my_dest = list(parent)
                break

            # shuffle visiting order of the neighbours
            combined = list(zip(row, col))
            random.shuffle(combined)
            row, col = zip(*combined)

            for i in range(len(row)):

                x, y = parent[0] + row[i], parent[1] + col[i]
                if (x < 0 or y < 0 or x >= len(self.layout) or y >= len(self.layout[0])): continue

                if (enqueued[(x,y)] == False ):
                    continue

                if(not isWall(self.layout,x,y) and visited[x][y] == 0):
                    visited[x][y] = 1
                    
                    #Compute cost of this transition
                    weight = 1
                    alternative = distance[parent] + weight

                    if (alternative < distance[(x,y)]):
                        distance[(x,y)] = alternative
                        parents[(x,y)]  = list(parent)
                        heapq.heappush(queue,[alternative, x, y])
                        enqueued[(x,y)] = True

        path = []
        at   = my_dest

        while at != source:
            path.append(at)
            at = parents[tuple(at)]

        path.reverse()
        return path

class Impostor(Agent) :
    def __init__(self, identifier, crewmates, layout, starting_room, communicates):
        Agent.__init__(self, identifier, layout, starting_room, communicates)

        self.font = pygame.font.SysFont("freesansbold", 16)
        self.textSurf = self.font.render("I", 1, BLACK, YELLOW)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.image.blit(self.textSurf, [4, 0])

        self.tasks               = []

        self.crewmates_locations = dict() #id:(pos)
        self.crewmates_status    = dict() #id: alive/dead (boolean)

        self.timer               = TIMER_NEAREST_CREWMATE #timer to calculate nearest crewmate
        self.kill_timer          = 0 #cooldown for the kill_function
        self.target              = 0
        self.target_locked       = False

        for agent in crewmates:
            self.crewmates_locations[agent.getID()] = agent.getPosition()
            self.crewmates_status[agent.getID()] = True

    def update(self, all_agents, agents_positions):
        for agent in all_agents:
            self.crewmates_locations[agent.getID()] = agent.getPosition()
        return super().update(all_agents, agents_positions)

    def closestCrewmate (self):
        closest      = -1
        min_distance = math.inf
        for agent in self.crewmates_status.keys():
            if (self.crewmates_status[agent]): #If crewmate is alive
                aux = len(self.Dijkstra([self.crewmates_locations[agent]]))
                if (aux < min_distance):
                    min_distance = aux
                    closest      = agent
                    
        return closest

    def updateTimers(self): #Updates the kill cooldown and update timer for the nearest crewmate
        if (self.timer < TIMER_NEAREST_CREWMATE):
            self.timer += 1
        if (self.kill_timer < COOLDOWN_KILL):
            self.kill_timer += 1

    #Impostor's plan function
    def plan_(self):
        if(self.kill_timer == COOLDOWN_KILL):
            if ( self.timer == TIMER_NEAREST_CREWMATE):
                self.target      = self.closestCrewmate() 
            crewmate_pos     = self.crewmates_locations[self.target]
            self.plan        = self.Dijkstra([crewmate_pos])

        else:
            self.plan = self.moveRandom()
            if (self.timer < TIMER_NEAREST_CREWMATE):
                self.timer      += 1

            if (self.kill_timer < COOLDOWN_KILL):
                self.kill_timer += 1

   
    def isImpostor(self):
        return True

    def kill(self, all_agents, dead_agents):

        if (self.timer == TIMER_NEAREST_CREWMATE and self.target == 0 ):

            isClose,self.target = self.isClose(all_agents)
            self.timer == 0
        
        if (self.target != 0):
            isClose,self.target = self.isClose(all_agents) 

        if (isClose and self.kill_timer == COOLDOWN_KILL and self.target != 0):

            for agent in all_agents:

                if agent.getID() == self.target:
                    victim = agent
           
            victim.die()
            dead_agents.add(victim)
            self.crewmates_status[self.target] = False
            victim.plan = []
            victim.setSettings(pygame.font.SysFont("freesansbold", 16),WHITE,BLACK,2,0)
            self.kill_timer = 0
            self.target     = 0
            

    def isClose(self, all_agents):
        for agent in all_agents:
            if (not agent.isImpostor() and agent.getID() == self.target and not agent.isDead()):
                x = agent.x
                y = agent.y
                if (self.x + 1 == x or self.x - 1 == x or self.x == x):
                    if(self.y == y or self.y -1 == y or self.y + 1 == y):
                        return True,self.target
                return False,self.target
            else:
                if (not agent.isImpostor() and not agent.isDead()):
                    x = agent.x
                    y = agent.y
                    if (self.x + 1 == x or self.x - 1 == x or self.x == x):
                        if(self.y == y or self.y -1 == y or self.y + 1 == y):
                            return True,agent.getID()
        return False,0

class Crewmate(Agent):
    def __init__(self, identifier, layout, tasks,  starting_room, communicates):
        super().__init__(identifier, layout,  starting_room, communicates)
        self.tasks        = tasks
        self.inTask       = False
        self.taskLocked   = []
        self.timer        = TASK_TIME
        self.callingVote = False
        self.foundImpostor = -1

        tasks_aux = []
        nums = [j for j in range(NUM_TOTAL_TASKS)]

        for i in range (NUM_TASKS_AGENT):

            random_task = random.choice(nums)
            tasks_aux.append(self.tasks[random_task])
            nums.remove(random_task)

        self.tasks     = tasks_aux

        task_len = len(self.tasks[0])
        self.randTask  = random.randint(0,task_len-1)


    def isImpostor(self):
        return False

    def isTask (self, task):
        for i in range(len(task)):
            if (self.x == task[i][0] and self.y == task[i][1]):
                self.inTask = True
                if (self.timer == 0):
                    self.tasks      = self.tasks[1:]
                    self.taskLocked = []
                    if (len(self.tasks)>0):
                        self.randTask = random.randint(0,len(self.tasks)-1)
                    self.timer  = 20
                    self.inTask = False
                else:
                    self.timer -= 1
    
    def plan_(self):
        
        if (len(self.tasks) >0):
            if (not self.taskLocked):
                self.taskLocked = random.choice(self.tasks[0])
                
            new_plan = self.Dijkstra([self.taskLocked])
            #if (new_plan == self.plan_before and len(self.plan_before)!=0 and not self.inTask):
             #   self.queue +=1
            self.plan        = new_plan
        
        elif (len(self.tasks) == 0):
            self.plan = self.moveRandom()

    def rangeOfSight(self, radius):
        reachable_pos = []
        curr_pos = self.getPosition()
        for i in range(-radius, radius):
            for j in range(-radius, radius):
                pos = [curr_pos[0]+i, curr_pos[1]+ j]
                if not isWall(self.getLayout(), pos[0], pos[1]):
                    reachable_pos.append(pos)
        return reachable_pos

    #Our reactive agent logic
    def scanGround(self, all_agents): 
        range = self.rangeOfSight(4)
        for pos in range:
            #if agent is dead in any position, call meeting
            for agent in all_agents:
                if ((agent.getPosition() == pos) and (agent.isDead())):
                    self.callVoting()

            # check if the impostor killed a crewmate in front of me 
            # self.callVoting(impostorID)
        return

    #Crewmate only - calling a voting session to expose impostor
    def callVoting(self, impostorID = -1):
        print("Agent ", self.getID(), " called a voting session")
        self.callingVote = True
        self.foundImpostor = impostorID
        return

    def vote(self):
        return
    

        

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Cafetaria(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Cafetaria_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Admin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Admin_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Storage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_WEIRD_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Storage_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_WEIRD_COLOR)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Shield_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Navigation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_WATER_BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Navigation_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_WATER_BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Weapons(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Weapons_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []


class Eletrical_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED_DARK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Eletrical(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED_WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Reactor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Reactor_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []

class Medbay(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHT_GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE

class Medbay_task(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARK_GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE 
        self.rect.y = self.y * TILESIZE
        self.pos = []
