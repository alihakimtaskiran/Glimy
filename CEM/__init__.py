import numpy as np
from math import sin,pi
import CEM.geo1D
import CEM.geo2D
import CEM.geo3D
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt


__sqrt_1_2=1/(2)**.5

__sqrt_1_3=1/(3)**.5
c=299792458
PI_2=pi*2
__E=None
__H=None

__E_mul=None
__H_mul=None

__nx, __ny, __nz=None, None, None

class Continuum(object):
    def __init__(self, dim, grid_size, ds, ANC=False):
        if not isinstance(dim, int):
            raise TypeError("# of dimensions must be an integer")
        if not dim in {1,2,3}:
            raise ValueError("# of dimensions must be 1, 2 or 3")
        

        if not isinstance(grid_size,(tuple,list)):
            raise TypeError("# of pixels of grid must be carried by a tuple or a list")
        if len(grid_size)!=dim:
            raise ValueError("# of elements in grid must be the same as # of dimensions")
            
        if not isinstance(ds, (int,float)):
            raise TypeError("ds(Δs) must be a float or int")
            
        if not isinstance(ANC, bool):
            raise TypeError("ANC can exist or not. Never both")


        self.__dim=dim
        self.__grid_size=grid_size
        self.__ANC=ANC
        self.__geometries=[]
        self.__ds=ds
        self.__dt=ds/c
        self.__energizers=[]
        self.__n_of_objects=0
        
        
    def add(self, arg):
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add(element)
        elif self.__dim==1 and not isinstance(arg, (geo1D.Line,)):
            raise TypeError("In 1-D, only lines are allowed")
        
        elif self.__dim==2 and not isinstance(arg, (geo2D.Rectangle, geo2D.Circle)):
            raise TypeError("In 2-D, only defined geometries are allowed")
        
        elif self.__dim==3 and not isinstance(arg, (geo3D.RectPrism, geo3D.Cylinder, geo3D.Sphere)):
            raise TypeError("In 3-D, only defined geometries are allowed")
        
        else:
            self.__geometries.append(arg)
            self.__n_of_objects+=1
        
        
    def add_energizer(self, arg):
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add_energizer(element)
        elif not isinstance(arg, (DotSource,)):
             raise TypeError("Only defined energizers are allowed")
        else:
            __=arg.inf
            print(__[4]*PI_2*self.__dt)
            if __[0]==0:
                self.__energizers.append((__[:4]+[__[4]*PI_2*self.__dt,__[5]]))
            
        
    def __pre_render(self):
  
            
        
        if self.__dim==1:
            
            Z=376.730313668
            Z_1=1/Z
            
            
            self.__E=np.zeros(self.__grid_size)
            self.__H=np.zeros(self.__grid_size)
            
            self.__H_mul=np.empty(self.__grid_size)
            self.__E_mul=np.empty(self.__grid_size)
            
            
            for i in range(self.__grid_size[0]):
                prior=1000,-1
                for o in range(self.__n_of_objects):
                    if self.__geometries[o].isIn(i) and self.__geometries[o].inf[0]<prior[0]:
                        prior=self.__geometries[o].inf[0],o
                        
                    if prior[-1]==-1:
                        self.__H_mul[i]=Z_1
                        self.__E_mul[i]=Z

                    else:
                        self.__H_mul[i]=Z_1/self.__geometries[prior[-1]].inf[-1]
                        self.__E_mul[i]=Z/self.__geometries[prior[-1]].inf[1]
                    
                        
                    
            
        elif self.__dim==2:
            
            Z=376.730313668*__sqrt_1_2
            Z_1=__sqrt_1_2/Z
            
            self.__E=np.zeros(self.__grid_size)
            self.__H=np.zeros((2,)+self.__grid_size)
            self.__H_mul=np.empty(self.__grid_size)
            self.__E_mul=np.empty(self.__grid_size)
            
            
            for i in range(self.__grid_size[0]):
                for j in range(self.__grid_size[1]):
                    prior=1000,-1
                    for o in range(self.__n_of_objects):
                        if self.__geometries[o].isIn((i,j)) and self.__geometries[o].inf[0]<prior[0]:
                            prior=self.__geometries[o].inf[0],o
                        if prior[-1]==-1:
                            self.__H_mul[i][j]=Z_1
                            self.__E_mul[i][j]=Z

                        else:
                            self.__H_mul[i][j]=Z_1/self.__geometries[prior[-1]].inf[-1]
                            self.__E_mul[i][j]=Z/self.__geometries[prior[-1]].inf[1]
                            
            plt.imshow(self.__E_mul)
                        
            
            
            
            
        elif self.__dim==3:
            
            Z=376.730313668*__sqrt_1_3
            Z_1=__sqrt_1_3/Z
            
            self.__E=np.zeros((3,)+self.__grid_size)
            self.__H=np.zeros((3,)+self.__grid_size)
            self.__H_mul=np.empty(self.__grid_size)
            self.__E_mul=np.empty(self.__grid_size)
            
            
            for i in range(self.__grid_size[0]):
                for j in range(self.__grid_size[1]):
                    for k in range(self.__grid_size[2]):
                        prior=1000,-1
                        for o in range(self.__n_of_objects):
                            if self.__geometries[o].isIn((i,j,k)) and self.__geometries[o].inf[0]<prior[0]:
                                prior=self.__geometries[o].inf[0],o
                            if prior[-1]==-1:
                                self.__H_mul[i][j][k]=Z_1
                                self.__E_mul[i][j][k]=Z
    
                            else:
                                self.__H_mul[i][j][k]=Z_1/self.__geometries[prior[-1]].inf[-1]
                                self.__E_mul[i][j][k]=Z/self.__geometries[prior[-1]].inf[1]
                            
        else:
            raise NotImplementedError("Field Arrays couldn't be initialized")
        
            
    def view_structure(self, *slice_):
        self.__pre_render()
        
        if self.__dim==1:
            plt.clf()
            plt.plot(self.__E_mul)
            plt.show()
        elif self.__dim==2:
            plt.clf()
            plt.imshow(self.__E_mul)
            plt.show()

            
            
    def view_field(self):
        if self.__dim==1:
            plt.clf()
            plt.plot(self.__E)     
            plt.show()

        
    def export_for_renderer(self):
        self.__pre_render()
        return self.__dim, self.__grid_size, self.__E, self.__H, self.__E_mul, self.__H_mul, self.__energizers

    def load_from_renderer(self, E, H):
        self.__E=E
        self.__H=H


def __update_H_1D(x):
    return (__E[x+1]-__E[x])*__H_mul[x]
def __update_E_1D(x):
    return (__H[x]-__H[x-1])*__E_mul[x]
            


def Render(field, n_time_steps):
    if not isinstance(field, Continuum):
        raise TypeError("Only Continuum is rendered")
        
    if not isinstance(n_time_steps, int):
        raise TypeError("# of time steps(n_time_steps) must be an int")
        
    params=field.export_for_renderer()
    cc=cpu_count()
    
    global __E
    global __H
    global __H_mul
    global __E_mul
    
    __E=params[2]
    __H=params[3]
    __E_mul=params[4]
    __H_mul=params[5]
    
    if params[0]==1:
        iterator_E=[i for i in range(params[1][0])]
        iterator_H=iterator_E[:-1]
        
        

        for t in range(n_time_steps):
            mpu=Pool(cc)
            __H[:-1]+=np.array(mpu.map(__update_H_1D, iterator_H))
            mpu=Pool(cc)
            __E+=np.array(mpu.map(__update_E_1D, iterator_E))
            
            
            for source in params[6]:
                if source[0]==0 and source[2][0]<=t<=source[2][1]:
                    __E[source[1][0]]+=source[3]*np.sin(source[4]*t+source[5])
                    
        field.load_from_renderer(__E, __H)
            
        

class DotSource(object):
    def __init__(self, location, presence ,amplitude, frequency, phase=0):
        self.__location=location
        self.__amplitude=amplitude
        self.__frequency=frequency
        self.__phase=phase
        self.__presence=presence
        
    def __repr__(self):
        __=""
        for i in self.__location:
            __+=str(i)+" "
        for i in self.__presence:
            __+=str(i)+" "
        __+=f"Dot Source Amplitude:{self.__amplitude} Frequency:{self.__frequency} Phase:{self.__phase}"
        
        return __

    @property
    def inf(self):
        return [0, self.__location, self.__presence, self.__amplitude, self.__frequency, self.__phase]
