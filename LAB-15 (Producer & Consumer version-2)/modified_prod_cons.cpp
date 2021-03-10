// Producer and Consumer Problem using semaphores and threads
// 2017ucp1234, Yukti Khurana 

// compile using:
// g++ filename.cpp -lpthread 

// both producers working fine
#include <bits/stdc++.h>
#include <semaphore.h>
#include <random>
#include <unistd.h>
#include <pthread.h>
using namespace std;

#define buffer_size 6
#define prod_no 2
#define cons_no 2

// repectuve index for consumer and producers
int idp=0, idc=0;
int buf[buffer_size];


// declaring semaphores for cs solution 
sem_t empty, full, mutex1;

bool p2_wait = false;
bool c2_wait = false;


void display_buffer(){
	cout<<"\n------BUFFER-----------------------------------------------\n";
	for(int i=0;i<buffer_size;i++){
		cout<<buf[i]<<" ";
	}
	cout<<"\n-----------------------------------------------------------\n";
}


// using semaphore solution for critical section problem  

void *Producer1(void *no){
	while(1){
		
		sem_wait(&empty); // waiting on empty buffer 
		sem_wait(&mutex1); // lock the cs
			// critical section
			cout<<"p2_wait = "<<p2_wait<<endl;
			if (p2_wait==true){
				// if producer-2 has pending task then producer-1 will relinquish the cs
				cout<<"Producer-1 has to wait for producer2..."<<endl;
				sem_post(&mutex1);		
			
				
				
			} 
			else{
				// no waiting required
				if (buf[idp]==-1){
					int item = rand()%100;
					buf[idp] = item;
					cout<<"\nProducer - "<<1<<" Produced :  "<<item<<" at position = "<<idp<<endl<<endl;
					idp = (idp+1)%buffer_size;
					display_buffer();
				}	
			
				sem_post(&mutex1);		
				sem_post(&full);
				
			}	
			
	sleep(2);
	}
	

}
// can produce two items at once 
void *Producer2(void *no){
	
	while(1){
		sem_wait(&empty); // waiting on empty buffer 
		sem_wait(&mutex1); // lock the cs
		if (p2_wait == true){
					
					if (buf[idp]==-1){
					        cout<<"Producer-2 will now complete its pending job..."<<endl<<endl;
					       
						// there is space in buffer so no need to wait 
						int item2 = rand()%90;
						buf[idp] = item2;								
						cout<<"\nProducer - "<<2<<" Produced item2 :  "<<item2<<" at position = "<<idp<<endl<<endl;
						idp = (idp+1)%buffer_size;
						display_buffer();
						cout<<"Producer-"<<2<<" completed its pending job and is leaving the cs!!"<<endl<<endl;
						p2_wait = false;
						sem_post(&mutex1);
						sem_post(&full);
						
											
					}
					else{
						// p2 was waiting
						cout<<"Producer-2 waiting.... for idp = "<<idp<<endl<<endl;
						sem_post(&mutex1);
						
					}					
					
							
						
					
		}else{		
		
			// critical section 
			if (buf[idp]==-1){
				
								
					int item1 = rand()%100;
					buf[idp] = item1;
					cout<<"\nProducer - 2 Produced item1 :  "<<item1<<" at position = "<<idp<<endl<<endl;
					idp = (idp+1)%buffer_size;
					display_buffer();
					cout<<"idp now = "<<idp<<endl;			
				
								
					if (buf[idp] == -1){
						// there is space in buffer so no need to wait 
						int item2 = rand()%90;
						buf[idp] = item2;								
						cout<<"\nProducer - "<<2<<" Produced item2 :  "<<item2<<" at position = "<<idp<<endl<<endl;
						idp = (idp+1)%buffer_size;
						display_buffer();
						sem_post(&mutex1);		
						sem_post(&full);
						
						
							
						
						
					}else{
						cout<<"Producer-2 could not find more space..."<<endl;
						// producer-2 has to wait 
						p2_wait = true;
						sem_post(&mutex1); // release the lock 		
						
						
							
									
					}
				
				
				
				
			}else{    sem_post(&mutex1);}  
		}	
		
	
	sleep(2);
		
	}

}

void *Consumer1(void *no){
	while(1){
		
		sem_wait(&full); // waiting on empty buffer 
		sem_wait(&mutex1); // lock the cs
			// critical section
			cout<<"c2_wait = "<<c2_wait<<endl;
			if (c2_wait==true){
				// if consumer-2 has pending task then consumer-1 will relinquish the cs
				cout<<"Consumer-1 has to wait for Consumer-2..."<<endl;
				sem_post(&mutex1);							
				
			} 
			else{
				// no waiting required
				if (buf[idc]!=-1){
					int item = buf[idc];
					buf[idc] = -1;
					cout<<"\nConsumer - 1 consumed :  "<<item<<" at position = "<<idc<<endl<<endl;
					idc = (idc+1)%buffer_size;
					display_buffer();
				}	
			
				sem_post(&mutex1);		
				sem_post(&empty);
				
			}	
			
	sleep(3);
	}
	
}


void *Consumer2(void *no){
	while(1){
		sem_wait(&full); // waiting on full buffer
		sem_wait(&mutex1); // lock the cs
		if (c2_wait == true){
					
					if (buf[idc]!=-1){
					        cout<<"Consumer-2 will now complete its pending job..."<<endl<<endl;
					       
						//  no need to wait 
						
						int item2 = buf[idc];
						buf[idc] = -1;
						cout<<"\nConsumer - 2 consumed : item2: "<<item2<<" at position = "<<idc<<endl<<endl;
						idc = (idc+1)%buffer_size;
						display_buffer();						
						
						cout<<"Consumer-2 completed its pending job and is leaving the cs!!"<<endl<<endl;
						c2_wait = false;
						sem_post(&mutex1);
						sem_post(&empty);
						
											
					}
					else{
						// c2 was waiting
						cout<<"Consumer-2 waiting.... for idc = "<<idc<<endl<<endl;
						sem_post(&mutex1);
						
					}					
					
							
						
					
		}else{		
		
			// critical section 
			if (buf[idc]!=-1){
			
					int item1 = buf[idc];
					buf[idc] = -1;
					cout<<"\nConsumer - 2 consumer :  "<<item1<<" at position = "<<idc<<endl<<endl;
					idc = (idc+1)%buffer_size;
					display_buffer();
					cout<<"idc now = "<<idp<<endl;	
						
				
								
					if (buf[idc] != -1){
						
						
						int item2 = buf[idc];	
						buf[idc]  = -1;							
						cout<<"\nConsumer - 2 consumed item2 :  "<<item2<<" at position = "<<idp<<endl<<endl;
						idc = (idc+1)%buffer_size;
						display_buffer();
						sem_post(&mutex1);
						sem_post(&empty);

						
					}else{
						cout<<"Consumer-2 could not find more data..."<<endl;
						c2_wait = true;
						sem_post(&mutex1); // release the lock 		
						
						
							
									
					}
				
				
				
				
			}else{    sem_post(&mutex1);} 
		}	
		
	
	sleep(3);
		
	}
	
	
}


	





int main(){
	srand(time(NULL));
	cout<<"\n\nWelcome to Producer and Consumer Problem Solution!\n\n"<<endl;
	
	// initialising the semaphores used
	sem_init(&empty,0, buffer_size);
	sem_init(&full,0,0);
	sem_init(&mutex1,0, 1); // lock on critical section
	
	for(int i=0;i<buffer_size;i++){
		buf[i] = -1;
	}
	cout<<"Initial Buffer is empty with all -1's"<<endl;
	display_buffer();
	
	int producers[prod_no], consumers[cons_no];
	// for getting ids of producers and consumers
	for(int i=0;i<prod_no;i++){
		producers[i] = i;
	}
	
	for(int i=0;i<cons_no;i++){
		consumers[i] = i;
	}
	
	
	// create threads for different processes
	pthread_t tid1[prod_no], tid2[cons_no], prodid[2], consid[2];
	int p1[1], p2[1], c1[1], c2[1];
	p1[0] = 1;
	p2[0] = 2;
	c1[0] = 1;
	c2[0] = 2;
	
	// creating total four threads, producer1, producer 2, consumer-1 and consumer-2
	
	pthread_create(&prodid[0], NULL, Producer1, (void*)&p1[0]);
	pthread_create(&prodid[1], NULL, Producer2, (void*)&p2[0]);
	
	pthread_create(&consid[0], NULL, Consumer1, (void*)&c1[0]);
	pthread_create(&consid[1], NULL, Consumer2, (void*)&c2[0]);
	
	
	// joining threads for synchronisation
	for(int i=0;i<2;i++){
		pthread_join(prodid[i], NULL);
	}
	for(int i=0;i<2;i++){
		pthread_join(consid[i], NULL);
	}
	

	
	return 0;
}


