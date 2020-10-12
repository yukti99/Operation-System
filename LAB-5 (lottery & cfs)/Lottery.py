'''
LOTTERY SCHEDULING 
YUKTI KHURANA

'''

def displayInfo(pno,processes,t,pids):
	print("\n**********************  Lottery and Stride Scheduling *******************\n")
	print("The total number of processes = ",pno)
	print("The total number of tickets = ",t)
	print("Process ID | ResponseTime | WaitingTime | Turn-AroundTime| RunTimes")
	avgrt=0
	avgwt=0
	avgtat=0
	for i in pids:
		x = processes[i]
		print(x["pid"],"\t\t",x["response"],"\t\t",x["wt"],"\t\t",x["tat"],"\t\t",x["runtimes"])
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
	f = open("lottery.dat", "r")
	tickets =  int(f.readline())
	pno = int(f.readline())
	largeNo = int(f.readline())
	
	# list of process ids
	processes = dict()
	pids = []
	for i in range(pno):
		l = f.readline().strip().split(" ")
		# process info is stored in the form of a dictionary which is appended to the list of processes
		d = dict()
		d["pid"] = int(l[0])
		d["cpushare"] = int(l[1])
		pids.append(int(l[0]))
		pid = int(l[0])
		d["burst"] = l[2:]		
		for i,j in enumerate(d["burst"]):
			# converting the burst timings to integer type for calculations
			if not j in ["P", "I", "O"]:
				d["burst"][i] = int(j)
				
		d["response"] = -1
		d["tat"] = 0
		d["wt"] = 0
		d["pos"] = 0	
		cpushare = d["cpushare"]
		d["stride"] = int(largeNo/((cpushare*tickets)/100))
		d["pass"] = 0
		d["complete"] = False
		d["runtimes"] = 0
				
		processes[pid] = d		
	

	# pqueue will contain (pid,workposition,stride) of a ready process
	pqueue = []	
	inputqueue = []
	outputqueue = []
	# current process time left	
	ptime = 0
	# for I/O operation
	io=False	
	time = 0	
	processRunning = -1
	done=False	
	quanta = 1
	timeLeft = quanta
	for pi in pids:
		# all processes arrive at t=0
		next = processes[pi]["pos"]+1
		#print(processes[pi])
		pqueue.append([pi, processes[pi]["burst"][next],processes[pi]["pass"]])
		pqueue.sort(key = lambda x: (x[2]))

	while(True):		
		if len(inputqueue) != 0:
			ip, ileft,p = inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1
				pqueue.append([ip, processes[ip]["burst"][next],processes[ip]["pass"]])
				pqueue.sort(key = lambda x: (x[2]))
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft,p = outputqueue[0]		
			if oLeft == 0:
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				pqueue.append([op, processes[op]["burst"][next],processes[op]["pass"]])
				# sort according to min pass
				pqueue.sort(key = lambda x: (x[2]))
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
		
		# no process running, so we must assign some process to cpu	
		if (processRunning == -1):			
			if (len(pqueue) != 0):				
				processRunning, ptime, processPass = pqueue[0]
				print("Current Running Process = ",processRunning)
				processes[processRunning]["runtimes"] += 1
				print("\nPROCESS - ",processRunning,"IS RUNNING!!\n")
				print(pqueue)
				# Response Time = Time at which process first gets the CPU – Arrival time
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time
				
				pqueue.pop(0)		

		# incrementing time
		time += 1
		if (timeLeft>0):
			timeLeft-=1
		
		print("\n******************************\n")
		print("At time = ",time)
		print("Current process = ",processRunning)
		if (processRunning !=-1):
			print("Current process pass = ",processes[processRunning]["pass"])
		print("pqueue = ",pqueue)
		print("Input queue = ",inputqueue)
		print("Output queue = ",outputqueue)
		
		for i in range(len(pqueue)):
			pid = pqueue[i][0]
			pqueue[i][2] = processes[pid]["pass"]
		pqueue.sort(key = lambda x: (x[2]))
		print(pqueue)
		
		#calculating waiting time
		for s in pqueue:
			processes[s[0]]["wt"] += 1
			print("process with pid = ",s[0]," has been waiting for time = ",processes[s[0]]["wt"])
			
		print("\n******************************\n")
		
		# some process is currently running
		if (processRunning != -1):			
			ptime -= 1
			# process completed its burst						
			if (ptime == 0):				
				processes[processRunning]["pos"] += 2
				next = processes[processRunning]["pos"]
				nextop  = processes[processRunning]["burst"][next]
				# process pass incremented by stride for next burst
				s  = processes[processRunning]["stride"]
				print("Stride = ",s,"for process",processRunning)
				processes[processRunning]["pass"] += s
				print("The pass value of process-",processRunning," incremented to ",processes[processRunning]["pass"])
				#print(processes[processRunning])
				pqueue.sort(key = lambda x: (x[2]))

				if nextop  == -1:
					processes[processRunning]["tat"] = time
					processes["complete"] = True
					# return its tickets to system
				else:
					
					io = True
				
				lastProcess = processRunning
				processRunning = -1
			# if process burst is not done and quantum is over	
			elif (ptime !=0 and timeLeft==0):
				timeLeft = quanta
				# context switch to be done and new pass calculated
				next = processes[processRunning]["pos"]
				#  burst decremented
				processes[processRunning]["burst"][next] = ptime
				
				# process pass incremented by stride for next burst
				s  = processes[processRunning]["stride"]
				print("Stride = ",s,"for process",processRunning)
				processes[processRunning]["pass"] += s
				print("####The pass value of process-",processRunning," incremented to ",processes[processRunning]["pass"])
				print(processes[processRunning])
				
				# current process added to back of queue with remaining burst time
				pqueue.append([processRunning,ptime,processes[processRunning]["pass"]])
				pqueue.sort(key = lambda x: (x[2]))
				# next process in queue taken to run
				print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				print("CONTEXT SWITCH HAPPENED TO NEXT PROCESS!!!")
				print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
				#print(pqueue)
				
				lastProcess = processRunning
				processRunning= -1
			else:
				# keep progressing the current process
				nextop = None
		else:
			nextop = None

		# adding processes to input and output queue
		if io and nextop  == "I":
			next = processes[lastProcess]["pos"]+1
			inputqueue.append([lastProcess, processes[lastProcess]["burst"][next],processes[lastProcess]["pass"]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the input queue at time = ",time)
			io = False

		elif io and nextop == "O":
			next = processes[lastProcess]["pos"]+1
			outputqueue.append([lastProcess, processes[lastProcess]["burst"][next],processes[lastProcess]["pass"]])
			print("Process - ",processes[lastProcess]["pid"],"has been added to the output queue at time = ",time)
			io = False

		else:
			pass

		if (processRunning==-1 and  len(pqueue)==0 and len(inputqueue)==0 and  len(outputqueue)==0):
			break	
	
	displayInfo(pno,processes,tickets,pids)
	
		
	
main()
'''
LOTTERY SCHEDULING 
YUKTI KHURANA

'''

