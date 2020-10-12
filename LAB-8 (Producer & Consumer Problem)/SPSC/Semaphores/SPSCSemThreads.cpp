/* SINGLE PRODUCER - SINGLE CONSUMER PROBLEM USING SEMAPHORES USING THREADS */

#include <bits/stdc++.h>
#include <thread>
#include <semaphore.h>
#include <random>
#include <unistd.h>


using namespace std;

#define BUFFER_SIZE 100

int buffer[BUFFER_SIZE];
int idp=0,idc=0;

//  declaring semaphores (signaing mechanism)
sem_t full,empty;

// producer process
void* produce(void* arg){
	while(1){
		sleep(1);
		// producer thread blocks till value of empty > 0, waiting 
		sem_wait(&empty); // down()
				int item = rand()%50;
				buffer[idp] = item;
				cout<<"\nProducer Produced :  "<<item<<" at pos = "<<idp<<endl<<endl;
				idp = (idp+1)%BUFFER_SIZE;
				
		//semaphore released
		sem_post(&full); //up()
		//sleep(1);
	}
}
// consumer process
void* consume(void* arg){
	while(1){
		sleep(1);
		// consumer thread blocks (down) till value of full > 0,waiting 
		sem_wait(&full);
				int item = buffer[idc];
				cout<<"Consumer Consumed :  "<<item<<" at pos = "<<idc<<endl<<endl;
				idc = (idc+1)%BUFFER_SIZE;				
		sem_post(&empty);
		//sleep(3);
	}
}

int main(){
	pthread_t producer,consumer;
	// INTIALISING THE SEMAPHORES TO 0
	sem_init(&empty,0,BUFFER_SIZE);
	sem_init(&full,0,0);
	// THREADS CREATION
	pthread_create(&producer,NULL,&produce,NULL);
	pthread_create(&consumer,NULL,&consume,NULL);
	pthread_join(producer, NULL);
	pthread_join(consumer, NULL);
	return 0;
}