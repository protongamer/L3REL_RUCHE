import time, os
from pipo import *
	
while True:
	
	if(TIME_OUT > 100):
		#run script here
		os.system("echo run script")
		#os.system("py script.py")
		TIME_OUT = 0;
		time.sleep(1)
	
	
	TIME_OUT = TIME_OUT + 1
	time.sleep(0.01)