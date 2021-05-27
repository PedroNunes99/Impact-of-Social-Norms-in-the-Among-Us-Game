import subprocess

f = open("dummy.txt",'w')
for i in range (100):
	print("dummy ",i)
	out = subprocess.run(['python','main.py','1','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")

f = open("test1.txt",'w')
for i in range (100):
	print("test1 ",i)
	out = subprocess.run(['python','main.py','2','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")


f = open("test2.txt",'w')
for i in range (100):
	print("test2 ",i)
	out = subprocess.run(['python','main.py','3','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")

f = open("test3.txt",'w')
for i in range (100):
	print("test3 ",i)
	out = subprocess.run(['python','main.py','4','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")
'''
f = open("test3_belief_03.txt",'w')
for i in range (100):
	print("test4c ",i)
	out = subprocess.run(['python','main.py','4','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")
'''