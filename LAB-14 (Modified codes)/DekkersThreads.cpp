/*
YUKTI KHURANA 
2017UCP1234
*/
 #include <bits/stdc++.h> 
#include <unistd.h> 
#include <pthread.h>
using namespace std;
#define THREADS 1

int val = 30; 
bool P1_wantstoEnter = false;
bool P2_wantstoEnter = false;
int favouredProcess = 1;

void *Process1(void *vargp){ 
	P1_wantstoEnter=true;
	while(P2_wantstoEnter){
		if(favouredProcess==2){
			P1_wantstoEnter=false;
			while(favouredProcess==2); // wait till the favoured process is 2
					//sleep(10);

			P1_wantstoEnter=true;
		}
	}
	// critical section
	cout<<"\nPROCESS-1 ENTERED CS!"<<endl;
	cout<<"PROCESS-1 THREAD current : val = "<<val<<endl;
	val = val + 12;
	cout<<"PROCESS-1 THREAD value altered to : val = "<<val<<endl;
	cout<<"PROCESS-1 EXITED CS!\n"<<endl;
	favouredProcess=2;
	P1_wantstoEnter = false;
	
} 

void *Process2(void *vargp){ 
	P2_wantstoEnter=true;
	while(P1_wantstoEnter){
		if(favouredProcess==1){
			P2_wantstoEnter=false;
			while(favouredProcess==1);
					//sleep(10);

			P2_wantstoEnter=true;
		}
	}
	//critical section
	cout<<"\nPROCESS-2 ENTERED CS!"<<endl;
	cout<<"PROCESS-2 THREAD current val : val = "<<val<<endl;
	val = val - 10;
	cout<<"PROCESS-2 THREAD value altered to : val = "<<val<<endl;
	cout<<"PROCESS-2 EXITED CS!\n"<<endl;
	favouredProcess=1;
	P2_wantstoEnter = false;
	
	
} 


int main(){ 
	
	pthread_t tid1[THREADS],tid2[THREADS]; 

	// three threads created
	for (int i = 0; i < THREADS; i++) {
		pthread_create(&tid1[i], NULL, Process1, NULL); 
		pthread_create(&tid2[i],NULL,Process2,NULL);
	}
	for (int i = 0; i < THREADS; i++){
		pthread_join(tid1[i], NULL);
		pthread_join(tid2[i], NULL);
	}

	return 0; 
} 
/*
YUKTI KHURANA 
2017UCP1234
*/

