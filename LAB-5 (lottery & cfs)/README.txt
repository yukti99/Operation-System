PROBLEM STATEMENT


In this assignment, we shall be implementing following scheduling algorithms. 
Input shall be in the following format for Lottery and Stride Scheduling. 
Should be read from file "lottery.dat" 

<Num_Tickets>
<Num_Processes>
<Large_Number>   // Used in stride scheduling to compute stride of each process
<Process_ID>  <CPU Share in %> P <Burst_Time> I <Burst_Time> P <Burst_Time>... -1
...
<Process_ID> <CPU share in %> P <Burst_Time> I <Burst_Time> P <Burst_Time>... -1

Input shall be in the following format for CFS (Completely Fair Scheduler). 
Should be read from file "cfs.dat" 


<Sched_Latency>
<Min_Granularity>
<Process_ID>  <Nice_Value> P <Burst_Time> I <Burst_Time> P <Burst_Time>... -1
...
<Process_ID> <Nice_Value> P <Burst_Time> I <Burst_Time> P <Burst_Time>... -1
Implementation using Red-Black tree (without using any library or standard templates) shall earn bonus points.

In all these assignments, all processes arrive at time t=0.