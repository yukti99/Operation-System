Programming Language: C/C++

The OS (aka Linux) is a program that uses various data structures. Like all programs in execution, you can determine the performance and other behaviour patterns of the OS by inspecting its states - the values stored in its various data structures. In this part of the assignment, you are to study some aspects of the organization and behaviour of a Linux system by observing values of kernel data structures exposed through the /proc virtual file system. 

Linux uses the /proc file system to collect information from kernel data structures. The /proc implementation provided with Linux can read many different kernel data structures. If you cd to /proc on any Linux machine, you will see a number of files and directories at that location. Each of the Files in this directory subtree corresponds to some kernel data structure. The subdirectories with numeric names contain virtual files with information about the process whose Process ID is the same as the directory name. Files in /proc can be read like ordinary ASCII text files. You can open each file and read it using library routines such as fgets() or fscanf(). The proc (5) manual page explains the virtual files and their content available through the /proc file system. 


Program Specifications

In this assignment, you will write a program (shall consist of a number of C files) to report the behaviour of the Linux kernel.
 Your program should be compiled as ProcInfo and run in three different modes. 
The default version should print the information as specified in 2(a). Second version should print, at intervals, information specifed in 2(b). 
And in third version, it should print information about a  process as described in 2(c). All values should be printed on stdout:  

Following are the command lines for three versions
ProcInfo
ProcInfo <read_rate> <out_rate>
ProcInfo Process <pid>

Assignment 4(a):   C File name “MachineInfo.c”.In this file, you will write a program to report the behaviour of the Linux kernel and print following information

Processor type
The number of CPUs in your machine and their clock speed, number of cores.
The version of Linux kernel running on your system
The amount of memory configured into this computer
Amount of time since the system was last booted (day:hr:min:sec format)



Assignment 4(b):  File name “SystemInfo.c”

Code for this part should be in SystemInfo.c. When run in this mode, the program should run continuously and print lists of the following dynamic values (each value in the lists is the average over a specified interval): 
The percentage of time the processor(s) spend in user mode, system mode, and the percentage of time the processor(s) are idle
The amount and percentage of available (or free) memory
The total usable and currently free memory in the system
The total swap space and the currently used swap space in the system
The swap partitions and their sizes
The average load on the system in the last 15 minutes
The number of context switches made by the system so far
The number of interrupts handled by the system so far
The rate (number of blocks per second) of disk read/write in the system
The rate (number per second) of context switches in the kernel
The rate (number per second) of process creations in the system
If your program (compiled executable) is called ProcInfo, running it without any parameter should print out information required for the first version. Running it with two parameters "ProcInfo <read_rate> <out_rate>" should print out information required for the second version. read_rate represents the time interval between two consecutive reads on the /proc file system. out_rate indicates the time interval over which the average values should be calculated. Both read_rate and out_rate are in seconds. 

For instance, ProcInfo 2 60 should read kernel data structures once every two seconds. It should then print out averaged kernel statistics once a minute (average of 30 samples). The second version of your program doesn't need to terminate. 

Assignment 4(c):  File name “ProcessInfo.c”
You have to write code for this part in ProcessInfo.c that will read the /proc file system and gets the following information specific to a process. The program takes the pid of the process as a command line argument.
The command line with which the process was started
The time spent by the process in running and in waiting
The time spent by the process in the user mode, kernel mode
The environment of the process
The contents of the address space of the process
In order to answer the above questions, the files of the /proc filesystem that will be relevant for you are cpuinfo, uptime, loadavg, cmdline, stat, meminfo, mem, schedstat, maps. 
Some of these files will be under /proc directly, some will be under the directory for the specific process, and some will be under both.
 You will need to read and understand what is contained in these files from the net and implement the above program. 
Note that the exact format of the files vary somewhat between different versions of Linux, so you should try to write your program in as format-independent manner as possible (the names of things are mostly standard).


