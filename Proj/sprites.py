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
    def __init__(self, identifier, layout, starting_room):
        pygame.sprite.Sprite.__init__(self)
        self.id           = identifier
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 11,bold = True)
        self.textSurf = self.font.render(str(self.id), 1, WHITE,DARKRED)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKRED)
        self.image.blit(self.textSurf, [2, -1]) 

        self.rect = self.image.get_rect()

        self.beliefs      = dict() #id:(belief)
        self.layout       = layout
        self.plan         = []
        self.dead         = False
        self.range        = VIS_RANGE

        pos = random.choice(starting_room) #randomly chooses a position from cafetaria to spawn
            
        self.x = pos[0]
        self.y = pos[1]

        self.new_x = -1
        self.new_y = -1

        self.draw  = False
        
    def vote(self):
        min_value = min(self.beliefs.values()) #Searches for the min value
        keys = [key for key in self.beliefs if self.beliefs[key] == min_value]
        if len(keys) > 1:
            return -1
        else:
            return keys[0] 

    def setSettings(self,id_color,background_color,pos_x,pos_y):
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 11,bold=True)
        self.textSurf = self.font.render(str(self.id), 1, id_color,background_color)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(background_color)
        self.image.blit(self.textSurf, [pos_x, pos_y])

    def normalizeBeliefs(self):
        sum_beliefs = sum(self.beliefs.values())
        for b in self.beliefs.keys():
            self.beliefs[b] = self.beliefs[b]/sum_beliefs

    def decreaseBelief(self, id, factor):
        self.beliefs[id] -= self.beliefs[id]*factor
        self.normalizeBeliefs()

    def increaseBelief(self, id, factor):
        self.beliefs[id] += self.beliefs[id]*factor
        self.normalizeBeliefs()

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

 
    def rangeOfSight(self): #We know it's ugly. C'est la vie
        reachable_pos = []
        curr_pos = self.getPosition()
        for i in range(-self.range, self.range):
            for j in range(-self.range, self.range):
                pos = [curr_pos[0]+i, curr_pos[1]+ j]
                if not isWall(self.getLayout(), pos[0], pos[1]):
                    reachable_pos.append(pos)
   
        return reachable_pos


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

    def Dijkstra(self,initial_pos, dests): #TODO change to receive position!!!!!!
        if (initial_pos == []):
            source  = [self.x, self.y]

        else:
            source = initial_pos

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
    def __init__(self, identifier, crewmates, layout, tasks, starting_room):
        Agent.__init__(self, identifier, layout, starting_room)

        self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 11,bold=True)
        self.textSurf = self.font.render("I", 1, BLACK, YELLOW)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.image.blit(self.textSurf, [4, -1])

        self.tasks               = tasks
        self.task_locked         = []

        self.crewmates_locations = dict() #id:(pos)
        self.crewmates_status    = dict() #id: alive/dead (boolean)

        self.timer               = TIMER_NEAREST_CREWMATE #timer to calculate nearest crewmate
        self.kill_timer          = 0 #cooldown for the kill_function
        self.timerMostIsolated   = 0
        self.target              = 0
        self.target_locked       = False

        for agent in crewmates:
            self.crewmates_locations[agent.getID()] = agent.getPosition()
            self.crewmates_status[agent.getID()] = True

    def update(self, all_agents, agents_positions):
        for agent in all_agents:
            self.crewmates_locations[agent.getID()] = agent.getPosition()
        return super().update(all_agents, agents_positions)
    
    def mostIsolatedCrewmate(self, all_agents):
        dist_mostIsolated = dict()
        mostIsolated = dict()
        for agent in all_agents:
            if (not agent.isDead() and not agent.isImpostor()):
                aux_mostIsolated = dict()
                for agent2 in all_agents:
                    if (not agent2.isDead() and agent!=agent2 and not agent2.isImpostor()):
                        aux_mostIsolated[agent2.getID()] =  len(self.Dijkstra([agent.x,agent.y],[[agent2.x,agent2.y]]))
            
                mostIsolated[agent.getID()] = aux_mostIsolated 

        for agent in all_agents:
            if (not agent.isDead() and not agent.isImpostor()):
                dist_mostIsolated[agent.getID()] = min(mostIsolated[agent.getID()].values())

        sorted_keys = sorted(dist_mostIsolated, key=dist_mostIsolated.get)
        
        return sorted_keys

    def updateBeliefDeliberation(self, all_beliefs):
        #The impostor will trust less any crewmate that doesn't trust him
        #The impostor will trust more any crewmate that does trust him
        average_reputation = 0
        for id in all_beliefs.keys():
            if(id != self.id):
                average_reputation += all_beliefs[id][self.id]
        average_reputation = average_reputation/(len(all_beliefs) - 1)

        for id in self.beliefs:
            if(id != self.id):
                if(all_beliefs[id][self.id] < average_reputation):
                    self.decreaseBelief(id, 0.2)
                elif(all_beliefs[id][self.id] > average_reputation):
                    self.increaseBelief(id, 0.1)

    def updateBeliefAfterVote(self, vote_list):

        #The impostor will trust less any crewmate that voted for him
        for id in vote_list.keys():
            if id != self.getID():
                if vote_list[id] == self.id:
                    self.decreaseBelief(id, 0.5)

    def closestCrewmate (self): 
        # Returns a sorted list of crewmates ids from closest to furthest
        crewmates_distance      = dict()
        
        for id in self.beliefs.keys():
            if (self.crewmates_status[id]): #If crewmate is alive
                crewmates_distance[id] = len(self.Dijkstra([],[self.crewmates_locations[id]]))
                                   
        return sorted(crewmates_distance, key=crewmates_distance.__getitem__)
    
    def vote(self,voting_list):
        min_value = min(self.beliefs.values()) #Searches for the min value
        keys = [key for key in self.beliefs if self.beliefs[key] == min_value]
        if len(keys) > 1:
            return -1
        else:
            for vote in voting_list.values():
                if vote != -1:
                    return keys[0] 
            return -1

    def leastTrustedCrewmate(self): 
        # Returns a sorted list of crewmate ids from least trusted to most trusted
        return sorted(self.beliefs, key=self.beliefs.__getitem__)
       
    def getNewTarget(self, closest_crewmates = [], least_trusted_crewmates = [], isolated_crewmates=[]):
        # Returns the crewmate that minimizes the three heuristics scores, to be the new target

        total_score = dict() #crewmate_id: sum(score across lists)
        for id in self.beliefs.keys():
            total_score[id] = 0

        i = 0
        while((i<len(closest_crewmates)) or (i<len(least_trusted_crewmates)) or (i<len(isolated_crewmates))):
            if(i< len(closest_crewmates)):
                total_score[closest_crewmates[i]] += i

            if(i< len(least_trusted_crewmates)):
                total_score[least_trusted_crewmates[i]] += i

            if(i< len(isolated_crewmates)):
                total_score[isolated_crewmates[i]] += i
            i +=1

        target = 0
        while(target == 0):
            min_value = min(total_score.values()) #Searches for the min value
            ids = [key for key in total_score if total_score[key] == min_value]
            rand_id = random.choice(ids)
            if (self.crewmates_status[rand_id] == True):
                target = rand_id
            else:
                total_score.pop(rand_id)
        return target

    def updateTimers(self): #Updates the kill cooldown and update timer for the nearest crewmate
        if (self.timer < TIMER_NEAREST_CREWMATE):
            self.timer += 1
        if (self.kill_timer < COOLDOWN_KILL):
            self.kill_timer += 1
        if (self.timerMostIsolated < TIMER_MOST_ISOLATED):
            self.timerMostIsolated += 1

    #Impostor's plan function
    def plan_(self, all_agents,mode):
        if(self.kill_timer == COOLDOWN_KILL):
            if ( self.timer == TIMER_NEAREST_CREWMATE):
                if (mode != '1'):
                    self.task_locked = []
                    crewmates_trust = []
                    crewmates_isolated = []
                    crewmates_dist = self.closestCrewmate()
                    if (mode == '2'):
                        crewmates_trust = self.leastTrustedCrewmate()
                    if (self.timerMostIsolated == TIMER_MOST_ISOLATED):
                        self.timerMostIsolated = 0
                        if (mode == '4'):
                            crewmates_isolated = self.mostIsolatedCrewmate(all_agents)
                    self.target      = self.getNewTarget(closest_crewmates= crewmates_dist, least_trusted_crewmates= crewmates_trust,isolated_crewmates=crewmates_isolated)
                    
            
            target_pos     = self.crewmates_locations[self.target]
            self.plan        = self.Dijkstra([],[target_pos])

        else:
            if (mode == '1' or mode == '2'):
                self.plan = self.moveRandom()
            else:
                if self.task_locked == []:
                    task_locked = self.choseRandomTask()
                    self.task_locked = random.choice( task_locked)
                self.plan = self.Dijkstra([],[self.task_locked])
        

 
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

                range = self.rangeOfSight()

                if (agent.getID() == self.target):
                    victim = agent

                elif (agent.getPosition() in range):
                    agent.foundImpostor = self.getID()
           
            victim.die()
            dead_agents.add(victim)
            self.crewmates_status[self.target] = False
            victim.plan = []
            victim.setSettings(WHITE,BLACK,2,0)
            self.kill_timer = 0
            self.target     = 0
            
    def isClose(self, all_agents):
        #Used to check if impostor is within range of a crewmate
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
        return False, self.getNewTarget()
    
    def choseRandomTask(self):
        fake_task = random.choice(self.tasks)
        return fake_task

class Crewmate(Agent):
    def __init__(self, identifier, layout, tasks,  starting_room):
        super().__init__(identifier, layout,  starting_room)
        self.tasks        = tasks
        self.inTask       = False
        self.taskLocked   = []
        self.tasksDone     = 0
        self.timer        = TASK_TIME

        self.callingVote = False
        self.foundImpostor = -1
        self.lastSeenAgents = []

        self.maxStepsAlongside = dict()
        self.currentStepsAlongside = dict()
        for id in range(1, NUM_AGENTS+1):
            if (id != self.id):
                self.maxStepsAlongside[id] = 0
                self.currentStepsAlongside[id] = 0

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

    
    def scanGround(self, all_agents, mode): 
        range = self.rangeOfSight()
        new_seen_agents = []

        for pos in range:
            #we want to keep track of all alive agents within my range of sight
            for agent in all_agents:
                if((agent.getPosition() == pos) and (not agent.isDead()) and (agent.getID() != self.id)):
                    new_seen_agents.append(agent.getID())
        
        
        if len(new_seen_agents) > 0:
            self.lastSeenAgents = new_seen_agents
            for id in self.lastSeenAgents:
                self.currentStepsAlongside[id] +=1
                if(self.currentStepsAlongside[id] > self.maxStepsAlongside[id]):
                    self.maxStepsAlongside[id] = self.currentStepsAlongside[id]
                    
                    if (mode == '4'):
                        self.updateBeliefStepsAlongside()

        else:
            self.currentStepsAlongside = dict.fromkeys(self.currentStepsAlongside, 0)

        #Our reactive agent logic
        for pos in range:
            #if agent is dead in any position, call meeting
            for agent in all_agents:
                if ((agent.getPosition() == pos) and (agent.isDead())):
                    self.callVoting(mode)
                
        return

    def isTask (self, task):
        abort = True
        for i in range(len(task)):
            if (self.x == task[i][0] and self.y == task[i][1]):
                self.inTask = True
                if (self.timer == 0):
                    self.tasks      = self.tasks[1:]
                    self.taskLocked = []
                    self.tasksDone += 1
                    if (len(self.tasks)>0):
                        self.randTask = random.randint(0,len(self.tasks)-1)
                    self.timer  = 20
                    self.inTask = False
                else:
                    self.timer -= 1
                    if (self.timer == 0 and abort):
                        rand = random.random()
                        if (rand > TASK_SUCCESS):
                            self.timer = 20
                            abort = False
    
    def plan_(self):
        
        if (len(self.tasks) >0):
            if (not self.taskLocked):
                self.taskLocked = random.choice(self.tasks[0])
                
            new_plan = self.Dijkstra([],[self.taskLocked])
            #if (new_plan == self.plan_before and len(self.plan_before)!=0 and not self.inTask):
             #   self.queue +=1
            self.plan        = new_plan
        
        elif (len(self.tasks) == 0):
            self.plan = self.moveRandom()

    #Crewmate only - calling a voting session to expose impostor
    def callVoting(self, mode):
        #print("Agent ", self.getID(), " called a voting session")
        self.callingVote = True
    
        if (self.foundImpostor != -1):
            #print("Agent ",self.getID(), " found the impostor: ",self.foundImpostor)
            self.decreaseBelief(self.foundImpostor, 1) #remove all trust in the agent

        else:
            #print("Agent ",self.getID(), " now suspects of agents :",self.lastSeenAgents )
            if (mode == '3' or mode == '4'):
                for id in self.lastSeenAgents:
                    self.decreaseBelief(id, 0.1)
            return
    
    def updateBeliefDeliberation(self, all_beliefs):
        for id in all_beliefs.keys():
            if (id != self.id):
                for a in all_beliefs[id].keys(): #iterating through agent #id's beliefs
                    if(a != self.id):
                        diff = all_beliefs[id][a] - self.beliefs[a] #difference in beliefs about agent #a
                        if( diff < 0):
                            self.decreaseBelief(a, abs(diff)*self.beliefs[id])
                        elif( diff > 0):
                            self.increaseBelief(a, abs(diff)*self.beliefs[id])
        
    def updateBeliefAfterVote(self, voting_list):

        for id in voting_list.keys():

            if (id != self.getID()):

                #increases belief if an agent has the same vote as me
                if (voting_list[id] == voting_list[self.getID()]):
                    self.increaseBelief(id, 0.2)

                #decreases belief if an agent votes on me
                elif (voting_list[id] == self.getID()):
                    self.decreaseBelief(id, 0.2)
    
    def updateBeliefStepsAlongside(self):
        averageMaxSteps = sum(self.maxStepsAlongside.values())/len(self.maxStepsAlongside)

        for id in self.beliefs.keys():
            if self.maxStepsAlongside[id] > averageMaxSteps:
                self.increaseBelief(id, 0.01)

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
