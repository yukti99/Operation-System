"""DES ALGORITHM"""
# Permutation tables and Sboxes
import binascii
# parity bit drop table to convert 64-bit key to 56-bit key
KeyP = (
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
)

# Initial permutation vector
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7 
    )
# final permuations table
IP_INV = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
)
# key compression table to convert 56-bit key to 48-bits
key_comp = (
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)
# for expansion permuatation
E  = (
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)
 # representation of s-boxes in the form of a dictionary
Sboxes = {
    0: (
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ),
    1: (
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
        3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
        0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9 
    ),
    2: (
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
        1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 
    ),
    3: (
        7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
        3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ),
    4: (
        2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
        4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ),
    5: (
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
        9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
        4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ),
    6: (
        4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
        1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
        6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ),
    7: (
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
        1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
        7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
        2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    )
}
# straight permuatation table
P = (
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11, 4,  25
)
# to represent the no of bit-shifts in each of 16-rounds of DES
shift_table = [1,1,2,2,
			   2,2,2,2,
			   1,2,2,2,
			   2,2,2,1 ]
"""
def binToHex(x):
	s = str(hex(int(x,2)))
	pos=0
	for i in range(len(s)):
		if (s[i] == 'x'):
			pos = i
			break
	s = s[pos+1:]
	s=s.upper()
	return s



def hexToBin(x):
	n = int(x,16)
	b = ""
	while(n>0):
		b = str(n%2)+b
		n = n>>1
	return b
"""
rkb = [] # roundkeys in binary
rkh = []	# roundkeys in hexadecimal

def hexToBin(x):
	m = {'0':"0000",'1':"0001",'2':"0010",'3':"0011",'4':"0100",
		'5':"0101",'6':"0110",'7':"0111",'8':"1000",'9':"1001",
		'A':"1010",'B':"1011",'C':"1100",'D':"1101",'E':"1110",'F':"1111"}
	b = ""
	x = str(x)
	for i in range(len(x)):
		b += m[x[i]]
	return b

def binToHex(x):
	m = {"0000":"0","0001":"1","0010":"2","0011":"3","0100":"4",
		"0101":"5","0110":"6","0111":"7","1000":"8","1001":"9",
		"1010":"A","1011":"B","1100":"C","1101":"D","1110":"E","1111":"F"}
	h = ""
	x = str(x)
	for i in range(0,len(x),4):
		ch = x[i]+x[i+1]+x[i+2]+x[i+3]
		h += m[ch]
	return h


# for permutation of the key/plaintext during encryption
def permute(s,table,n):
	# s  is the string to be permuted using permutation table
	p = ""
	for i in range(n):
		p += s[table[i]-1]
	return p

# to shift the string left by n bits
def shift_left(s,n):
	# n is the no of shifts to be done
	a = ""
	for i in range(n):
		for j in range(1,28):
			a+=s[j]
		a+=s[0]
		s = a
		a = ""
	return s
def xor(a,b):
    return ''.join([hex(ord(a[i%len(a)]) ^ ord(b[i%(len(b))]))[2:] for i in range(max(len(a), len(b)))])
"""
def performXOR(a,b):
	res = ""
	for i in a:
		for j in b:
			if i == j:
				res += "0"
			else:
				res += "1"
	return res
"""
def performXOR(a,b):
	res = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			res += "0"
		else:
			res += "1"
	return res

def KEY_GENERATION(key):
	global rkb,rkh
	# converting hex key to binary
	#print("key = ",key)
	k = hexToBin(key)
	print("1. ",k)

	"""1. KEY TRANSFORMATION """
	# getting 56-bit key from 64 bit key using parity bits
	# initial 64-bit key is transformed into a 56-bit key by discarding every 8th bit of the initial key
	k = permute(k,KeyP,56) 
	print("2. ",k)

	# splitting the key into left and right substrings
	# the 56 bit key is divided into two halves, each of 28 bits. These halves are circularly shifted left 
	# by one or two positions, depending on the round.
	left = k[0:28]
	right = k[28:]

	print("left  = ",left)
	print("right = ",right)

	
	# generating the 16 round keys
	for i in range(16):
		# shifting
		left = shift_left(left,shift_table[i])
		right = shift_left(right,shift_table[i])
		# combining after every round
		combine = left+right
		# key compression
		#After an appropriate shift, 48 of the 56 bit are selected
		roundKey = permute(combine,key_comp,48)
		print("\nROUND-",i+1," KEY : ",roundKey,"\n")
		rkb.append(roundKey)
		rkh.append(binToHex(roundKey).lower())
		#Since the key transformation process involves permutation as well as selection of a 48-bit sub set of the original 
		# 56-bit key it is called Compression Permutation.

def encrypt_block(pt):
	# Initial permutation of 64-bit plaintext using IP 
	pt = permute(pt,IP,64)
	print("4. ",pt)

	# splitting into left and right substrings
	left_pt = pt[0:32]
	right_pt = pt[32:]
	print("left plaintext  = ",binToHex(left_pt))
	print("right plaintext = ",binToHex(right_pt))

	# EXPANSION PERMUTATION: 32 bits to 48 bits
	for i in range(16):
		print("\nROUND-",i+1,"\n")
		# expansion D-box
		right_expanded = permute(right_pt,E,48)

		# XOR roundkey of current round and right_expanded
		x = performXOR(rkb[i],right_expanded)

		# S-BOXES
		op = ""
		for j in range(8):
			row = 2*int(x[j*6]) + 1*int(x[j*6+5])
			col = 8*int(x[j*6 + 1]) + 4*int(x[j*6 + 2]) + 2*int(x[j*6 + 3]) + 1*int(x[j*6 + 4])
			#print("row = ",row,"and col = ",col)
			val = Sboxes[j][16*row+col]
			op += str(int(val/8))
			val = val%8
			op += str(int(val/4))
			val = val%4
			op += str(int(val/2))
			val = val%2
			op += str(int(val))

		print("op = ",op)
		# Straight D-box
		op = permute(op,P,32)

		# XOR left and op
		x = performXOR(op,left_pt)
		left_pt = x

		# SWAPPER except in last round
		if (i!=15):
			# swapping left and right
			left_pt,right_pt = right_pt,left_pt


	combine_pt = left_pt+right_pt
	cipher = binToHex(permute(combine_pt,IP_INV,64))
	return cipher

def pad(plaintext):
    padding_len = 64 - (len(plaintext) % 64)
    padding = "0"*padding_len
    return plaintext + padding

def unpad(plaintext):
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def split_blocks(message, block_size=64):
    assert len(message) % block_size == 0
    return [message[i:i+64] for i in range(0, len(message), block_size)]

def encrypt(pt,key):

	KEY_GENERATION(key)	
	
	# converting hex key to binary
	print("pt = ",pt)
	pt = hexToBin(pt)
	print("3. ",len(pt))
	pt = pad(pt)
	print("pt = ",len(pt))

	cipher = ""
	# splitting in blocks of size 64-bit
	for plaintext_block in split_blocks(pt):
		c = encrypt_block(plaintext_block)
		#print("c = ",c)
		cipher+=c
		
	#writing cipher to file
	print("\nCIPHER TEXT AFTER ENCRYPTION = ",cipher,"\n")
	f = open("cipher.dat","w+")
	f.write(cipher)
	f.close()	
	return cipher

def decrypt_block(c):
	# Initial permutation of 64-bit plaintext using IP 
	c = permute(c,IP,64)
	print("4. ",c)

	# splitting into left and right substrings
	left_pt = c[0:32]
	right_pt = c[32:]
	print("left plaintext  = ",binToHex(left_pt))
	print("right plaintext = ",binToHex(right_pt))

	# EXPANSION PERMUTATION: 32 bits to 48 bits
	for i in range(16):
		print("\nROUND-",i+1,"\n")
		# expansion D-box
		right_expanded = permute(right_pt,E,48)

		# XOR roundkey of current round and right_expanded
		x = performXOR(rkb[15-i],right_expanded)

		# S-BOXES
		op = ""
		for j in range(8):
			row = 2*int(x[j*6]) + 1*int(x[j*6+5])
			col = 8*int(x[j*6 + 1]) + 4*int(x[j*6 + 2]) + 2*int(x[j*6 + 3]) + 1*int(x[j*6 + 4])
			#print("row = ",row,"and col = ",col)
			val = Sboxes[j][16*row+col]
			op += str(int(val/8))
			val = val%8
			op += str(int(val/4))
			val = val%4
			op += str(int(val/2))
			val = val%2
			op += str(int(val))

		print("op = ",op)
		# Straight D-box
		op = permute(op,P,32)

		# XOR left and op
		x = performXOR(op,left_pt)
		left_pt = x

		# SWAPPER except in last round
		if (i!=15):
			# swapping left and right
			left_pt,right_pt = right_pt,left_pt


	combine_pt = left_pt+right_pt
	p = permute(combine_pt,IP_INV,64)
	p = binToHex(p)
	return p

def decrypt(key):
	KEY_GENERATION(key)	

	# will read the encrypted cipher stored in cipher.dat by the encrypt function
	f = open("cipher.dat","r")
	cipher = f.readline().strip().upper()
	print(cipher)
	if (cipher == ""):
		print("Please encrypt the plaintext to create a cipher first!!")
		return 0
	f.close()
	print("*****DECRYPTING CIPHER = ",cipher,"*******")
	# converting hex key to binary
	c = hexToBin(cipher)

	plaintext = ""
	# splitting in blocks of size 64-bit
	for cipher_block in split_blocks(c):
		p = decrypt_block(cipher_block)
		plaintext+=p	

	plaintext = plaintext.lower()
	plaintext = bytearray.fromhex(plaintext).decode()
	print("\nPLAIN TEXT AFTER DECRYPTION = ",plaintext,"\n")



	

def main():
	
	print("DES ALGORITHM IN COMPUTER SECURITY")	
	f = open("aesinput.dat","r")
	pt = f.readline().strip().upper()
	key = f.readline().strip().upper()

	
	
	key = key.encode("utf-8")
	key = binascii.hexlify(key)
	key = key.decode().upper()

	pt = pt.encode("utf-8")
	pt = binascii.hexlify(pt)
	pt = pt.decode().upper()
	print("The Key = ",key)	
	print("The Plaintext = ",pt)


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