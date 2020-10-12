/*
YUKTI KHURANA 
2017UCP1234
*/
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
using namespace std;

static int* val;
static bool* P1_wantstoEnter ;
static bool* P2_wantstoEnter ;
static int* favouredProcess;;

// process P1 will increment shared variable value
void Process1(){

	*P1_wantstoEnter = true;
	*favouredProcess=2;

	while(*P2_wantstoEnter && *favouredProcess==2){
		// process-1 will wait while process-2 is in critical section
		sleep(2);
	}
	cout<<"\nPROCESS-1 THREAD current : val = "<<val<<endl;
	cout<<"PROCESS-1 PREVIOUS VALUE = "<<*val<<endl;	
	*val = *val + 12;
	cout<<"PROCESS-1 VALUE CHANGED = "<<*val<<endl;
	*P1_wantstoEnter=false;
	cout<<"PROCESS-1 EXITED CS!\n"<<endl;
}
// process P2 will decrement shared variable value
void Process2(){

	*P2_wantstoEnter = true;
	*favouredProcess=1;
	while(*P1_wantstoEnter && *favouredProcess==1){
		// process-2 will wait while process-1 is in critical section
		sleep(2);
	}
	//critical section
	cout<<"\nPROCESS-2 ENTERED CS!"<<endl;
	cout<<"PROCESS-2 PREVIOUS VALUE = "<<*val<<endl;
	*val = *val - 10;
	cout<<"PROCESS-2 VALUE CHANGED = "<<*val<<endl;
	*P2_wantstoEnter = false;
	cout<<"PROCESS-2 EXITED CS!\n"<<endl;
}

int main(){
	//  shared memory
	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	favouredProcess = static_cast<int*>(mmap(NULL, sizeof *favouredProcess, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P1_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P1_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P2_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P2_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

	// initialisations
	*favouredProcess=1;
	*P1_wantstoEnter=false;
	*P2_wantstoEnter=false;	
	*val = 30;

	// process creation by fork
	int pid = fork();

	// process creation failed
	if(pid<0){
		cout<<"Sorry!!Process creation failed!!"<<endl;
		exit(0);
	}
	else if(pid==0){
		Process1();
	}
	else{
		Process2();
	}

	return 0;
}
/*
YUKTI KHURANA 
2017UCP1234
*/

