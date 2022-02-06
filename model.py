import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import uniform
from scipy.stats import norm
from scipy.integrate import quad 




#oracle true probability of duplicates
p = float(input("assumed probability of duplicate messages: "))

# bloom filter params
m = int(input("number of bits in Bloom Filter: "))
k = int(input("number of hash functions in Bloom Filter: "))

# # bloom caching params
C = int(input("max number of messages in Bloom Filter: "))
n = int(input("current number of messages in Bloom Filter: "))
if (n > C):
	print("current number should be less than max!")
	exit(0)

T = int(input("max TTL: "))
# if (T <= C):
# 	print("max TTL must be greater than max messages!")
# 	exit(0)


D = int(input("Assumed distribution of duplicate TTL's: \n 1. Uniform \n 2. Normal \n enter a number: "))

# bloom filter false positive probability
p_false_pos = (1 - (1 - 1/m)**(k*n))**k
# print("Bloom Filter false positive probability for next message: ", p_false_pos)

# default distribution params

# uniform (time always ranges from 1 to T)
a = 1
b = T

# normal
u = 0
s = 1

if (D == 2): # Normal distribution
	print("Normal distribution: ")
	u = float(input("mean TTL: (between 1 and T)"))
	s = float(input("standard deviation TTL: "))

	tMin = 1
	tMax = T
	x = np.linspace(tMin, tMax, 10000) # 10,000 evenly spaced values between tMin and tMax 
	y = norm.pdf(x, u, s)
	def normal_pdf(x):
		y = norm.pdf(x, u, s)
		return y 

	# integrate PDF from a to max num messages in cache 
	resultLo, errLo = quad(normal_pdf, 1, C/2)
	resultHi, errHi = quad(normal_pdf, 1, C)
	print("---")
	print()

	print("For a Two-Phase bloom filter with", m, "bits and", k, "hash functions, maximum of", C, " messages \nstored at once,", n , "current messages, max TTL of", T, ", assumed true probability of duplicates of", p)

	print("TRUE POSITIVE probability (CAUGHT duplicates): ")
	p_overall_lo = p * resultLo 
	p_overall_hi = p * resultHi
	print("low: ", p_overall_lo)
	print("hi: ", p_overall_hi)

	print("FALSE NEGATIVE probability (MISSED duplicates): ")
	print("low: ", p * (1 - resultLo))
	print("hi: ", p * (1 - resultHi))

	print("FALSE POSITIVE probability (new messages incorrectly classified as duplicates): ")
	print((1-p) * p_false_pos)

	print("TRUE NEGATIVE probability (new messages correctly classified): ")
	print((1-p) * (1 - p_false_pos))

if (D == 1): # Uniform distribution (max value is T)
	print("Uniform distribution: ")
	a = 1
	b = T

	# definte the uniform PDF
	x = np.linspace(a, b, 10000) # 10,000 evenly spaced values between 1 and T 
	def uniform_pdf(x):
		y = uniform.pdf(x, a, b-a) # uniform from 1 to T
		return y

	# integrate PDF from a to max num messages in cache 
	resultLo, errLo = quad(uniform_pdf, a, C/2)
	resultHi, errHi = quad(uniform_pdf, a, C)
	# print("PDF integration min: ", resultLo)
	# print("PDF integration max: ", resultHi)

	print("---")
	print()

	print("For a Two-Phase bloom filter with", m, "bits and", k, "hash functions, maximum of", C, " messages \nstored at once,", n , "current messages, max TTL of", T, ", assumed true probability of duplicates of", p)

	print("TRUE POSITIVE probability (CAUGHT duplicates): ")
	p_overall_lo = p * resultLo 
	p_overall_hi = p * resultHi
	print("low: ", p_overall_lo)
	print("hi: ", p_overall_hi)

	print("FALSE NEGATIVE probability (MISSED duplicates): ")
	print("low: ", p * (1 - resultLo))
	print("hi: ", p * (1 - resultHi))

	print("FALSE POSITIVE probability (new messages incorrectly classified as duplicates): ")
	print((1-p) * p_false_pos)

	print("TRUE NEGATIVE probability (new messages correctly classified): ")
	print((1-p) * (1 - p_false_pos))








