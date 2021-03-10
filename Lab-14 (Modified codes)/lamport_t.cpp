// Lamport solution using threads

#include <bits/stdc++.h>
#include <unistd.h>
#include <thread>
#include <sys/mman.h>

using namespace std;

#define no_t 5

int val = 5;
bool choosing[no_t];
int tickets[no_t];
thread tid[no_t];

int max_ticket(){
    return *max_element(tickets, tickets+no_t);
}

void startProcess(int x){

    choosing[x] = true;
    tickets[x] = max_ticket()+1; 
    choosing[x] = false;

    for(int i=0;i<no_t;i++){
        if (i==x){
            continue;
        }
        while(choosing[i]){
            sleep(5);
        }
        
        while(tickets[i]!=0 && tickets[i] < tickets[x]){
            sleep(5);
        }

        if (tickets[i] == tickets[x] && i<x){
            while(tickets[i]!=0){
                sleep(5);
            }
        }
    }

    // cs entered
    cout<<"\nPROCESS-"<<x+1<<" ENTERED CS!"<<endl;
	val = val + 10;
	cout<<"PROCESS - "<<x+1<<": value = "<<val<<endl;
	cout<<"PROCESS-"<<x+1<<" EXITED CS!"<<endl<<endl;

	tickets[x]=0;

}


int main(){
    // initialising the tickets as 0 for each process
    for(int i=0;i<no_t;i++){
        tickets[i] = 0;
    }
    cout<<"Total no of processes = "<<no_t<<endl;
	cout<<"INITIAL VALUE OF SHARED VARIABLE = "<<val<<endl;

    //  thread creation 
    for(int i=0;i<no_t;i++){
        tid[i] = thread(startProcess, i);
    }

    // join for sync
    for(int i=0;i<no_t;i++){
        tid[i].join();
    }
    cout<<"THE VALUE AT THE END OF ALL PROCESSES = "<<val<<endl;
    return 0;
}