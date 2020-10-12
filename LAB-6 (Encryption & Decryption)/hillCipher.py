
import numpy as np
import math


l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def matrix(x,y,initial):
	return [[initial for i in range(x)] for j in range(y)]

def transpose(m):
	msize = len(m)
	result = matrix(msize,msize,0)
	for i in range(len(m)):
		for j in range(len(m[0])):
			result[j][i] = m[i][j]
	return result
def getMinor(m,i,j):
	return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getDeterminant(m):
	#base case for 2x2 matrix
	if len(m) == 2:
		return m[0][0]*m[1][1]-m[0][1]*m[1][0]
	d = 0
	for c in range(len(m)):
		d += ((-1)**c)*m[0][c]*getDeterminant(getMinor(m,0,c))
	return d

def multi_inverse(b, n):
    r1 = n
    r2 = b
    t1 = 0
    t2 = 1
    while(r1 > 0):
        q = int(r1/r2)
        r = r1 - q * r2
        r1 = r2
        r2 = r
        t = t1 - q * t2
        t1 = t2 
        t2 = t

        if(r1 == 1):
            inv_t = t1
            break
    return inv_t




def encrypt(pt,key):
	# multiplication of matrix and vector , then mod26 for encryption
	cipher = [0 for i in range(size)]
	#print(cipher)
	for i in range(size):
		for j in range(1):
			for x in range(size):
				cipher[i] = cipher[i] + (keym[i][x] * pt[x])
				cipher[i] %= 26
	#print(cipher)
	c=""
	for i in range(size):
		c+= l[cipher[i]]
	c = c.lower()
	print("CIPHER : ",c)	
	f = open("cipher.dat","w+")
	f.write(c)
	f.close()

	

def decrypt(key):
	# will read the encrypted cipher stored in cipher.dat by the encrypt function
	f = open("cipher.dat","r")
	cipher = f.readline().strip().upper()
	f.close()
	# cipher vector
	c = [0 for i in range(size)]
	for i in range(size):
		c[i] = letters[cipher[i]]
	#print(c)
	# inverse of key
	# ik = inverseMatrix(key)
	 # Inverse matrix
	#ik = inverseMatrix(key)
	#print(ik)
	#ik = inverseMatrix(key)
	
	ik = [[8,5,10],[21,8,21],[21,12,8]]
	km = np.array(key)
	print(km)
	#ik = np.linalg.inv(np.matrix(km))
	#utils.multi_inverse(np.linalg.det(key_matrix), 26) % 26	
	ik = np.linalg.inv(np.matrix(km))*np.linalg.det(km)*multi_inverse(np.linalg.det(km), 26) % 26
	#for i in range(len(ik)):
	#	for j in range(len(ik[0])):
	#		ik[i][j] = int(ik[i][j])


	print("\nInverse Key Matrix: \n", ik)

	"""msg = [0 for i in range(size)]
	# multiplying inverse matrix of key and cipher vector
	for i in range(size):
		for j in range(1):
			for x in range(size):
				msg[i] += (ik[i][x]*c[x])
				msg[i] %= 26

	#print(msg)"""
	message = ""
	result = np.array(np.dot(ik, c))
	for i in range(size):
		message += chr(int(round(result[0][i], 0) % 26 + 65))
	print("\nTHE DECRYPTED TEXT = ",message.lower())
	

def main():
	global letters,size,keym
	letters = dict()
	for i in range(len(l)):
		letters[l[i]] = i
	print("HILL CIPHER ALGORITHM IN COMPUTER SECURITY")	
	f = open("hinput.dat","r")
	pt = f.readline()
	print("Plain Text = ",pt)
	pt = pt.upper()
	size = len(pt)-1
	print("size = ",size)
	# taking input key form file
	key = []
	for i in range(size):
		k = f.readline().strip().upper()
		#print(k)
		key.append(k)
	
	print("key = ",key)
	f.close()
	keym = matrix(size,size,0)
	k=0
	for i in range(size):
		for j in range(size):
			keym[i][j] = letters[key[i][j]]
			k+=1
	ptv = []
	for i in range(size):
		ptv.append(letters[pt[i]])

	while(1):
	    choice = int(input("\n 1.Encryption \n 2.Decryption: \n 3.EXIT\n\n"))
	    if choice == 1:
	    	print("\nEncrypting....\n")	    	
	    	encrypt(ptv,keym)
	    	break
	    elif choice == 2:
	    	print("\nDecrypting....\n")
	    	decrypt(keym)
	    	break
	    elif choice == 3:
	    	print("\nTHANK YOU")
	    	exit()
	    else:
	    	print("\nChoose correct choice\n")



main()	        