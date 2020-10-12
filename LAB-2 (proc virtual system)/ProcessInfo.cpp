#include <bits/stdc++.h>
using namespace std;

// 4(c)

int main(int argc, char **argv) {
   
    string pid = argv[1];
    string file1 = "/proc/"+pid+"/cmdline";   
   
    ifstream f;
    f.open(file1);
    string cmdLine;
    while (f) {   
        getline(f, cmdLine);
        cout<<"The commandline with which the process was started = "<<cmdLine<<endl;
        break;      
    
    }   
    f.close();
    cout<<"\nProcess statistics : "<<endl;      
    f.open("/proc/stat");
    string line;
    while(f){
	getline(f, line);
	int c = line.find("cpu");
	if(c==string::npos)
		break;
	cout<<line<<endl;
    }
    f.close();
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
    cout<<"Time spent in user mode: "<<userTime*100/totalTime<<" %"<<endl;
    cout<<"Time spent in kernel mode: "<<kernelTime*100/totalTime<<" %"<<endl;
    cout<<"Idle time spent: "<<idleTime*100/totalTime<<" %"<<endl;
      
    string file2 = "/proc/"+pid+"/schedstat";     
    string cputime,waitingtime,timeslices;
    ifstream f2;
    f2.open(file2);
    f2>>cputime>>waitingtime>>timeslices;
    cout<<"\nProcess with pid "<<pid<<endl;
    cout<<"CPU Time spent by process  = "<<pid<<cputime<<" seconds"<<endl;
    cout<<"Waiting time of the process =  "<<waitingtime<<" seconds"<<endl;
    cout<<"Number of time slices run on this cpu = "<<timeslices<<endl;
    f2.close();
    
    cout<<"\nThe ENVIRONMENT of the process : "<<endl;
    string file3 = "/proc/"+pid+"/environ";
    ifstream f3;
    f3.open(file3);
    string env;
    while(f3){
    	getline(f3,env);
    	cout<<env<<endl;
    }
    cout<<endl<<env<<endl<<endl; 
    f3.close();   

    return 0;
   
}

