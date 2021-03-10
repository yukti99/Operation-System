#include <bits/stdc++.h>
#include <unistd.h>
#include <pthread.h>
using namespace std;

#define t_no 1

int val = 20;
int fp = 2;
bool p1_wants = false;
bool p2_wants = false;

void *Process1(void* vargp){
    p1_wants = true;
    fp=2;
    while(p2_wants && fp==2); // busy wait

    // cs entered
    cout<<"\nPROCESS-1 THREAD current : val = "<<val<<endl;
	val = val + 15;
	cout<<"\nPROCESS-1 THREAD value altered to : val = "<<val<<endl;   
    p1_wants = false;

}

void *Process2(void* vargp){
    p2_wants = true;
    fp = 1;
    while(p1_wants && fp==1 ); // busy wait

    // cs entered 
    cout<<"\nPROCESS-2 THREAD current val : val = "<<val<<endl;
	val = val - 10;
	cout<<"\nPROCESS-2 THREAD value altered to : val = "<<val<<endl;
	p2_wants = false;

}

int main(){

    pthread_t tid1[t_no],tid2[t_no];
    for(int i=0;i<t_no;i++){
        pthread_create(&tid1[i], NULL, Process1,NULL);
        pthread_create(&tid2[i], NULL, Process2, NULL);
    }

    // joining for syncronisation
    for(int i=0;i<t_no;i++){
        pthread_join(tid1[i], NULL);
        pthread_join(tid2[i], NULL);
    }
    return 0;
}