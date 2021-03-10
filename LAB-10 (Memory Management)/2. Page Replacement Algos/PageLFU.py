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
	print("\n*************************LEAST FREQUENTLY USED ALGORITHM**********************")
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
		if (l[i][0]==item):
			return i
	return -1

def pagePos(pf,x):
	for i in range(len(pf)):
		if (pf[i] == x):
			return i
	return -1 



# least frequently used algorithm 
def LFU(pages,pagestr,lfu):
	global hit,miss,time	
	k=0
	leastUsed = -1
	for i  in pagestr:
		print("\nPAGE REQUEST: ",i)	
		if (i not in pf):
			print("PAGE MISS!!\n")
			miss+=1
			if ("X" in pf):
				pf[k] = i
				k = (k+1)%pages
			else:			
				# gives the least frequently used page to replace with current page			
				j=0
				while(1):
					index = pagePos(pf,lfu[j][0])
					if (index!=-1):
						break
					else:
						j+=1
				print(index)
				pf[index] = i			
		else:
			print("PAGE HIT!!\n")			
			hit+=1

		x = findIndex(lfu,i)
		lfu[x][2] = time	# current time it came
		lfu[x][1] += 1		# frequency of access
		lfu = sorted(lfu, key=lambda x: (x[1], x[2]))
		displayPages()
		if (time != 0 and time%25 == 0):
			Result(hit,miss)
		time+=1			

def main():
	global time,pF,done,hit,miss	
	print("LEAST FREQUENTLY USED PAGE REPLACEMENT ALGORITHM")
	f = open("reference.dat","r")
	pages = int(f.readline().strip())
	print("NUMBER OF PAGES = ",pages)
	pagestr = list(map(int,f.readline().split()))
	pagestr.remove(-1)
	print(pagestr)
	# stores the frequency of access of pages 
	lfu = []
	for i in range(pages):
		pf.append("X")
	h=[]
	for i in pagestr:
		if i not in h:
			h.append(i)
	for i in h:
			lfu.append([i,0,0])
	LFU(pages,pagestr,lfu)
	print("Final Hit ratio : ")
	Result(hit,miss)

main()