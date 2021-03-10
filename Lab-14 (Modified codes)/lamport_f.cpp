// Lamport solution using threads

#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdio.h>
#include <sys/wait.h>
using namespace std;

#define N 5

static int *tickets;
static int *val;
static int *k;
static bool *choosing;


int max_ticket(){
    //return *max_element(tickets, tickets+N);
    int m = INT_MIN;
	for(int i=0;i<N;i++){
		if(tickets[i]>m)
			m=tickets[i];
	}
	return m;
}

void startProcess(int x){
    choosing[x] = true;
    tickets[x] = max_ticket()+1;
    //cout<<"ticket value of x = "<<x<<" is = "<<tickets[x];
    choosing[x] = false;

    for(int i=0;i<N;i++){
        if(i==x){
            continue;
        }
        while(choosing[i]){
            
        }
        while(tickets[i]!=0 && tickets[i]<tickets[x]){
            
        }
        if(tickets[i] == tickets[x] && i<x){
            while(tickets[i]!=0){
            }
        }
    }   
    // cs entered
    cout<<"\nPROCESS-"<<x+1<<" ENTERED CS!"<<endl;
	*val = *val + 10;
	cout<<"PROCESS - "<<x+1<<": value = "<<*val<<endl;
	cout<<"PROCESS-"<<x+1<<" EXITED CS!"<<endl<<endl;

	tickets[x]=0;
    if(x == N-1){
        cout<<"THE VALUE AT THE END OF ALL PROCESSES = "<<*val<<endl;
    }

}


int main(){
    
    // declaring shared memory variables
    val = (int*)malloc(sizeof(int));
    choosing = (bool*)malloc(sizeof(bool)*N);   
    tickets = (int*)malloc(sizeof(int)*N);   


    val = static_cast<int*>(mmap(NULL, sizeof*val, PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS, -1,0));
    choosing = static_cast<bool*>(mmap(NULL, sizeof *choosing, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	tickets = static_cast<int*>(mmap(NULL, sizeof *tickets, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
   

    // initialising the tickets as 0 for each process
    for(int i=0;i<N;i++){
        tickets[i] = 0;
    }
    //memset((void*)tickets, 0, sizeof(tickets));
    *val = 0;
   

    cout<<"Total no of processes = "<<N<<endl;
	cout<<"INITIAL VALUE OF SHARED VARIABLE = "<<*val<<endl;

    // creating N processes using fork
    for(int i=0;i<N;i++){
        if (fork()==0){
            startProcess(i);            
            exit(0);
        }
    }

    for(int i=0;i<N;i++){
        wait(NULL);
    }   
 
    
    return 0;
}