#include <bits/stdc++.h>
using namespace std;

// 4(a) Processor type,no of cpus and their clock speed, no of cores,version of kernel linux,amount of memory, amount of time since last reboot

int main(int argc, char **argv){
	ifstream f1;
	// using proc/stat file    
	string file1 = "/proc/stat";  
	f1.open(file1);
	string s;
	cout<<"-------------------------------------------------------------------------------------------------"<<endl;
	cout<<"Number of CPU's :"<<endl;
	while(f1){
		getline(f1,s);
	    	cout<<s<<endl;
	}	    
	f1.close(); 
	cout<<endl<<endl;	
	string line; 
	ifstream f2; 
	// using cpuinfo file from /proc
	f2.open("/proc/cpuinfo");
	int processors=0,cpu_cores;
	string processor_type="",clock_speed="";
	while (f2) { 
		getline(f2, line);
		int p = line.find("processor");
		if(p!=string::npos)
			processors++;
		if(cpu_cores==0){
			p=line.find("cpu cores");
			if(p!=string::npos){
				cpu_cores=(int)(line[12]-'0');
			}
		}
		if(clock_speed==""){
			p=line.find("model name");
			if(p!=string::npos){
				clock_speed=line.substr(46);
			}
		}
		if(processor_type==""){
			p=line.find("model name");
			if(p!=string::npos){
				processor_type=line.substr(13);
			}
		}

		// Print line in Console 
	} 
	cout<<"-------------------------------------------------------------------------------------------------"<<endl;
	cout<<"-------------------------------------------------------------------------------------------------"<<endl;
	cout<<"Processor type =  "<<processor_type<<endl;
	cout<<"Number of processors = "<<processors<<endl;
	cout<<"Number of cpu cores = "<<cpu_cores<<endl;
	cout<<"clock speed in MHz: "<<clock_speed<<endl;		
	f2.close();
	// using version file for kernel version
	f2.open("/proc/version");
	string version;
	getline(f2, line);
	int f = line.find("version");
	int end = line.find("(");
	version=line.substr(f+8, end-f-9);
	cout<<"linux kernel version: "<<version<<endl;
	f2.close();	
	// using uptime file 
	f2.open("/proc/uptime");
	getline(f2, line);
	f2.close();
	f=line.find(" ");
	string time = line.substr(0, f);
	float tsec= std::stof(time);
	int days, hour, minute, sec;
	days=(int)(tsec/86400);
	tsec=tsec-days*86400;
	hour=(int)(tsec/3600);
	tsec-=hour*3600;
	minute=(int)(tsec/60);
	tsec-=minute*60;
	sec=tsec;
	cout<<"Time from last reboot"<<days<<" days "<<hour<<" hours "<<minute<<" minutes "<<sec<<" seconds "<<endl;
	// using meminfo file
	cout<<"-------------------------------------------------------------------------------------------------"<<endl;
	cout<<"-------------------------------------------------------------------------------------------------"<<endl;
	cout<<endl<<endl<<"Memory related information : "<<endl;
	f2.open("/proc/meminfo");	
	while(f2){
		getline(f2, line);
		cout<<line<<endl;
	}
	f2.close();
	
   	return 0;
}


