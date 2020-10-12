'''
FCFS: FIRST COME FIRST SERVE SCHEDULING ALGORITHM 
YUKTI KHURANA

'''

def displayInfo(pno,quantum,processes):
	print("\n**************SCHEDULING ALGORTIHM : FIRST COME FIRST SERVE****************\n")
	print("The total number of processes = ",pno)
	print("Quantum = ",quantum)
	print("Process ID | ResponseTime | WaitingTime | Turn-AroundTime")
	avgrt=0
	avgwt=0
	avgtat=0
	for i, x in enumerate(processes):
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
	processes = []
	for i in range(pno):
		l = f.readline().split(" ")
		# process info is stored in the form of a dictionary which is appended to the list of processes
		d = dict()
		d["pid"] = int(l[0])
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
		
		processes.append(d)
	#print(processes)
	
	# sorting the processes according to their arrival times in ascending order
	processes.sort(key=lambda x: (x["arrival"]))
		
	# queues for processes waiting, input and output	
	# pqueue will contain (pid,workposition) of a ready process
	pqueue = []	
	inputqueue = []
	outputqueue = []	
	ptime = 0
	io=False	
	time = 0	
	processRunning = -1
	pi=0
	
	# infinite loop till all processes are completed
	while(True):
		# checking the processes that have reached their arrival time by looping through all the  processes
		while (pi<pno and time == processes[pi]["arrival"]):
			next = processes[pi]["pos"]+1
			print("pqueue = ",pqueue)
			print("Process - ",processes[pi]["pid"],"has been added to the ready queue at time = ",time)
			pqueue.append([pi, processes[pi]["burst"][next]])
			pi += 1
			
		# now the pqueue contains all the processes in their ready state at current time
		# if input queue is not empty
		if len(inputqueue) != 0:
			ip, ileft =inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1
				pqueue.append([ip, processes[ip]["burst"][next]])
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft = outputqueue[0]		
			if oLeft == 0:
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				pqueue.append([op, processes[op]["burst"][next]])
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
			
		if processRunning == -1:			
			if len(pqueue) != 0:
				processRunning, ptime = pqueue[0]
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
		for k, p in enumerate(pqueue):
			processes[p[0]]["wt"] += 1
		print("\n******************************\n")
		
		# some process is currently running		
		if (processRunning != -1):			
			ptime -= 1			
			if ptime == 0:				
				processes[processRunning]["pos"] += 2
				next = processes[processRunning]["pos"]
				nextop  = processes[processRunning]["burst"][next]

				if nextop  == -1:
					processes[processRunning]["tat"] = time-processes[processRunning]["arrival"]
				else:
					io = True
				
				currentCopy = processRunning
				processRunning = -1
			else:
				nextop = None
		else:
			nextop = None

		# adding processes to input and output queue
		if io and nextop  == "I":
			next = processes[currentCopy]["pos"]+1
			inputqueue.append([currentCopy, processes[currentCopy]["burst"][next]])
			io = False

		elif io and nextop == "O":
			next = processes[currentCopy]["pos"]+1
			outputqueue.append([currentCopy, processes[currentCopy]["burst"][next]])
			io = False

		else:
			pass

		if (pi==pno and  processRunning==-1 and  len(pqueue)==0 and len(inputqueue)==0 and  len(outputqueue)==0):
			break

		
	
	displayInfo(pno,quantum,processes)
	
		
	
main()
'''
FCFS: FIRST COME FIRST SERVE SCHEDULING ALGORITHM 
YUKTI KHURANA
'''
