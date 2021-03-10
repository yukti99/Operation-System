/*
YUKTI KHURANA 
2017UCP1234
*/

#include<bits/stdc++.h>
#include<unistd.h>
#include<sys/mman.h>
using namespace std;

static int* val;
static bool* P1_wantstoEnter ;
static bool* P2_wantstoEnter ;
static int* favouredProcess;;

void Process1(){
	*P1_wantstoEnter=true;
		while(*P2_wantstoEnter){
			if(*favouredProcess==2){
				*P1_wantstoEnter=false;
				while(*favouredProcess==2)
						sleep(10);

				*P1_wantstoEnter=true;
		}
	}
	// value incremented
	// CS
	cout<<"\nPROCESS-1 ENTERED CS!"<<endl;
	cout<<"PROCESS-1 PREVIOUS VALUE = "<<*val<<endl;
	*val=*val+5;
	cout<<"PROCESS-1 VALUE CHANGED = "<<*val<<endl;
	*favouredProcess=2;
	*P1_wantstoEnter=false;	
	cout<<"PROCESS-1 EXITED CS!\n"<<endl;
}

void Process2(){

	*P2_wantstoEnter=true;
		while(*P1_wantstoEnter){
			if(*favouredProcess==1){
				*P2_wantstoEnter=false;
				while(*favouredProcess==1)
						sleep(10);

				*P2_wantstoEnter=true;
		}
	}
	//critical section
	cout<<"\nPROCESS-2 ENTERED CS!"<<endl;
	cout<<"PROCESS-2 PREVIOUS VALUE = "<<*val<<endl;
	*val = *val+3;
	cout<<"PROCESS-2 VALUE CHANGED = "<<*val<<endl;
	*favouredProcess=1;
	*P2_wantstoEnter=false;	
	cout<<"PROCESS-2 EXITED CS!\n"<<endl;
}

int main(){

	val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ | PROT_WRITE,MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	favouredProcess = static_cast<int*>(mmap(NULL, sizeof *favouredProcess, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P1_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P1_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	P2_wantstoEnter = static_cast<bool*>(mmap(NULL, sizeof *P2_wantstoEnter, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	

	*P1_wantstoEnter=false;
	*P2_wantstoEnter=false;
	*favouredProcess=1;

	*val = 10;
	int pid = fork();

	// process creation failed
	if(pid<0){
		cout<<"Sorry!!Process creation failed!!"<<endl;
		exit(0);
	}
	else if(pid == 0){
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
