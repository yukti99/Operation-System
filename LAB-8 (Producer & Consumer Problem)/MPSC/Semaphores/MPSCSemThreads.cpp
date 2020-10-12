/*MULTIPLE PRODUCERS MULTIPLE CONSUMERS USING SEMAPHORES USING THREADS*/

#include <bits/stdc++.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
using namespace std;

#define prod_n 5
#define cons_n 1
#define BUFFER_SIZE 100

// thread  array for multiple producer and consumers
pthread_t producers[prod_n];
pthread_t consumers[cons_n];

// 3 semaphores used for sync
sem_t mutex1,empty,full;

int idp = 0,idc = 0;
int buf[BUFFER_SIZE];

int produce(pthread_t self){
	int i = 0;
	int p = 1 + rand()%60;
	while(!pthread_equal(producers[i],self) && i < prod_n){
		i++;
	}
	printf("\nProducer - %d produced %d \n\n",i+1,p);
	return p;
}


void consume(int p,pthread_t self){
	int i = 0;
	while(!pthread_equal(consumers[i],self) && i < cons_n){
		i++;
	}
	printf("\nConsumer - %d consumed %d\n\n",i+1,p);
	
}


void* producer(void *args){

	while(1){
		sleep(1);
		int p = produce(pthread_self());
		sem_wait(&empty);
			sem_wait(&mutex1);
				// critical section
				buf[idp] = p;
				idp = (idp+1)%BUFFER_SIZE; 
				sem_post(&mutex1);
		sem_post(&full);
	}
	
	return NULL;
}


void* consumer(void *args){
	while(1){
		sleep(1);
		sem_wait(&full);
			int c = buf[idc];
			consume(c,pthread_self());
			idc = (idc+1)%BUFFER_SIZE;
		sem_post(&empty);
	}
	return NULL;

}

int main(){
	
	int i,err;
	srand(time(NULL));

	// initialising semaphores
	sem_init(&mutex1,0,1);
	sem_init(&full,0,0);
	sem_init(&empty,0,BUFFER_SIZE);

	// creating multiple producers
	for(i=0;i<prod_n;i++){
		pthread_create(&producers[i],NULL,&producer,NULL);
		
	}
	// creating single consumer
	for(i=0;i<cons_n;i++){
		pthread_create(&consumers[i],NULL,&consumer,NULL);		
	}

	// join() for all threads
	for(i=0;i<prod_n;i++){
		pthread_join(producers[i],NULL);
	}
	for(i=0;i<cons_n;i++){
		pthread_join(consumers[i],NULL);
	}


	return 0;
}