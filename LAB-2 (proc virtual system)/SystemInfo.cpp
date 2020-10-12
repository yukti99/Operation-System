#include <bits/stdc++.h>
#include <unistd.h> 
#include <pthread.h>
using namespace std;

void *currentMem(void *vargp);
long long int arr[16];
int readrate=0;
int outrate=0;
int t;

int main(int argc, char **argv){
	t=0;
    	cout<<"******************************REALTIME CHANGING VALUES ACCORDING TO READ AND OUT RATE************************************"<<endl;
 	arr[16] = {};
	long long int value = 0;
	int n=1;
	string a,b,c,line;
	ifstream f,f1;
	pthread_t thread_id;
	pthread_create(&thread_id, NULL, currentMem, NULL); 
	int swapPart=0;
	readrate = stoi(argv[1]);
	outrate = stoi(argv[2]);
	
	int timeinsecofread = outrate;
	while(1){	
		f.open("/proc/meminfo");
		while(f){	
			getline(f, line);  	
		        f>>a>>b>>c; 
			if(a == "MemAvailable:"){
				stringstream obj(b);
				obj>>value;
				// calculating the average of realtime changing values
				arr[0] = (arr[0]*(n-1) + value)/n;
			}
			else if(a == "MemFree:"){	 
				stringstream obj(b);
				obj>>value;				
				// calculating the average of realtime changing values
				arr[1] = (arr[1]*(n-1) + value)/n;
				
			
			}
			else if( a == "SwapTotal:"){
				stringstream obj(b);
				obj>>value;				
				// calculating the average of realtime changing values
				swapPart++;
				arr[2] = (arr[2]*(n-1) + value)/n;
				arr[7] = swapPart;
			
			}
			else if(a == "SwapFree:"){			
				stringstream obj(b);
				obj>>value;
				// calculating the average of realtime changing values
				arr[3] = (arr[3]*(n-1) + value)/n;			

			}
			n++;	
			
			
		}
		f.close();
		// now to print the realtime statistics
		f1.open("/proc/stat");	
		int j=0,cs=0,t1=0;
		while(f1){
			getline(f1,line);
			f1>>a>>b;
			//int g = a.find("ctxt");
			//if (g!=string::npos){
			if (a=="ctxt"){
				cs++;
				stringstream obj(b);
				obj>>value;
				arr[10] = (arr[10]*(cs-1) + value)/cs;	
				//break;
			
			}
			if (a=="processes"){
			
				t1++;
				stringstream obj(b);
				obj>>value;
				arr[11] = ((arr[11]*(t1-1)+value)/t1);
				arr[12] = arr[11]/t;
			}
		}
		f1.close();
		f1.open("/proc/stat");
		while(f1){
			getline(f1, line);
			int c = line.find("cpu");
			if(c!=string::npos)
				break;
		}
		
		string intr;
		while(f1){
			getline(f1,intr);
			int b = intr.find("intr");
			if (b!=string::npos)
				break;
		
		}
		j++;
		int i = stoi(intr.substr(5,13));
		arr[8] = (arr[8]*(j-1) + i)/j;
		 //"<<intr[5]<<intr[6]<<intr[7]<<intr[8]<<intr[9]<<intr[10]<<intr[11]<<intr[12]<<endl;
		f1.close();
		
		int b =line.find(" ", 5);
          	float userTime=stoi(line.substr(5, b-5));
    		float kernelTime,idleTime;
    		int c=line.find(" ", b+1);
    		userTime+=stoi(line.substr(b+1, c-b-1));
    		b=c;
    		c=line.find(" ", b+1);
    		kernelTime+=stoi(line.substr(b+1, c-b-1));
    		b=c;
    		c=line.find(" ", b+1);
    		idleTime+=stoi(line.substr(b+1,c-b-1));
    		float totalTime = userTime+kernelTime+idleTime;
    		arr[4] = userTime*100/totalTime;
    		arr[5] = kernelTime*100/totalTime;
    		arr[6] = idleTime*100/totalTime;  
    		
    		f1.open("/proc/loadavg");
		getline(f1, line); 
		int last15 = stoi(line.substr(22,26));
		arr[13] = (arr[13]*(j-1)+last15)/j;
		
		f1.close();
		
		f1.open("/proc/diskstats");
		int rw=0;
		while(f1){
			getline(f1, line); 
			if (rw==4){
				value = stoi(line.substr(19,4));
				//cout<<"reads completed successfully = ";
				arr[14] = (arr[14]*(j-1)+value)/j;
				
			}
			if (rw==5){
				//cout<<"writes completed successfully = ";
				value = stoi(line.substr(18,3));
				arr[15] = (arr[15]*(j-1)+value)/j;
				
				break;			
			}
			rw++;
		
		}		
		
		f1.close();
		
		
		
		t+=timeinsecofread;	   		
		sleep(timeinsecofread); // or 2 (default)
		
		
		
	}
	// for sync
	pthread_join(thread_id, NULL);
	exit(0); 
}

void *currentMem(void *vargp){ 
	while(1){
		int timeinsecofsleep = outrate;
		t+=outrate;
		sleep(timeinsecofsleep); // or 4(default)
		cout<<"-----------------------------------------------------------\n";		
		cout<<"Total Memory Available (kBs) = "<<arr[0]<<endl;
		cout<<"Usable Free Memory (kBs) = "<<arr[1]<<endl;
		cout<<"Total Swap Space (kBs) = "<<arr[2]<<endl;
		cout<<"Used Swap Space (kBs) = "<<arr[2]-arr[3]<<endl;
		cout<<"Free Swap Space (kBs) = "<<arr[3]<<endl;
		cout<<"Total swap partitions: "<<arr[7]<<endl;
		cout<<"Time spent in user mode (s) = "<<arr[4]<<" %"<<endl;
		cout<<"Time spent in kernel mode =  "<<arr[5]<<" %"<<endl;		
		cout<<"CPU Idle time spent = "<<arr[6]<<" %"<<endl;
		cout<<"Total no of context switches = "<<arr[10]<<endl;
		cout<<"Current processes running = "<<arr[11]<<endl;
		cout<<"Rate of process creation in the system (no/sec) = "<<arr[12]<<endl;		
		cout<<"No of interrupts handled by the system since boot = "<<arr[8]<<endl;
		cout<<"No of reads completed successfully = "<<arr[14]<<endl;
		cout<<"No of writes completed successfully = "<<arr[15]<<endl;
		cout<<"Load on system for last 15 minutes = "<<arr[13]<<endl<<endl;
		cout<<"-----------------------------------------------------------\n";		
	}
	return NULL; 
} 


