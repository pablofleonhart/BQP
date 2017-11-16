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

	def getBestNeighbor( self, solution, variable ):
		dts = copy.deepcopy( self.deltas )
		result = dts[variable]
		bestDelta = -999999999
		bestVariable = 0

		value = solution[variable]

		for i in xrange( self.n ):
			if i == variable:
				dts[i] *= -1

			else:
				dts[i] += 2 * self.q[variable][i] * ( 1 - 2 * solution[i] ) * ( 1 - 2 * value )

			if dts[i] > bestDelta:				
				solution[variable] = self.invertValue( solution[variable] )
				solution[i] = self.invertValue( solution[i] )

				if solution not in self.tabuList:
					bestDelta = dts[i]
					bestVariable = i

				solution[variable] = self.invertValue( solution[variable] )				
				solution[i] = self.invertValue( solution[i] )

		return result, dts, bestDelta, bestVariable

	def run( self, duration, rand = False ):
		self.tabuList = []
		noImprove = 0
		iterations = 1

		solution = self.generateAttempt( time.time() )
		cSolution = copy.deepcopy( solution )
		self.tabuList.append( cSolution )
		bestGlobalSolution = cSolution
		bestSolution = cSolution
		bestGlobalValue = self.calc( solution )
		bestValue = bestGlobalValue
		bestDelta = -999999999
		bestVariable = 0

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution, i )

			if self.deltas[i] > bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		bestValue += bestDelta
		duration = math.ceil( duration * self.n )
		start = time.time()
		tt = 0
		itt = 0

		while noImprove < self.n * 20 and time.time() - start < 300:					
			result, self.deltas, bt, bv = self.getBestNeighbor( solution, bestVariable )
			
			solution[bestVariable] = self.invertValue( solution[bestVariable] )

			if bestValue > bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( solution )
				tt = time.time() - start
				itt = iterations

			else:
				noImprove += 1

			self.tabuList.append( copy.deepcopy( solution ) )

			if rand:
				dr = duration + random.randint( 1, 10 )

			else:
				dr = duration

			if len( self.tabuList ) >= dr:
				self.tabuList.pop( 0 )

			iterations += 1

			bestValue += bt
			bestVariable = bv

		return bestGlobalValue, itt, tt, iterations, time.time() - start

if ( len( sys.argv ) <= 1 ):
	print "Use:", sys.argv[0], "<sat_problem.(sparse, txt)>"
	sys.exit( 1 )

param = sys.argv[1:]

pattern = "{:7s}{:14s}{:4s}{:4s}{:12s}{:10s}{:8s}"
patternResult = "{:<7s}{:<14s}{:<4d}{:<4d}{:<12d}{:<10d}{:<8f}"
print pattern.format( "tenure", "instance", "d", 'rep', 'v', "it", "time" )

ti = []
iterations = []
values = []
durations = [25, 50, 100, 200]
files = ["files/p7000-1.txt"]

file = param[0]
f = file.split( "/" )[1]
nfile = f.replace( ".txt", '' )
nfile = f.replace( ".sparse", '' )

bqp = BQP( file )

# fixed tabu list's duration
for z in xrange( 1, 11 ):
	for d in durations:
		result = bqp.run( 1/( d * 1.0 ) )
		print patternResult.format( 'F', nfile, d, z, result[0], result[1], result[2] )

# random tabu list's duration
for z in xrange( 1, 11 ):
	for d in durations:
		result = bqp.run( 1/( d * 1.0 ), True )
		print patternResult.format( 'R', nfile, d, z, result[0], result[1], result[2] )