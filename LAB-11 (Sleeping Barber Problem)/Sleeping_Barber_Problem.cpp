/* YUKTI KHURANA
   2017UCP1234 
*/

#include <bits/stdc++.h>
#include <semaphore.h>
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <pthread.h>
using namespace std;
#define N 1
#define s 3
#define cutting_time 3

// for waiting customers
sem_t cust;
sem_t barber;
sem_t chairs;

int seat[s];
int sitherenext = 0;
int servemenext = 0;


int Freechairs = s;
static int cnt=0;
static int bb=0;
int c=0,b=0;
static int done;
static int gone=0;

// sleeps till the customer doesn't arrive 
void *barbers(void* arg){
	//cout<<"hi"<<endl;
	//int index = 0;
	//int index = *(int*)(arg);
	//cout<<index<<endl;
	int mynext,ct;
	//bb = (bb+1)%b;
	cout<<"\nBarber id : "<<pthread_self()%10000<<" joins shop"<<endl;	
	while(done!=0){
		cout<<"\nBarber id : "<<pthread_self()%10000<<" goes to sleep "<<endl;
		sem_wait(&barber); 
			sem_wait(&chairs);
				servemenext = (servemenext+1)%s;
				mynext = servemenext;
				ct = seat[mynext];
				seat[mynext] = pthread_self()%10000;		
			sem_post(&chairs);
		sem_post(&cust);
		cout<<"\nBarber id : "<<pthread_self()%10000<<" wakes up and is cutting hair of customer - "<<ct<<endl;
		sleep(cutting_time);
		done--;
		cout<<"\nBarber id : "<<pthread_self()%10000<<" is done cutting hair of customer - "<<ct<<endl;
		
		
	}
}
void *customers(void* arg){
		int myseat,br;	
		sem_wait(&chairs);
		cnt++;
		cout<<"\nCustomer - "<<cnt<<" id : "<<pthread_self()%10000<<" Entered barber shop!"<<endl;
		if (Freechairs > 0){
			Freechairs--;
			cout<<"\nCustomer -"<<cnt<<" sits in waiting room!"<<endl;
			sitherenext = (sitherenext+1)%s;
			myseat = sitherenext;
			seat[myseat] = cnt;
			sem_post(&chairs);
			sem_post(&barber);			
			sem_wait(&cust);
			sem_wait(&chairs);
			br = seat[myseat];
			Freechairs++;
			sem_post(&chairs);
			
			
		}else{
			sem_post(&chairs);
			done--;gone++;
			cout<<"\nCustomer - "<<cnt<<" finds no seat and leaves!"<<endl;

		}
		pthread_exit(0);
	
	
}
int main(){
	cout<<"Enter the number of barbers = ";
	cin>>b;
	cout<<"Enter the number of customers = ";
	cin>>c;
	done = c;
	// refers to free seats initially when no customers came 
	//cout<<"Enter the number of chairs = ";
	//cin>>Freechairs;
	cout<<"No of free chairs in shop = "<<s<<endl;

	// initialise the semaphores
	sem_init(&cust,0,0);	
	sem_init(&barber,0,0);
	sem_init(&chairs,0,1);

	pthread_t tid1[b];
	pthread_t tid2[c];
	// creating b barber threads 
	for(int i=0;i<b;i++){
		pthread_create(&tid1[i],NULL,barbers,NULL);
	
	}
	// creating c barber threads 
	for(int i=0;i<c;i++){
		pthread_create(&tid2[i],NULL,customers,(void*)&i);
	
	}
	// joining for sync
	for(int i=0;i<b;i++){
		pthread_join(tid1[i],NULL);
	}
	for(int i=0;i<c;i++){
		pthread_join(tid2[i],NULL);	
	}
	cout<<"\nTotal customers visited the shop = "<<c<<endl;
	cout<<"Customers served = "<<c-gone<<endl;
	cout<<"Customers gone without haircut = "<<gone<<endl;
	cout<<"Barber shop closes!\n";
	sem_destroy(&barber);
	sem_destroy(&cust);
	sem_destroy(&chairs);
		
	return 0;
}
/* YUKTI KHURANA
   2017UCP1234 
*/
