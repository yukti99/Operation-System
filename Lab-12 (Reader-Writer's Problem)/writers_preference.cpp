#include <bits/stdc++.h>
#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
using namespace std;

// defining the number of readers and writers 
#define total_writers 10
#define total_readers 15

// declaring semaphores 
sem_t resource, rmutex, wmutex, readTry;

int cnt = 1; //critical section variable
// to keep track of the count of readers and writers 
int numreader = 0;
int numwriter = 0;

void *writer(void *wno){  
    sem_wait(&wmutex);
    numwriter++;
    if(numwriter==1)
	sem_wait(&readTry);
    sem_post(&wmutex);
    sem_wait(&resource);
    cnt = cnt+1;
    printf("Writer %d modified shared variable to %d\n",(*((int *)wno)),cnt);
    sem_post(&resource);
    sem_wait(&wmutex);
    numwriter--;
    if(numwriter==0)
	sem_post(&readTry);
    sem_post(&wmutex);
}

void *reader(void *rno){   
    // Reader acquire the lock before modifying no of readers
    sem_wait(&readTry);
    sem_wait(&rmutex);
    numreader++;
    if(numreader == 1) {
        sem_wait(&resource); // If this id the first reader, then it will block the writer
    }
    sem_post(&rmutex);
    sem_post(&readTry);
    // Reading Section
    printf("Reader %d: read shared variable as %d\n",*((int *)rno),cnt);
    // Reader acquire the lock before modifying numreader
    sem_wait(&rmutex);
    numreader--;
    if(numreader == 0) {
        sem_post(&resource); // If this is the last reader, it will wake up the writer.
    }
    sem_post(&rmutex);
}

int main(){   

    pthread_t read[total_readers],write[total_writers];
    // initialising the semaphores 
    sem_init(&resource,0,1);
    sem_init(&rmutex,0,1);
    sem_init(&wmutex,0,1);
    sem_init(&readTry,0,1);

    printf("Initial Value = \n", cnt);
  
    int Writer_Number[total_writers];
    int Reader_Number[total_readers];

    int i =0;
    // for numbering the readers and writers
    for(int i=0;i<total_writers;i++){
	    Writer_Number[i] = i;
    }

    for(i=0;i<total_readers;i++){
	    Reader_Number[i] = i;
    }
	// launching threads for readers and writers
    for(int i = 0; i < total_writers; i++) {
        pthread_create(&write[i], NULL, (void *)writer, (void *)&Writer_Number[i]);
    }

    for(int i = 0; i < total_readers; i++) {
        pthread_create(&read[i], NULL, (void *)reader, (void *)&Reader_Number[i]);
    }
    // joining threads for synchronization
    for(int i = 0; i < total_readers; i++) {
        pthread_join(read[i], NULL);
    }
    for(int i = 0; i < total_writers; i++) {
        pthread_join(write[i], NULL);
    }

    return 0;   
}
