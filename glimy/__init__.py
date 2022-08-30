import numpy as np
from math import sin,pi
import glimy.geo1D
import glimy.geo2D
import glimy.geo3D
import glimy.curved
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt


G=6.6743e-11
c=299792458
c_2=c**2
PI_2=pi*2
__E=None
__H=None

__E_mul=None
__H_mul=None

__nx, __ny, __nz=None, None, None

class Continuum(object):

    def __init__(self, dim, grid_size, ds):
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
        
        self.__dim=dim
        self.__grid_size=grid_size
        self.__geometries=[]
        self.__ds=ds
        self.__dt=ds/c/(dim**.5)
        self.__energizers=[]
        self.__n_of_objects=0
        self.__curved=False
        self.__celestials=[]

        
    def add(self, arg):
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add(element)
        
        else:
                
            if self.__curved:
                if not isinstance(arg, curved.SingularCelestial):
                    raise TypeError("Only defined Celestial objects are allowed")
                elif not arg.export[0]==self.__dim:
                    raise ValueError("Celestial must live in the same dimensions with the Continuum")
                else:
                    self.__celestials.append(arg)
                      
            
            else:
                if self.__dim==1 and not isinstance(arg, (geo1D.Line,)):
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
            if __[0]==0:
                if len(__[1])!=self.__dim:
                    raise ValueError("DotSource must live in the same dimensional space with Continuum")
                for i in range(self.__dim):
                    if self.__grid_size[i]<=__[1][i]:
                        raise ValueError("Location of the DotSource must be in the grid")
                

                self.__energizers.append((__[:4]+[__[4]*PI_2*self.__dt,__[5]]))
            
    def set_curve(self, curved=False):
        if type(curved)==bool:
            self.__curved=curved
        else:
            raise TypeError("Continuum can be curved or not")
        
    def __pre_render(self):
        
        if self.__curved:
            if self.__dim==1:

                Z=376.730313668
                Z_1=1/Z
                
                
                self.__E=np.zeros(self.__grid_size)
                self.__H=np.zeros(self.__grid_size)
                
                self.__H_mul=np.empty(self.__grid_size)
                self.__E_mul=np.empty(self.__grid_size)
                
                l_c=len(self.__celestials)
                for i in range(self.__grid_size[0]):
                    if l_c==0:
                        self.__E_mul[i]=Z
                        self.__H_mul[i]=Z_1
                    else:
                        for celestial in self.__celestials:
                            c=celestial.export
                            
                            
                            if c[1][0]==i:
                                self.__E_mul[i]=Z/1e260
                                self.__H_mul[i]=Z_1/1e260
                            else:
                                __=1+G*c[2]/abs(c[1][0]-i)/c_2/self.__ds
                                self.__E_mul[i]=Z/__
                                self.__H_mul[i]=Z_1/__
                            
            elif self.__dim==2:
                __sqrt_1_2=1/(2**.5)
                
                Z=376.730313668*__sqrt_1_2
                Z_1=__sqrt_1_2/376.730313668
                
                self.__E=np.zeros(self.__grid_size)
                self.__H=np.zeros((2,)+self.__grid_size)
                self.__H_mul=np.empty(self.__grid_size)
                self.__E_mul=np.empty(self.__grid_size)
                
                l_c=len(self.__celestials)
                
                for i in range(self.__grid_size[0]):
                    for j in range(self.__grid_size[1]):
                        if l_c==0:
                            self.__E_mul[i][j]=Z
                            self.__H_mul[i][j]=Z_1
                        else:
                            for celestial in self.__celestials:
                                c=celestial.export
                                
                                if c[1][0]==i and c[1][1]==j:
                                    self.__E_mul[i][j]=Z/1e260
                                    self.__H_mul[i][j]=Z_1/1e260
                                else:
                                    r=( (c[1][0]-i)**2 + (c[1][1]-j)**2 )**.5
                                    __=1+G*c[2]/r/c_2/self.__ds
                                    self.__E_mul[i][j]=Z/__
                                    self.__H_mul[i][j]=Z_1/__
                                    
                                    
            elif self.__dim==3:
                __sqrt_1_3=1/(3)**.5
                Z=376.730313668*__sqrt_1_3
                Z_1=__sqrt_1_3/376.730313668
                
                self.__E=np.zeros((3,)+self.__grid_size)
                self.__H=np.zeros((3,)+self.__grid_size)
                self.__H_mul=np.empty(self.__grid_size)
                self.__E_mul=np.empty(self.__grid_size)
                
                l_c=len(self.__celestials)
                
                for i in range(self.__grid_size[0]):
                    for j in range(self.__grid_size[1]):
                        for k in range(self.__grid_size[2]):
                            if l_c==0:
                                self.__E_mul[i][j][k]=Z
                                self.__H_mul[i][j][k]=Z_1
                            else:
                                for celestial in self.__celestials:
                                    c=celestial.export
                                    
                                    if c[1][0]==i and c[1][1]==j and  c[1][2]==k:
                                        self.__E_mul[i][j][k]=Z/1e260
                                        self.__H_mul[i][j][k]=Z_1/1e260
                                    else:
                                        r=( (c[1][0]-i)**2 + (c[1][1]-j)**2 + (c[1][2]-k)**2 )**.5
                                        __=1+G*c[2]/r/c_2/self.__ds
                                        self.__E_mul[i][j][k]=Z/__
                                        self.__H_mul[i][j][k]=Z_1/__
                            

        else: 
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
                __sqrt_1_2=1/(2**.5)
                
                Z=376.730313668*__sqrt_1_2
                Z_1=__sqrt_1_2/376.730313668
                
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
                __sqrt_1_3=1/(3)**.5
                Z=376.730313668*__sqrt_1_3
                Z_1=__sqrt_1_3/376.730313668
                
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
        
            
    def view_structure(self,bypass=True, *kwargs):

        if not bypass:
            self.__pre_render()
        
        if self.__dim==1:
            plt.clf()
            plt.plot(self.__E_mul)
            plt.show()
        elif self.__dim==2:
            plt.clf()
            plt.imshow(self.__E_mul)
            plt.show()
            
        elif self.__dim==3:
            plt.clf()
            if kwargs[0]==0:
                plt.imshow(self.__E_mul[kwargs[1], :, :])   
            elif kwargs[0]==1:
                plt.imshow(self.__E_mul[:, kwargs[1], :])
            elif kwargs[0]==2:
                plt.imshow(self.__E_mul[:, :, kwargs[1]])
            plt.show()
            
            
    def view_field(self, *kwargs):
        if self.__dim==1:
            plt.clf()
            plt.plot(self.__E)     
            plt.show()
            
        elif self.__dim==2:
            plt.clf()
            plt.imshow(self.__E)     
            plt.show()
            
        elif self.__dim==3:
            plt.clf()
            if kwargs[0]==0:
                plt.imshow(self.__E[2,kwargs[1], :, :])   
            elif kwargs[0]==1:
                plt.imshow(self.__E[2,:, kwargs[1], :])
            elif kwargs[0]==2:
                plt.imshow(self.__E[2,:, :, kwargs[1]])
            
            
            plt.show()

        
    def export_for_renderer(self):
        self.__pre_render()
        return self.__dim, self.__grid_size, self.__E, self.__H, self.__E_mul, self.__H_mul, self.__energizers

    def load_from_renderer(self, E, H):
        self.__E=E
        self.__H=H
        
    def export_E_field(self):
        return self.__E

def Render(field, n_time_steps):
    if not isinstance(field, Continuum):
        raise TypeError("Only Continuum is rendered")
        
    if not isinstance(n_time_steps, int):
        raise TypeError("# of time steps(n_time_steps) must be an int")
        
    params=field.export_for_renderer()
    cc=cpu_count()

    E=params[2]
    H=params[3]
    E_mul=params[4]
    H_mul=params[5]
    
    if params[0]==1:
        
        

        for t in range(n_time_steps):
            H[:-1]+=(E[1:]-E[:-1])*H_mul[:-1]
            
            for j in range(params[1][0]):
                E[j]+=(H[j]-H[j-1])*E_mul[j]
            
            
            for source in params[6]:
                if source[0]==0 and source[2][0]<=t<=source[2][1]:
                    E[source[1]]+=source[3]*np.sin(source[4]*t+source[5])
                    
        field.load_from_renderer(E, H)
        
    elif params[0]==2:
        for t in range(n_time_steps):
 
            for x in range(params[1][0]-1):
                    H[0][x][:-1]-=(E[x][1:]-E[x][:-1])*H_mul[x][:-1]
                    H[1][x][:-1]+=(E[x+1][:-1]-E[x][:-1])*H_mul[x][:-1]
            


            
            for x in range(params[1][0]):
                for y in range(params[1][1]):
                    E[x][y]+=(H[1][x][y]-H[1][x-1][y]-H[0][x][y]+H[0][x][y-1])*E_mul[x][y]
                    
            for source in params[6]:
                if source[0]==0 and source[2][0]<=t<=source[2][1]:
                    E[source[1]]+=source[3]*np.sin(source[4]*t+source[5])
        
        field.load_from_renderer(E, H)
        
    elif params[0]==3:
        for t in range(n_time_steps): 
        
            for x in range(params[1][0]-1):
                for y in range(params[1][1]-1):
                    for z in range(params[1][2]-1):
                        H[0][x][y][z]-=(E[2][x][y+1][z]-E[2][x][y][z]-E[1][x][y][z+1]+E[1][x][y][z])*H_mul[x][y][z]
                        H[1][x][y][z]-=(E[0][x][y][z+1]-E[0][x][y][z]-E[2][x+1][y][z]+E[2][x][y][z])*H_mul[x][y][z]
                        H[2][x][y][z]-=(E[1][x+1][y][z]-E[1][x][y][z]-E[0][x][y+1][z]+E[0][x][y][z])*H_mul[x][y][z]
        
            for x in range(0,params[1][0]):
                for y in range(0,params[1][1]):
                    for z in range(0,params[1][2]):
                        E[0][x][y][z]+=(H[2][x][y][z]-H[2][x][y-1][z]-H[1][x][y][z]+H[1][x][y][z-1])*E_mul[x][y][z]
                        E[1][x][y][z]+=(H[0][x][y][z]-H[0][x][y][z-1]-H[2][x][y][z]-H[2][x-1][y][z])*E_mul[x][y][z]
                        E[2][x][y][z]+=(H[1][x][y][z]-H[1][x-1][y][z]-H[0][x][y][z]+H[0][x][y-1][z])*E_mul[x][y][z]
            
            
            for source in params[6]:
                if source[0]==0 and source[2][0]<=t<=source[2][1]:
                    E[2][source[1]]+=source[3]*np.sin(source[4]*t+source[5])
        
        plt.plot(E[2,10,:,0])
        field.load_from_renderer(E, H)

                    
        

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
