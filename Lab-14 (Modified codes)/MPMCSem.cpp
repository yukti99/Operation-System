/* MULTIPLE PRODUCERS MULTIPLE CONSUMERS USING SEMAPHORES & THREADS*/

#include <bits/stdc++.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
using namespace std;

#define prod_n 5
#define cons_n 5
#define BUFFER_SIZE 100

// thread  array for multiple producer and consumers
pthread_t producers[prod_n];
pthread_t consumers[cons_n];

// 3 semaphores used for synchronisation
sem_t mutex1,empty,full;

int idp = 0,idc = 0;
// creating a buffer
int buf[BUFFER_SIZE];

void* producer(void *no){
	int p_num = * (int *)no;
	while(1){
		sleep(2);
		// producer will wait till the buffer is full
		sem_wait(&empty);
			// locking the critical section
			sem_wait(&mutex1);
				int p = 1 + rand()%60;			
				// critical section
				buf[idp] = p;
				printf("\nProducer - %d produced %d at index %d\n",p_num+1,p,idp);
				idp = (idp+1)%BUFFER_SIZE;					
			sem_post(&mutex1);			
		sem_post(&full);
	}
	
	return NULL;
}


void* consumer(void *no){
	int c_num = * (int *)no;
	while(1){
		sleep(2);
		sem_wait(&full);
			sem_wait(&mutex1);
                                // consumer entered the critical section 
				int c = buf[idc];
				//consume(c,pthread_self());
				printf("\nConsumer - %d consumed %d at index %d\n",c_num+1,c,idc);
				idc = (idc+1)%BUFFER_SIZE;				
			sem_post(&mutex1);
		sem_post(&empty);
	}
	return NULL;

}

int main(){
	
	int i,err;
	srand(time(NULL));
	int Cons_Number[cons_n];
    	int Prod_Number[prod_n];
	for (i = 0; i < cons_n; i++){
        	Cons_Number[i] = i;
	}
	for (i = 0; i < prod_n; i++){
		Prod_Number[i] = i;
	}

	// initialising semaphores
	sem_init(&mutex1,0,1);
	sem_init(&full,0,0);
	sem_init(&empty,0,BUFFER_SIZE);


	// creating multiple producers
	for(i=0;i<prod_n;i++){
		pthread_create(&producers[i],NULL,&producer, (void *)&Prod_Number[i]);
		
	}
	// creating multiple consumers
	for(i=0;i<cons_n;i++){
		pthread_create(&consumers[i],NULL,&consumer, (void *)&Cons_Number[i]);	
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
/*YUKTI KHURANA 
2017UCP1234*/
/*
YUKTI KHURANA 
2017UCP1234
*/
