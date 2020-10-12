PROBLEM STATEMENT 


Extend simulator in Assignment 5 to implement MLFQ. 
The simulator reads input from MLFQ.dat. 
The first line is number of queues Q (priorities are assigned in range of 0..Q-1; 
each queue with different priority; 0 is highest priority). 
Next line is quanta for different queues (first value is for queue with highest priority);
RR algorithm is used for each queue.  
Third line is allocated time, T1 (time after which the priorities are downgraded by -1) 
and T2( time after which priorities are upgraded by +1). 
This is followed by burst time descriptions of each process



<PID> <Arrival Time> <Priority> P <burst time>  ......
as in the previous assignment.
Output should be 
Turnaround time of each process, Average turnaround time 
Response time of each process, Average turnaround time 
Waiting time of each process, Average turnaround time 