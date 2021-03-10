// Producer Consumer (single producer and consumer using semaphores and threads)

#include <bits/stdc++.h>
#include <unistd.h>
#include <semaphore.h>
#include <random>
#include <pthread.h>
using namespace std;

#define pno 5
#define cno 5
#define size 20

int buffer[size];
int idp = 0, idc = 0;
sem_t full, empty, mutex1;

pthread_t producers[pno];
pthread_t consumers[cno];

void *Producer(void *no){
    int pnum = *(int*)no;
    while(1){
        sleep(2);
        sem_wait(&empty);
            sem_wait(&mutex1);
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
            sem_post(&mutex1);
        sem_post(&full);

    }

}

void *Consumer(void *no){
    int cnum = *(int*)no;
    while(1){
        sleep(4);
        sem_wait(&full);
            sem_wait(&mutex1);
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
            sem_post(&mutex1);
        sem_post(&empty);

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
    sem_init(&empty, 0, size);
    sem_init(&full, 0, 0);
    sem_init(&mutex1, 0,1);

    for(int i=0;i<size;i++){
        buffer[i] = -1;
    }
    cout<<"\nInitial buffer : "<<endl;
    cout<<"\n------BUFFER---------------------------------------\n";
    for(int i=0;i<size;i++){
            cout<<buffer[i]<<" ";
    }
    cout<<"\n---------------------------------------------------\n";

    // creating threads
    for(int i=0;i<pno;i++){
        pthread_create(&producers[i],NULL, &Producer, (void*)&p[i]);
    }
    for(int i=0;i<cno;i++){
        pthread_create(&consumers[i],NULL, &Consumer, (void*)&c[i]);
    }

    // join() for all threads
	for(int i=0;i<pno;i++){
		pthread_join(producers[i],NULL);
	}
	for(int i=0;i<cno;i++){
		pthread_join(consumers[i],NULL);
	} 
    
    return 0;
}