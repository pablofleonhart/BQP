from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import *
import numpy as np

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

file = open( "resultsMaxSAT.txt", "r" )
cf = []
ckf = []
cp = []
ckp = []
c0 = []
c1 = []
c2 = []
c3 = []
c4 = []
c5 = []
c6 = []
c7 = []
c8 = []
c9 = []
c10 = []
c11 = []

gf = []
gkf = []
gp = []
gkp = []
g0 = []
g1 = []
g2 = []
g3 = []
g4 = []
g5 = []
g6 = []
g7 = []
g8 = []
g9 = []
g10 = []
g11 = []

finish = False
k = "0"
while not finish:
	line = file.readline()
	if not line:
		finish = True

	else:
		line = line.split()
		if line[1] == "flat50-1" and line[0] == "C":
			if line[2] == "0":
				c0.append( int( line[4] ) )
			if line[2] == "1":
				c1.append( int( line[4] ) )
			if line[2] == "2":
				c2.append( int( line[4] ) )
			if line[2] == "3":
				c3.append( int( line[4] ) )
			if line[2] == "4":
				c4.append( int( line[4] ) )
			if line[2] == "5":
				c5.append( int( line[4] ) )
			cf.append( int( line[4] ) )
			ckf.append( line[2] )
		elif line[1] == "par8-5-c" and line[0] == "C":
			if line[2] == "0":
				c6.append( int( line[4] ) )
			if line[2] == "1":
				c7.append( int( line[4] ) )
			if line[2] == "2":
				c8.append( int( line[4] ) )
			if line[2] == "3":
				c9.append( int( line[4] ) )
			if line[2] == "4":
				c10.append( int( line[4] ) )
			if line[2] == "5":
				c11.append( int( line[4] ) )
			cp.append( int( line[4] ) )
			ckp.append( line[2] )
		elif line[1] == "flat50-1" and line[0] == "G":
			if line[2] == "0":					
				g0.append( int( line[4] ) )
			if line[2] == "1":
				g1.append( int( line[4] ) )
			if line[2] == "2":
				g2.append( int( line[4] ) )
			if line[2] == "3":
				g3.append( int( line[4] ) )
			if line[2] == "4":
				g4.append( int( line[4] ) )
			if line[2] == "5":
				g5.append( int( line[4] ) )
			gf.append( int( line[4] ) )
			gkf.append( line[2] )
		elif line[1] == "par8-5-c" and line[0] == "G":
			if line[2] == "0":
				g6.append( int( line[4] ) )
			if line[2] == "1":
				g7.append( int( line[4] ) )
			if line[2] == "2":
				g8.append( int( line[4] ) )
			if line[2] == "3":
				g9.append( int( line[4] ) )
			if line[2] == "4":
				g10.append( int( line[4] ) )
			if line[2] == "5":
				g11.append( int( line[4] ) )
			gp.append( int( line[4] ) )
			gkp.append( line[2] )

file.close()

#print len(cf), len(ckf)
data = np.core.records.fromarrays( [ckf, cf], dtype=[( 'k', '|U5' ), ( 'value', '<i8' )] )
#print data

f, p = stats.f_oneway(data[data['k'] == '0'].value,
                      data[data['k'] == '1'].value,
                      data[data['k'] == '2'].value,
                      data[data['k'] == '3'].value,
                      data[data['k'] == '4'].value,
                      data[data['k'] == '5'].value)

print f, p
print "here", stats.f_oneway( c0, c1, c2, c3, c4, c5 )[1]
mc = MultiComparison( data['value'], data['k'] )
result = mc.tukeyhsd()
 
print(result)
print(mc.groupsunique)
#print mc.allpairtest(stats.ttest_rel, method='b')[0]

data = np.core.records.fromarrays( [ckp, cp], dtype=[( 'k', '|U5' ), ( 'value', '<i8' )] )
f, p = stats.f_oneway(data[data['k'] == '0'].value,
                      data[data['k'] == '1'].value,
                      data[data['k'] == '2'].value,
                      data[data['k'] == '3'].value,
                      data[data['k'] == '4'].value,
                      data[data['k'] == '5'].value)

print f, p
print "here", stats.f_oneway( c6, c7, c8, c9, c10, c11 )[1]
#print data
mc = MultiComparison( data['value'], data['k'] )
result = mc.tukeyhsd()

print ''
print ''
print(result)
print(mc.groupsunique)
#print mc.allpairtest(stats.ttest_rel, method='b')[0]

data = np.core.records.fromarrays( [gkf, gf], dtype=[( 'k', '|U5' ), ( 'value', '<i8' )] )
f, p = stats.f_oneway(data[data['k'] == '0'].value,
                      data[data['k'] == '1'].value,
                      data[data['k'] == '2'].value,
                      data[data['k'] == '3'].value,
                      data[data['k'] == '4'].value,
                      data[data['k'] == '5'].value)

print f, p
print "here", stats.f_oneway( g0, g1, g2, g3, g4, g5 )[1]
#print data
mc = MultiComparison( data['value'], data['k'] )
result = mc.tukeyhsd()
 
print ''
print ''
print(result)
print(mc.groupsunique)
#print mc.allpairtest(stats.ttest_rel, method='b')[0]

data = np.core.records.fromarrays( [gkp, gp], dtype=[( 'k', '|U5' ), ( 'value', '<i8' )] )
f, p = stats.f_oneway(data[data['k'] == '0'].value,
                      data[data['k'] == '1'].value,
                      data[data['k'] == '2'].value,
                      data[data['k'] == '3'].value,
                      data[data['k'] == '4'].value,
                      data[data['k'] == '5'].value)

print f, p
print "here", stats.f_oneway( g6, g7, g8, g9, g10, g11 )[1]
#print data
mc = MultiComparison( data['value'], data['k'] )
result = mc.tukeyhsd()

print ''
print ''
print(result)
print(mc.groupsunique)
#print mc.allpairtest(stats.ttest_rel, method='b')[0]
#significancia de p-value < 0.05
#U_value, p = mannwhitneyu( lista1, lista2 )
#p_value = 2 * p

#print p_value
print stats.f_oneway( c0, g0 )[1]
U_value, p = mannwhitneyu( c0, g0 )
print str( '{0:,.2f}'.format( mean( c0 ) ) ), str( '{0:,.2f}'.format( pstdev( c0 ) ) )
print str( '{0:,.2f}'.format( mean( g0 ) ) ), str( '{0:,.2f}'.format( pstdev( g0 ) ) )
#print 2 * p

print stats.f_oneway( c1, g1 )[1]
U_value, p = mannwhitneyu( c1, g1 )
print str( '{0:,.2f}'.format( mean( c1 ) ) ), str( '{0:,.2f}'.format( pstdev( c1 ) ) )
print str( '{0:,.2f}'.format( mean( g1 ) ) ), str( '{0:,.2f}'.format( pstdev( g1 ) ) )
#print 2 * p

print stats.f_oneway( c2, g2 )[1]
U_value, p = mannwhitneyu( c2, g2 )
print str( '{0:,.2f}'.format( mean( c2 ) ) ), str( '{0:,.2f}'.format( pstdev( c2 ) ) )
print str( '{0:,.2f}'.format( mean( g2 ) ) ), str( '{0:,.2f}'.format( pstdev( g2 ) ) )
#print 2 * p

print stats.f_oneway( c3, g3 )[1]
U_value, p = mannwhitneyu( c3, g3 )
print str( '{0:,.2f}'.format( mean( c3 ) ) ), str( '{0:,.2f}'.format( pstdev( c3 ) ) )
print str( '{0:,.2f}'.format( mean( g3 ) ) ), str( '{0:,.2f}'.format( pstdev( g3 ) ) )
#print 2 * p

print stats.f_oneway( c4, g4 )[1]
U_value, p = mannwhitneyu( c4, g4 )
print str( '{0:,.2f}'.format( mean( c4 ) ) ), str( '{0:,.2f}'.format( pstdev( c4 ) ) )
print str( '{0:,.2f}'.format( mean( g4 ) ) ), str( '{0:,.2f}'.format( pstdev( g4 ) ) )
#print 2 * p

print stats.f_oneway( c5, g5 )[1]
U_value, p = mannwhitneyu( c5, g5 )
print str( '{0:,.2f}'.format( mean( c5 ) ) ), str( '{0:,.2f}'.format( pstdev( c5 ) ) )
print str( '{0:,.2f}'.format( mean( g5 ) ) ), str( '{0:,.2f}'.format( pstdev( g5 ) ) )
#print 2 * p

print stats.f_oneway( c6, g6 )[1]
U_value, p = mannwhitneyu( c6, g6 )
print str( '{0:,.2f}'.format( mean( c6 ) ) ), str( '{0:,.2f}'.format( pstdev( c6 ) ) )
print str( '{0:,.2f}'.format( mean( g6 ) ) ), str( '{0:,.2f}'.format( pstdev( g6 ) ) )
#print 2 * p

print stats.f_oneway( c7, g7 )[1]
U_value, p = mannwhitneyu( c7, g7 )
print str( '{0:,.2f}'.format( mean( c7 ) ) ), str( '{0:,.2f}'.format( pstdev( c7 ) ) )
print str( '{0:,.2f}'.format( mean( g7 ) ) ), str( '{0:,.2f}'.format( pstdev( g7 ) ) )
#print 2 * p

print stats.f_oneway( c8, g8 )[1]
U_value, p = mannwhitneyu( c8, g8 )
print str( '{0:,.2f}'.format( mean( c8 ) ) ), str( '{0:,.2f}'.format( pstdev( c8 ) ) )
print str( '{0:,.2f}'.format( mean( g8 ) ) ), str( '{0:,.2f}'.format( pstdev( g8 ) ) )
#print 2 * p

print stats.f_oneway( c9, g9 )[1]
U_value, p = mannwhitneyu( c9, g9 )
print str( '{0:,.2f}'.format( mean( c9 ) ) ), str( '{0:,.2f}'.format( pstdev( c9 ) ) )
print str( '{0:,.2f}'.format( mean( g9 ) ) ), str( '{0:,.2f}'.format( pstdev( g9 ) ) )
#print 2 * p

print stats.f_oneway( c10, g10 )[1]
U_value, p = mannwhitneyu( c10, g10 )
print str( '{0:,.2f}'.format( mean( c10 ) ) ), str( '{0:,.2f}'.format( pstdev( c10 ) ) )
print str( '{0:,.2f}'.format( mean( g10 ) ) ), str( '{0:,.2f}'.format( pstdev( g10 ) ) )
#print 2 * p

print stats.f_oneway( c11, g11 )[1]
U_value, p = mannwhitneyu( c11, g11 )
print str( '{0:,.2f}'.format( mean( c11 ) ) ), str( '{0:,.2f}'.format( pstdev( c11 ) ) )
print str( '{0:,.2f}'.format( mean( g11 ) ) ), str( '{0:,.2f}'.format( pstdev( g11 ) ) )
#print 2 * p