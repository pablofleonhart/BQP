from random import *
import copy
import math
import numpy as np
import random
import resource
import sys
import time

class BQP:
	m = 0
	n = 0
	q = []
	deltas = []
	fitness = 0
	r = 20
	c = 40
	b1 = 0
	b2 = 0
	refSet = []
	b1Set = []
	b2Set = []

	def __init__( self, filename ):
		file = open( filename, 'r' )

		finish = False
		read = False

		if filename.startswith( "files/p" ):
			while not finish:
			    line = file.readline()

			    if not line:
			        finish = True

			    else:
			        line = line.split()
			        tam = len( line )
			        if tam > 0:
			            if len( line ) == 2:
			                self.n = int( line[1] )
			                self.q = [[0 for x in xrange( self.n )] for y in xrange( self.n )]
			                read = True
			                i = 0
			                j = 0

			            elif read:
			            	for z in xrange( tam ):
			            		self.q[i][j] = int( line[z] )
			            		j += 1

			            		if j == self.n:
			            			i += 1
			            			j = 0

		elif filename.startswith( "files/bqp" ):
			while not finish:
				line = file.readline()

				if not line:
					finish = True

				else:
					line = line.split()

					if len( line ) > 0:
						if len( line ) == 2:
							self.n = int( line[0] )
							self.m = int( line[1] )
							self.q = [[0 for x in xrange( self.n )] for y in xrange( self.n )]
							read = True                

						elif read:
							i = int( line[0] ) - 1
							j = int( line[1] ) - 1
							k = int( line[2] )

							self.q[i][j] = k
							self.q[j][i] = k

		file.close()

		self.deltas = [0 for x in xrange( self.n )]

	def calc( self, solution ):
		tsolution = np.transpose( solution )
		a = np.dot( solution, self.q )
		return np.dot( a, tsolution )

	def generateAttempt( self, s ):
		seed( s )
		result = []
		for i in xrange( self.n ):
			result.append( randint( 0, 1 ) )

		return result

	def invertValue( self, v ):
		if v == 0:
			return 1
		else:
			return 0

	def calcDelta( self, solution, variable ):
		value = solution[variable]
		ssum = 0

		for i in xrange( self.n ):
			if i != variable and solution[i] == 1:
				ssum += self.q[i][variable]

		return ( 1 - ( 2 * value ) ) * ( self.q[variable][variable] + 2 * ssum )

	def quickSort( self, array ):
		less = []
		equal = []
		greater = []

		if len( array ) > 1:
			pivot = array[0][1]
			for x, y in array:
				if y > pivot:
					less.append( ( x, y ) )
				if y == pivot:
					equal.append( ( x, y ) )
				if y < pivot:
					greater.append( ( x, y ) )
			return self.quickSort( greater ) + equal + self.quickSort( less )
		else:
			return array

	def hamming( self, s1, s2 ):
		assert len( s1 ) == len( s2 )
		return sum( c1 != c2 for c1, c2 in zip( s1, s2 ) )

	def getFirstNeighbor( self, solution, variable ):
		dts = copy.deepcopy( self.deltas )
		result = dts[variable]
		bestDelta = 0
		bestVariable = 0
		find = False

		value = solution[variable]

		for i in np.random.permutation( self.n - 1 ):
			if i == variable:
				dts[i] *= -1

			else:
				dts[i] += 2 * self.q[variable][i] * ( 1 - 2 * solution[i] ) * ( 1 - 2 * value )

			if dts[i] < bestDelta and not find:				
				bestDelta = dts[i]
				bestVariable = i
				find = True

		return result, dts, bestDelta, bestVariable

	def firstImprovementMonotonousSearch( self, solution ):
		# busca encerra quando nao consegue melhorar a solucao corrente
		iterations = 1
		improve = True		

		bestValue = solution[1]
		bestDelta = 0
		bestVariable = 0

		print solution, bestValue

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution[0], i )

			if self.deltas[i] < bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		bestValue += bestDelta
		#print self.deltas, bestDelta, bestVariable

		while improve:
			result, self.deltas, bt, bv = self.getFirstNeighbor( solution[0], bestVariable )
			print self.deltas, bt, bv		
			solution[0][bestVariable] = self.invertValue( solution[0][bestVariable] )
			bestValue += bt
			bestVariable = bv
			iterations += 1
			print solution
			if bt >= 0:
				improve = False

		self.refSet[0] = ( solution[0], bestValue )
		return iterations

	def getMinDistance( self, sol ):
		minDistance = self.n + 1
		pos = 0
		it = 0		

		for s in self.refSet:
			print s, sol
			dist = self.hamming( s[0], sol[0] )
			print dist
			if dist < minDistance:
				minDistance = dist
				pos = it

			it += 1

		print ( pos, minDistance )
		return ( pos, minDistance )

	def updateRefSet( self, newSet ):
		d = 4
		auxSet = copy.deepcopy( self.refSet )
		for sol in newSet:
			dist = self.getMinDistance( sol )
			print 
			if len( auxSet ) < self.b1 + self.b2:
				auxSet.append( sol )

			elif sol[1] < self.auxSet[0][1] or ( sol[1] < self.auxSet[-1:][1] and dist[1] < d ):
				self.auxSet[dist[0]] = dist[1]

		self.refSet = self.quickSort( auxSet )
		self.b1Set = self.refSet[:self.b1]
		self.b2Set = self.refSet[self.b1:self.b1 + self.b2]

	def pathRelinking( self ):
		it = 1
		for i in xrange( len( self.refSet ) ):
			for j in xrange( i + 1, len( self.refSet ) ):
				print it, self.refSet[i], self.refSet[j]
				it += 1

	def printSolutions( self, solutions ):		
		for sol in solutions:
			print sol[1], sol[0]

		print "###################################"

	def run( self, y ):
		self.b1 = 2 * y
		self.b2 = self.r - self.b1

		diverseSolutions = []
		self.refSet = [] # mantem as melhores solucoes (b1 + b2)
		self.b1Set = []
		self.b2Set = []

		# constroi C solucoes aleatorias
		for i in xrange( self.c ):
			sol = bqp.generateAttempt( time.time() )	

			fitness = bqp.calc( sol )
			diverseSolutions.append( ( sol, fitness ) )

		diverseSolutions = bqp.quickSort( diverseSolutions )
		self.refSet = diverseSolutions[:self.r]
		self.b1Set = self.refSet[:self.b1]
		self.b2Set = self.refSet[self.b1:self.b1 + self.b2]

		print "Solucoes iniciais:"
		self.printSolutions( self.refSet )
		self.printSolutions( self.b1Set )
		self.printSolutions( self.b2Set )

		print self.getMinDistance( diverseSolutions[25] )

		#self.pathRelinking()

		#iterations = self.firstImprovementMonotonousSearch( self.refSet[0] )
		#print self.refSet[0], iterations
		#print refSet
		#print bqp.hamming( refSet[0][0], refSet[1][0] )
		#print b1Set
		#print b2Set

		# calc: utiliza somente ao gerar a solucao para prover o valor inicial de fitness
		# calcDelta: utiliza para manter o valor de fitness a partir da solucao construida

		# com a distancia de ham. define os subconjuntos		
		#for solution in refSet:
			# path rel. para gerar solucoes filhas

			# busca local para melhorar solucoes filhas


		# aplica path relinking e depois a busca local

if ( len( sys.argv ) <= 1 ):
	print "Use:", sys.argv[0], "<sat_problem.(sparse, txt)>"
	sys.exit( 1 )

param = sys.argv[1:]

file = param[0]
f = file.split( "/" )[1]
nfile = f.replace( ".txt", '' )
nfile = f.replace( ".sparse", '' )

bqp = BQP( file )

# executar cada instancia com diferentes valores de b1(2y) e b2(R-2y) p/ y = [1,9]
for y in xrange( 1, 2 ):
	bqp.run( y )