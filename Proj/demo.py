import subprocess

f = open("test1.txt",'w')
for i in range (100):
	out = subprocess.run(['python','main.py','1','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")
	
f = open("test2.txt",'w')
for i in range (100):
	out = subprocess.run(['python','main.py','2','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")

f = open("test3.txt",'w')
for i in range (100):
	out = subprocess.run(['python','main.py','3','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")

f = open("test4.txt",'w')
for i in range (100):
	out = subprocess.run(['python','main.py','4','demo'], capture_output=True,universal_newlines=True).stdout
	f.write(out+"\n")
