"""
YUKTI KHURANA
2017UCP1234

<no of pages>
<page reference string> -1

"""

time = 0
pf = []
done = 0
miss = 0
hit = 0

def Result(hit,miss):
	global time
	print("\n*****************LEAST RECENTLY USED PAGE REPLACEMENT ALGORITHM****************")
	print("Time: ",time)
	print("Total request = ",hit+miss)
	print("Page requests successful/hits = ",hit)
	print("Page requests Page faults/misses = ",miss)
	e = "{:.4f}".format(hit*1.0/(miss+hit))
	print("Hit Ratio = ",e)
	print("*******************************************************************************\n")

def displayPages():
	print("\nPAGES : ")
	for i in pf:
		print("|",i,"|")
	print("\n")

def findIndex(l,item):
	for i in range(len(l)):
		if (l[i]==item):
			return i
	return -1

# least recently used algorithm 
def LRU(pages,pagestr,lru):
	global hit,miss,time	
	k=0
	leastUsed = -1
	for i  in pagestr:
		print("\nPAGE REQUEST: ",i)
		if (i not in pf):	
			print("PAGE MISS!!\n")		
			miss+=1
			# to replace the page from frame which is least recently used
			leastUsed = min(lru)
			pageReplaced = findIndex(lru,leastUsed)
			pf[pageReplaced] = i
			lru[pageReplaced] = max(lru)+1
		else:
			pageFound = findIndex(pf,i)
			lru[pageFound] = max(lru)+1
			print("PAGE HIT!!\n")
			hit+=1
		displayPages()
		if (time != 0 and time%25 == 0):
			Result(hit,miss)
		time+=1			

def main():
	global time,pF,done,hit,miss	
	print("LEAST RECENTLY USED PAGE REPLACEMENT ALGORITHM")
	f = open("reference.dat","r")
	pages = int(f.readline().strip())
	print("NUMBER OF PAGES = ",pages)
	pagestr = list(map(int,f.readline().split()))
	pagestr.remove(-1)
	print(pagestr)
	# pages must have an extra flag to represent how recently have they been used	
	lru = []
	for i in range(pages):
		# lower the value of priority flag, less recently used -> so will be replaced 
		lru.append(i)
		pf.append("X")

	print(lru,pf)
	LRU(pages,pagestr,lru)
	print("Final Hit ratio : ")
	Result(hit,miss)

main()