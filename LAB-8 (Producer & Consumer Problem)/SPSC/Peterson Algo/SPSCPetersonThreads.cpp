/* SINGLE PRODUCER SINGLE CONSUMER USING PETERSON'S SOLUTION IN THREADS */

#include <bits/stdc++.h> 
#include <unistd.h> 
#include <pthread.h>
using namespace std;

#define BUFFER_SIZE 100

int buffer[BUFFER_SIZE];
int idp=0,idc=0; 
bool P1_wantstoEnter = false;
bool P2_wantstoEnter = false;
int favouredProcess = 1;

void *Producer(void *vargp){ 
	while(1){
		sleep(1);
		P1_wantstoEnter = true;
		favouredProcess = 1;
		while(P2_wantstoEnter && favouredProcess==2){
			// process-1 will wait while process-2 is in critical section
			sleep(2);
		}
		// critical section
		cout<<"\nPRODUCER THREAD IN CS "<<endl;
		int item = rand()%60;
		buffer[idp] = item;
		cout<<"Producer Produced :  "<<item<<endl;
		idp = (idp+1)%BUFFER_SIZE;

		P1_wantstoEnter = false;
	}
} 

void *Consumer(void *vargp){
	while(1){
		sleep(1); 
		P2_wantstoEnter = true;
		favouredProcess = 1;
		while(P1_wantstoEnter && favouredProcess==1){
			// process-2 will wait while process-1 is in critical section
			sleep(2);
		}
		//critical section
		cout<<"\nCONSUMER THREAD IN CS "<<endl;
		int item = buffer[idc];
		cout<<"Consumer Consumed :  "<<item<<endl<<endl;
		idc = (idc+1)%BUFFER_SIZE;

		P2_wantstoEnter = false;
	}

} 


int main(){ 
	pthread_t tid1[1],tid2[1]; 
	int i=0;
	pthread_create(&tid1[0], NULL, Producer, NULL); 
	pthread_create(&tid2[0],NULL,Consumer,NULL);
	// for synchronisation
	pthread_join(tid1[0], NULL);
	pthread_join(tid2[0], NULL);
	return 0; 
} 

