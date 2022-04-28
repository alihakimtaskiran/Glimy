import platform
import os
import numpy as np
from . import geo2D, geo3D
oss=platform.system()

if oss=="Linux":
    tmp="/tmp/MemoriesWillFade"
elif oss=="Windows":
    pass
elif oss=="Mac":
    pass

try:       
    os.mkdir(tmp)
except:
    pass

class Grid(object):
    """
    Creates a reality
    """
    def __init__(self, dim, deltaS, deltaT, metric="Flat Space"):
        if not type(dim) is int:
            raise TypeError("Dimensions must be an integer")
        if not type(dim) in {float,int}:
            raise TypeError("Spatial delta must be a float")
        if not type(dim) in {float,int}:
            raise TypeError("Temporal delta must be a float")
        
        if not dim in {1,2,3}:
            raise ValueError("Space is defined to posess 1 to 3 dimensions")
        
        self.__guv=np.array([[0]*dim]*dim)
        if metric=="Flat Space":
            for i in range(dim):
                self.__guv[i][i]=1 
        self.__deltaS=deltaS
        self.__deltaT=deltaT
        self.__dim=dim
        self.__objects=[]
