import numpy as np
import matplotlib.pyplot as plt

M = 1000
sigma = 500

#2d table for a fixed M, m, sigma
# l rows, k columns
# l = 0, 1, 2, ...
# k = 1, 2, 3, ...
k = 15
l = k + 1 # default range of l is k + 1
assert(l == k+1)

# constraints on M, k and sigma
assert(sigma >= 2*k)
assert(M >= k + sigma)

# fill arrays for these values of m (default: sigma + 1)
mRange = sigma + 1

# constraint on m for this sigma
assert(mRange - 1 <= sigma)

# construct transition probability arrays for each m 
transitionArrs = [] 
for m in range(mRange):	
	arr = [[0 for i in range(k)] for j in range(l)]
	#base case: first row (l=0, no additional bits added)
	for col in range(k):

		kVal = col + 1 # k starts from 1
		arr[0][col] =  (m/M)**(kVal)

	#base case: l = 1, k = 1 (one additional bit, one hash function)
	arr[1][0] = (M - m)/(M)

	#base case: l > k (impossible)
	for row in range(l):
		for col in range(k):
			kVal = col+1
			if row > (kVal): # k starts from 1
				arr[row][col] = 0

	# recursive cases 
	for row in range(l):
		for col in range(k):
			kVal = col + 1

			# actual cases we need to fill in
			if row > 0 and kVal > 1:  
				arr[row][col] = arr[row][col-1] * (m + row) / (M) + arr[row-1][col-1] * (M - (m + row - 1))/(M)

	# we now have our arr for this value of m
	# print("m =", m)
	# for row in range(l):
	# 	print(arr[row])
	transitionArrs.append(arr)

# we now have our transition probability arrays for each m
print()
print()
print("---TRANSITION PROBABILTY ARRAYS:---")
for m in range(len(transitionArrs)):
	print("m =", m)
	for row in range(l):
		print(transitionArrs[m][row])

# construct the markov matrix (sigma+1) x (sigma+1):
P = np.zeros((sigma+1, sigma+1))

for row in range(sigma+1):
	for col in range(sigma+1):
		# fill in the entries m <= sigma - k
		if row <= sigma - k:
			# grab the relevant transition arr 
			refTransitionArr = transitionArrs[row]
			# get the relevant transition COLUMN
			refTransitionCol = []
			for i in range(l):
				kIndex = k-1 # because k starts at 1
				refTransitionCol.append(refTransitionArr[i][kIndex])
			# fill in this row!
			for i in range(len(refTransitionCol)):
				rowOffset = i + row
				P[row][rowOffset] = refTransitionCol[i]
		
		else: # entries with backwards transitions
			# grab the relevant transition arr 
			refTransitionArr = transitionArrs[row]
			# get the relevant transition COLUMN
			refTransitionCol = []
			for i in range(l):
				kIndex = k-1 # because k starts at 1
				refTransitionCol.append(refTransitionArr[i][kIndex])
			
			# forward transitions
			numForward = sigma+1 - row
			# print(row,col)
			# print(numForward)
			for i in range(numForward):
				rowOffset = row
				P[row][i + rowOffset] = refTransitionCol[i]

			# "extra" forward probability left over for this row:
			spillOverProb = 0
			for i in range(numForward,len(refTransitionCol)):
				spillOverProb += refTransitionCol[i]
			# print(spillOverProb)

			# backward transitions (k entires per row)

			# get m=0 column
			zeroArr = transitionArrs[0]
			zeroCol = []
			for i in range(l):
				kIndex = k-1 # because k starts at 1
				zeroCol.append(zeroArr[i][kIndex])
			
			
			# fill in backwards entires
			for i in range(k):
				rowOffset = 1
				P[row][i+rowOffset] = spillOverProb*zeroCol[i+1]
			
print()
print()
print("---MARKOV CHAIN MATRIX:---")
print(P)
print("---")
print()
print()
print("---LONG TERM PROBABILITY VECTOR:---")
s = np.linalg.matrix_power(P,1000000)
#print(s)
print(s[0])
print("column difference:", s[0][1] - s[1][1])
print("row sum:",sum(s[0]))

x = range(len(s[0])) 
plt.plot(x,s[0])
plt.xlabel("# of bits")
plt.ylabel("probabilty")
plt.title("probability of # of bits")
plt.show()
# A = np.array([[0, 1/6, 5/6, 0, 0], [0, .02777777777777, .41666666666666, 5/9, 0], [0, 0, 1/9, 5/9, 3/9], [0, 2/72, 10/72, 3/12, 7/12], [0, (1/6)*(.4999999999999 + 5/90), (5/6)*(.4999999999999 + 5/90), 0, 4/9]])
# print(A)
# print("---")
# s = np.linalg.matrix_power(A,1001)
# print(s)
# print(sum(s[0]))