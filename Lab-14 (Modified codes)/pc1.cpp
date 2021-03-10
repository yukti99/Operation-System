// Producer Consumer 

#include <bits/stdc++.h>
#include <unistd.h>
#include <pthread.h>
using namespace std;

#define size 15

int buffer[size];
int idp = 0, idc = 0;
bool p1_wants = false;
bool p2_wants = false;
int fp = 1;

void *Producer(void *vargp){
    while(1){
        sleep(1);
        p1_wants = true;
        fp=2;
        while(p2_wants && fp==2){
            sleep(2);
        }
        // cs entered
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
        p1_wants = false;

    }

}

void *Consumer(void *vargp){
    while(1){
        sleep(3);
        p2_wants = true;
        fp=1;
        while(p1_wants && fp==1){
            sleep(2);
        }
        // cs entered
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
        p2_wants = false;

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
    pthread_create(&tid1[0], NULL, Producer, NULL);
    pthread_create(&tid2[0], NULL, Consumer, NULL);

    pthread_join(tid1[0], NULL);
    pthread_join(tid2[0], NULL);
    
    return 0;
}