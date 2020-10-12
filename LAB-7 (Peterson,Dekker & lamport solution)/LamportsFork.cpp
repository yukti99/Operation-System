/*
YUKTI KHURANA 
2017UCP1234
*/

#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
using namespace std;

static int *tickets;
static bool *choosing;
static int *val;
static int*k;
#define N 4

// To calculate the value of max ticket that the current process will get
int maxValue(){
	int m = INT_MIN;
	for(int i=0;i<N;i++){
		if(tickets[i]>m)
			m=tickets[i];
	}
	return m;
}


void initialiseTickets(){
	tickets = (int*)malloc(sizeof(int)*N);
	memset((void*)tickets, 0, sizeof(tickets)); 
}




void startProcess(int x){
	choosing[x]=true;
	tickets[x]= maxValue()+1;
	choosing[x]=false;
	int i=0;
	// ALL PROCESSES PERFORM THIS
	for(i=0;i< N;i++){
		if(i==x)
			continue;
		while(choosing[i])
			 sleep(3);
		while(tickets[i]!=0 && tickets[i]<tickets[x])
			 sleep(3);
		if(tickets[i]==tickets[x] && i<x){
			while(tickets[i]!=0)
				 sleep(3);
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
	choosing = (bool*)malloc(sizeof(bool)*N); 
	val = (int*)malloc(sizeof(int)*N);
	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	choosing = static_cast<bool*>(mmap(NULL, sizeof *choosing*N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	tickets = static_cast<int*>(mmap(NULL, sizeof *tickets*N, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	k = (int*)malloc(sizeof(int)*N);
	k = static_cast<int*>(mmap(NULL, sizeof *k, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

	// initial shared memory allocation
	*val = 10;
	*k=1;
	/*int processNo=0;
	int pid=fork();
	
	if(pid<0){
		cout<<"Processes are not created"<<endl;
		exit(0);
	}
	else if(pid==0){
		processNo=0;
		startProcess(processNo);
	}
	else{
		processNo=1;
		startProcess(processNo);
	}*/

	for(int i=0;i<N;i++){ 
        if(fork() == 0){ 
            
            //cout<<"k - "<<*k<<endl;
            startProcess(*k);
            *k = (*k)+1;
            exit(0); 
        } 
    } 
	return 0;
}
/*
YUKTI KHURANA 
2017UCP1234
*/
