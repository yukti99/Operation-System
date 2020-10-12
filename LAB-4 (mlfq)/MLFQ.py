'''
Multilevel Feedback Queue Scheduling (MLFQ) CPU Scheduling
YUKTI KHURANA

0 -> highest priority queue
q-1 -> lowest priority queue

Basic rules for MLFQ:

Rule 1: If Priority(A) > Priority(B), A runs (B doesn’t).
Rule 2: If Priority(A) = Priority(B), A & B run in RR.
Rule 3: When a job enters the system, it is placed at the highest priority (the topmost queue). 
Rule 4:  T1 (time after which the priority is downgraded by -1) and T2( time after which priority is upgraded by +1)

'''

def displayInfo(qno,pqueue,processes):
	print("\n******************* MULTILEVEL FEEDBACK QUEUE SCHEDULING *******************\n")
	print("The number of Queues = ",qno)
	print("Process ID | ResponseTime | WaitingTime | Turn-AroundTime")
	avgrt=0
	avgwt=0
	avgtat=0
	for y in processes.items():
		x = y[1]
		print(x["pid"],"\t\t",x["response"],"\t\t",x["wt"],"\t\t",x["tat"])
		avgrt+=x["response"]
		avgtat+=x["tat"]
		avgwt+=x["wt"]
	avgrt/=qno
	avgwt/=qno
	avgtat/=qno
	avgrt = "{:.2f}".format(avgrt)
	avgwt = "{:.2f}".format(avgwt)
	avgtat = "{:.2f}".format(avgtat)
	print("Average Response Time | Average Waiting Time | Average Turn-Around Time")
	print(avgrt,"\t\t\t",avgwt,"\t\t\t",avgtat,"\t\t\t")
	print("\n***************************************************************************\n")
	

	
def decrementPriority(qno,processes,pqueue,processRunning):
	if (processRunning != -1):
		cp = processes[processRunning]["queue"]
		print("cp = ",cp)
		newPrior = cp-1		
		if (newPrior < 0):
			newPrior = qno-1
		print("np = ",newPrior)
		posi = processes[processRunning]["pos"]+1
		print(processes[processRunning])
		j = processes[processRunning]["burst"][posi]
		l = [processRunning,j]
		print("Appending ",l)
		pqueue[newPrior].append(l)
		processes[processRunning]["queue"] -= 1
			
def incrementPriority(qno,processes,pqueue,processRunning):
	if (processRunning != -1):
		cp = processes[processRunning]["queue"]
		newPrior = cp+1
		if (newPrior >= qno):
			newPrior = 0
		posi = processes[processRunning]["pos"]+1
		j = processes[processRunning]["burst"][posi]
		l = [processRunning,j]
		print("Appending ",l)
		pqueue[newPrior].append(l)
		processes[processRunning]["queue"] += 1				

def main():	
	# taking input from file- "input.py"
	f = open("MLFQ.dat", "r")
	qno = int(f.readline())
	quanta = list(map(int,f.readline().strip().split(" ")))
	t1,t2 = list(map(int,f.readline().strip().split(" ")))	
	pno = int(f.readline())
	print("t1 = ",t1)
	print("t2 = ",t2)
	
	print("Quanta values : ",quanta)
		
	# dictionary that contains (pid : {process info}) pairs <- nested dictionary
	processes = dict()
		
	pids = []
	for i in range(pno):
		l = f.readline().strip().split(" ")
		# dictionary that stores all process info
		d = dict()
		d["pid"] = int(l[0])
		pids.append(int(l[0]))
		pid = int(l[0])
		d["arrival"] = int(l[1])
		d["prior"] = int(l[2])		
		d["burst"] = l[3:]
		for i,j in enumerate(d["burst"]):
			# converting the burst timings to integer type for calculations
			if not j in ["P", "I", "O"]:
				d["burst"][i] = int(j)			
		d["response"] = -1
		d["tat"] = 0
		d["wt"] = 0
		d["pos"] = 0	
		d["arrived"] = False
		d["queue"] = 0
		d["complete"] = False
		d["quanta"] = 0
		# nested dictionary 		
		processes[pid] = d
		
	
		
	# sorting process in ascending order by arrival times
	processes = dict(sorted(processes.items(), key = lambda x: (x[1]["arrival"],-x[1]["prior"])))
			
	# VARIABLES USED FOR MLFQ
	
	# time variable to keep track of time
	time=0	
	
	# Input queue [..[pid,queuePriority,burst]..]
	inputqueue = []
	
	# Output queue [..[pid,queuePriority,burst]..]
	outputqueue = []
	
	# reprsents the pid of current process running in particular queue 
	processRunning = -1
	
	# time left for current process to complete its queue's respective quanta
	timeLeft=0
	
	# time for which the process has been running to keep track of change of its process burst over time
	ptime=0
	
	# extra variables to store the downgrade and upgrade values
	downgrade = t1
	upgrade = t2
	
	# input/output operation
	io = False
	
	# pid of current process in execution in cpu
	processRunning = -1
	
	# list that contains current running processes parameters; pqueue = [..[.. (0-pid,2-workposition).. ]..] - list of list
	pqueue=[]
	
	# priority of queue in which current running process is present
	currentPrior = 0
	ptime=0
	currentQuanta=0
	
	for i in range(qno):
		pqueue.append([])
	print(pqueue)
	
	# MLFQ SCHEDULING BEGINS
	# infinite loop till all qno of processes are completed
	while(True):
	
		# checking the processes that have reached their arrival time by looping through all the  processes
		for pi in pids:
			if (time == processes[pi]["arrival"]):
				# next Index
				next = processes[pi]["pos"]+1
				q = quanta[0]
				
				# on arrival the process is given the highest priority queue i.e 0 
				l = [ processes[pi]["pid"], processes[pi]["burst"][next] ]
				pqueue[0].append(l)
				
				processes[pi]["queue"] = 0
				processes[pi]["arrived"] = True
				processes[pi]["quanta"] = q
				
				# the quantum for current running process in highest priority queue
				timeLeft = quanta[0]
				
				print("Process - ",processes[pi]["pid"],"has been added to the ready queue-0 at time = ",time)
				print("pqueue = ",pqueue)
				pi+=1		
		
		# if input queue is not empty
		if len(inputqueue) != 0:
			ip, ileft = inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1	
				p = processes[ip]["queue"]	
				l = [ ip, processes[ip]["burst"][next] ]				
				pqueue[p].append(l)			
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft = outputqueue[0]		
			if oLeft == 0:
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				p = processes[op]["queue"]	
				l = [ op, processes[op]["burst"][next] ]				
				pqueue[p].append(l)	
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
		
		# at a time only the highest priority queue's processes will execute in Round Robin
		# cpu is free for a process to run 
		
		if (processRunning == -1):
			if (len(pqueue[currentPrior]) != 0 ):	
				timeLeft = quanta[currentPrior]
				processRunning,ptime = pqueue[currentPrior][0]			
				print("Current process = ",processRunning)
				print("Ready Pqueue = ",pqueue)
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
				pqueue[currentPrior].pop(0)	
			else:
				currentPrior+=1	
				print("!!!!!!!NOW PRIORITY QUEUE - ",currentPrior,"WILL RUN IN ROUND ROBIN!!!!!!!")
				if (currentPrior >= qno):
					currentPrior = 0	
		
		
		# incrementing time
		time += 1
		if (t1>0):
			t1-=1
		if (t2>0):
			t2-=1
			
		if (timeLeft>0):
			timeLeft-=1
		
		
		print("\n******************************\n")
		print("At time = ",time)
		print("Current process = ",processRunning)
		print("time left for current process = ",timeLeft)
		print("ptime = ",ptime)
		print("pqueue = ",pqueue)
		print("Input queue = ",inputqueue)
		print("Output queue = ",outputqueue)
		
		#calculating waiting time
		for h in pqueue:
			if (len(h)!=0):
				for g in h:	
					processes[g[0]]["wt"] += 1
					print("process with pid = ",g[0]," has been waiting for time = ",processes[g[0]]["wt"])
		print("\n******************************\n")
		
		if (processRunning != -1):
			# priority downgraded by -1 
			if (t1 == 0 and ptime!=0):
				print("the priority of process - ",processRunning," is increased")
				t1 = downgrade
				decrementPriority(qno,processes,pqueue,processRunning)
				processRunning=-1
				
				
				
			# priorities are upgraded by +1 
			if (t2 == 0 and ptime!=0):
				print("the priority of process - ",processRunning," is decreased")
				t2 = upgrade
				incrementPriority(qno,processes,pqueue,processRunning)
				processRunning=-1
				
				
			
		# printing status of all queues and processes
		k=0	
		for a in pqueue:
			print("Priority -",k,":",)
			for b in a:
				print(b,";"),
			k+=1

			
		# when some process is running in cpu
		if (processRunning != -1):		
			# its ptime decremented			
			ptime -= 1
			print("process burst left for current running process = ",ptime)
			
			# if process burst is done before finish of its respective queue quanta
			# it's priority is not decremented
			if (ptime == 0):			

				processes[processRunning]["pos"] += 2
				next = processes[processRunning]["pos"]
				nextop  = processes[processRunning]["burst"][next]
				
				if (nextop  == -1):
					processes[processRunning]["complete"] = True	
					processes[processRunning]["tat"] = time-processes[processRunning]["arrival"]
					print("\n\nPROCESS ",processRunning,"COMPLETED!!!!!!!!\n\n")	
				else:
					io = True
				
				lastProcess = processRunning
				processRunning = -1 # cpu is ready to handle next process in queue
				
			# if process burst is not done and quantum is over,context switch to next process in queue
			# if a process takes longer burst than t1, its queue priority is decremented	
			elif (ptime !=0 and timeLeft==0):
				
				print("The quanta for current process-",processRunning,"is over")
				print("Context switch to next process in current priority queue!")
							
				# context switch to be done
				next = processes[processRunning]["pos"]+1
								
				# processor burst set to remaining time 
				processes[processRunning]["burst"][next] = ptime
				
				#print("Burst changed !!!!")
				#print(processes[processRunning])
				#print("next = ",next)

				# current process added to back of queue with remaining burst time
				l = [processRunning,ptime]
				pqueue[currentPrior].append(l)
				
				print("pqueue : ",pqueue,"\n")
				
				# next process in queue taken to run
				lastProcess = processRunning
				processRunning= -1
		
								
			else :
				# keep progressing the current process
				nextop = None			
			
		else:
			nextop = None		
			
		# adding processes to input and output queue
		if (io and nextop  == "I"):
			next = processes[lastProcess]["pos"]+1
			inputqueue.append([lastProcess, processes[lastProcess]["burst"][next]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the input queue at time = ",time)
			io = False

		elif (io and nextop == "O"):
			next = processes[lastProcess]["pos"]+1
			outputqueue.append([lastProcess, processes[lastProcess]["burst"][next]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the input queue at time = ",time)
			io = False

		else:
			pass
					
		if (processRunning==-1  and len(inputqueue)==0 and  len(outputqueue)==0):			
			done = True
			for pid in pids:
				if (processes[pid]["complete"] == False):
					done = False
					break
			if (done == True):
				print(pqueue)
				break # all the processes are completed!!
		
		
	
	displayInfo(qno,pqueue,processes)		
	
main()


			
