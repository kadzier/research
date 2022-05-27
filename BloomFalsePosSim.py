import random

arr = []
# random.randint:
# 100,000,000 random coin tosses gets (nearly) 4 significant digits of accuracy


# m = 2, k = 2, n = 1 experiment


msgVals = 4096
hashFuncs = []
valIndices = range(msgVals)
k = 2
for i in range(k):
	hashFuncs.append(("h" + str(i)))
# create the hash table! keys are the MESSAGES, values are the k indices message hashes to 
hashTable={ hF:{ key:[] for key in range(msgVals)} for hF in hashFuncs}



# populate the hash table randomly
# for hk in hashTable.keys(): # the k hash functions
# 	hf = hashTable[hk]
# 	for i in range(msgVals):
# 		b = random.randint(0,1)
# 		hf[i] = b 

# populate the hash table deterministically 
keyIndex = 0
for hk in hashTable.keys():
	hf = hashTable[hk]
	
	# switch between 0's and 1's every divLen messages
	divLen = msgVals / (2**(keyIndex+1))
	switchCounter = 0
	zeroFlag = True
	
	for i in range(msgVals):
		# switch between 0 blocks and 1 blocks
		# every |w| / (2*(keyindex+1)) msgVals
		if switchCounter >= divLen:
			zeroFlag = not zeroFlag
			switchCounter = 0

		if (zeroFlag  ==  True):
			hf[i] = 0
		else:
			hf[i] = 1

		switchCounter += 1

		

		
	keyIndex += 1


hashTable['h1'][1] = 1
hashTable['h1'][0] = 1
print(hashTable)
tpEvents = 0
fpEvents = 0
N = 1000000

for n in range(N): # experiment iterations
	m = 2
	B = [0] * m
	
	
	
	# hash a random message
	m1 = random.randint(0,msgVals-1)
	for hk in hashTable.keys():
		hf = hashTable[hk]
		ind = hf[m1]
		B[ind] = 1
		
	
	

	# hash another random message
	m2 = random.randint(0,msgVals-1)
	fullColl = True
	for hk in hashTable.keys():
		hf = hashTable[hk]
		ind = hf[m2]
		
		if (B[ind] == 0): # guaranteed new msg! 
			fullColl = False 
			

	if fullColl == True: # positive- either true or false!
		
		if (m1 == m2):
			tpEvents += 1
		else:
			fpEvents += 1

	
print(tpEvents)
print(fpEvents)
print((tpEvents + fpEvents)/N)

