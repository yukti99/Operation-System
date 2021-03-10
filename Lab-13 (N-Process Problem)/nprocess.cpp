/*
PROBLEM STATEMENT: 

Consider a sharable resource with the following characteristics. 
As long as there are fewer than N processes using the resource, new process can start using it right away. 
Once there are N processes using the resource, all N must leave before any new process can start using it. 
Processes do not block themselves while in exclusion, new processes are prevented from using the resource if there are (or were) N active users and 
the last process to depart unlocks upto N waiting processes.
N is user input.

*/



#include <bits/stdc++.h>
#include <semaphore.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
using namespace std;


int n = 0;
int pn=0;


// declaring semaphores
sem_t cmutex, block;

// for counting threads
int active = 0;
int waiting = 0;
bool must_wait = false;



void *procedure(void *no){
    int pno = *(int *)no;
    
    sem_wait(&cmutex);
        if (must_wait){ // if there are N users already
            waiting++;
            cout<<"\n\nProcess - "<<pno+1<<" has entered the waiting room...\n";
            sem_post(&cmutex);
            sem_wait(&block);
            // we reach here when all current users are departed
            sem_wait(&cmutex);
            waiting--; // not waiting anymore
        }
        active++;
        cout<<"Process - "<<pno<<" is now active ...\n";
        must_wait = (active == n);
    sem_post(&cmutex);

    // critical section
    cout<<"Process - "<<pno<<" is working in the critical section ...\n\n";

    sem_wait(&cmutex);
        active--;
        cout<<"Process - "<<pno<<" is de-activated now ...\n";
        if(active == 0){
            int x;
            if (waiting < n){
                x = waiting;
            }else{
                x = n;
            }
            // since this is the last process, it unblocks up to n waiting processes
            while(x>0){
                sem_post(&block);
                x--;
            }
            // since critical section is empty now, new processes don't have to wait
            must_wait = false;
        }

    sem_post(&cmutex);




}


int main(){
    cout<<"Enter the value of N = ";
    cin>>n;
    cout<<"Enter the number of processes = ";
    cin>>pn;
    int pr[pn];
    for(int i=0;i<pn;i++){
        pr[i] = i;
    }

    // initialising the semaphores
    sem_init(&cmutex, 0, 1);
    sem_init(&block, 0, 0);

    pthread_t tid[pn];

    // creating the threads
    for(int i=0;i<pn;i++){
        pthread_create(&tid[i], NULL, procedure, (void*)&pr[i]);
    }

    for(int i=0;i<pn;i++){
        pthread_join(tid[i],NULL);
    }
    
    return 0;
}