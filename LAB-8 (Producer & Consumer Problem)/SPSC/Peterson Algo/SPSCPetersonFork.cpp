/*
YUKTI KHURANA 
2017UCP1234

SINGLE PRODUCER SINGLE CONSUMER PETERSON SOLUTION USING FORK
*/
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
using namespace std;

#define BUFFER_SIZE 100

static int *buffer;
static bool* P1_wantstoEnter ;
static bool* P2_wantstoEnter ;
static int* favouredProcess;


int idc = 0,idp = 0;

void *Producer(){ 
	while(1){
		*P1_wantstoEnter = true;
		*favouredProcess = 1;
		while(*P2_wantstoEnter && *favouredProcess==2){
			// process-1 will wait while process-2 is in critical section
			sleep(2);
		}
		// critical section
		//cout<<"\nPRODUCER THREAD IN CS "<<endl;
		int item = rand()%60;
		buffer[idp] = item;
		cout<<"Producer Produced :  "<<item<<endl;
		idp = (idp+1)%BUFFER_SIZE;

		*P1_wantstoEnter = false;
		sleep(2); 
	}
} 

void *Consumer(){
	while(1){
		
		*P2_wantstoEnter = true;
		*favouredProcess = 1;
		while(*P1_wantstoEnter && *favouredProcess==1){
			// process-2 will wait while process-1 is in critical section
			sleep(2);
		}
		//critical section
		//cout<<"\nCONSUMER THREAD IN CS "<<endl;
		int item = buffer[idc];
		cout<<"Consumer Consumed :  "<<item<<endl<<endl;
		idc = (idc+1)%BUFFER_SIZE;

		*P2_wantstoEnter = false;
		sleep(2); 
	}

} 

int main(){
	//  shared memory
	
	favouredProcess = static_cast<int*>(mmap(NULL, sizeof *favouredProcess, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P1_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P1_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P2_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P2_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	buffer = static_cast<int*>(mmap(NULL, sizeof *buffer*BUFFER_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));


	// initialisations
	*favouredProcess=1;
	*P1_wantstoEnter=false;
	*P2_wantstoEnter=false;	

	for(int i=0;i<BUFFER_SIZE;i++){
		buffer[i] = 0;
	}
	int child2;
	int child1 = fork();

	if (child1 == 0){
		Producer();
	}else{
		child2 = fork();
		if (child2 == 0){
			Consumer();
		}

	}
	return 0;
}
/*
YUKTI KHURANA 
2017UCP1234
*/

