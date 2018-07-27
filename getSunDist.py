'''
Routine to check the distance of a pulsar from the sun at a 
given time of arrival.
Required modules:
astropy
psrqpy
'''

import sys
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS
from astropy.coordinates import get_sun
import astropy.units as u
from astropy.time import Time
import psrqpy
expArgs = 2
sunDistThresh = 10 #sun distance threshold in degrees

def getSunDist(psrName, toa):
	'''
	Function to return the distance (in degrees) between a pulsar and the sun
	Pulsar coordinates is queried from the ATNF catalog
	
	Parameters
	-----------
	psrName : string, name of pulsar
	
	toa : float, Time of Arrival in MJD
	
	Return value
	----------
	Float: Distance of sun from pulsar in degrees
	'''
	
	q = psrqpy.QueryATNF(params=['RaJ','DecJ'], psrs=[psrName])
	t = q.table()

	if len(t) == 0:
		print('No pulsar found with name %s in ATNF! Try again.'%psrName)
		print('\n\n')
		sys.exit(1)
	
	c = SkyCoord(ra=t['RAJ'][0], dec=t['DECJ'][0], frame='icrs', unit=(u.hourangle, u.deg))
	
	t = Time(toa, format='mjd')
	sun = get_sun(t)
	
	sep = c.separation(sun)
	return sep.degree

	
def isNearSun(psrName, toa):
	'''
	Check if the given pulsar was within a distance threshold of the sun
	at the time of arrival
	
	Parameters
	-------------
	psrName : string, name of pulsar
	
	toa : float, Time of Arrival in MJD
	
	Return value
	--------------
	Boolean: True if the distance (in degrees) is smaller than sunDistThresh
	Otherwise returns False
	
	'''
	
	sunDist = getSunDist(psrName, toa)
	if sunDist < sunDistThresh:
		return True
	else:	
		return False
		

if __name__ == '__main__':
	'''
	Main function for direct execution
	Execution format is:
	python getSunDist.py <psrName> <MJD TOA>
	'''
	
	numArgs = len(sys.argv)-1
	if numArgs!=expArgs:
		print('Incorrect number of arguments. Use getSunDist.py <psrName> <MJD TOA>')
	else:
		sunDist = getSunDist(sys.argv[1],float(sys.argv[2]))
		nearSun = isNearSun(sys.argv[1],float(sys.argv[2]))
		print('Distance is %.3f degrees. Proximity to sun is %s.\n'%(sunDist, nearSun))
	
