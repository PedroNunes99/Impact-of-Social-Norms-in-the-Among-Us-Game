from settings import HEIGHT, NUM_AGENTS, WIDTH
import pygame
from auxiliary import *
from random import choices
from settings import *
from sprites import *
from copy import deepcopy
import time

def drawGrid():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(SCREEN, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(SCREEN, BLACK, (0, y), (WIDTH, y))

def createWalls():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isWall(layout,i,j)):
                wall = Wall(i,j)
                all_sprites.add(wall)
                all_walls.add(wall)

def createMedbay():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isMedBay(layout,i,j)):
                medbay = Medbay(i,j)
                all_sprites.add(medbay)
                all_medbay.add(medbay)

def createMedbay_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isMedBay_task(layout,i,j)):
                medbay_task = Medbay_task(i,j)
                all_sprites.add(medbay_task)
                all_medbay_task.add(medbay_task)

def createCafetaria():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isCafetaria(layout,i,j)):
                cafetaria = Cafetaria(i,j)
                all_sprites.add(cafetaria)
                all_cafetaria.add(cafetaria)

def createCafetaria_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isCafetaria_task(layout,i,j)):
                cafetaria_task = Cafetaria_task(i,j)
                all_sprites.add(cafetaria_task)
                all_cafetaria_task.add(cafetaria_task)

def createReactor():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isReactorEngine(layout,i,j)):
                reactor = Reactor(i,j)
                all_sprites.add(reactor)
                all_reactor.add(reactor)

def createReactor_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isReactorEngine_task(layout,i,j)):
                reactor_task = Reactor_task(i,j)
                all_sprites.add(reactor_task)
                all_reactor_task.add(reactor_task)

def createEletricalTask():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isEletrical_task(layout,i,j)):
                eletrical_task = Eletrical_task(i,j)
                all_sprites.add(eletrical_task)
                all_eletrical_task.add(eletrical_task)

def createEletrical():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isEletrical(layout,i,j)):
                eletrical = Eletrical(i,j)
                all_sprites.add(eletrical)
                all_eletrical.add(eletrical)

def createAdmin():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isAdmin(layout,i,j)):
                admin = Admin(i,j)
                all_sprites.add(admin)
                all_admin.add(admin)

def createAdmin_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isAdmin_task(layout,i,j)):
                admin_task = Admin_task(i,j)
                all_sprites.add(admin_task)
                all_admin_task.add(admin_task)

def createStorage():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isStorage(layout,i,j)):
                storage = Storage(i,j)
                all_sprites.add(storage)
                all_storage.add(storage)

def createStorage_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isStorage_task(layout,i,j)):
                storage_task = Storage_task(i,j)
                all_sprites.add(storage_task)
                all_storage_task.add(storage_task)

def createShields():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isShield(layout,i,j)):
                shield = Shield(i,j)
                all_sprites.add(shield)
                all_shield.add(shield)

def createShields_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isShield_task(layout,i,j)):
                shield_task = Shield_task(i,j)
                all_sprites.add(shield_task)
                all_shield_task.add(shield_task)

def createNavigation():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isNavigation(layout,i,j)):
                navigation = Navigation(i,j)
                all_sprites.add(navigation)
                all_navigation.add(navigation)

def createNavigation_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isNavigation_task(layout,i,j)):
                navigation_task = Navigation_task(i,j)
                all_sprites.add(navigation_task)
                all_navigation_task.add(navigation_task)

def createWeapons():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isWeapons(layout,i,j)):
                weapons = Weapons(i,j)
                all_sprites.add(weapons)
                all_weapons.add(weapons)

def createWeapons_task():
    for i in range(int(GRIDWIDTH)):
        for j in range(int(GRIDHEIGHT)):
            if (isWeapons_task(layout,i,j)):
                weapons_task = Weapons_task(i,j)
                all_sprites.add(weapons_task)
                all_weapons_task.add(weapons_task)

def pause_():

	paused = True

	while paused:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused = False

def drawVotingScreen(old_beliefs, new_beliefs, voting_list, idEjected):

	## DELIBERATION PHASE - SHOWING OLD BELIEFS ##
	SCREEN.fill(WHITE)
	rect_side = HEIGHT/NUM_AGENTS -2
	drawText(SCREEN, "Deliberation Phase", 30, WIDTH/2, 10)
	drawText(SCREEN, "Old beliefs", 20, WIDTH/2, 50)
	s = 'Press P'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT)
	s = 'for pause'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT+20)
	top, left  = HEIGHT-60,  30

	font = pygame.font.SysFont('freesansbold', 50)
	for agent in all_agents:
		if (top <= 60):
			top = HEIGHT-60
			left += 300
		for belief in old_beliefs.keys():
			for value in old_beliefs[belief].keys():
				old_beliefs[belief][value] = round(old_beliefs[belief][value],2)
		SCREEN.blit(font.render(str(agent.getID()), 1, WHITE, RED), (left+10, top))
		drawText(SCREEN, str(old_beliefs[agent.getID()]), 15, left+150, top+4)
		pygame.display.update()
		top -=  rect_side + 60

	pygame.display.flip()	
	time.sleep(5)
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause_()


	## DELIBERATION PHASE - SHOWING NEW BELIEFS ##
	SCREEN.fill(WHITE)
	pygame.display.flip()
	time.sleep(0.5)

	SCREEN.fill(WHITE)
	rect_side = HEIGHT/NUM_AGENTS -2
	drawText(SCREEN, "Deliberation Phase", 30, WIDTH/2, 10)
	drawText(SCREEN, "New beliefs", 20, WIDTH/2, 50)
	s = 'Press P'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT)
	s = 'for pause'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT+20)
	top, left  = HEIGHT-60,  30

	font = pygame.font.SysFont('freesansbold', 50)
	for agent in all_agents:
		if (top <= 60):
			top = HEIGHT-60
			left += 300
		for belief in new_beliefs.keys():
			for value in new_beliefs[belief].keys():
				new_beliefs[belief][value] = round(new_beliefs[belief][value],2)
		SCREEN.blit(font.render(str(agent.getID()), 1, WHITE, RED), (left+10, top))
		drawText(SCREEN, str(new_beliefs[agent.getID()]), 15, left+150, top+4)
		pygame.display.update()
		top -=  rect_side + 60

	pygame.display.flip()
	time.sleep(5)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause_()

	## VOTING PHASE - SHOWING VOTES ##
	SCREEN.fill(WHITE)
	pygame.display.flip()
	time.sleep(0.5)

	SCREEN.fill(WHITE)
	rect_side = HEIGHT/NUM_AGENTS -2
	drawText(SCREEN, "Voting Phase", 30, WIDTH/2, 10)
	s = 'Press P'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT)
	s = 'for pause'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT+20)

	top, left  = HEIGHT-60,  30

	font = pygame.font.SysFont('freesansbold', 50)
	for agent in all_agents:
		if (top <= 60):
			top = HEIGHT-60
			left += 300
		SCREEN.blit(font.render(str(agent.getID()), 1, WHITE, RED), (left+10, top))
		if(voting_list[agent.getID()] == -1):
			drawText(SCREEN, "Agent chose not to vote", 20, left+150, top+4)
		else:
			drawText(SCREEN, str(voting_list[agent.getID()]), 20, left+150, top+4)
		pygame.display.update()
		top -=  rect_side + 60

	pygame.display.flip()
	time.sleep(5)	

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause_()	

	## VOTING PHASE - SHOWING EJECTED AGENT ##
	SCREEN.fill(DARK_WATER_BLUE)
	
	if(idEjected == 0):
		drawText(SCREEN, "No one was ejected...", 30, WIDTH/2, 10)

	else:
		font = pygame.font.SysFont('freesansbold', 80)
		SCREEN.blit(font.render(str(idEjected), 1, WHITE, RED), (WIDTH/2, HEIGHT/2))
		s = "Agent "+ str(idEjected) + " was ejected"
		drawText(SCREEN, s, 40, WIDTH/2, 10)

	pygame.display.flip()
	time.sleep(5)

	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause_()

def drawWinImpostor():
	SCREEN.fill(WHITE)
	s = "The Impostor Won"
	drawText(SCREEN, s, 34, WIDTH/2, HEIGHT/2)
	pygame.display.flip()
	pygame.mixer.pause()
	time.sleep(3)
	pygame.quit()
	quit()

def drawWinCrewmates():
	SCREEN.fill(WHITE)
	s = "The Crewmates Won"
	drawText(SCREEN, s, 34, WIDTH/2, HEIGHT/2)
	pygame.display.flip()
	pygame.mixer.pause()
	time.sleep(3)
	pygame.quit()
	quit()

#Draw main world
def draw():		 		
	SCREEN.fill(WHITE)

	all_walls.draw(SCREEN)
	all_eletrical.draw(SCREEN)
	all_eletrical_task.draw(SCREEN)
	all_reactor_task.draw(SCREEN)
	all_reactor.draw(SCREEN)
	all_medbay.draw(SCREEN)
	all_medbay_task.draw(SCREEN)
	all_cafetaria.draw(SCREEN)
	all_cafetaria_task.draw(SCREEN)
	all_admin.draw(SCREEN)
	all_admin_task.draw(SCREEN)
	all_storage.draw(SCREEN)
	all_storage_task.draw(SCREEN)
	all_shield.draw(SCREEN)
	all_shield_task.draw(SCREEN)
	all_weapons.draw(SCREEN)
	all_weapons_task.draw(SCREEN)
	all_navigation.draw(SCREEN)
	all_navigation_task.draw(SCREEN)
	all_agents.draw(SCREEN)

	agents_dead_count = 0
	agents_alive_count = 0

	for agent in all_agents:
		if (agent.isDead() and not agent.isImpostor()):
			agents_dead_count +=1
		elif not agent.isDead() and not agent.isImpostor():
			agents_alive_count += 1

	s = 'Crewmates Alive: ' + str(agents_alive_count)
	drawText(SCREEN, s, 34, WIDTH/3 - WIDTH/8, HEIGHT)
	s = 'Dead Crewmates: '+ str(agents_dead_count)
	drawText(SCREEN, s, 34, WIDTH/3 + 3*WIDTH/10, HEIGHT)
	s = 'Press P'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT)
	s = 'for pause'
	drawText(SCREEN,s, 17, WIDTH - WIDTH/15,HEIGHT+20)
	
	drawGrid()
	pygame.display.flip()

# Draw Text in screen
font_name = pygame.font.match_font('arial')
def drawText(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, BLACK, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (int(x),int(y))
	surf.blit(text_surface, text_rect)


def communicate(speaker):
	if (not speaker.isCommunicative()):
		return
	for listener in all_agents:
		if (speaker.getID() == listener.getID()): continue
		if assertInRange(speaker, listener):
			listener.receiveMessage(speaker.getLayout())

#repositions agents after a voting session
def repositionAgents():
	
	cafetaria_pos = list(getCafetaria(layout))

	for agent in all_agents:
		rand_pos = random.choice(cafetaria_pos)
		agent.x = rand_pos[0]
		agent.y = rand_pos[1]
		agent.plan = []
		cafetaria_pos.remove(rand_pos)
		if agent.isImpostor():
			agent.timer = TIMER_NEAREST_CREWMATE
			agent.kill_timer = 0


def updateWorld():
	voting = False
	all_tasks_done = True
	unassigned_tasks = []
	all_agents.update(all_agents, agents_locations)

	#If Impostor killed NUM_AGENT-1 crewmates, IMPOSTOR WINS
	if (len(dead_agents) == NUM_AGENTS - 2): 	
		drawWinImpostor()
		return 


	#update agents locations
	for agent in all_agents:
		agents_locations[agent.getID()] = agent.getPosition()
		
	#check if an agent called a voting session
	for agent in all_agents:
		if (not agent.isImpostor()) and (agent.callingVote) and not agent.isDead():
			votingSession()
			voting = True
			agent.callingVote = False
			repositionAgents()
			break

	for agent in dead_agents:
		if len(agent.tasks) != 0:
			for task in agent.tasks:
				unassigned_tasks.append(task)
				agent.tasks.remove(task)
		
	agents_ids = []

	for agent in all_agents:
		if not agent.isDead() and not agent.isImpostor():
			agents_ids.append(agent.getID())


	for task in unassigned_tasks:
		rand_id = random.choice(agents_ids)
		
		for agent in all_agents:
			if agent.getID() == rand_id and not agent.isDead():
				agent.tasks.append(unassigned_tasks[0])
				unassigned_tasks = unassigned_tasks[1:]


	if(voting):
		for agent in all_agents:
			agent.callingVote = False

		#If Impostor was voted out, CREWMATES WIN
		for agent in dead_agents: 				
			if (agent.isImpostor()):
				drawWinCrewmates()
				return

		#If the voted agent was a crewmate and there are only 2 crewmates left, IMPOSTOR WINS
		if (len(dead_agents) == NUM_AGENTS - 2): 
			drawWinImpostor()
			return 

	for agent in all_agents:
		if not agent.isDead() and not agent.isImpostor():
			if len(agent.tasks) != 0:
				all_tasks_done = False
				break
	#If all assigned tasks are done, CREWMATES WIN
	if(all_tasks_done):
		drawWinCrewmates()
		return
	draw() 	#draw all agents

def checkMajority(array):
	maxCount = 0
	index = -1

	n = len(array)

	majority = 0

	for i in range(n):
		count = 0
		if (array[i] != -1):
			for j in range(n):
				if (array[i] == array[j]):
					count += 1
			
			if (count > maxCount):
				maxCount = count
				index  = i

	if (maxCount > n//2):
		majority = array[index]
	else:
		return 0

	return majority

def votingSession():
	
	#delete already found dead bodies and re-distribute tasks
	unassigned_tasks = [] #non completed tasks previously belonging to dead agents

	aux_voting_list = dict() #id : [beliefs about agent #id]
	voting_list = dict()

	old_beliefs = dict() #id: [beliefs that agent #id holds]
	new_beliefs = dict() #id: [beliefs that agent #id holds]
	
	#removes the beliefs of all dead agents from other alive agents, removing the dead
	#agent from all_agents list
	for agent in all_agents:
		if agent.isDead():
			for task in agent.tasks:
				unassigned_tasks.append(task)
			for agent2 in all_agents:
				if agent != agent2 and not agent2.isDead():
					agent2.beliefs.pop(agent.getID())
					
			all_agents.remove(agent)

	#Get the beliefs of each agent before deliberation
	for agent in all_agents:
		old_beliefs[agent.getID()] = agent.beliefs.copy()
	
    #Collective Deliberation
	for agent in all_agents:
		if not agent.isDead():
			list_ = []
			for agent2 in all_agents:
				if not agent2.isDead() and agent2 != agent:
					list_.append(agent2.beliefs[agent.getID()])
			
			aux_voting_list[agent.getID()] = sum(list_)/len(list_)

	#Voting Session
	for agent in all_agents:
		if (not agent.isDead()):
			agent.updateBeliefDeliberation(old_beliefs)
		
		new_beliefs[agent.getID()] = agent.beliefs.copy()
		if (not agent.isImpostor()):
			voting_list[agent.getID()] = agent.vote()
		else:
			voting_list_ = voting_list.copy()
			voting_list[agent.getID()] = agent.vote(voting_list_)

	idEjected = checkMajority(list(voting_list.values()))
	drawVotingScreen(old_beliefs, new_beliefs, voting_list, idEjected)

	for agent in all_agents:
		agent.updateBeliefAfterVote(voting_list)
	

	#If there was a majority in the vote
	if (idEjected != 0):
		for agent in all_agents:
			if (idEjected == agent.getID()):
				dead_agents.add(agent)
				all_agents.remove(agent)
			else:
				agent.beliefs.pop(idEjected)

	#Re-Assigning the dead crwmates's unfinished tasks to alive crewmates
	for agent in all_agents:
		if(len(unassigned_tasks) > 0):
			task = unassigned_tasks[len(unassigned_tasks)-1]
			agent.tasks.append(task)
			unassigned_tasks.remove(task)
		else:
			break
	return

# Main
if __name__ == "__main__":
	global SCREEN, run, CLOCK, layout, all_sprites, all_agents, dead_agents, agents_locations, all_admin,all_admin_task,all_storage,all_storage_task,all_shield,all_shield_task,all_navigation,all_navigation_task,all_weapons,all_weapons_task ,all_cafetaria, all_cafetaria_task, all_medbay, all_medbay_task, all_reactor, all_reactor_task, all_eletrical,all_eletrical_task, all_walls,  tasks

	pygame.init()
	pygame.display.set_caption("Among US simulation")
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT+40))
	CLOCK = pygame.time.Clock()

	# Create agents
	layout = getLayout(None)
	
	#List of all tasks
	tasks = []
	cafetaria_tasks_pos = list(getCafetaria_task(layout))
	admin_tasks_pos = list(getAdmin_task(layout))
	eletrical_tasks_pos = list(getEletrical_task(layout))
	medbay_tasks_pos = list(getMedBay_task(layout))
	navigation_tasks_pos = list(getNavigation_task(layout))
	shield_tasks_pos = list(getShield_task(layout))
	storage_tasks_pos = list(getStorage_task(layout))
	weapons_tasks_pos = list(getWeapons_task(layout))
	reactorEngine_tasks_pos = list(getReactorEngine_task(layout))
	tasks.append(cafetaria_tasks_pos)
	tasks.append(admin_tasks_pos)
	tasks.append(eletrical_tasks_pos)
	tasks.append(medbay_tasks_pos)
	tasks.append(navigation_tasks_pos)
	tasks.append(reactorEngine_tasks_pos)
	tasks.append(shield_tasks_pos)
	tasks.append(storage_tasks_pos)
	tasks.append(weapons_tasks_pos)


	all_sprites = pygame.sprite.Group()
	all_walls   = pygame.sprite.Group()
	all_eletrical_task = pygame.sprite.Group()
	all_eletrical = pygame.sprite.Group()
	all_reactor = pygame.sprite.Group()
	all_reactor_task = pygame.sprite.Group()
	all_medbay = pygame.sprite.Group()
	all_medbay_task = pygame.sprite.Group()
	all_cafetaria = pygame.sprite.Group()
	all_cafetaria_task = pygame.sprite.Group()
	all_admin = pygame.sprite.Group()
	all_admin_task = pygame.sprite.Group()
	all_storage = pygame.sprite.Group()
	all_storage_task = pygame.sprite.Group()
	all_shield = pygame.sprite.Group()
	all_shield_task = pygame.sprite.Group()
	all_navigation = pygame.sprite.Group()
	all_navigation_task = pygame.sprite.Group()
	all_weapons = pygame.sprite.Group()
	all_weapons_task = pygame.sprite.Group()
	all_agents  = pygame.sprite.Group()
	dead_agents = pygame.sprite.Group()

	createWalls()
	createEletricalTask()
	createEletrical()
	createReactor()
	createReactor_task()
	createMedbay()
	createMedbay_task()
	createCafetaria()
	createCafetaria_task()
	createAdmin()
	createAdmin_task()
	createStorage()
	createStorage_task()
	createWeapons()
	createWeapons_task()
	createNavigation()
	createNavigation_task()
	createShields()
	createShields_task()

	cafetaria_pos = list(getCafetaria(layout))

	agents_locations = dict() #id: location

	for i in range(1, NUM_AGENTS):
		player = Crewmate(i, deepcopy(layout), tasks, cafetaria_pos)
		pos =[player.x,player.y]
		cafetaria_pos.remove(pos) 
		all_sprites.add(player)
		all_agents.add(player)
		agents_locations[i] = pos
	
	player = Impostor(i+1, all_agents, deepcopy(layout), tasks, cafetaria_pos)
	agents_locations[i] = player.getPosition()
	all_sprites.add(player)
	all_agents.add(player)

	for agent in all_agents:
		for agent2 in all_agents:
			if (agent != agent2):
				agent.beliefs[agent2.getID()] = INITIAL_BELIEF
	

	pause = False
	run   = True
	
	# Main cycle
	i = 0
	while run:
		
		CLOCK.tick(FPS)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					pause_()

		if pause:
			pygame.mixer.pause()
		else:
			pygame.mixer.unpause()
		
		if not pause:
			
			for agent in all_agents:
				if (agent.isImpostor()):
					agent.kill(all_agents, dead_agents)
					agent.updateTimers()
				if (not agent.isImpostor() and len(agent.tasks)>0 and not agent.isDead()):
					agent.scanGround(all_agents)
					task = agent.tasks[0]
					agent.isTask(task)
				
				agent.draw = True 
				#communicate(agent)
			for agent in all_agents:
				if (not agent.isDead()):
					if(not agent.isImpostor()):
						agent.plan_()
					else:
						agent.plan_(all_agents)
			
			updateWorld()		

		i+=1

	pygame.mixer.pause()
	time.sleep(5)
	pygame.quit()

