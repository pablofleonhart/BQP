from random import *
import copy
import numpy as np
import sys
import time
import resource

class BQP:
	m = 0
	n = 0
	q = []
	deltas = []
	fitness = 0
	prevVar = 0

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

	def getVariable( self ):
		return randint( 0, self.n - 1 )

	def randrange_float( self, start, stop, step ):
		return randint( 0, int( ( stop - start ) / step ) ) * step + start

	def mean( self, data ):
	    n = len( data )
	    if n < 1:
	        return 0.00

	    return sum( data ) / n

	def _ss( self, data ):
	    c = self.mean( data )
	    ss = sum( ( x - c ) ** 2 for x in data )
	    return ss

	def pstdev( self, data ):
	    n = len( data )
	    if n < 2:
	        return 0.00
	    ss = self._ss( data )
	    pvar = ss / n
	    return pvar ** 0.5

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
				bestDelta = dts[i]
				bestVariable = i

		return result, dts, bestDelta, bestVariable

	def getFirstNeighbor( self, solution, variable ):
		dts = copy.deepcopy( self.deltas )
		result = dts[variable]
		bestDelta = -999999999
		bestVariable = 0
		find = False

		value = solution[variable]

		for i in np.random.permutation( self.n - 1 ):
			if i == variable:
				dts[i] *= -1

			else:
				dts[i] += 2 * self.q[variable][i] * ( 1 - 2 * solution[i] ) * ( 1 - 2 * value )

			if dts[i] > bestDelta and not find:				
				bestDelta = dts[i]
				bestVariable = i
				find = True

		return result, dts, bestDelta, bestVariable

	def bestImprovementSearch( self, maxTime ):
		iterations = 1

		solution = self.generateAttempt( time.time() )
		cSolution = copy.deepcopy( solution )
		bestGlobalSolution = cSolution
		bestSolution = cSolution
		bestGlobalValue = self.calc( solution )
		bestValue = bestGlobalValue
		bestDelta = -999999999
		bestVariable = 0
		
		ts = time.time()
		drt = 0
		it = 0

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution, i )

			if self.deltas[i] > bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		bestValue += bestDelta

		start = time.time()
		tt = 0
		itt = 0

		while time.time() - start < maxTime:
			result, self.deltas, bt, bv = self.getBestNeighbor( solution, bestVariable )
			
			solution[bestVariable] = self.invertValue( solution[bestVariable] )

			if bestValue > bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( solution )
				tt = time.time() - start
				itt = iterations

			iterations += 1

			bestValue += bt
			bestVariable = bv

		return bestGlobalValue, itt, tt, iterations, time.time() - start

	def firstImprovementSearch( self, maxTime ):
		iterations = 1

		solution = self.generateAttempt( time.time() )
		cSolution = copy.deepcopy( solution )
		bestGlobalSolution = cSolution
		bestSolution = cSolution
		bestGlobalValue = self.calc( solution )
		bestValue = bestGlobalValue
		bestDelta = -999999999
		bestVariable = 0
		
		ts = time.time()
		drt = 0
		it = 0

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution, i )

			if self.deltas[i] > bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		bestValue += bestDelta

		start = time.time()
		tt = 0
		itt = 0

		while time.time() - start < maxTime:
			result, self.deltas, bt, bv = self.getFirstNeighbor( solution, bestVariable )
			
			solution[bestVariable] = self.invertValue( solution[bestVariable] )

			if bestValue > bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( solution )
				tt = time.time() - start
				itt = iterations

			iterations += 1

			bestValue += bt
			bestVariable = bv

		return bestGlobalValue, itt, tt, iterations, time.time() - start

	def randomLocalSearch( self, maxTime ):
		iterations = 1

		solution = self.generateAttempt( time.time() )
		cSolution = copy.deepcopy( solution )
		bestGlobalSolution = cSolution
		bestSolution = cSolution
		bestGlobalValue = self.calc( solution )
		bestValue = bestGlobalValue
		bestDelta = -999999999
		bestVariable = 0
		
		ts = time.time()
		drt = 0
		it = 0

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution, i )

			if self.deltas[i] > bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		bestValue += bestDelta

		start = time.time()
		tt = 0
		itt = 0

		while time.time() - start < maxTime:
			result, self.deltas, bt, bv = self.getBestNeighbor( solution, bestVariable )
			
			solution[bestVariable] = self.invertValue( solution[bestVariable] )

			if bestValue > bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( solution )
				tt = time.time() - start
				itt = iterations

			iterations += 1

			bestValue += bt
			bestVariable = bv

		return bestGlobalValue, itt, tt, iterations, time.time() - start

if ( len( sys.argv ) != 2 ):
	print "Use:", sys.argv[0], "<sat_problem.(sparse, txt)> <MaxTime(s)>"
	sys.exit( 1 )

param = sys.argv[1:]

filename = param[0]
f = filename.split( "/" )[1]
nfile = f.replace( ".sparse", '' )
nfile = nfile.replace( ".txt", '' )
maxTime = int( param[1] )

bqp = BQP( filename )

pattern = "{:5s}{:14s}{:4s}{:8s}{:12s}{:10s}"
patternResult = "{:<5s}{:14s}{:<4d}{:<8.2f}{:<12d}{:<10d}"
file = open( "resultsList1.txt", 'a' )
file.write( pattern.format( "alg", "instance", "rep", 'time', 'iterations', 'value' ) + '\n' )
file.close()
print pattern.format( "alg", "instance", "rep", 'time', 'iterations', 'value' )

ti = []
iterations = []
values = []

# random local search
for z in xrange( 1, 11 ):
	result = bqp.randomLocalSearch( maxTime )
	file = open( "resultsList1.txt", 'a' )
	print patternResult.format( "0.50", nfile, z, result[2], result[1], result[0] ), result[3], result[4]
	file.write( patternResult.format( "0.50", nfile, z, result[2], result[1], result[0] ) + '\n' )
	file.close()
	ti.append( result[2] )
	iterations.append( result[1] )
	values.append( result[0] )

print str( "0.50" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( ti ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( ti ) ) )
print str( "0.50" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( iterations ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( iterations ) ) )
print str( "0.50" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( values ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( values ) ) )

ti = []
iterations = []
values = []

# best improvement
for z in xrange( 1, 11 ):
	result = bqp.bestImprovementSearch( maxTime )
	file = open( "resultsList1.txt", 'a' )
	print patternResult.format( "MM", nfile, z, result[2], result[1], result[0] ), result[3], result[4]
	file.write( patternResult.format( "MM", nfile, z, result[2], result[1], result[0] ) + '\n' )
	file.close()
	ti.append( result[2] )
	iterations.append( result[1] )
	values.append( result[0] )

print str( "MM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( ti ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( ti ) ) )
print str( "MM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( iterations ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( iterations ) ) )
print str( "MM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( values ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( values ) ) )

ti = []
iterations = []
values = []

# first improvement
for z in xrange( 1, 11 ):
	result = bqp.firstImprovementSearch( maxTime )
	file = open( "resultsList1.txt", 'a' )
	print patternResult.format( "PM", nfile, z, result[2], result[1], result[0] ), result[3], result[4]
	file.write( patternResult.format( "PM", nfile, z, result[2], result[1], result[0] ) + '\n' )
	file.close()
	ti.append( result[2] )
	iterations.append( result[1] )
	values.append( result[0] )

print str( "PM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( ti ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( ti ) ) )
print str( "PM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( iterations ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( iterations ) ) )
print str( "PM" ) + " " + nfile + " " + str( '{0:,.2f}'.format( bqp.mean( values ) ) ), str( '{0:,.2f}'.format( bqp.pstdev( values ) ) )