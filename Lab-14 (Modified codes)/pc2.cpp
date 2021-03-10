/*
YUKTI KHURANA 
2017UCP1234

SINGLE PRODUCER SINGLE CONSUMER PETERSON SOLUTION USING FORK
*/
#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
using namespace std;

#define size 15

static int *buffer;
static bool* p1_wants ;
static bool* p2_wants ;
static int* fp;


int idc = 0,idp = 0;

void *Producer(){
    while(1){
        sleep(2);
        *p1_wants = true;
        *fp=2;
        while(*p2_wants && *fp==2){
            sleep(2);
        }
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
        *p1_wants = false;

    }

}

void *Consumer(){
    while(1){
        sleep(3);
        *p2_wants = true;
        *fp=1;
        while(*p1_wants && *fp==1){
            sleep(2);
        }
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
        *p2_wants = false;

    }

}

int main(){
	//  shared memory
	
	fp = static_cast<int*>(mmap(NULL, sizeof *fp, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	p1_wants= static_cast<bool*>(mmap(NULL, sizeof *p1_wants, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	p2_wants = static_cast<bool*>(mmap(NULL, sizeof *p2_wants, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));
	buffer = static_cast<int*>(mmap(NULL, sizeof *buffer*size, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0));


	// initialisations
	*fp=1;
	*p1_wants=false;
	*p2_wants=false;	

	for(int i=0;i<size;i++){
		buffer[i] = -1;
	}
    /*
	int child2;
	int child1 = fork();

	if (child1 == 0){
		Producer();
	}else{
		child2 = fork();
		if (child2 == 0){
			Consumer();
		}

	}*/

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
/*
YUKTI KHURANA 
2017UCP1234
*/
