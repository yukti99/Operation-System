
def textToBytes(x):
	b = []
	for i in x:
		b.append(ord(str(i)))
	return b
def hexToBytes(x):
	b = []
	for i in range(0,len(x),2):
		byte = x[i:i+2]
		b.append(int('0X'+byte,16))
	return b
def bytesToHex(x):
	t=""
	for i in x:
		h = "0"+hex(i)[2:]
		t += h[-2:].upper()
	return t
def bytesToText(x):
	t=""
	for i in x:
		t+=chr(i)
	return t


def generateKeystream(pt,key):
	keylen = len(key)
	ptlen = len(pt)
	# key generation 
	keyStream = []
	cipherStream = []
	S = [i for i in range(0,256)]
	j=0
	for i in range(256):
		#permute
		j = (j + S[i] + key[i % keylen]) % 256
		S[i], S[j] = S[j], S[i]
	#print(S)
	i,j = 0,0
	#Pseudo random key stream generation
	for l in range(ptlen):
		#permute
		i=(i+1)%256
		j=(j+S[i])%256
		S[i], S[j] = S[j], S[i]
		k = S[(S[i] + S[j]) % 256]
		keyStream.append(k)
		# keystream xor plaintext gives cipher stream
		# encryption one byte at a time
		cipherStream.append(k^pt[l])
	return (keyStream,cipherStream)

def encrypt(pt,key):
	# converting text and key to bytes so that they can be encrypted using keystreams byte by byte
	byte = textToBytes(pt)
	print(byte)
	keybytes = textToBytes(key)
	print(keybytes)
	keyStream,cipherStream = generateKeystream(byte,keybytes)
	print(cipherStream)
	# stored in the form of hex code
	keyStream = bytesToHex(keyStream)
	print("keyStream = ",keyStream)
	cipher = bytesToHex(cipherStream)
	print("\nCIPHER : ",cipher,"\n")
	f = open("cipher.dat","w+")
	f.write(cipher)
	f.close()

def decrypt(key):
	f = open("cipher.dat","r")
	cipher = f.readline().strip().upper()
	f.close()
	#cipher text stored in hex is converted to bytes
	cipherbytes = hexToBytes(cipher)
	print(cipherbytes)
	keybytes = textToBytes(key)
	# cipherbytes is  used in place of plaintext to do the reverse process using the keybytes
	keystreambytes,plainbytes = generateKeystream(cipherbytes,keybytes)
	keyStream = bytesToHex(keystreambytes)
	print("keyStream = ",keyStream)
	print(plainbytes)
	# bytes converted to text format as in real message
	p = bytesToText(plainbytes)
	print("\nPLAINTEXT AFTER DECRYPTION : ",p,"\n")


def main():
	
	print("RC4 ALGORITHM IN COMPUTER SECURITY")	
	f = open("rc4input.dat","r")
	pt = f.readline().strip().upper()
	key = f.readline().strip().upper()
	print("The Plaintext = ",pt)
	print("The Key = ",key)	


	while(1):
	    choice = int(input("\n 1.Encryption \n 2.Decryption: \n 3.EXIT\n\n"))
	    if choice == 1:
	    	print("\nEncrypting....\n")	    	
	    	encrypt(pt,key)
	    	
	    elif choice == 2:
	    	print("\nDecrypting....\n")
	    	decrypt(key)
	    	
	    elif choice == 3:
	    	print("\nTHANK YOU")
	    	exit()
	    else:
	    	print("\nChoose correct choice\n")



main()	        