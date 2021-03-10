/*
YUKTI KHURANA
2017UCP1234

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



int N=0;
struct Node{
	int data;
	struct Node* next;
};
struct Node* slist = NULL;



void search(int no){	
	int item = rand()%100;
	printf("\nI AM SEARCHER-%d Searching for %d...\n",no,item);
	int f=0;
	struct Node* temp = slist;
	while(temp!=NULL){
		if (item == temp->data){
			f=1;
			printf("Element %d found in list!\n",item);
		}
		temp = temp->next;
	
	}
	if (f == 0)
		printf("Element %d not found in list!\n",item);

}
void print(){
	printf("LIST : \n");
	struct Node* n = slist;
	if (n == NULL)printf("List is empty!\n");
	while(n!=NULL){
	printf("%d ",n->data);
	n = n->next;
	}
	printf("\n");

}
void insert(int no){
	printf("\nI AM INSERTER-%d! \n",no);
	struct Node* n = (struct Node*)malloc(sizeof(struct Node));
	struct Node* last = slist;
	n->data = rand()%100;
	n->next = NULL;
	if (NULL == slist){
		printf("Inserting first element %d!\n",n->data);
		slist = n;
		print();
		return ;
	}
	while(NULL!=last->next){
		last = last->next;
	}
	last->next = n;
	printf("Inserted %d at the end of the list\n",n->data);
	print();
	
}

void Delete(int no){
	printf("\nI AM DELETER-%d !\n",no);
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
		print();
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
	print();
	
}

sem_t noSearch; // to signal deleter that no searching is taking place 
sem_t noInsert; // to signal deleter that no insertion is taking place 
sem_t searchMutex, insertMutex; // to protect shared variable noSearchers and noInserters
sem_t ins_Sem; // to  provide mutual exclusion between two inserters
sem_t del;
int noSearchers = 0; // to keep a count of searchers
int noInserters = 0; // to keep a count of inserters

// searcher process (only examines the list)
void* Searcher(void* no){
	int sno = *(int *)no;
	while(1){
		sem_wait(&searchMutex);
			noSearchers++;
			if (noSearchers == 1){
				sem_wait(&noSearch); // signal to deleters that a searcher has entered CS
			}
		sem_post(&searchMutex);
			search(sno); // multiple searches can occur simultaneously so no need to lock this CS
		sem_wait(&searchMutex);
			noSearchers--;
			if (noSearchers == 0){
				sem_post(&noSearch); // signal to deleters that all searchers are out of CS
			}
		sem_post(&searchMutex);
		sleep(2);
	}
	
}

// inserter process (inserts element at the end of the list)
void* Inserter(void* no){
	int ino = *(int*)no;
	while(1){
		sem_wait(&insertMutex);
			noInserters++;
			if (noInserters == 1){
				sem_wait(&noInsert); // signal to deleters that a inserter has entered CS
			}
		sem_post(&insertMutex);
		
			sem_wait(&ins_Sem);
				insert(ino); // CS locked to provide mutual exclusion between two inserters
			sem_post(&ins_Sem);
			
		sem_wait(&insertMutex);
			noInserters--;
			if (noInserters == 0){
				sem_post(&noInsert); // signal to deleters that all inserters are out of CS
			}
		sem_post(&insertMutex);		
		sleep(2);
	}	
	
}
// deleter process (removes element from anywhere in the list)
void* Deleter(void* no){
	int dno = *(int*)no;
	while(1){
		sem_wait(&noSearch); // wait for signal from searcher
			sem_wait(&noInsert);// wait for signal from inserter 
				sem_wait(&del);
					Delete(dno);
				sem_post(&del);
			sem_post(&noInsert);
		sem_post(&noSearch);
		sleep(2);
	}	
}


int main(){
	int s,in,d;
	printf("Enter the number of searchers, inserters and deleters = ");
	scanf("%d %d %d",&s,&in,&d);
	
	srand(time(0));
	// creating threads for all three processes 
	pthread_t inserter[in],deleter[d],searcher[s];
	
	// INTIALISING THE SEMAPHORES 
	sem_init(&noSearch,0,1);
	sem_init(&noInsert,0,1);
	sem_init(&ins_Sem,0,1);
	sem_init(&searchMutex,0,1);
	sem_init(&insertMutex,0,1);
	sem_init(&del,0,1);
	
	int ser[s], ins[in], dele[d];
	for(int i=0;i<s;i++){
		ser[i] = i;
	}
	for(int i=0;i<in;i++){
		ins[i] = i;
	}
	for(int i=0;i<d;i++){
		dele[i] = i;
	}
	
	
	// THREADS CREATION
	for(int i=0;i<s;i++){
		pthread_create(&searcher[i],NULL,&Searcher,(void*)&ser[i]);
	}
	for(int i=0;i<in;i++){
		pthread_create(&inserter[i],NULL,&Inserter,(void*)&ins[i]);
	}
	for(int i=0;i<d;i++){
		pthread_create(&deleter[i],NULL,&Deleter,(void*)&dele[i]);
	}
	
	//joining threads for synchronisation
	
	for(int i=0;i<s;i++){
		pthread_join(searcher[i], NULL);
	}
	for(int i=0;i<in;i++){
		pthread_join(inserter[i], NULL);
	}
	for(int i=0;i<d;i++){
		pthread_join(deleter[i], NULL);
	}

	return 0;
}

/*
YUKTI KHURANA
2017UCP1234

*/

