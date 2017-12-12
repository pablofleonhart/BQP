import os
import sys
from scipy.stats import *

def mean( data ):
    n = len( data )
    if n < 1:
        return 0.00

    return sum( data ) / n

def _ss( data ):
    c = mean( data )
    ss = sum( ( x - c ) ** 2 for x in data )
    return ss

def pstdev( data ):
    n = len( data )
    if n < 2:
        return 0.00
    ss = _ss( data )
    pvar = ss / n
    return pvar ** 0.5

la = []
la2 = []
la3 = []
la4 = []
la5 = []
la6 = []
la7 = []
la8 = []
la9 = []
la10 = []
lb = []
lb2 = []
lb3 = []
lb4 = []
lb5 = []
lb6 = []
lb7 = []
lb8 = []
lb9 = []
lb10 = []

it = []
it2 = []
it3 = []
it4 = []
it5 = []
it6 = []
it7 = []
it8 = []
it9 = []
it10 = []
itb = []
itb2 = []
itb3 = []
itb4 = []
itb5 = []
itb6 = []
itb7 = []
itb8 = []
itb9 = []
itb10 = []

tia = []
tia2 = []
tia3 = []
tia4 = []
tia5 = []
tia6 = []
tia7 = []
tia8 = []
tia9 = []
tia10 = []
tib = []
tib2 = []
tib3 = []
tib4 = []
tib5 = []
tib6 = []
tib7 = []
tib8 = []
tib9 = []
tib10 = []

file = open( "exec_p_25R.txt", "r" )

finish = False
while not finish:
	line = file.readline()
	if not line:
		finish = True
	else:
		line = line.split()
		if line[0] == "F":
			if line[1] == "p3000-1.txt":
				la.append( float( line[4] ) )
				it.append( float( line[5] ) )
				tia.append( float( line[6] ) )
			elif line[1] == "p3000-2.txt":
				la2.append( float( line[4] ) )
				it2.append( float( line[5] ) )
				tia2.append( float( line[6] ) )
			elif line[1] == "p4000-1.txt":
				la3.append( float( line[4] ) )
				it3.append( float( line[5] ) )
				tia3.append( float( line[6] ) )
			elif line[1] == "p4000-2.txt":
				la4.append( float( line[4] ) )
				it4.append( float( line[5] ) )
				tia4.append( float( line[6] ) )
			elif line[1] == "p5000-1.txt":
				la5.append( float( line[4] ) )
				it5.append( float( line[5] ) )
				tia5.append( float( line[6] ) )
			elif line[1] == "p5000-2.txt":
				la6.append( float( line[4] ) )
				it6.append( float( line[5] ) )
				tia6.append( float( line[6] ) )
			elif line[1] == "p6000-1.txt":
				la7.append( float( line[4] ) )
				it7.append( float( line[5] ) )
				tia7.append( float( line[6] ) )
			elif line[1] == "p6000-2.txt":
				la8.append( float( line[4] ) )
				it8.append( float( line[5] ) )
				tia8.append( float( line[6] ) )
			elif line[1] == "p7000-1.txt":
				la9.append( float( line[4] ) )
				it9.append( float( line[5] ) )
				tia9.append( float( line[6] ) )
			elif line[1] == "p7000-2.txt":
				la10.append( float( line[4] ) )
				it10.append( float( line[5] ) )
				tia10.append( float( line[6] ) )

file.close()

file = open( "exec_p_10F.txt", "r" )

finish = False
while not finish:
	line = file.readline()
	if not line:
		finish = True
	else:
		line = line.split()
		if line[0] == "F":
			if line[1] == "p3000-1.txt":
				lb.append( float( line[4] ) )
				itb.append( float( line[5] ) )
				tib.append( float( line[6] ) )
			elif line[1] == "p3000-2.txt":
				lb2.append( float( line[4] ) )
				itb2.append( float( line[5] ) )
				tib2.append( float( line[6] ) )
			elif line[1] == "p4000-1.txt":
				lb3.append( float( line[4] ) )
				itb3.append( float( line[5] ) )
				tib3.append( float( line[6] ) )
			elif line[1] == "p4000-2.txt":
				lb4.append( float( line[4] ) )
				itb4.append( float( line[5] ) )
				tib4.append( float( line[6] ) )
			elif line[1] == "p5000-1.txt":
				lb5.append( float( line[4] ) )
				itb5.append( float( line[5] ) )
				tib5.append( float( line[6] ) )
			elif line[1] == "p5000-2.txt":
				lb6.append( float( line[4] ) )
				itb6.append( float( line[5] ) )
				tib6.append( float( line[6] ) )
			elif line[1] == "p6000-1.txt":
				lb7.append( float( line[4] ) )
				itb7.append( float( line[5] ) )
				tib7.append( float( line[6] ) )
			elif line[1] == "p6000-2.txt":
				lb8.append( float( line[4] ) )
				itb8.append( float( line[5] ) )
				tib8.append( float( line[6] ) )
			elif line[1] == "p7000-1.txt":
				lb9.append( float( line[4] ) )
				itb9.append( float( line[5] ) )
				tib9.append( float( line[6] ) )
			elif line[1] == "p7000-2.txt":
				lb10.append( float( line[4] ) )
				itb10.append( float( line[5] ) )
				tib10.append( float( line[6] ) )

file.close()

print "{:.3f}".format( mean( la )/1000.0 ), "{:.3f}".format( pstdev( la )/1000.0 )
print "{:.3f}".format( mean( it ) ), "{:.3f}".format( pstdev( it ) )
print "{:.3f}".format( mean( tia ) ), "{:.3f}".format( pstdev( tia ) )
print "{:.3f}".format( mean( la2 )/1000.0 ), "{:.3f}".format( pstdev( la2 )/1000.0 )
print "{:.3f}".format( mean( it2 ) ), "{:.3f}".format( pstdev( it2 ) )
print "{:.3f}".format( mean( tia2 ) ), "{:.3f}".format( pstdev( tia2 ) )
print "{:.3f}".format( mean( la3 )/1000.0 ), "{:.3f}".format( pstdev( la3 )/1000.0 )
print "{:.3f}".format( mean( it3 ) ), "{:.3f}".format( pstdev( it3 ) )
print "{:.3f}".format( mean( tia3 ) ), "{:.3f}".format( pstdev( tia3 ) )
print "{:.3f}".format( mean( la4 )/1000.0 ), "{:.3f}".format( pstdev( la4 )/1000.0 )
print "{:.3f}".format( mean( it4 ) ), "{:.3f}".format( pstdev( it4 ) )
print "{:.3f}".format( mean( tia4 ) ), "{:.3f}".format( pstdev( tia4 ) )
print "{:.3f}".format( mean( la5 )/1000.0 ), "{:.3f}".format( pstdev( la5 )/1000.0 )
print "{:.3f}".format( mean( it5 ) ), "{:.3f}".format( pstdev( it5 ) )
print "{:.3f}".format( mean( tia5 ) ), "{:.3f}".format( pstdev( tia5 ) )
print "{:.3f}".format( mean( la6 )/1000.0 ), "{:.3f}".format( pstdev( la6 )/1000.0 )
print "{:.3f}".format( mean( it6 ) ), "{:.3f}".format( pstdev( it6 ) )
print "{:.3f}".format( mean( tia6 ) ), "{:.3f}".format( pstdev( tia6 ) )
print "{:.3f}".format( mean( la7 )/1000.0 ), "{:.3f}".format( pstdev( la7 )/1000.0 )
print "{:.3f}".format( mean( it7 ) ), "{:.3f}".format( pstdev( it7 ) )
print "{:.3f}".format( mean( tia7 ) ), "{:.3f}".format( pstdev( tia7 ) )
print "{:.3f}".format( mean( la8 )/1000.0 ), "{:.3f}".format( pstdev( la8 )/1000.0 )
print "{:.3f}".format( mean( it8 ) ), "{:.3f}".format( pstdev( it8 ) )
print "{:.3f}".format( mean( tia8 ) ), "{:.3f}".format( pstdev( tia8 ) )
print "{:.3f}".format( mean( la9 )/1000.0 ), "{:.3f}".format( pstdev( la9 )/1000.0 )
print "{:.3f}".format( mean( it9 ) ), "{:.3f}".format( pstdev( it9 ) )
print "{:.3f}".format( mean( tia9 ) ), "{:.3f}".format( pstdev( tia9 ) )
print "{:.3f}".format( mean( la10 )/1000.0 ), "{:.3f}".format( pstdev( la10 )/1000.0 )
print "{:.3f}".format( mean( it10 ) ), "{:.3f}".format( pstdev( it10 ) )
print "{:.3f}".format( mean( tia10 ) ), "{:.3f}".format( pstdev( tia10 ) )

print "{:.3f}".format( mean( lb )/1000.0 ), "{:.3f}".format( pstdev( lb )/1000.0 )
print "{:.3f}".format( mean( itb ) ), "{:.3f}".format( pstdev( itb ) )
print "{:.3f}".format( mean( tib ) ), "{:.3f}".format( pstdev( tib ) )
print "{:.3f}".format( mean( lb2 )/1000.0 ), "{:.3f}".format( pstdev( lb2 )/1000.0 )
print "{:.3f}".format( mean( itb2 ) ), "{:.3f}".format( pstdev( itb2 ) )
print "{:.3f}".format( mean( tib2 ) ), "{:.3f}".format( pstdev( tib2 ) )
print "{:.3f}".format( mean( lb3 )/1000.0 ), "{:.3f}".format( pstdev( lb3 )/1000.0 )
print "{:.3f}".format( mean( itb3 ) ), "{:.3f}".format( pstdev( itb3 ) )
print "{:.3f}".format( mean( tib3 ) ), "{:.3f}".format( pstdev( tib3 ) )
print "{:.3f}".format( mean( lb4 )/1000.0 ), "{:.3f}".format( pstdev( lb4 )/1000.0 )
print "{:.3f}".format( mean( itb4 ) ), "{:.3f}".format( pstdev( itb4 ) )
print "{:.3f}".format( mean( tib4 ) ), "{:.3f}".format( pstdev( tib4 ) )
print "{:.3f}".format( mean( lb5 )/1000.0 ), "{:.3f}".format( pstdev( lb5 )/1000.0 )
print "{:.3f}".format( mean( itb5 ) ), "{:.3f}".format( pstdev( itb5 ) )
print "{:.3f}".format( mean( tib5 ) ), "{:.3f}".format( pstdev( tib5 ) )
print "{:.3f}".format( mean( lb6 )/1000.0 ), "{:.3f}".format( pstdev( lb6 )/1000.0 )
print "{:.3f}".format( mean( itb6 ) ), "{:.3f}".format( pstdev( itb6 ) )
print "{:.3f}".format( mean( tib6 ) ), "{:.3f}".format( pstdev( tib6 ) )
print "{:.3f}".format( mean( lb7 )/1000.0 ), "{:.3f}".format( pstdev( lb7 )/1000.0 )
print "{:.3f}".format( mean( itb7 ) ), "{:.3f}".format( pstdev( itb7 ) )
print "{:.3f}".format( mean( tib7 ) ), "{:.3f}".format( pstdev( tib7 ) )
print "{:.3f}".format( mean( lb8 )/1000.0 ), "{:.3f}".format( pstdev( lb8 )/1000.0 )
print "{:.3f}".format( mean( itb8 ) ), "{:.3f}".format( pstdev( itb8 ) )
print "{:.3f}".format( mean( tib8 ) ), "{:.3f}".format( pstdev( tib8 ) )
print "{:.3f}".format( mean( lb9 )/1000.0 ), "{:.3f}".format( pstdev( lb9 )/1000.0 )
print "{:.3f}".format( mean( itb9 ) ), "{:.3f}".format( pstdev( itb9 ) )
print "{:.3f}".format( mean( tib9 ) ), "{:.3f}".format( pstdev( tib9 ) )
print "{:.3f}".format( mean( lb10 )/1000.0 ), "{:.3f}".format( pstdev( lb10 )/1000.0 )
print "{:.3f}".format( mean( itb10 ) ), "{:.3f}".format( pstdev( itb10 ) )
print "{:.3f}".format( mean( tib10 ) ), "{:.3f}".format( pstdev( tib10 ) )

#significancia de p-value < 0.05
print la, lb
Ue_value, p = mannwhitneyu( la, lb )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

print la2, lb2
Ue_value, p = mannwhitneyu( la2, lb2 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la3, lb3 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la4, lb4 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la5, lb5 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la6, lb6 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la7, lb7 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la8, lb8 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la9, lb9 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'

Ue_value, p = mannwhitneyu( la10, lb10 )
pe_value = 2 * p

if pe_value <= 0.05:
	print pe_value, 'S'
else:
	print pe_value, 'NS'