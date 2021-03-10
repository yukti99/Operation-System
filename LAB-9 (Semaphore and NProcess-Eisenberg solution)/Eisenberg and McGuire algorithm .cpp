/*
YUKTI KHURANA 
2017UCP1234

Eisenberg and McGuire algorithm is used to solve the critical section problem for n-processes
It is a general version of dining philosophers problem

*/
#include <iostream>
#include <unistd.h>
#include <sys/mman.h>
#include <thread>
using namespace std;

//no of processes
const int N = 6; 
static int *val;

// all N processes share the following variables 
// The flags variable for each process is set to WAITING whenever it intends to enter the critical section.
// flags can be either idle or waiting or active  
enum pstate {IDLE, WAITING,ACTIVE} flags[N];
int turn; // arbritary no between 0 and n-1

void EntryProtocol(int i){	
	int index;
	do{
		// the process declares that it needs a resource (shared)
		flags[i] = WAITING;		
		//printf("PROCESS -%d is waiting for the resource !\n",i);
		
		// scan processes from the one with the turn, up to this process
		index = turn; // index is initialised to  process with current turn
		
		// repeat until the scan finds all processes idle from turn to current one
		// i is the current process number (acts like a waiting loop)
		while(index!=i){
			if (flags[index] != IDLE)
				index = turn;
			else 
				index = (index+1)%N; // circular queue of N processes
		}
		// process tentively claims the resource
		flags[i] = ACTIVE;
		
		
		// find the first active process besides current i
		index = 0;
		while((index < N) && ((index == i) || (flags[index] != ACTIVE))){
			index+=1;
		}
		
	// if there were no active processes and we have turn or else whoever has turn is idle  then we can proceed to CS otherwise repeat whole sequence 
	}while (!((index >= N) && ((turn == i) || (flags[turn] == IDLE))));
	
	// our turn for CS
	turn = i;	

}

void ExitProtocol(int i){
	// find another process which is not idle 
	int  index = (turn+1)%N;
	while(flags[index]==IDLE){
		index=(index+1)%N;
	}	
	// if no other process, we will find i/ ourselves
	turn = index;
	
	// we are done 
	flags[i] = IDLE;
	
	printf("PROCESS -%d is IDLE !\n",i);
	// REMAINDER SECTION 
	
}

void NProcess(int i){
	EntryProtocol(i);
	// CRITICAL SECTION
	cout<<"\nPROCESS-"<<i<<" ENTERED CS!"<<endl;	
	*val = *val + 10;
	cout<<"PROCESS - "<<i<<": value = "<<*val<<endl;
	cout<<"PROCESS-"<<i<<" EXITED CS!"<<endl<<endl;
	ExitProtocol(i);
}

int main(){
	// shared variable  for N processes	
	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	// intialising the value of shared memory variable
	*val = 20;
	cout<<"Total no of processes = "<<N<<endl;
	cout<<"INITIAL VALUE OF SHARED VARIABLE = "<<*val<<endl;

	turn = 0;
	
	thread tid[N];
	// initialising all processes as idle 
	for (int i = 0; i < N; i++) {
		flags[i] = IDLE;
	}

	for (int i = 0; i < N; i++) {
		tid[i] = thread(NProcess, i);
	}
	// joining processes for synchronisation
	for (int i = 0; i < N; i++) {
		tid[i].join();
	}
	//cout<<"THE VALUE AT THE END OF ALL PROCESSES = "<<*val<<endl;

	return 0;
}
/*
YUKTI KHURANA 
2017UCP1234
*/

