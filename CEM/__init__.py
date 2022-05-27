import os
import platform
import numpy as np
import CCCEM.geo1D
import CCCEM.geo2D


oss=platform.system()

if oss=="Linux":#The most Prior
    tmp="/tmp/MemoriesWillFade"
elif oss=="Windows":#The most Ubiqious
    tmp="C://Users/Default/AppData/Local/CEM/MemoriesWillFade"
elif oss=="Darwin":
    tmp="/tmp/MemoriesWillFade"


try:       
    os.mkdir(tmp)
except:
    pass




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
        self.__object_types=[0,0,0]
        self.__ds=ds
        self.__energizers=[]
        
    def add(self, arg):
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add(element)
        elif self.__dim==1 and not isinstance(arg, (geo1D.Line,)):
            raise TypeError("In 1-D, only lines are allowed")
        
        elif self.__dim==2 and not isinstance(arg, (geo2D.Rectangle, geo2D.Circle)):
            raise TypeError("In 2-D, only defined geometries are allowed")
        
        else:
            self.__geometries.append(arg)
            self.__object_types[arg.t()]+=1
        
        
    def add_energizer(self, arg):
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add_energizer(element)
        elif not isinstance(arg, (DotSource,)):
             raise TypeError("Only defined energizers are allowed")
        else:
            self.__energizers.append(arg)
            
    def __export_Topology(self):
        file=open(tmp+"/structure.tgf", "w")
        file.write("PREAMBLE\n")
        file.write(f"{self.__dim}\n{len(self.__geometries)}\n{int(self.__ANC)}\n{self.__ds}\n")
        __=""
        for i in range(self.__dim):
            __+=str(self.__grid_size[i])+"\n"

        file.write(__+"DATA\n")

        for arg in self.__geometries:
            file.write(repr(arg)+"\n")

        
        file.close()
    
    def __export_shape_counts(self):
        file=open(tmp+"/counts.tgf", "w")
        file.write("1\n")
        for i in self.__object_types:
            file.write(str(i)+"\n")
        file.close()    
        
    def __export_energizers(self):
        file=open(tmp+"/energizers.wm","w")
        file.write(str(len(self.__energizers))+"\n")
        for energizer in self.__energizers:
            file.write(repr(energizer)+"\n")
        file.close()
        
    def render(self, n_time_steps, sampler_position, savedir=tmp):
        
        if not isinstance(n_time_steps, int):
            raise TypeError("# of time steps(n_time_steps) must be an int")
        
        
        if not isinstance(sampler_position, (tuple, list, np.array)):
            raise TypeError("sampler_position must be a tuple, list or np.array or None")
            
        elif np.array(sampler_position).shape!=(self.__dim,):
            raise ValueError("# of elements contained by sampler position must be the same as # of dimensions")
        
        for i in range(self.__dim):
            if not isinstance(sampler_position[i], int):
                raise TypeError("Each component of coordinate of sampler must be an int")
            if not 0<=sampler_position[i]<self.__grid_size[i]:
                raise ValueError("Sampler must be located on a place defined on the grid")
    
        
        if not isinstance(savedir, str):
            raise TypeError("savedir must be a string")          
    
        file=open(tmp+"/renderer.dat","w")
        file.write(str(n_time_steps)+"\n")
        for i in sampler_position:
            file.write(str(i)+"\n")
     
        file.write(savedir)
        file.close()
        file=open(savedir+"/wave.wm","w")
        file.close()
        self.__export_Topology()
        self.__export_shape_counts()
        self.__export_energizers()
        os.system("cd CCCEM;./FDTD_renderer")

    

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
        __+=f"{self.__amplitude} {self.__frequency} {self.__phase}"
        
        return __
        

    
        
        

    
