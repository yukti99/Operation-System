/*
YUKTI KHURANA 
2017UCP1234
*/
 #include <bits/stdc++.h> 
#include <unistd.h> 
#include <pthread.h>
using namespace std;


static int val = 30; 
bool P1_wantstoEnter = false;
bool P2_wantstoEnter = false;
int favouredProcess = 1;

void *Process1(void *vargp){ 
	P1_wantstoEnter = true;
	favouredProcess = 1;
	while(P2_wantstoEnter && favouredProcess==2){
		// process-1 will wait while process-2 is in critical section
		sleep(3);
	}
	// critical section
	cout<<"\nPROCESS-1 THREAD current : val = "<<val<<endl;
	val = val + 12;

	cout<<"\nPROCESS-1 THREAD value altered to : val = "<<val<<endl;
	P1_wantstoEnter = false;
} 

void *Process2(void *vargp){ 
	P2_wantstoEnter = true;
	favouredProcess = 1;
	while(P1_wantstoEnter && favouredProcess==1){
		// process-2 will wait while process-1 is in critical section
		sleep(3);
	}
	//critical section
	cout<<"\nPROCESS-2 THREAD current val : val = "<<val<<endl;
	val = val - 10;
	cout<<"\nPROCESS-2 THREAD value altered to : val = "<<val<<endl;
	P2_wantstoEnter = false;
	//cout<<"PROCESS-2 VALUE = "<<*val<<endl; 

} 


int main(){ 
	
	pthread_t tid1[1],tid2[1]; 
	pthread_create(&tid1[0], NULL, Process1, NULL); 
	pthread_create(&tid2[0],NULL,Process2,NULL);
	// for synchronisation
	pthread_join(tid1[0], NULL);
	pthread_join(tid2[0], NULL);
	return 0; 
} 
/*
YUKTI KHURANA 
2017UCP1234
*/

