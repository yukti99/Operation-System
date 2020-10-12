/*
YUKTI KHURANA 
2017UCP1234
*/
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
#include <thread>
using namespace std;

#define NO_THREADS  6 //no of threads

bool choosing[NO_THREADS];
int tickets[NO_THREADS];
thread tid[NO_THREADS];

static int *val;

int maxTicketValue(){
	return *max_element(tickets,tickets+ NO_THREADS);
}


void initialiseTickets(){
	for(int i=0;i< NO_THREADS;i++){
		tickets[i]=0;
	}
}


void startProcess(int x){

	choosing[x]=true;
	tickets[x]= maxTicketValue()+1;
	choosing[x]=false;
	int i=0;
	// ALL PROCESSES PERFORM THIS
	for(i=0;i< NO_THREADS;i++){
		if(i==x)
			continue;
		while(choosing[i])
			 sleep(6);
		while(tickets[i]!=0 && tickets[i]<tickets[x])
			 sleep(6);
		if(tickets[i]==tickets[x] && i<x){
			while(tickets[i]!=0)
				 sleep(6);
		}

	}
	cout<<"\nPROCESS-"<<x+1<<" ENTERED CS!"<<endl;
	// CRITICAL SECTION
	*val = *val + 15;
	cout<<"PROCESS - "<<x+1<<": value = "<<*val<<endl;
	cout<<"PROCESS-"<<x+1<<" EXITED CS!"<<endl<<endl;
	tickets[x]=0;
}

int main(){

	initialiseTickets();
	// shared memory variable
	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	// intialising the value of shared memory variable
	*val = 20;
	cout<<"Total no of processes = "<<NO_THREADS<<endl;
	cout<<"INITIAL VALUE OF SHARED VARIABLE = "<<*val<<endl;

	// thread creation
	for(int i=0;i<NO_THREADS;i++){
		 tid[i]=thread(startProcess,i);
	}
	//for synchronisation
	for(int i=0;i<NO_THREADS;i++){
		tid[i].join();
	}

	cout<<"THE VALUE AT THE END OF ALL PROCESSES = "<<*val<<endl;

	return 0;
}
/*
YUKTI KHURANA 
2017UCP1234
*/

