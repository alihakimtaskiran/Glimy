import platform
import os
import numpy as np
from . import geo1D, geo2D, geo3D
oss=platform.system()
import zipfile

if oss=="Linux":#The most Prior
    tmp="/tmp/MemoriesWillFade"
elif oss=="Windows":#The most Ubiqious
    tmp="C://Users/Default/AppData/Local/CEM/MemoriesWillFade"
elif oss=="Darwin":#
    tmp="/tmp/MemoriesWillFade"

try:       
    os.mkdir(tmp)
except:
    pass

class Grid(object):
    """
    Creates a reality
    """
    def __init__(self, dim, deltaS, deltaT, metric="Euclid"):
        
        if not type(dim)==int:
            raise TypeError("Number of dimensions must be a float")
        if not dim in {1,2,3}:
            raise ValueError()
        if not type(deltaS) in {float,int}:
            raise TypeError("Spatial delta must be a float")
        if not type(deltaT) in {float,int}:
            raise TypeError("Temporal delta must be a float")
        
        
        self.__guv=np.array([[0]*dim]*dim)
        if metric.lower()=="euclid":
            for i in range(dim):
                self.__guv[i][i]=1 
            self.__curvilinear=0
        else:
            self.__curvilinear=1
        self.__dim=dim
        self.__deltaS=deltaS
        self.__deltaT=deltaT
        self.__objects=[]
        
        
        
    def add(self, arg):
        """
        Adds new objects into the Grid
        """
        __=type(arg)
        if __ in {tuple, list, set}:
            self.__add_multiple(arg)
        else:
            if not __ in {geo1D.Line, geo2D.Plane, geo3D.RecPrism, geo3D.Sphere, geo3D.Cylinder} and self.__dim==3:
                raise TypeError("Only given types are defined on space")
            if not __ in {geo2D.Rectangle, geo2D.Circle} and self.__dim==2:
                raise TypeError("Only given types are defined on plane")
            if not __ == geo1D.Line and self.__dim==1:
                raise TypeError("Only given types are defined on line")
            self.__objects.append(arg)

    def __add_multiple(self, argv):
        for element in argv:
            __=type(element)

            if not __ in {geo1D.Line, geo2D.Plane, geo3D.RecPrism, geo3D.Sphere, geo3D.Cylinder} and self.__dim==3:
                raise TypeError("Only given types are defined on space")
            if not __ in {geo2D.Rectangle, geo2D.Circle} and self.__dim==2:
                raise TypeError("Only given types are defined on plane")
            if not __ == geo1D.Line and self.__dim==1:
                raise TypeError("Only given types are defined on line")
            self.__objects.append(element)
     

    def TopoRender(self):
        file=open(tmp+"/structure.tgf","w") #topological geometry file
        file.write(f"PREAMBLE\n{self.__dim}\n{self.__curvilinear}\n")
        _____={geo3D.RecPrism, geo3D.Sphere, geo3D.Cylinder}
        for element in self.__objects:
            ___=type(element)
            if ___ in _____:
                file.write(repr(element))
            
            elif ___ == geo2D.Plane:
                file.write(element.mixtape())
                
                    
        file.close()
        file=open(tmp+"/metric.guv","w")
        file.write(str(self.__guv))
        file.close()
    
    def RenderWiev(self):
        pass
    
    def EMRender(self, renderer="FDTD"):
        if renderer=="FDTD":#Finite-Difference Time-Domain
            pass
        elif renderer=="FDFD":#Finite-Difference Frequency-Domain
            pass
        
        
        
