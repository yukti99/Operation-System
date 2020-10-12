'''

SRTF : A process with shortest burst time begins execution. If a process with even a shorter burst time arrives, the current process is removed or preempted from execution, and the shorter job is allocated CPU cycle. 

YUKTI KHURANA

'''

def displayInfo(pno,quantum,processes):
	print("****************** SHORTEST REMAINING TIME FIRST - PREEMPTIVE SJF ***********\n")
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
	f = open("srtfin.dat", "r")
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
		print(d["pid"])
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
	
	
	# sorting the processes according to their arrival times in ascending order
	#print(processes,"\n")

	processes = dict(sorted(processes.items(), key = lambda x: x[1]["arrival"])) 
	#print(processes)
		
	# queues for processes waiting, input and output	
	# pqueue will contain (pid,workposition) of a ready process
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
	#currentPid=-1
	alldone=False
	
	# infinite loop till all processes are completed
	while(True):
		# checking the processes that have reached their arrival time by looping through all the  processes
		# PROCESS ARRIVAL - srtf requires a check if any process in ready queue has burst smaller than current process time left
		for pi in pids:
			if (time == processes[pi]["arrival"]):
				next = processes[pi]["pos"]+1
				pqueue.append([processes[pi]["pid"], processes[pi]["burst"][next]])				
				processes[pi]["arrived"] = True
				print("Process - ",processes[pi]["pid"],"has been added to the ready queue at time = ",time)
				pqueue.sort(key = lambda x: (x[1]))
				print("Current sorted pqueue = ",pqueue)
				# on every process arrival there is a possibility of context switch to smaller burst process
				# ------------------------------------------------------------------------------------------
				if (processRunning!=-1 and len(pqueue)!=0 and ptime !=0 and pqueue[0][1] < ptime):
					# context switch to this process and uncompleted current process added to pqueue in a sorted manner
					pqueue.append([processRunning,ptime])
					t = processRunning				
					# now new process with shorted burst will run
					processRunning, ptime = pqueue[0]
					print("\n$$Process with pid = ",processRunning,"preempted process with pid = ",t,"$$$\n")
					# Response Time = Time at which process first gets the CPU – Arrival time
					if processes[processRunning]["response"] == -1:
						processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
					
					pqueue.pop(0)
					pqueue.sort(key = lambda x: (x[1]))		
				
				# ------------------------------------------------------------------------------------------		
				
				pi+=1		
		
		
		# now the pqueue contains all the processes in their ready state at current time
		
		# if input queue is not empty
		if len(inputqueue) != 0:
			ip, ileft = inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1				
				pqueue.append([processes[ip]["pid"], processes[ip]["burst"][next]])
				pqueue.sort(key = lambda x: (x[1]))
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft = outputqueue[0]		
			if oLeft == 0:
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				pqueue.append([processes[op]["pid"], processes[op]["burst"][next]])
				pqueue.sort(key = lambda x: (x[1]))
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
		
		# if no process is running in cpu, we have to give cpu time to next process in queue considering their shortest time	
		if processRunning == -1:			
			if (len(pqueue) != 0):
				# here we have to sort the pqueue according to shortest burst times
				pqueue.sort(key = lambda x: (x[1]))
				print("Current sorted pqueue = ",pqueue)
				print("pqueue[0] = ",pqueue[0])
				processRunning, ptime = pqueue[0]
				# Response Time = Time at which process first gets the CPU – Arrival time
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
				
				pqueue.pop(0)		

		# incrementing time
		time += 1
		
		print("\n******************************\n")
		print("At time = ",time)
		print("Current process = ",processRunning)
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
			processes[processRunning]["burst"][processes[processRunning]["pos"]] = ptime
			print("\nThe burst left for current process with pid = ",processRunning," is = ",ptime)
			print("pqueue = ",pqueue,"\n")
			# check  if any process in ready queue has burst time less than process time left
			
			if (len(pqueue)!=0 and ptime !=0 and pqueue[0][1] < ptime):
				# context switch to this process and uncompleted current process added to pqueue in a sorted manner
				pqueue.append([processRunning,ptime])
				t = processRunning				
				# now new process with shorted burst will run
				processRunning, ptime = pqueue[0]
				print("\n$$$Process with pid = ",processRunning,"preempted process with pid = ",t,"$$$\n")
				# Response Time = Time at which process first gets the CPU – Arrival time
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time-processes[processRunning]["arrival"]
				
				pqueue.pop(0)
				pqueue.sort(key = lambda x: (x[1]))	
				
					
			if ptime == 0:				
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
			for v in processes.items():
				allDone = True				
				if (v[1]["arrived"] == False):
					allDone = False
			if (allDone == True):			
				break

		
	
	displayInfo(pno,quantum,processes)
	
		
	
main()
'''
SRTF : A process with shortest burst time begins execution. If a process with even a shorter burst time arrives, the current process is removed or preempted from execution, and the shorter job is allocated CPU cycle. 

YUKTI KHURANA

'''
