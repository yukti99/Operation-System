PROBLEM STATEMENT:

Given a finite buffer, you need to implement solution for Producer Consumer Problem for the following versions
(1) Single Producer Single Consumer
(2) Single Producer Single Consumer
(3) Single Producer Single Consumer
(4) Single Producer Single Consumer
through use of 
(a) Peterson's algorithm 
(b) Atomic instruction supported by hardware (XCHG is an atomic instruction only if threads are scheduled on same core, otherwise read for LOCK XCHG https://www.cse.iitd.ernet.in/~sbansal/os/lec/l21.html,  https://nptel.ac.in/content/storage2/nptel_data3/html/mhrd/ict/text/106106144/lec28.pdf, https://stackoverflow.com/questions/3144335/on-a-multicore-x86-is-a-lock-necessary-as-a-prefix-to-xchg)
(c) Semaphore(s)
for avoiding race condition in critical section.

Solutions need to be implemented in three different modes - Producer(s) and Consumer(s)
(1) are child processes of some process in a given program
(2) different programs
(3) threads within the same program



SOLUTION:

For Semaphore files using process(fork)
compile using command:
Eg:	g++ SPSCSemFork.cpp -lrt  -lpthread


For Thread files:
Eg:	g++ SPSCSemthreads.cpp  -lpthread

