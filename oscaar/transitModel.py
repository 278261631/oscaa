'''
    transitModel.py defines the function occultquad(), which 
    loads the C library containing the function of the same 
    name so that analytical transit light curves can be 
    produced in python by passing pythonic arguments to the C code. 
'''
import numpy as np
import ctypes
import os
## Resources on using ctypes:
# http://docs.python.org/2/library/ctypes.html#ctypes.c_float
# http://www.scipy.org/Cookbook/Ctypes#head-0c422ad0dcf3a37f8c16d4cfd85e37e1f7290214
# http://docs.scipy.org/doc/numpy/reference/routines.ctypeslib.html

## Save the absolute path to this document, so as to successfully
## call the C library stored in the oscaar/c/ directory
#oscaarModuleDir = os.path.split(os.path.abspath(oscaar.__file__))[0]
transitModelDir = os.path.dirname(os.path.abspath(__file__))
#print __file__ , os.path.abspath(__file__) , os.path.dirname(os.path.abspath(__file__))
#def occultquad(t,p,ap,i,t0,gamma1=0.23,gamma2=0.45,P=1.58,e=0.0,longPericenter=0.0):

def occultquad(t,modelParams):
    """
    Calculates the analytical transit light curve for a planet occulting a star, according to the formalism
    of Mandel & Agol (2002) [1]_.

    Parameters
    ----------
    t : list or numpy.ndarray
    	List of the times sampled in Julian Date

    modelParams : list
    	List of the planetary system parameters, in the following order: 
    	- :math:`$R_p/R_s$`: Ratio of the radius of the planet to the radius of the star
    	- :math:`$a/R_s$`: Ratio of the semi-major axis to the radius of the star
    	- :math:`$P$`: Orbital period
    	- :math:`$\gamma_1$`: Limb-darkening coefficient, linear
    	- :math:`$\gamma_2$`: Limb-darkening coefficient, quadratic
    	- :math:`$e$`: Eccentricity
    	- `longPericenter`: Longitude of pericenter
    	- :math:`$t_0$`: Mid-transit time (JD)

    Returns
    -------
    F : numpy.ndarray
    	Relative fluxes at each time of the time vector `t`

    .. [1] Mandel & Agol. "Analytic Light Curvesfrom glob import glob
 for Planetary Transit Searches". 
           The Astrophysical Journal, Volume 580, Issue 2, pp. L171-L175. 2002.
    """
    [p,ap,P,i,gamma1,gamma2,e,longPericenter,t0] = modelParams
    #[p,ap,P,i,gamma1,gamma2,e,longPericenter,t0] = modelParams

    ###################################################################################################
    ## Ctypes definitions from C-libraries
    lib = np.ctypeslib.load_library(os.path.join(transitModelDir,'c','windowsBinaries','analyticalTransitModel.so'),'.') 	## Loads .so library
    #lib = np.ctypeslib.load_library('transit1forLMLS.so','.')
    occultquadC = lib.occultquad
    occultquadC.argtypes = [np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS'),	#t
                               ctypes.c_double,	# p
                               ctypes.c_double,	# ap
                               ctypes.c_double,	# P
                               ctypes.c_double,	# i
                               ctypes.c_double,	# gamma1
                               ctypes.c_double,	# gamma2
                               ctypes.c_double,	# e
                               ctypes.c_double, # longPericenter
                               ctypes.c_double, # t0
                               ctypes.c_double,	# n
                               np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS')]	# F
    ## argtypes defines what each function argument's type will be using the numpy.ctypeslib and ctypes libraries. 
    ## NOTE!: If vector input is going to be a vector of C-floats, use np.ctypeslib.ndpointer(np.float32,flags='aligned,C_CONTIGUOUS')
    ##        If vector input is going to be a vector of C-doubles, use np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS')

    ## The arguments of occultquad are: occultquad(float *t, float *phi, float p, float ap, float P, float i, float gamma1, 
    ##											   float gamma2, double e, double longPericenter, double t0, float n, float *F);

    occultquadC.restype = None	## Put the return type of the function here. If "return void" in C func, restype=None

    #################################################################
   
    ## np.require() will force the ndarrays to the right dtype as assigned in the `argtypes` list.
    n = np.float64(len(t))
    t = np.require(t,np.float64)
    F = np.empty_like(t,dtype=np.float64)
    occultquadC(t, p,  ap,  P,  i,  gamma1,  gamma2, e,longPericenter, t0,  n,  F)	## Simulate fake data
    return F

def ellipk(k):
    """
    Computes polynomial approximation for the complete elliptic integral of the first kind (Hasting's approximation):
    """
    ###################################################################################################
    ## Ctypes definitions from C-libraries
    lib = np.ctypeslib.load_library(os.path.join(oscaarModuleDir,'c','analyticalTransitModel.so'),'.') 	## Loads .so library
    Kfunction = lib.K
    Kfunction.argtypes = [ctypes.c_double]	
    ## argtypes defines what each function argument's type will be using the numpy.ctypeslib and ctypes libraries. 
    ## NOTE!: If vector input is going to be a vector of C-floats, use np.ctypeslib.ndpointer(np.float32,flags='aligned,C_CONTIGUOUS')
    ##        If vector input is going to be a vector of C-doubles, use np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS')

    ## The arguments of occultquad are: occultquad(float *t, float *phi, float p, float ap, float P, float i, float gamma1, 
    ##											   float gamma2, double e, double longPericenter, double t0, float n, float *F);

    Kfunction.restype = ctypes.c_double	## Put the return type of the function here. If "return void" in C func, restype=None

    #################################################################
    return Kfunction(k)

def ellipe(k):
    """
    Computes polynomial approximation for the complete elliptic integral of the second kind (Hasting's approximation)
    """
    ###################################################################################################
    ## Ctypes definitions from C-libraries
    lib = np.ctypeslib.load_library(os.path.join(oscaarModuleDir,'c','analyticalTransitModel.so'),'.') 	## Loads .so library
    Efunction = lib.E
    Efunction.argtypes = [ctypes.c_double]	
    ## argtypes defines what each function argument's type will be using the numpy.ctypeslib and ctypes libraries. 
    ## NOTE!: If vector input is going to be a vector of C-floats, use np.ctypeslib.ndpointer(np.float32,flags='aligned,C_CONTIGUOUS')
    ##        If vector input is going to be a vector of C-doubles, use np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS')

    ## The arguments of occultquad are: occultquad(float *t, float *phi, float p, float ap, float P, float i, float gamma1, 
    ##											   float gamma2, double e, double longPericenter, double t0, float n, float *F);

    Efunction.restype = ctypes.c_double	## Put the return type of the function here. If "return void" in C func, restype=None

    #################################################################
    return Efunction(k)

def ellippi(n,k):
    """
    Computes the complete elliptical integral of the third kind using the algorithm of Bulirsch (1965)
    """
    ###################################################################################################
    ## Ctypes definitions from C-libraries
    lib = np.ctypeslib.load_library(os.path.join(oscaarModuleDir,'c','analyticalTransitModel.so'),'.') 	## Loads .so library
    PIfunction = lib.PI
    PIfunction.argtypes = [ctypes.c_double,ctypes.c_double]	
    ## argtypes defines what each function argument's type will be using the numpy.ctypeslib and ctypes libraries. 
    ## NOTE!: If vector input is going to be a vector of C-floats, use np.ctypeslib.ndpointer(np.float32,flags='aligned,C_CONTIGUOUS')
    ##        If vector input is going to be a vector of C-doubles, use np.ctypeslib.ndpointer(np.float64,flags='aligned,C_CONTIGUOUS')

    ## The arguments of occultquad are: occultquad(float *t, float *phi, float p, float ap, float P, float i, float gamma1, 
    ##											   float gamma2, double e, double longPericenter, double t0, float n, float *F);

    PIfunction.restype = ctypes.c_double	## Put the return type of the function here. If "return void" in C func, restype=None

    #################################################################
    return PIfunction(n,k)
