"""
python code to implement Partition Allocation Strategies 
YUKTI KHURANA 
2017UCP1234

alloc.dat 
<memory size>
<time instant> <size of block requested> <time for which allocation remains valid>


"""

# list that stores free spaces in memory for allocation
totalMem = 0
# time variable 
time = 0

# to store the process allocation requirements
proc = []

# to store the no of successful allocation requests
succesfulReq = 0;

# total requests 
totalReq = 0

# unsuccessful requests
failedReq = 0

# external Fragmentation size of  KB
extFrag = 0;

# data structure to store memory space info for each fragment
mem = dict()
# mem = {start,end,size,freeflag}
# free flag is true if space is free to be allocated 

# actual memory
M = []

# extra pointer to keep track of last allotted hole
ptr = dict()


def displayMemory():
	global M
	M = sorted(M,key = lambda j:j["start"])
	print("========================================================================================")
	print("MEMORY ADDRESSES AT TIME = ",time," : ")
	#if (ptr != None):
	#	print("POINTER = ",ptr)
	for i in M:
		status = "free"
		if (i["free"]==False):
			status = "Allocated"		
		if (i["process"]!=None):
			print("size = ",i["size"],"->[",i["start"],"--",i["end"],"] -> ",status,"to Process - ",i["process"])			
		else:
			print("size = ",i["size"],"->[",i["start"],"--",i["end"],"] -> ",status)


	print("========================================================================================\n\n")
			

def coallesceMemory():
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,ptr,Maxtime
	f=0
	g=0
	while(f<len(M)-1):
		if (f+1<=len(M)-1):
			before = M[f]
			after = M[f+1]
			if (after["free"] == True and before["free"] == True):
				
				M.remove(after)
				before["end"] = after["end"]
				before["size"] = before["end"]-before["start"]+1
				before["free"] = True
				before["process"] = None
				before["t"] = -1 
				M = sorted(M,key = lambda j:j["start"])
				g=1
			f+=1
	if (g==1):
		coallesceMemory()

def Results():
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,totalMem
	print("********************* AT TIME = ",time,"*******************************")		
	perc = (succesfulReq*100.0)/totalReq
	print("Total Requests uptil now = ",totalReq)
	print("Successful Request = ",succesfulReq)
	perc = "{:.2f}".format(round(perc, 2))
	print("The precentage of succesful requests = ",perc,"%")
	# calculate external fragmentation
	if (len(M)>1):
		for f in range(len(M)):
			if (f>1 and f<len(M)-1):
				frag = M[f]
				before = M[f-1]
				after = M[f+1]
				if frag["free"] == True  and before["free"] == False and after["free"] == False:						
						extFrag+=frag["size"]
		if (M[0]["free"] == True and M[1]["free"]==False):
			extFrag+=M[0]["size"]
		l = len(M)
		if (M[l-1]["free"] == True and M[l-2]["free"]==False):
			extFrag+=M[l-1]["size"]


	# print extFrag 
	if (extFrag!=0):
		print("External Fragmentation = ",extFrag,"KB")
		print("Total Memory = ",totalMem,"KB")
		e = (extFrag*100.0)/totalMem
		e = "{:.2f}".format(e)
		print("The percentage External Fragmentaion in memory = ",e,"%\n")
	else:
		print("No  external Fragmentation as of now!")
	print("**********************************************************************\n\n")


def split(a,i):
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,ptr,Maxtime,totalMem
	s=0
	cnt=0
	for b in M:
		if (b==a):
			break
		cnt+=1

	if (a["size"]==i[1] and a["free"] == True):
		# no need of spitting
		M[cnt]["free"] = False
		M[cnt]["process"] = i[3]
		M[cnt]["t"] = i[2]+i[0]
		s=1
	elif (a["size"]>i[1] and a["free"] == True):
		# use the first free memory segment to allocate current process request
		#  create new allocated fragment
		# splitting!
		
		x = M.remove(a)
		n1 = dict()
		#print("FREE SPACE FOUND AT ",a["start"])
		n1["start"] = a["start"]
		n1["end"] = n1["start"]+i[1]-1
		n1["size"] = i[1]
		n1["free"] = False
		n1["process"] = i[3] # process number 
		n1["t"] = i[2]+i[0]
		
		
		n2 = dict()
		n2["start"] = n1["end"]+1
		n2["end"] = a["end"]
		n2["size"] = n2["end"]-n2["start"]+1
		n2["free"] = True
		n2["process"] = None
		n2["t"] = -1

		# set pointer at next-fit
		ptr = n2
		print("ptr changed to ",ptr)

		M.append(n1)
		M.append(n2)
		s=1
		M = sorted(M,key = lambda j:j["start"])
		displayMemory()
		# successful allocations
		succesfulReq+=1;
	return s





# after every 50 time units, print the external fragmentation of the memory and % of successful requests
def NextFit():	
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,ptr,Maxtime,totalMem
	k=0;
	while(len(proc)!=0 and time <= Maxtime):

		if (time%50 == 0 and totalReq!=0):
			Results()
		# DEALLOCATION CHECK 
		for i in M:
			if (i["t"] == time): # time for which occupency lasts
				print("DEALLOCATION CHECK AT TIME = ",time)
				print("Process - ",i["process"],"'s memory deallocated!")
				i["t"] = -1
				i["free"] = True
				i["process"] = None
				coallesceMemory()
				print("After deallocation: \n")
				displayMemory()


		# at each instance, a new ready process request has to be allocated if possible
		# ALLOCATION CHECK		
		k=0;
		#displayMemory()
		if (len(proc)==0):
			break
		if (proc[0][0] == time):
			totalReq+=1
			i = proc.pop(0)
			# allocate this process free memory	
			s=0	
			# searching from next-fit
			for a in M:
				if (a!=ptr):
					continue
				s = split(a,i)
				if (s==1):
					break

			if (s==0):
				
				for l in range(len(M)):
					s = split(M[l],i)
					if (s==1):
						break
					if (l!=0 and M[l-1] == ptr):
						break

			
			# search complete
			if (s == 0):
				# increment count of unsuccessful requests
				failedReq+=1; # concerned process aborts and error message given 
				print("SORRY!! AT TIME = ",time,": The request for allocation of Process - ",i[3]," at time = ",i[0],"and allocation request of ",i[1],"failed!!\n")
		# increment time 
		time+=1
		
		
	
	

def main():
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,ptr,Maxtime,totalMem
	print("\n********* MEMORY ALLOCATION TECHNIQUES *******\n")
	f = open("alloc.dat","r")
	totalMem = int(f.readline().strip())
	print("The total memory available = ",totalMem,"KB\n")
	count=1
	while(1):
		r = f.readline().strip().split(" ")
		if (r[0] == "-1"):
			break
		p = []
		for i in r:
			p.append(int(i))
		p.append(count)
		count+=1
		proc.append(p)
	proc.sort(key = lambda x: x[0])  
	
	for i in proc:
		print("P",i[3],"->",i[0],",",i[1],",",i[2],"\n")

	# intitialse the mem dictionary
	print("\nInitial status of Memory : ")
	mem["start"] = 0
	mem["end"] = totalMem-1
	mem["size"] = mem["end"]-mem["start"]+1
	mem["free"] = True
	mem["process"] = None
	mem["t"] = -1 # time for which it remains occupied if not free
	M.append(mem)
	displayMemory()
	Maxtime = proc[len(proc)-1][0]
	ptr = None
	NextFit()

	
	print("\nFinal Memory :\n")
	displayMemory()
	print("RESULTS FOR NEXT-FIT AFTER ALL PROCESSES DONE: \n")
	Results()
		
main();
	
	
	

