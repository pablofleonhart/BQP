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
	objective = None
	r = 20
	c = 190
	b1 = 0
	b2 = 0
	refSet = []
	b1Set = []
	b2Set = []
	distances = []
	its = 0
	avFitness = 0

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

		if value == 1:
			self.avFitness += ssum
		
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

			if self.objective == "min":
				return self.quickSort( greater ) + equal + self.quickSort( less )
			else:
				return self.quickSort( less ) + equal + self.quickSort( greater )
		else:
			return array

	def hamming( self, s1, s2 ):
		assert len( s1 ) == len( s2 )
		return sum( c1 != c2 for c1, c2 in zip( s1, s2 ) )

	def getFirstBestNeighbor( self, solution, variable ):
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

			if ( self.objective == "min" and dts[i] < bestDelta and not find ) or ( self.objective == "max" and dts[i] > bestDelta and not find ):
				bestDelta = dts[i]
				bestVariable = i
				find = True

		return result, dts, bestDelta, bestVariable

	def monotonousSearch( self, solution ):		
		# busca encerra quando nao consegue melhorar a solucao corrente
		iterations = 1
		improve = True		

		bestValue = solution[1]
		bestDelta = 0
		bestVariable = 0

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution[0], i )

			if ( self.objective == "min" and self.deltas[i] < bestDelta ) or ( self.objective == "max" and self.deltas[i] > bestDelta ):
				bestDelta = self.deltas[i]
				bestVariable = i

		if bestDelta >= 0:
			improve = False
		else:
			bestValue += bestDelta

		while improve:
			result, self.deltas, bt, bv = self.getFirstBestNeighbor( solution[0], bestVariable )
			solution[0][bestVariable] = self.invertValue( solution[0][bestVariable] )
			bestValue += bt
			bestVariable = bv
			iterations += 1
			self.its += 1
			if bt >= 0:
				improve = False

		return solution[0], bestValue, iterations

	def getMinDistance( self, sol, curSet ):
		minDistance = self.n + 1
		pos = 0
		it = 0
		minSol = []
		self.distances = []

		for s in self.refSet:
			dist = self.hamming( s[0], sol[0] )
			self.distances.append( dist )
			if dist < minDistance and ( ( self.objective == "min" and sol[1] < s[1] ) or ( self.objective == "max" and sol[1] > s[1] ) ):
				minDistance = dist
				pos = it
				minSol = s

			it += 1

		return pos

	def updateRefSet( self, newSet ):
		changed = False
		auxSet = copy.deepcopy( self.refSet )
		for sol in newSet:	
			dist = self.getMinDistance( sol, auxSet )
			if len( auxSet ) < self.b1 + self.b2:
				auxSet.append( sol )
				changed = True

			elif ( ( sol[1] < auxSet[0][1] or sol[1] < auxSet[self.r - 1][1] ) and auxSet[dist][1] > sol[1] ) or ( ( sol[1] > auxSet[0][1] or sol[1] > auxSet[self.r - 1][1] ) and auxSet[dist][1] < sol[1] ):
				auxSet[dist] = sol
				changed = True

		self.refSet = self.quickSort( auxSet )
		self.b1Set = self.refSet[:self.b1]
		self.b2Set = self.refSet[self.b1:self.b1 + self.b2]

		return changed

	def getDifferences( self, s1, s2 ):
		v = []
		it = 0

		for c1, c2 in zip( s1, s2 ):
			if c1 != c2:
				v.append( it )
			it += 1

		return v

	def updatePath( self, deltas, solution, variable ):
		dts = copy.deepcopy( deltas )

		value = solution[variable]

		for i in xrange( self.n ):
			if i == variable:
				dts[i] *= -1

			else:
				dts[i] += 2 * self.q[variable][i] * ( 1 - 2 * solution[i] ) * ( 1 - 2 * value )

		return dts

	def pathRelinking( self ):
		children = []
		it = 0
		for i in xrange( self.b1 ):
			# calcula deltas para solucao i			
			deltas = [0 for x in xrange( self.n )]			

			start = time.time()
			for k in xrange( self.n ):
				deltas[k] = self.calcDelta( self.refSet[i][0], k )

			for j in xrange( self.b1, self.b1 + self.b2 ):
				start = time.time()
				dts = copy.deepcopy( deltas )
				bestSol = self.refSet[i][0]
				bestValue = self.refSet[i][1]
				res = bestValue
				solution = copy.deepcopy( self.refSet[i][0] )

				diff = self.getDifferences( self.refSet[i][0], self.refSet[j][0] )
				while diff:
					var = random.choice( diff )
					res += dts[var]
					
					dts = self.updatePath( dts, solution, var )
					solution[var] = self.invertValue( solution[var] )
					if ( self.objective == "min" and res < bestValue ) or ( self.objective == "max" and res > bestValue ):
						bestValue = res
						bestSol = copy.deepcopy( solution )

					diff.remove( var )
					self.its += 1

				it += 1

				if ( self.objective == "min" and self.refSet[j][1] < bestValue ) or ( ( self.objective == "max" and self.refSet[j][1] > bestValue ) ):
					bestValue = self.refSet[j][1]
					bestSol = self.refSet[j][0]

				children.append( ( bestSol, bestValue ) )

		return children

	def printSolutions( self, solutions ):		
		for sol in solutions:
			print sol[1], sol[0]

		print "###################################"

	def run( self, obj ):
		self.objective = obj
		self.its = 0		

		diverseSolutions = []
		self.refSet = [] # mantem as melhores solucoes (b1 + b2)
		self.b1Set = []
		self.b2Set = []

		start = time.time()
		# constroi C solucoes aleatorias
		for i in xrange( self.c ):
			sol = bqp.generateAttempt( time.time() )

			start = time.time()
			fitness = bqp.calc( sol )
			diverseSolutions.append( ( sol, fitness ) )

		diverseSolutions = bqp.quickSort( diverseSolutions )
		self.refSet = diverseSolutions[:self.r]
		self.b1Set = self.refSet[:self.b1]
		self.b2Set = self.refSet[self.b1:self.b1 + self.b2]

		start = time.time()
		changedRefSet = True

		while changedRefSet and ( time.time() - start ) < 300:
			children = self.pathRelinking()

			tam = len( children )
			for i in xrange( tam ):
				res = self.monotonousSearch( children[i] )
				children[i] = res[0], res[1]

			changedRefSet = self.updateRefSet( children )

		return self.refSet[0][1], self.its, time.time() - start

if ( len( sys.argv ) <= 1 ):
	print "Use:", sys.argv[0], "<sat_problem.(sparse, txt)>, <min, max>"
	sys.exit( 1 )

param = sys.argv[1:]

file = param[0]
obj = param[1]
f = file.split( "/" )[1]
nfile = f.replace( ".txt", '' )
nfile = f.replace( ".sparse", '' )

bqp = BQP( file )

pattern = "{:14s}{:4s}{:4s}{:4s}{:10s}{:8s}{:10s}"
patternResult = "{:<14s}{:<4d}{:<4d}{:<4d}{:<10d}{:<8.2f}{:<10d}"
print pattern.format( "instance", "b1", "b2", "rep", "value", "t", "it" )

# executar cada instancia com diferentes valores de b1(2y) e b2(R-2y) p/ y = [1,9]
for y in xrange( 1, 10 ):
	values = 0
	its = 0
	tis = 0
	for i in xrange( 15 ):
		bqp.b1 = 2 * y
		bqp.b2 = bqp.r - bqp.b1
		res = bqp.run( obj )
		values += res[0]
		its += res[1]
		tis += res[2]
		print patternResult.format( nfile, bqp.b1, bqp.b2, i + 1, res[0], res[2], res[1] )

	print values/15, its/15.0, tis/15.0
