# Impact of Social Norms in the Among Us Game

## Autonomous Agents and Multi-Agent Systems 2021

This project consists of a simulation of the Among Us Game, applied to a multi-agent system context. It was done as our project in the Autonomous Agents and Multi-Agent Systems course.

### Brief Project Description
The project simulates an Among Us game, where there are two kinds of players: the Crewmates, and the Impostor. There is only one Impostor in this implementation.

Most of the game plays out in the _spaceship screen_.

The Crewmates have tasks to complete. To do this, each room in the spaceship has a few _highlighted positions_, where the Crewmates can sit on and perform the task. More details about this are in  `report`. 

In certain situations, a _voting session_ takes place. Then, the _voting screen appears_. There are multiple stages of a voting session, that appear sequentially: The deliberation phase, the voting phase, and the ejection screen.

### Directory and Module Organization
The project is alocated in the `Proj/` directory. There, we'll find a number of files:
* `main.py`: The main module where the project execution is done. 
* `sprites.py`: A file with the project classes. The most important ones are the _Agent_, _Crewmate_, and _Impostor_. The rest are only simple classes describing the spaceship rooms, the tasks, and other necessary rendering classes.
* `settings.py`: A file with a number of supporting fixed variables used throughout the simulation.
* `AmongUs.txt`: A support file to build the spaceship screen.
* `auxiliary.py`: A support file containing a few getter functions for the tasks and map recognition.
* `demo.py`: A file to run our experimental results.

### Running and Requirements
Our project is implemented in [Python](https://www.python.org/downloads/). To run our project, you must have the following packages installed:
* [Numpy](https://numpy.org/install/)
* [PyGame](https://www.pygame.org/wiki/GettingStarted)
* [MatplotLib](https://matplotlib.org/stable/users/installing.html)

The project can be executed according to four distinct execution modes:
* Dummy, a very basic implementation, with very little interaction between agents. 
```
python main.py 1
```
* Mode #1, a slightly more complex implementation, where the Impostor focuses on killing Crewmates that don't trust them and the Crewmates have some cooperation.
```
python main.py 2
```
* Mode #2, in which the Impostor also tries to fool other agents, and Crewmates now suspect of agents that they've last seen before finding a dead body.
```
python main.py 3
```

* Mode #3, our most sophisticated model. Now, the Impostor can find out more vulnerable targets and Crewmates will trust more in who's been near them.
```
python main.py 4
```

It is possible to reproduce our results and run the project in several different execution modes. Running `demo.py` will execute each of the execution modes 100 times and print out a summary for each execution in the following structure:
```
Winner(C/I) num-voting-sessions num-false-accusations num-iterations
```

To try out this demonstration, simply run:
```
python demo.py
```
