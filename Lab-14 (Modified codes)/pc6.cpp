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

int idp = 0, idc = 0;
sem_t *full, *empty, *mutex1;
static int *buffer;

#define pno 5
#define cno 5
#define size 20





void *Producer(int pnum){
    //int pnum = *(int*)no;
    while(1){
        sleep(2);
        sem_wait(empty);
            sem_wait(mutex1);
                // cs entered        
                if(buffer[idp]==-1){                    
                    int item = rand()%100;
                    buffer[idp] = item;
                    printf("\nProducer - %d produced %d at index %d\n",pnum+1,item,idp);
                    idp = (idp+1)%size;
                    cout<<"\n------BUFFER---------------------------------------\n";
                    for(int i=0;i<size;i++){
                        cout<<buffer[i]<<" ";
                    }
                    cout<<"\n---------------------------------------------------\n";
                }
            sem_post(mutex1);
        sem_post(full);

    }

}

void *Consumer(int cnum){
    //int cnum = *(int*)no;
    while(1){
        sleep(3);
        sem_wait(full);
            sem_wait(mutex1);
                // cs entered
                if (buffer[idc]!=-1){
                    
                    int item = buffer[idc];
                    printf("\nConsumer - %d consumed %d at index %d\n",cnum+1,item,idc);
                    buffer[idc] = -1;
                    idc = (idc+1)% size;
                    cout<<"\n------BUFFER---------------------------------------\n";
                    for(int i=0;i<size;i++){
                        cout<<buffer[i]<<" ";
                    }
                    cout<<"\n---------------------------------------------------\n";
                }
            sem_post(mutex1);
        sem_post(empty);

    }

}

int main(){

    srand(time(NULL));
    int c[cno];
    int p[pno];
    for(int i=0;i<pno;i++){
        p[i] = i;
    }
    for(int i=0;i<pno;i++){
        c[i] = i;
    }

    buffer = static_cast<int*>(mmap(NULL, sizeof *buffer*size,PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    full = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    empty = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t),PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
    mutex1 = static_cast<sem_t*>(mmap(NULL, sizeof(sem_t),PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));

    sem_init(empty, 0, size);
    sem_init(full, 0, 0);
    sem_init(mutex1, 0,1);

    for(int i=0;i<size;i++){
        buffer[i] = -1;
    }
    cout<<"\nInitial buffer : "<<endl;
    cout<<"\n------BUFFER---------------------------------------\n";
    for(int i=0;i<size;i++){
            cout<<buffer[i]<<" ";
    }
    cout<<"\n---------------------------------------------------\n";

    // creating processes using fork
    
    for(int i=0;i<pno;i++){
        if (fork()==0){
            Producer(i);          
            exit(0);
        }
        
    }
    
    for(int i=0;i<cno;i++){
        if (fork()==0){
            Consumer(i);       
            exit(0);
        }
    }

    for(int i=0;i<pno+cno;i++){
        wait(NULL);
    }   
    for(int i=0;i<cno;i++){
        wait(NULL);
    }
    /*
    int child2;
	int child1 = fork();
    int i=0,j=0;
	if (child1 == 0){
		fork();
		fork();
		Producer(i);
        i++;
	}else{
		child2 = fork();
		if (child2 == 0){
			fork();
			fork();
			Consumer(j);
            j++;
		}

	}
    */

 

    
    return 0;
}