// Producer Consumer (single producer and consumer using semaphores and threads)

#include <bits/stdc++.h>
#include <unistd.h>
#include <semaphore.h>
#include <random>
#include <pthread.h>
using namespace std;

#define size 15

int buffer[size];
int idp = 0, idc = 0;
sem_t full, empty;

void *Producer(void *vargp){
    while(1){
        sleep(1);
        sem_wait(&empty);
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
        sem_post(&full);

    }

}

void *Consumer(void *vargp){
    while(1){
        sleep(3);
        sem_wait(&full);
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
        sem_post(&empty);

    }

}

int main(){
    for(int i=0;i<size;i++){
        buffer[i] = -1;
    }
    cout<<"\nInitial buffer : "<<endl;
    cout<<"\n------BUFFER---------------------------------------\n";
    for(int i=0;i<size;i++){
            cout<<buffer[i]<<" ";
    }
    cout<<"\n---------------------------------------------------\n";

    pthread_t tid1[1], tid2[1];
    sem_init(&empty, 0, size);
    sem_init(&full, 0, 0);

    pthread_create(&tid1[0], NULL, Producer, NULL);
    pthread_create(&tid2[0], NULL, Consumer, NULL);

    pthread_join(tid1[0], NULL);
    pthread_join(tid2[0], NULL);
    
    return 0;
}