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



def displayMemory():
	print("========================================================================================")
	print("MEMORY ADDRESSES AT TIME = ",time," : \n")
	global M
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
	#print("COALESSING!!")
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,totalMem
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
				#displayMemory()
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


# after every 50 time units, print the external fragmentation of the memory and % of successful requests
def BestFit():	
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,Maxtime,totalMem
	k=0;
	while(len(proc)!=0 and time <= Maxtime):

		if (time%50 == 0 and totalReq!=0):
			Results()
		# DEALLOCATION CHECK 
		for i in M:
			#print(i)
			if (i["t"] == time): # time for which occupency lasts
				print("DEALLOCATION CHECK AT TIME = ",time)
				print("Process - ",i["process"],"'s memory deallocated!")
				i["t"] = -1
				i["free"] = True
				i["process"] = None
				coallesceMemory()
				displayMemory()


		# at each instance, a new ready process request has to be allocated if possible
		# ALLOCATION CHECK
		if (proc[0][0] == time):
			totalReq+=1
			i = proc.pop(0)
			# allocate this process free memory	
			s=0	
			# FINDING THE SMALLEST FRAGMENT ENOUGH TO SATIFY PROCESS ALLOCATION REQUEST
			minSize = totalMem+1000
			node = None
			for a in M:
				
				if (a["free"] == True and a["size"] >= i[1] and minSize > a["size"]):
					minSize = a["size"]
					node = a
					

			if (node == None):
				failedReq+=1; 
				print("SORRY! AT TIME = ",time,": The request for allocation of Process - ",i[3]," at time = ",i[0],"and allocation request of ",i[1],"failed!!\n")
			else:
				# splitting this node!
				a = node
				x = M.remove(a)
				n1 = dict()
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

				M.append(n1)
				if (n2["size"] != 0):
					M.append(n2)
					#otherwise no need of splitting
				

				M = sorted(M,key = lambda j:j["start"])
				displayMemory()
				# successful allocations
				succesfulReq+=1;
						
				
		# increment time 
		time+=1
		
		
	
	

def main():
	global proc,time,succesfulReq,totalReq,failedReq, extFrag,M,Maxtime,totalMem
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
	BestFit()

	
	
	print("\nFinal Memory :\n")
	displayMemory()
	print("RESULTS FOR BEST-FIT AFTER ALL PROCESSES DONE: \n")
	Results()
		
main();
	
	
	

