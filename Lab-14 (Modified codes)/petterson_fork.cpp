#include <bits/stdc++.h>
#include <unistd.h>
#include <sys/mman.h>
using namespace std;


static int* val;
static bool* p1_wants;
static bool* p2_wants;
static int* fp;


void Process1(){
    *p1_wants = true;
    *fp=2;
    while(*p2_wants && *fp==2); // busy wait

    // cs entered
    cout<<"\nPROCESS-1 THREAD current : val = "<<*val<<endl;
	*val = *val + 12;
	cout<<"\nPROCESS-1 THREAD value altered to : val = "<<*val<<endl;   
    *p1_wants = false;

}

void Process2(){
    *p2_wants = true;
    *fp=1;
    while(*p1_wants && *fp==1); // busy wait

    // cs entered
    cout<<"\nPROCESS-2 THREAD current : val = "<<*val<<endl;
	*val = *val - 5;
	cout<<"\nPROCESS-2 THREAD value altered to : val = "<<*val<<endl;   
    *p2_wants = false;

}

int main(){
    // shared memory;
    val = static_cast<int*>(mmap(NULL, sizeof *val, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1,0));
    fp = static_cast<int*>(mmap(NULL, sizeof*fp, PROT_READ|PROT_WRITE,MAP_SHARED|MAP_ANONYMOUS,-1,0));
    p1_wants =static_cast<bool*>(mmap(NULL, sizeof *p1_wants, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS,-1,0));
    p2_wants =static_cast<bool*>(mmap(NULL, sizeof *p1_wants, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS,-1,0));

    // initialising
    *val = 10;
    *fp = 1;
    *p1_wants = false;
    *p2_wants = false;

    int pid = fork();
    if (pid < 0){
        cout<<"Error!!";
        exit(0);
    }
    else if (pid==0){
        Process1();
    }
    else{
        Process2();
    }
    return 0;

    

}