'''
COMPLETELY FAIR SCHEDULING  
YUKTI KHURANA

'''

def displayInfo(pno,processes,pids):
	print("\n********************** COMPLETELY FAIR SCHEDULING *******************\n")
	print("The total number of processes = ",pno)
	print("Process ID | ResponseTime | WaitingTime | Turn-AroundTime")
	avgrt=0
	avgwt=0
	avgtat=0
	for i in pids:
		x = processes[i]
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
	

	f = open("cfs.dat","r")
	s = int(f.readline())
	mg = int(f.readline())
	pno = int(f.readline())
	
	# list of process ids
	processes = dict()
	pids = []
	for i in range(pno):
		l = f.readline().strip().split(" ")
		# process info is stored in the form of a dictionary which is appended to the list of processes
		d = dict()
		d["pid"] = int(l[0])
		pids.append(d["pid"])
		pid = int(l[0])
		d["nice"] = int(l[1])
		d["burst"] = l[2:]
		for i,j in enumerate(d["burst"]):
			# converting the burst timings to integer type for calculations
			if not j in ["P", "I", "O"]:
				d["burst"][i] = int(j)
				
		d["response"] = -1
		d["tat"] = 0
		d["wt"] = 0
		d["pos"] = 0
		d["vruntime"] = 0
		d["quanta"] = 0		
		processes[pid] = d
		
		
	print(processes)
	
	

	weight = {-20:88761,-19:71755,-18:56483,-17:46273,-16:36291,-15:29154,-14:23254,-13:18705,-12:14949,-11:11916,-10:9548,-9:7620,-8:6100,-7:4904,-6:3906,-5:3121,-4:2501,-3:1991,-2:1586,-1:1277,0:1024,1:820,2:655,3:526,4:423,5:335,6:272,7:215,8:172,9:137,10:110,11:87,12:70,13:56,14:45,15:36,16:29,17:23,18:18,19:15}
	total_weight=0
	print(pids)
	
	for i in pids:
		print("i = ",i)
		print(processes[i])
		niceness = processes[i]["nice"]
		total_weight += weight[niceness]
	
	for i in pids:
		niceness = processes[i]["nice"]
		time_slice = (weight[niceness]/total_weight)*s
		processes[i]["quanta"] = int(max(mg,time_slice))
	
	
	
	pqueue = []	
	inputqueue = []
	outputqueue = []	
	ptime = 0
	io=False	
	time = 0	
	processRunning = -1
	pi=0
	timeLeft = 0
	m=0
	# infinite loop till all processes are completed
	for pi in pids:	
		next = processes[pi]["pos"]+1
		pqueue.append([pi, processes[pi]["burst"][next],0])	
	
	wo  = weight[processes[1]["nice"]]	
	while(True):
		
		# if input queue is not empty
		if len(inputqueue) != 0:
			ip, ileft =inputqueue[0]		
			if ileft == 0:
				# means current process is done taking the input, and can be popped out from the queue
				processes[ip]["pos"] += 2
				next = processes[ip]["pos"]+1
				pqueue.append([ip, processes[ip]["burst"][next],processes[ip]["vruntime"]])
				pqueue.sort(key = lambda x: (x[2]))	
				inputqueue.pop(0)

		# if output queue is not empty
		if len(outputqueue) != 0:
			op, oLeft = outputqueue[0]		
			if oLeft == 0:
				processes[op]["pos"] += 2
				next = processes[op]["pos"]+1
				pqueue.append([op, processes[op]["burst"][next],processes[ip]["vruntime"]])
				outputqueue.pop(0)
		
		if len(inputqueue) != 0:
			# input operation time decremented			
			inputqueue[0][1] -= 1
			
		if len(outputqueue) != 0:
			# output operation time decremented
			outputqueue[0][1] -= 1
			
		# no process running in cpu
		if (processRunning == -1):			
			if (len(pqueue) != 0):
				# quantum time given to next process in queue
				processRunning, ptime,vruntime = pqueue[0]
				timeLeft = processes[processRunning]["quanta"]
				
				print("\n$$PROCESS-",processRunning,"has started running !!$$\n")
				
				if processes[processRunning]["response"] == -1:
					processes[processRunning]["response"] = time
				pqueue.pop(0)		

		# incrementing time
		time += 1
		if (timeLeft>0):
			timeLeft-=1
			
		for i in range(len(pqueue)):
			pid = pqueue[i][0]
			pqueue[i][2] = processes[pid]["vruntime"]
		
		pqueue.sort(key = lambda x: (x[2]))		
		
		print("\n******************************\n")
		print("At time = ",time)
		print("Current process = ",processRunning)
		print("time left for current process = ",timeLeft)		
		print("pqueue = ",pqueue)
		print("Input queue = ",inputqueue)
		print("Output queue = ",outputqueue)
		
		
		
		#calculating waiting time
		for k, p in enumerate(pqueue):
			processes[p[0]]["wt"] += 1
		print("\n******************************\n")
		
		
		# some process is running
		if (processRunning != -1):
			# its ptime decremented			
			ptime -= 1
			print("process burst current left = ",ptime)
			
			# if process burst is done 
			if ptime == 0 :				
				processes[processRunning]["pos"] += 2
				next = processes[processRunning]["pos"]
				nextop  = processes[processRunning]["burst"][next]
				if nextop  == -1:
					processes[processRunning]["tat"] = time
				else:
					io = True			
				
				processes[processRunning]["vruntime"] += int((wo/weight[processes[processRunning]["nice"]])*time)		
								
				lastProcess = processRunning
				processRunning = -1
				
			# if process burst is not done and quantum is over
				
			elif (ptime !=0 and timeLeft==0):
							
				# context switch to be done
				next = processes[processRunning]["pos"]
				processes[processRunning]["burst"][next] = ptime
				
				# current process added to back of queue with remaining burst time				
				processes[processRunning]["vruntime"] += int((wo/weight[processes[processRunning]["nice"]])*time)	
				pqueue.append([processRunning,ptime,processes[processRunning]["vruntime"]])
				pqueue.sort(key = lambda x: (x[2]))	
				print(pqueue)
				
				# next process in queue taken to run
				lastProcess = processRunning
				processRunning= -1
								
				
			else :
				# keep progressing the current process
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
			break	
		
	
	displayInfo(pno,processes,pids)
	
		
	
main()
'''
COMPLETELY FAIR SCHEDULING  
YUKTI KHURANA

'''

