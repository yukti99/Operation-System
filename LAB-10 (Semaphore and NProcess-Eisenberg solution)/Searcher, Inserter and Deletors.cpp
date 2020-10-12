/*
Ques 3(a)
SINGLY LINKED LIST
Three kinds of threads share access to a singly linked list; searchers, inserters and deleters. It is known that Searchers merely examine the list; hence they can execute concurrently with each other.Inserters add new elements at the end of the list; insertions must be mutually exclusive to preclude two inserters from inserting new elements at the same time. However one insert can proceed in parallel with any number of searches. Finally, deleters remove elements from anywhere in the list. At most one deleter process can access the list at a time, and deletion must also be mutually exclusive with searches and insertions. Write pseudocode using semaphores to provide a solution to this problem  
*/

#include <bits/stdc++.h>
#include <thread>
#include <stdlib.h>
#include <semaphore.h>
#include <random>
#include <unistd.h>
using namespace std;

#define p 5

int N=0;
struct Node{
	int data;
	struct Node* next;
};
struct Node* slist = NULL;



// declaring semaphores
sem_t insert_mutex; // so that only one inserter is in its cs
sem_t ser,ins;  // to exclude deleters 
sem_t no_search, no_insert; // indicate no searcher or inserter in cs

void search(){
	printf("\nI AM SEARCHER!\n");
		struct Node* n = slist;
		if (n == NULL)printf("List is empty!\n");
		while(n!=NULL){
			printf("%d ",n->data);
			n = n->next;
		}
		printf("\n");

}
void insert(){
	printf("\nI AM INSERTER!\n");
	struct Node* n = (struct Node*)malloc(sizeof(struct Node));
	struct Node* last = slist;
	n->data = rand()%100;
	n->next = NULL;
	if (NULL == slist){
		printf("Inserting first element %d!\n",n->data);
		slist = n;
		return ;
	}
	while(NULL!=last->next){
		last = last->next;
	}
	last->next = n;
	printf("Inserted %d at the end of the list\n",n->data);
	
}

void Delete(){
	printf("\nI AM DELETER!\n");
	struct Node* temp = slist;
	if (slist==NULL || slist->next == NULL){
		slist = NULL;
		printf("Nothing deleted as list empty!\n");
		return;
	}
	int size=0;
	while(temp!=NULL){
		temp = temp->next;
		size++;
	}
	temp = slist;
	int randomPos = rand()%size;
	printf("random position = %d\n",randomPos);
	int x=-1;
	if (randomPos == 0){
		x = temp->data;
		slist = temp->next;			
		free(temp);
		printf("Deleted %d from list!\n",x);
		return ;
	}
	int c=0;	
	while(c!=randomPos-1){
		temp = temp->next;
		c++;
	}
	struct Node* n = temp->next->next;
	x = temp->next->data;
	free(temp->next);
	temp->next = n;
	printf("Deleted %d from list!\n",x);
	
}
// searcher process (only examines the list)
void* Searcher(void* arg){
	while(1){
		sem_wait(&ser); // only needs to worry about deleter 
			search();
		sem_post(&ser);
		sleep(1);
	}
	
}

// inserter process (inserts element at the end of the list)
void* Inserter(void* arg){
	while(1){
		sem_wait(&ins);
			//sem_wait(&ser);
				insert();
			//sem_post(&ser);
		sem_post(&ins);
		sleep(1);
	}
	
	
}
// deleter process (removes element from anywhere in the list)
void* Deleter(void* arg){
	while(1){
		sem_wait(&ins);
			sem_wait(&ser);
				Delete();
			sem_post(&ser);
		sem_post(&ins);
		sleep(1);
	}	
	
}


int main(){
	srand(time(0));
	// creating threads for all three processes 
	pthread_t inserter[p],deleter[p],searcher[p];
	
	// INTIALISING THE SEMAPHORES 
	//sem_init(&del,0,1);
	sem_init(&ins,0,1);
	sem_init(&ser,0,1);
	//sem_init(&full,0,0);
	
	// THREADS CREATION
	for(int i=0;i<p;i++){
		pthread_create(&searcher[i],NULL,&Searcher,NULL);
	}
	for(int i=0;i<p;i++){
		pthread_create(&inserter[i],NULL,&Inserter,NULL);
	}
	for(int i=0;i<p;i++){
		pthread_create(&deleter[i],NULL,&Deleter,NULL);
	}
	
	//joining threads for synchronisation
	
	for(int i=0;i<p;i++){
		pthread_join(searcher[i], NULL);
	}
	for(int i=0;i<p;i++){
		pthread_join(inserter[i], NULL);
	}
	for(int i=0;i<p;i++){
		pthread_join(deleter[i], NULL);
	}

	return 0;
}

