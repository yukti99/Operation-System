/* SINGLE PRODUCER - SINGLE CONSUMER PROBLEM USING SEMAPHORES USING THREADS */
#include <semaphore.h>
#include <bits/stdc++.h>
#include <stdlib.h>
#include <stdio.h>
#include <random>
#include <unistd.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/types.h> 
#include <sys/ipc.h> 
#include <sys/shm.h> 
#include <stdbool.h> 
#include <sys/stat.h>
#include <fcntl.h>
using namespace std;



#define BUFFER_SIZE 100
static int *buffer;
int idp=0,idc=0;

//  declaring semaphores (signaing mechanism)
sem_t *full,*empty,*mutex1;



// producer process
void* Producer(){
	while(1){
		sem_wait(empty); // down()
					int item = rand()%50;
					buffer[idp] = item;
					cout<<"\nProducer Produced :  "<<item<<" at pos = "<<idp<<endl<<endl;
					idp = (idp+1)%BUFFER_SIZE;				
		sem_post(full); //up()			
		sleep(2);
	}
}
// consumer process
void* Consumer(){

	while(1){
		sem_wait(full);
			sem_wait(mutex1);
				int item = buffer[idc];
				cout<<"Consumer Consumed :  "<<item<<" at pos = "<<idc<<endl<<endl;
				idc = (idc+1)%BUFFER_SIZE;
			sem_post(mutex1);			
		sem_post(empty);
		sleep(2);
	
	}
}

int main(){

	int shm;

  if ((shm = shm_open("myshm1", O_RDWR | O_CREAT, S_IRWXU))  < 0) {
    perror("shm_open");
    exit(1);
  }

  if ( ftruncate(shm, sizeof(sem_t)) < 0 ) {
    perror("ftruncate");
    exit(1);
  }

  full = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE,    MAP_SHARED, shm, 0));
   
  if (sem_init(full, 0, 0) < 0) {
    perror("semaphore initialization");
    exit(1);
  }
  int shm2;

  if ((shm2 = shm_open("myshm2", O_RDWR | O_CREAT, S_IRWXU))  < 0) {
    perror("shm_open");
    exit(1);
  }

  if ( ftruncate(shm2, sizeof(sem_t)) < 0 ) {
    perror("ftruncate");
    exit(1);
  }

  empty = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE,    MAP_SHARED, shm2, 0));
   
  if (sem_init(empty, 0, BUFFER_SIZE) < 0) {
    perror("semaphore initialization");
    exit(1);
  }

	// shared buffer by two processes
	buffer = static_cast<int*>(mmap(NULL, sizeof *buffer*BUFFER_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

	for(int i=0;i<BUFFER_SIZE;i++){
		buffer[i] = 0;
	}
	int shm3;

  if ((shm3 = shm_open("myshm3", O_RDWR | O_CREAT, S_IRWXU))  < 0) {
    perror("shm_open");
    exit(1);
  }

  if ( ftruncate(shm3, sizeof(sem_t)) < 0 ) {
    perror("ftruncate");
    exit(1);
  }

  mutex1 = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE,    MAP_SHARED, shm3, 0));
   
  if (sem_init(mutex1, 0, 1) < 0) {
    perror("semaphore initialization");
    exit(1);
  }
	
	int child2;
	int child1 = fork();

	if (child1 == 0){
		Producer();
	}else{
		child2 = fork();
		if (child2 == 0){
			fork();
			fork();
			fork();
			Consumer();
		}

	}

	return 0;
}