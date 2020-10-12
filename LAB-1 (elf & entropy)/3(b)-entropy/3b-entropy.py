'''Lab Assignment 3(b) - Yukti Khurana'''

# lesser the entropy of a file -> less randomness -> less secure 

import sys 
import math 

# read the whole file into a byte array
filename = sys.argv[1]
f = open(filename, "rb") 
l = f.read()
byteArr = map(ord,l) 
fileSize = len(l)
f.close()
print ("File size in bytes: ",fileSize)

# calculate the frequency of each byte value in the file 
freqList = [] 
for b in range(256): 
    ctr = 0 
    for byte in l:
       if byte == b: 
            ctr += 1 
    freqList.append(float(ctr) / fileSize) 

# Shannon Entropy of a file can be defined as the min avg no of bits per character required for encoding (compressing) the file
entropy = 0.0 
for freq in freqList: 
    if freq > 0: 
        entropy += freq * math.log(freq, 2) 
entropy = -entropy 
print ("Shannon entropy (min bits per byte-character): ",entropy) 

