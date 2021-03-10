// Producer Consumer (single producer and consumer using semaphores and fork)

#include <bits/stdc++.h>
#include <unistd.h>
#include <semaphore.h>
#include <random>
#include <pthread.h>
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
#include <sys/wait.h>
using namespace std;

#define size 15


int idp = 0, idc = 0;
sem_t *full, *empty;
static int *buffer;

void *Producer(){
    while(2){
        sleep(1);
        sem_wait(empty);
            // cs entered        
            if(buffer[idp]==-1){
                cout<<"\nProducer thread in cs"<<endl;
                int item = rand()%100;
                buffer[idp] = item;
                cout<<"Producer Produced = "<<item<<endl;
                idp = (idp+1)%size;
                cout<<"\n------BUFFER---------------------------------------\n";
                for(int i=0;i<size;i++){
                    cout<<buffer[i]<<" ";
                }
                cout<<"\n---------------------------------------------------\n";
            }
        sem_post(full);

    }

}

void *Consumer(){
    while(1){
        sleep(2);
        sem_wait(full);
        // cs entered
        if (buffer[idc]!=-1){
            cout<<"\nConsumer thread in cs"<<endl;
            int item = buffer[idc];
            cout<<"Consumer consumed "<<item<<endl<<endl;
            buffer[idc] = -1;
            idc = (idc+1)% size;
            cout<<"\n------BUFFER---------------------------------------\n";
            for(int i=0;i<size;i++){
                cout<<buffer[i]<<" ";
            }
            cout<<"\n---------------------------------------------------\n";
        }
        sem_post(empty);

    }

}

int main(){
     
   
    buffer = static_cast<int*>(mmap(NULL, sizeof *buffer*size,PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    full = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    empty = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t),PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    sem_init(empty, 0, size);
    sem_init(full, 0, 0);

    for(int i=0;i<size;i++){
        buffer[i] = -1;
    }

    cout<<"\nInitial buffer : "<<endl;
    cout<<"\n------BUFFER---------------------------------------\n";
    for(int i=0;i<size;i++){
            cout<<buffer[i]<<" ";
    }
    cout<<"\n---------------------------------------------------\n";
    if (fork()==0){
        Producer();
    }
    if (fork()==0){
        Consumer();
    }
    wait(NULL);
    wait(NULL);

   
    
    return 0;
}