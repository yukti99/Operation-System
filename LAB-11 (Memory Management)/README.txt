PROBLEM STATEMENT:

Implement simulation of 
1) first fit, next fit, best fit and worst fit algorithms for variable partition allocation strategies. 
Simulator should read requisite data from a file called alloc.dat. 
The first line of this file is memory size (in KB). 
All subsequent lines shall consist of a 3-tuple
time at which request comes, size of block requested (in KB), time duration for which allocation shall remain valid.
These lines are in ascending order of time of request.
The last line consists of -1, -1, -1
Output of simulator should be percentage of successful allocation requests 
and external fragmentation at intervals of 50 units of time for each of first/next/best/worst fit strategies.

2) Page replacement algorithms - FIFO, optimal, LRU, LFU, MFU
Data to be read from file reference.dat.
First line number of pages
Second line page reference string (at least 100 entries separated by comma: -1 is termination of the string)
For every strategy, the program should output
page requests that were served and page requests that were missed
Hit ratio
At an interval of 25 requests.