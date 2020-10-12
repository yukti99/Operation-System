
letters = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

def generatePlayfairMatrix(key):
	m = matrix(5,5,0)
	unique_key=""
	for i in key:
		if i not in unique_key:
			unique_key+=i
	#print(unique_key)
	pf = unique_key
	for i in letters:
		if i not in unique_key:
			pf+=i
	#print(pf)
	k=0
	for i in range(5):
		for j in range(5):
			m[i][j] = pf[k]
			k+=1
	return m


	
def matrix(x,y,initial):
	return [[initial for i in range(x)] for j in range(y)]
def getLocation(m,c):
	for i in range(5):
		for j in range(5):
			if c == m[i][j]:
				return (i,j)
	return (-1,-1)

def encrypt(pt,key):	
	#print(pt,key)
	message = pt
	Key = key
	# if plaintext contains J,  it is replaced by I
	c = pt.count("J",0,len(pt)-1)
	pt = pt.replace("J","I",c)
	c = key.count("J",0,len(pt)-1)
	key = key.replace("J","I",c)
	
	# creating playfair matrix
	m = generatePlayfairMatrix(key)
	#print(m)
	pt = pt.strip()
	# splitting plaintext into characters of two 
	if (len(pt)%2 != 0):
		pt = pt+'Z' # for odd length plaintext, we add a Z to make pairs
	spt = [(pt[i:i+2]) for i in range(0,len(pt),2)]
	#print(spt)
	cipher = ""
	# encryption using playfair matrix
	for i in spt:
		i = str(i)
		#print("i = ",i)
		x,y = i[0],i[1]
		xr,xc = getLocation(m,x)
		yr,yc = getLocation(m,y)
		# if same column
		if (xc == yc):
			cipher += m[(int(xr)+1)%5][xc]
			cipher += m[(int(yr)+1)%5][yc]
			#print("cipher = ",cipher)
		# if same row
		elif (xr == yr):
			cipher += m[xr][(int(xc)+1)%5]
			cipher += m[yr][(int(yc)+1)%5]
			#print("cipher = ",cipher)
		# neither follows
		else:
			# for rectangle and take horizontal opposites of the rect
			cipher += m[xr][yc]
			cipher += m[yr][xc]
			#print("cipher = ",cipher)
	cipher = cipher.lower()
	print("\nCIPHER : ",cipher,"\n")
	f = open("cipher.dat","w+")
	f.write(cipher)
	f.close()

def decrypt(key):
	# will read the encrypted cipher stored in cipher.dat by the encrypt function
	f = open("cipher.dat","r")
	cipher = f.readline().strip().upper()
	c = cipher
	m = generatePlayfairMatrix(key)
	#print(m) 
	# splitting ciphertext into characters of two 
	sc = [(c[i:i+2]) for i in range(0,len(c),2)]
	#print(sc)
	# decryption using playfair matrix
	message = ""
	for i in sc:
		i = str(i)
		#print("i = ",i)
		x,y = i[0],i[1]
		xr,xc = getLocation(m,x)
		yr,yc = getLocation(m,y)
		# if same column
		if (xc == yc):
			message += m[(int(xr)-1)%5][xc]
			message += m[(int(yr)-1)%5][yc]
			
		# if same row
		elif (xr == yr):
			message += m[xr][(int(xc)-1)%5]
			message += m[yr][(int(yc)-1)%5]
			
		# neither follows
		else:
			# for rectangle and take horizontal opposites of the rect
			message += m[xr][yc]
			message += m[yr][xc]
	print("THE DECRYPTED TEXT = ",message.lower())

def main():
	print("PLAYFAIR CIPHER ALGORITHM IN COMPUTER SECURITY")	
	f = open("einput.dat","r")
	pt = f.readline().upper()
	key = f.readline().upper()	
	f.close()

	while(1):
	    choice = int(input("\n 1.Encryption \n 2.Decryption: \n 3.EXIT\n\n"))
	    if choice == 1:
	    	print("\nEncrypting....\n")	    	
	    	encrypt(pt,key)
	    	break
	    elif choice == 2:
	    	print("\nDecrypting....\n")
	    	decrypt(key)
	    	break
	    elif choice == 3:
	    	print("\nTHANK YOU")
	    	exit()
	    else:
	    	print("\nChoose correct choice\n")



main()	        