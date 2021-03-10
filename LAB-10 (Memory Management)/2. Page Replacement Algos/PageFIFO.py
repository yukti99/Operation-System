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
	print("\n*****************FIRST IN FIRST OUT PAGE REPLACEMENT ALGORITHM*****************")
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

def FIFO(pages,pagestr):
	global hit,miss,time	
	k=0
	for i in pagestr:
		if i not in pf:
			pf[k] = i
			miss+=1
			k = (k+1)%pages
		else:
			hit+=1
		displayPages()
		if (time != 0 and time%25 == 0):
			Result(hit,miss)
		time+=1			

def main():
	global time,pF,done,hit,miss	
	print("FIRST IN FIRST OUT PAGE REPLACEMENT ALGORITHM")
	f = open("reference.dat","r")
	pages = int(f.readline().strip())
	print("NUMBER OF PAGES = ",pages)
	pagestr = list(map(int,f.readline().split()))
	pagestr.remove(-1)
	print(pagestr)
	for i in range(pages):
		pf.append("X")
	FIFO(pages,pagestr)
	print("Final Hit ratio : ")
	Result(hit,miss)

main()