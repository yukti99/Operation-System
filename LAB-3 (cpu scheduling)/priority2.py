'''

In Preemptive Priority Scheduling, at the time of arrival of a process in the ready queue, its Priority is compared with the priority of the other processes present in the ready queue as well as with the one which is being executed by the CPU at that point of time. The One with the highest priority among all the available processes will be given the CPU next.
The difference between preemptive priority scheduling and non preemptive priority scheduling is that, in the preemptive priority scheduling, the job which is being executed can be stopped at the arrival of a higher priority job.
Once all the jobs get available in the ready queue, the algorithm will behave as non-preemptive priority scheduling, which means the job scheduled will run till the completion and no preemption will be done.
YUKTI KHURANA

'''

def displayInfo(pno,quantum,processes):

	print("************************* PREEMPTIVE PRIORITY SCHEDULING *********************\n")
	print("The total number of processes = ",pno)
	print("Quantum = ",quantum)
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
	avgrt/=pno
	avgwt/=pno
	avgtat/=pno
	avgrt = "{:.2f}".format(avgrt)
	avgwt = "{:.2f}".format(avgwt)
	avgtat = "{:.2f}".format(avgtat)
	print("Average Response Time | Average Waiting Time | Average Turn-Around Time")
	print(avgrt,"\t\t\t",avgwt,"\t\t\t",avgtat,"\t\t\t")
	print("\n***************************************************************************\n")
	

def main():
	
	# taking input from file- "input.py"
	f = open("priorin2.dat", "r")
	pno = int(f.readline())
	quantum = int(f.readline())
	
	# list of process ids
	processes = dict()
	pids = []
	for i in range(pno):
		l = f.readline().split(" ")
		# process info is stored in the form of a dictionary which is appended to the list of processes
		d = dict()
		d["pid"] = int(l[0])
		pids.append(int(l[0]))
		pid = int(l[0])
		d["prior"] = int(l[1])
		d["arrival"] = int(l[2])
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
		processes[pid] = d		
	
	
	# sorting the processes according to their arrival times, priority in ascending order
	"""EDIT THIS PRIORITY SORTING"""
	processes = dict(sorted(processes.items(), key = lambda x: (x[1]["arrival"],x[1]["prior"]))) 
	print("pid,arrival,prior")
	for h in processes.items():
		print(h[1]["pid"],",",h[1]["arrival"],",",h[1]["prior"])
	print()	
	# queues for processes waiting, input and output	
	# pqueue will contain (pid,priority,burst) of a ready process
	pqueue = []	
	inputqueue = []
	outputqueue = []
	# current process time left	
	ptime = 0
	# for I/O operation
	io=False	
	time = 0	
	processRunning = -1
	pi=0
	currentPrior = 0
	alldone=False
	
	# infinite loop till all processes are completed
	while(True):
		# checking the processes that have reached their arrival time by looping through all the  processes
		# PROCESS ARRIVAL 
		for pi in pids:
			if (time == processes[pi]["arrival"]):
				next = processes[pi]["pos"]+1
				pqueue.append([processes[pi]["pid"],processes[pi]["prior"],processes[pi]["burst"][next]])				
				processes[pi]["arrived"] = True
				print("Process - ",processes[pi]["pid"],"has been added to the ready queue at time = ",time)
				
				# sort pqueue accoring to priority of processes
				"""EDIT THIS PRIORITY SORTING"""
				pqueue.sort(key = lambda x: (x[1]))
				print("Current sorted pqueue = ",pqueue)
				
				# on every process arrival there is a possibility of context switch to higher priority process
				# --------------------CONTEXT SWITCH CODE-------------------------------------------------
			
				# check  if any process in ready queue has higher priority than current running process	
				# lesser the value of priority, more preferred the process will be
				"""EDIT THIS PRIORITY SORTING"""
				if (processRunning!=-1 and len(pqueue)!=0 and ptime !=0 and pqueue[0][1] < currentPrior):	
					# context switch to this process and uncompleted current process added to pqueue in a sorted manner
					pqueue.append([processRunning,currentPrior,ptime])
					t = processRunning
					cp = currentPrior				
					# now new process with higher priority will execute in cpu
					processRunning,currentPrior,ptime = pqueue[0]
					
					print("\n$$$Process with pid = ",processRunning,"and priority = ",currentPrior,"preempted process with pid = ",t,"and priority = ",cp,"$$$\n")
					# Response Time = Time at which process first gets the CPU – Arrival time
					if processes[processRunning]["response"] == -1:
						processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
					
					pqueue.pop(0)
					# pqueue sorted again accoring to priority of processes
					"""EDIT THIS PRIORITY SORTING"""
					pqueue.sort(key = lambda x: (x[1]))	
				# -----------------------------------------------------------------------------------------
									
				pi+=1			
		
		# now the pqueue contains all the processes in their ready state at current time
		#print(processes)
		# if input queue is not empty
		if len(inputqueue) != 0:
			ip, ileft = inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1				
				pqueue.append([processes[ip]["pid"],processes[ip]["prior"], processes[ip]["burst"][next]])
				"""EDIT THIS PRIORITY SORTING"""
				pqueue.sort(key = lambda x: (x[1]))
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft = outputqueue[0]		
			if oLeft == 0:
				# means current process is done taking the output, and can be popped out from the queue
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				pqueue.append([processes[op]["pid"],processes[op]["prior"], processes[op]["burst"][next]])
				"""EDIT THIS PRIORITY SORTING"""
				pqueue.sort(key = lambda x: (x[1]))
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
		
		# if no process is running in cpu, we have to give cpu time to next process in queue considering their shortest time	
		if (processRunning == -1):			
			if (len(pqueue) != 0):		
				"""EDIT THIS PRIORITY SORTING"""		
				pqueue.sort(key = lambda x: (x[1]))
				print("Current sorted pqueue = ",pqueue)
								
				processRunning,currentPrior, ptime = pqueue[0]
				
				# Response Time = Time at which process first gets the CPU – Arrival time
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
				
				pqueue.pop(0)		

		# incrementing time
		time += 1
		
		print("\n******************************\n")
		print("At time = ",time)
		print("Current running process = ",processRunning,"with priority = ",currentPrior)
		print("pqueue = ",pqueue)
		print("Input queue = ",inputqueue)
		print("Output queue = ",outputqueue)
		
		
		#calculating waiting time
		for s in pqueue:
			processes[s[0]]["wt"] += 1
			print("process with pid = ",s[0]," has been waiting for time = ",processes[s[0]]["wt"])
		print("\n******************************\n")
		
		# some process is currently running
		if (processRunning != -1):
			# current running process time is updated as its burst			
			ptime -= 1
			
			# keep updating process burst time of current running process
			processes[processRunning]["burst"][processes[processRunning]["pos"]] = ptime
			
			print("\nThe burst left for current process with pid = ",processRunning," is = ",ptime)
			print("pqueue = ",pqueue,"\n")
			
			# --------------------CONTEXT SWITCH CODE-------------------------------------------------
			
			# check  if any process in ready queue has higher priority than current running process	
			# lesser the value of priority, more preferred the process will be
			"""EDIT THIS PRIORITY SORTING"""
			if (len(pqueue)!=0 and ptime !=0 and pqueue[0][1] < currentPrior):	
				# context switch to this process and uncompleted current process added to pqueue in a sorted manner
				pqueue.append([processRunning,currentPrior,ptime])
				t = processRunning
				cp = currentPrior				
				# now new process with higher priority will execute in cpu
				processRunning,currentPrior,ptime = pqueue[0]
				
				print("\n$$$Process with pid = ",processRunning,"and priority = ",currentPrior,"preempted process with pid = ",t,"and priority = ",cp,"$$$\n")
				# Response Time = Time at which process first gets the CPU – Arrival time
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
				
				pqueue.pop(0)
				# pqueue sorted again accoring to priority of processes
				pqueue.sort(key = lambda x: (-x[1]))	
			# ---------------------------------------------------------------------------------------	
					
			elif ptime == 0:				
				processes[processRunning]["pos"] += 2
				next = processes[processRunning]["pos"]
				nextop  = processes[processRunning]["burst"][next]

				if nextop  == -1:
					processes[processRunning]["tat"] = time-processes[processRunning]["arrival"]
				else:
					io = True
				
				lastProcess = processRunning
				processRunning = -1
			else:
				nextop = None
		else:
			nextop = None

		# adding processes to input and output queue
		if io and nextop  == "I":
			next = processes[lastProcess]["pos"]+1
			inputqueue.append([lastProcess, processes[lastProcess]["burst"][next]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the input queue at time = ",time)
			io = False

		elif io and nextop == "O":
			next = processes[lastProcess]["pos"]+1
			outputqueue.append([lastProcess, processes[lastProcess]["burst"][next]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the output queue at time = ",time)
			io = False

		else:
			pass
		
		if (processRunning==-1 and  len(pqueue)==0 and len(inputqueue)==0 and  len(outputqueue)==0):
			allDone = 1
			for v in processes.items():
				alldone = True				
				if (v[1]["arrived"] == False):
					allDone = 0
					break
			if (allDone == 1):
				break
					
		
	
	displayInfo(pno,quantum,processes)
	
		
	
main()
'''

In Preemptive Priority Scheduling, at the time of arrival of a process in the ready queue, its Priority is compared with the priority of the other processes present in the ready queue as well as with the one which is being executed by the CPU at that point of time. The One with the highest priority among all the available processes will be given the CPU next.
The difference between preemptive priority scheduling and non preemptive priority scheduling is that, in the preemptive priority scheduling, the job which is being executed can be stopped at the arrival of a higher priority job.
Once all the jobs get available in the ready queue, the algorithm will behave as non-preemptive priority scheduling, which means the job scheduled will run till the completion and no preemption will be done.
YUKTI KHURANA

'''
