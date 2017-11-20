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

	def quickSort( self, array ):
		less = []
		equal = []
		greater = []

		if len( array ) > 1:
			pivot = array[0][1]
			for x, y in array:
				if y < pivot:
					less.append( ( x, y ) )
				if y == pivot:
					equal.append( ( x, y ) )
				if y > pivot:
					greater.append( ( x, y ) )
			return self.quickSort( greater ) + equal + self.quickSort( less )
		else:
			return array

if ( len( sys.argv ) <= 1 ):
	print "Use:", sys.argv[0], "<sat_problem.(sparse, txt)>"
	sys.exit( 1 )

param = sys.argv[1:]

file = param[0]
f = file.split( "/" )[1]
nfile = f.replace( ".txt", '' )
nfile = f.replace( ".sparse", '' )

bqp = BQP( file )

r = 2
c = 4
b1 = r/2
b2 = r/2

diverseSolutions = []
refSet = [] # mantem as melhores solucoes (b1 + b2)

# constroi C solucoes aleatorias
for i in xrange( c ):
	sol = bqp.generateAttempt( time.time() )	
	#print bqp.calcDelta( sol, 0 )

	fitness = bqp.calc( sol )
	diverseSolutions.append( ( sol, fitness ) )
	'''for i in xrange( bqp.n ):
	bqp.deltas[i] = bqp.calcDelta( sol, i )'''

	'''if bqp.deltas[i] > bestDelta:
		bestDelta = bqp.deltas[i]
		bestVariable = i'''

	#print bqp.deltas

print bqp.quickSort( diverseSolutions )

# calc: utiliza somente ao gerar a solucao para prover o valor inicial de fitness
# calcDelta: utiliza para manter o valor de fitness a partir da solucao construida