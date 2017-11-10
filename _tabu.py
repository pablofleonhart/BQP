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
	expression = None
	deltas = []
	fitness = 0

	def __init__( self, filename ):
		file = open( filename, 'r' )

		finish = False
		read = False

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

	def calc2( self, sol ):
		start = time.time()
		result = 0
		for i in xrange( 1, len( sol ) ):
			for j in xrange( self.n + 1 ):
				result += sol[i] * self.q[j][i]

		#print 'nr', result, time.time() - start
		return result

	def calc( self, sol ):
		tsol = np.transpose( sol )
		a = np.dot( sol, self.q )
		#print 'a',a
		return np.dot( a, tsol )

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
		return randint( 1, self.n )

	def randrange_float( self, start, stop, step ):
		return randint( 0, int( ( stop - start ) / step ) ) * step + start

	def mean( self, data ):
	    tam = len( data )
	    if tam < 1:
	        return 0.00

	    return sum( data ) / tam

	def _ss( self, data ):
	    c = mean( data )
	    ss = sum( ( x - c ) ** 2 for x in data )
	    return ss

	def pstdev( self, data ):
	    tam = len( data )
	    if tam < 2:
	        return 0.00

	    ss = _ss( data )
	    pvar = ss / tam
	    return pvar ** 0.5

	def generateExpression( self ):
		content = ''

		for i in xrange( 1, self.n + 1 ):
			content += 'x' + str(i) + ' '

		#print content
		a = sy.Matrix( [sy.var( content )] )		
		b = sy.Matrix( self.q )
		c = sy.Matrix( sy.var( content ) )
		print c

		self.expression = sy.simplify( a * b * c )
		print self.expression

	def calcDelta( self, solution, variable ):
		value = solution[variable]
		ssum = 0
		#print solution, value

		for i in xrange( self.n ):
			if i != variable and solution[i] == 1:
				ssum += self.q[i][variable]

		return ( 1 - ( 2 * value ) ) * ( self.q[variable][variable] + 2 * ssum )

	def oneFlip( self, solution, variable ):
		#print 'receive', solution, variable
		dts = copy.deepcopy( self.deltas )
		result = dts[variable]
		bestDelta = 999999999
		bestVariable = 0

		value = solution[variable]

		for i in xrange( self.n ):
			if i == variable:
				dts[i] *= -1

			else:
				dts[i] += 2 * self.q[variable][i] * ( 1 - 2 * solution[i] ) * ( 1 - 2 * value )

			if dts[i] < bestDelta:				
				solution[variable] = self.invertValue( solution[variable] )
				solution[i] = self.invertValue( solution[i] )

				if solution not in self.tabuList:
					bestDelta = dts[i]
					bestVariable = i

				#print 'best neighbor', bestDelta, solution
				solution[variable] = self.invertValue( solution[variable] )				
				solution[i] = self.invertValue( solution[i] )

		solution[variable] = self.invertValue( solution[variable] )
		#print 'flip', dts, solution, result, self.calc( solution ), bestDelta, bestVariable
		solution[variable] = self.invertValue( solution[variable] )

		#self.fitness = result
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
		bestDelta = 999999999
		bestVariable = 0

		#print 'solution', solution

		for i in xrange( self.n ):
			self.deltas[i] = self.calcDelta( solution, i )

			if self.deltas[i] < bestDelta:
				bestDelta = self.deltas[i]
				bestVariable = i

		#print 'bests', bestDelta, bestVariable, bestValue, self.deltas

		bestValue += bestDelta
		#sol = copy.deepcopy( solution )
		
		#print solution, bestValue, self.deltas
		duration = math.ceil( duration * self.n )

		while noImprove < self.n * 20:					
			result, self.deltas, bt, bv = self.oneFlip( solution, bestVariable )
			
			#print 'bv', bv
			solution[bestVariable] = self.invertValue( solution[bestVariable] )

			#verificar melhor valor
			if bestValue < bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( solution )

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

			#print bestValue
			bestValue += bt
			bestVariable = bv
			#print self.deltas, solution, self.calc( solution )
			#print 'sol', sol
			'''for i in xrange( self.n ):
				result, dt, bt, bv = self.oneFlip( solution, i )

				if result > maxRes:
					maxRes = result
					bdt = dt
					bi = i'''

			#print '$$flip', self.oneFlip( solution, bestVariable )

			#print maxRes, bdt, bi
			#sol[bestVariable] = self.invertValue( sol[bestVariable] )

			#solution[bi] = self.invertValue( solution[bi] )
			#sol[bi] = self.invertValue( sol[bi] )
			#self.deltas = copy.deepcopy( bdt )
			#print bestGlobalValue

		#print bestGlobalValue
		return bestGlobalValue
		#print solution, self.expression.subs( solution )[0]

		'''cSolution = copy.deepcopy( solution )
		tabuList.append( cSolution )
		bestGlobalSolution = cSolution
		bestSolution = cSolution
		bestGlobalValue = self.calc( solution )
		bestValue = bestGlobalValue
		#print solution, bestValue

		while noImprove < self.n * 20:
			#print 'b', bestSolution
			solution = copy.deepcopy( bestSolution )	
			#print solution		
			#start = time.time()
			for i in xrange( self.n ):
				solution[i] = self.invertValue( solution[i] )
				
				start = time.time()
				#value = self.expression.subs( solution )[0]				
				value = self.calc( solution )
				#print solution, value
				print time.time() - start

				if solution not in tabuList and value > bestValue:
					bestSolution = copy.deepcopy( solution )
					bestValue = value

				solution[i] = self.invertValue( solution[i] )
			#print time.time() - start
						

			#print 'it', iterations, bestValue
			if bestValue > bestGlobalValue:
				bestGlobalValue = bestValue
				bestGlobalSolution = copy.deepcopy( bestSolution )

			else:
				noImprove += 1

			tabuList.append( copy.deepcopy( bestSolution ) )

			dr = math.ceil( duration * self.n ) + random.randint( 1, 10 )
			#print dr

			if len( tabuList ) >= dr:
				tabuList.pop( 0 )

			iterations += 1

		#print 'best', duration, bestGlobalValue, bestGlobalSolution
		return bestGlobalValue'''

#param = sys.argv[1:]
#filename = param[0]


pattern = "{:7s}{:14s}{:4s}{:4s}{:12s}{:8s}"
p2 = "{:<7s}{:<14s}{:<4d}{:<4d}{:<12d}{:<8f}"
#file = open( "q5.txt", 'a' )
#file.write( pattern.format( "alg", "instance", "rep", 'time', 'iterations', 'value' ) + '\n' )
#file.close()
print pattern.format( "tenure", "instance", "d", 'rep', 'v', "time" )
#prob = float( param[2] )
#rg = float( param[3] )

ti = []
iterations = []
values = []
durations = [25, 50, 100, 200]
files = ["files/bqp50-1.sparse", "files/bqp100-1.sparse", "files/bqp250-1.sparse", "files/bqp500-1.sparse"]

for file in files:
	f = file.split( "/" )[1]
	nfile = f.replace( ".sparse", '' )

	bqp = BQP( file )

	for z in xrange( 1, 11 ):
		'''s = time.time()
		solution = generateAttempt( n + 1, s )
		#solution = [1 for x in xrange( n + 1 )]
		#print solution
		bvalue = calc( n + 1, q, solution )
		start = time.time()
		ts = time.time()
		drt = 0
		it = 0

		while time.time() - start < crit:
			acp = False
			while not acp:
				p = getVariable( n )
				t = copy.deepcopy( solution )
				t[p] = invValue( t[p] )
				fitness = calc( n + 1, q, t )
				u = randrange_float( 0.0, 1.0, rg )
				if u <= prob:
					acp = True
			it += 1

			if fitness < bvalue:
				bvalue = fitness
				solution = copy.deepcopy( t )
				drt = time.time() - ts
				#print bvalue'''

		#vet = bqp.generateAttempt( time.time() )
		#print vet, bqp.calc( vet )

		#bqp.generateExpression()
		for d in durations:
			start = time.time()
			v = bqp.run( 1/( d * 1.0 ) )
			end = time.time() - start
			print p2.format( 'F', nfile, d, z, v, end )
		#result = bqp.run()

		'''file = open( "q5.txt", 'a' )
		print p2.format( prob, nfile, z+1, drt, it, bvalue )
		file.write( p2.format( prob, nfile, z+1, drt, it, bvalue ) + '\n' )
		file.close()
		ti.append( drt )
		iterations.append( it )
		values.append( bvalue )'''

	#print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( ti ) ) ), str( '{0:,.2f}'.format( pstdev( ti ) ) )
	#print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( iterations ) ) ), str( '{0:,.2f}'.format( pstdev( iterations ) ) )
	#print str( prob ) + " " + nfile + " " + str( '{0:,.2f}'.format( mean( values ) ) ), str( '{0:,.2f}'.format( pstdev( values ) ) )

	for z in xrange( 1, 11 ):
		for d in durations:
			start = time.time()
			v = bqp.run( 1/( d * 1.0 ), True )
			end = time.time() - start
			print p2.format( 'R', nfile, d, z, v, end )