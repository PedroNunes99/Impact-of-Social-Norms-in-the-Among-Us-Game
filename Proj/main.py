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
#

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
	dead_agents.draw(SCREEN)

	s = 'Saved Agents: ' + str(len(agents_saved))
	drawText(SCREEN, s, 34, WIDTH/3, HEIGHT)
	s = 'Dead Agents: ' + str(len(agents_dead))
	drawText(SCREEN, s, 34, 2*WIDTH/3, HEIGHT)

	drawGrid()
	pygame.display.flip()

# Draw Text in screen
font_name = pygame.font.match_font('arial')
def drawText(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE, BLACK)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (int(x),int(y))
	surf.blit(text_surface, text_rect)

def assertInRange(speaker, listener):
	return abs(speaker.x - listener.x)<=VOL_RANGE and abs(speaker.y - listener.y)<=VOL_RANGE

def communicate(speaker):
	if (not speaker.isCommunicative()):
		return
	for listener in all_agents:
		if (speaker.getID() == listener.getID()): continue
		if assertInRange(speaker, listener):
			listener.receiveMessage(speaker.getLayout())


# Main
if __name__ == "__main__":
	global SCREEN, CLOCK, layout, all_sprites, all_agents, dead_agents, all_admin,all_admin_task,all_storage,all_storage_task,all_shield,all_shield_task,all_navigation,all_navigation_task,all_weapons,all_weapons_task ,all_cafetaria, all_cafetaria_task, all_medbay, all_medbay_task, all_reactor, all_reactor_task, all_eletrical,all_eletrical_task, all_walls, all_fires, all_smokes, soundAlarm, tasks


	pygame.init()
	pygame.display.set_caption("Among US simulation")
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT+40))
	CLOCK = pygame.time.Clock()
	SCREEN.fill(BLACK)
	
	# Create agents
	layout = getLayout(None)
	
	#List of all tasks
	tasks = []
	cafetaria_tasks_pos = list(getCafetaria_task(layout))
	print(list(getCafetaria(layout)))
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
	dead_agents = pygame.sprite.Group()
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


	for i in range(NUM_AGENTS):
		player = Agent(i+1, deepcopy(layout), tasks, 1, True)
		#player.tasks = random.choice(tasks)
		all_sprites.add(player)
		all_agents.add(player)
	


	pause = False
	run   = True
	
	agents_saved = []
	agents_dead = []

	# Main cycle
	i = 0
	while run:
		
		CLOCK.tick(FPS)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					pause = not pause

		if pause:
			pygame.mixer.pause()
		else:
			pygame.mixer.unpause()


		#if len(agents_saved) + len(agents_dead) == NUM_AGENTS:
		#	break
		if not pause:
			

			for agent in all_agents:
				agent.percept(layout)
				if (len(agent.tasks)>0):
					task = agent.tasks[0]
					agent.isTask(task)
					if (i == 60):
						if (agent.id == 1):
							agent.dead = True
					print(all_agents)
				#agent.checkAlarm(soundAlarm)
				#communicate(agent)
			for agent in all_agents:
				agent.plan_()
				
			all_agents.update(all_agents,dead_agents)
			draw()

		i+=1

	pygame.mixer.pause()
	time.sleep(2)
	pygame.quit()