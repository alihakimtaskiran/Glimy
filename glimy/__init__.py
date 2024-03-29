print("Interacting with reality...")
import numpy as np
try:
    import cupy as cp
    print("GPU accelerated computing enabled. You can set Render('cupy') to benefit GPU utils.")
    cupy_enabled=True
except ImportError:
    cupy_enabled=False
    cp=np
    print("Running in CPU mode, set Render('numpy') to use it.")


import sys
import glimy.geo
import psutil
import warnings
import time
import matplotlib.pyplot as plt
import itertools
G=6.6743e-11
c=299792458
c_2=c**2
PI_2=np.pi*2
Z_0=376.730313
e_0=8.8541878128e-12
mu_0=1.25663706212e-6

e_0_2=e_0*2
mu_0_2=2*mu_0

class Continuum(object):
    def __init__(self, grid_size, ds):
        
        if not isinstance(grid_size,(tuple,list)):
            raise TypeError("# of pixels of grid must be carried by a tuple or a list")
        
        self.__dim=len(grid_size)
        
        if not self.__dim in {2,3}:
            raise ValueError("# of dimensions must be 2 or 3")
       
        if not isinstance(ds, (int,float)):
            raise TypeError("ds(Δs) must be a float or int")
            
            
        self.__grid_size=grid_size
        self.__ds=ds
        self.__dt=ds/c/(self.__dim**.5)
        
        self.__objects=[]
        
        self.__emo=[]
        self.__stellar=[]
        self.__energizers=[]
        
        self.__built=False
        
        self.__anisotropy=False
        self.__conductivity=False
        self.__conductivity_m=False
        
        self.__Jdt=np.ones(self.__grid_size)

        
        self.__video_starters={}
        self.__video_terminators={}
        self.__start_frames=set()
        self.__end_frames=set()
        
        self.__instance=0
        
        self.__bound=None
        self.__bound_bool=False
        self.__rendered=False
        
        self.__built_for=None
        

        
        
    def add(self, arg):
        
        if isinstance(arg, (set, tuple, list)):
            for element in arg:
                self.add(element)
        else:
            if isinstance(arg, (geo.SingularCelestial, geo.MassiveCluster, geo.PointCloud, geo.Rectangle, geo.RectPrism, geo.Circle, geo.Sphere, geo.Cylinder, DotSource, Boundaries)):
                if arg.dimensionality!=self.__dim:
                    raise ValueError(f"# of dimensions of Continuum and added object must match:\n{arg}")
                self.__objects.append(arg)
            else:
                raise TypeError("Each input object should be in glimy.geo module")
        
        self.__built=False
        self.__rendered=False
        self.__instance=0
        
        
    def __categorizer(self):   
        
        for element in self.__objects:
            __=type(element)
            
            if __ in {geo.PointCloud, geo.Rectangle, geo.RectPrism, geo.Circle, geo.Sphere, geo.Cylinder}:
                self.__emo.append(element)
                if element.anisotropy:
                    self.__anisotropy=True
                
                if element.conductivity:
                    self.__conductivity=True
                    
                if element.conductivity_m:
                    self.__conductivity_m=True

            elif __==geo.SingularCelestial:
                self.__stellar.append(element.export[1:])
                
            elif __==geo.MassiveCluster:
                for celestial in element.content:
                    self.__stellar.append(celestial.export[1:])
                    
            elif __ in {DotSource}:
                element.set_dt(self.__dt)
                self.__energizers.append(element)
                
            elif __==Boundaries:
                self.__bound=element()
                self.__bound_bool=True


    def __gravitonics(self):
        g_c_2=2*G/c_2
        def gp(*x):
            __=0
            x=np.array(x)
            for l,m in self.__stellar:
                __+=m/np.linalg.norm(l-x*self.__ds)
            return __

        self.__Jdt=1/(1+g_c_2*np.fromfunction(np.vectorize(gp), self.__grid_size, dtype=float))
        if self.__cupy_enabled:
            self.__Jdt_cp=cp.array(self.__Jdt)
        

    def __emo_video_creator(self):
        
        if self.__anisotropy:
            shape=self.__grid_size+(self.__dim,self.__dim)
            self.__e=np.full(shape,np.eye(self.__dim))
            self.__mu=np.full(shape,np.eye(self.__dim))

        else:
            shape=self.__grid_size
            self.__e=np.ones(shape)
            self.__mu=np.ones(shape)
            
        if self.__conductivity:
            self.__sigma=np.zeros(self.__grid_size)
        
        if self.__conductivity_m:
            self.__sigma_m=np.zeros(self.__grid_size)
            
            
        if self.__cupy_enabled:
            self.__e_cp=cp.array(self.__e)
            self.__mu_cp=cp.array(self.__mu)
            if self.__conductivity:self.__sigma_cp=cp.array(self.__sigma)
            if self.__conductivity_m:self.__sigma_m_cp=cp.array(self.__sigma_m)
        
        
        
        for element in self.__emo:
            if self.__anisotropy!=element.anisotropy:
                e=np.zeros((self.__dim,self.__dim))
                mu=np.zeros((self.__dim,self.__dim))
                for i in range(self.__dim):
                     e[i,i]=element.fielder[0]
                     mu[i,i]=element.fielder[1]
                
                fielder=e,mu,element.fielder[2]

            else:
                fielder=element.fielder

            mfs=[a[1]-a[0] for a in element.coverage]
            if not self.__anisotropy:
                modified_array=np.full(mfs,False,dtype=bool)
                ad=True
            else:
                modified_array=np.full(mfs+[self.__dim, self.__dim],False,dtype=bool)
                ad=[[True]*self.__dim]*self.__dim
            sl=np.array([element.coverage[i][0] for i in range(self.__dim)])
            for index in itertools.product(*(range(i) for i in mfs)):
                ind=index+sl
                if element.isIn(ind):                    
                    modified_array[index]=ad

            

            action=(element.layer, element.coverage, modified_array, fielder)
            
            if element.eternity:
                if 0 not in self.__start_frames:
                    self.__start_frames.add(0)
                    self.__video_starters[0]=[action]
                else:
                    self.__video_starters[0].append(action)
            
            else:
                if element.duration[0] not in self.__start_frames:
                    self.__start_frames.add(element.duration[0])
                    self.__video_starters[element.duration[0]]=[action]
                else:
                    self.__video_starters[element.duration[0]].append(action)
                    
                    
                if element.duration[1] not in self.__end_frames:
                    self.__end_frames.add(element.duration[1])
                    self.__video_terminators[element.duration[1]]=[action]
                else:
                    self.__video_terminators[element.duration[1]].append(action)
                

        for f in self.__video_starters:
            self.__video_starters[f].sort(reverse=True)

            
        for f in self.__video_terminators:
            self.__video_terminators[f].sort(reverse=True)

                
    def __grid_generator_at_t_0(self):
        if 0 in self.__start_frames:
            for action in self.__video_starters[0]:
                mfs=[a[1]-a[0] for a in action[1]]
                indices=tuple([slice(k[0], k[1]) for k in action[1]])
                if self.__anisotropy:
                    
                    self.__e[indices]*=np.logical_not(action[2])
                    self.__e[indices]+=np.full(mfs+[self.__dim, self.__dim],action[3][0])*action[2]
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    self.__mu[indices]+=np.full(mfs+[self.__dim, self.__dim],action[3][1])*action[2]
                    

                    if self.__conductivity:
                        
                        self.__sigma[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,action[3][2])*action[2][:,:,:,0,0]
                        self.__sigma[indices]+=tg_a

                    if self.__conductivity_m:
                            
                        self.__sigma_m[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,action[3][3])*action[2][:,:,:,0,0]
                        self.__sigma_m[indices]+=tg_a

      
                    if self.__cupy_enabled:
                        self.__e_cp[indices]=cp.array(self.__e[indices])
                        self.__mu_cp[indices]=cp.array(self.__mu[indices])
                        if self.__conductivity:self.__sigma_cp[indices]=cp.array(self.__sigma[indices])
                        if self.__conductivity_m:self.__sigma_m_cp[indices]=cp.array(self.__sigma_m[indices])

                else:
                    self.__e[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,action[3][0])*action[2]
                    self.__e[indices]+=tg_a
                    
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,action[3][1])*action[2]
                    self.__mu[indices]+=tg_a
                    
                    if self.__conductivity:    
                        self.__sigma[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,action[3][2])*action[2]
                        self.__sigma[indices]+=tg_a
                                                
                    if self.__conductivity_m:    
                        self.__sigma_m[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,action[3][3])*action[2]
                        self.__sigma_m[indices]+=tg_a
                                                
                        
                    if self.__cupy_enabled:
                        self.__e_cp[indices]=cp.array(self.__e[indices])
                        self.__mu_cp[indices]=cp.array(self.__mu[indices])
                        if self.__conductivity:self.__sigma_cp[indices]=cp.array(self.__sigma[indices])
                        if self.__conductivity_m:self.__sigma_m_cp[indices]=cp.array(self.__sigma_m[indices])
                    
        if self.__conductivity:
            if self.__cupy_enabled:
                self.__sigma_ex=self.__sigma_cp*self.__Jdt_cp*self.__dt/e_0_2/self.__e_cp
            else:
                self.__sigma_ex=self.__sigma*self.__Jdt*self.__dt/e_0_2/self.__e
        if self.__conductivity_m:
            if self.__cupy_enabled:
                self.__sigma_mux=self.__sigma_m_cp*self.__Jdt_cp*self.__dt/mu_0_2/self.__mu_cp
            else:
                self.__sigma_mux=self.__sigma_m*self.__Jdt*self.__dt/mu_0_2/self.__mu
            
        
        if self.__anisotropy:
            if self.__cupy_enabled:
                self.__e_inv=cp.linalg.inv(self.__e_cp)
                self.__mu_inv=cp.linalg.inv(self.__mu_cp)
            else:
                self.__e_inv=np.linalg.inv(self.__e)
                self.__mu_inv=np.linalg.inv(self.__mu)

        if self.__cupy_enabled:
            cp._default_memory_pool.free_all_blocks()

            
            
                    
    def __update_grid(self):

        self.__instance+=1
        
        change=False
        
        if self.__instance in self.__end_frames:
            change=True
            for action in self.__video_terminators[self.__instance]:
                
                mfs=[a[1]-a[0] for a in action[1]]
                indices=tuple([slice(k[0], k[1]) for k in action[1]])
                if self.__anisotropy:
                    self.__e[indices]*=np.logical_not(action[2])
                    self.__e[indices]+=np.full(mfs+[self.__dim, self.__dim],np.eye(self.__dim))*action[2]
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    self.__mu[indices]+=np.full(mfs+[self.__dim, self.__dim],np.eye(self.__dim))*action[2]
                    
                    if self.__conductivity:   
                        self.__sigma[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,0)*action[2][:,:,:,0,0]
                        self.__sigma[indices]+=tg_a
                        
                    if self.__conductivity_m:   
                        self.__sigma_m[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,0)*action[2][:,:,:,0,0]
                        self.__sigma_m[indices]+=tg_a 

                    
                else:
                    self.__e[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,1.)*action[2]
                    self.__e[indices]+=tg_a
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,1.)*action[2]
                    self.__mu[indices]+=tg_a
                    
                    if self.__conductivity:
                        self.__sigma[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,0)*action[2]
                        self.__sigma[indices]+=tg_a  
                        
                    if self.__conductivity_m:
                        self.__sigma_m[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,0)*action[2]
                        self.__sigma_m[indices]+=tg_a

                if self.__cupy_enabled:
                    self.__e_cp[indices]=cp.array(self.__e[indices])
                    self.__mu_cp[indices]=cp.array(self.__mu[indices])
                    if self.__conductivity:self.__sigma_cp[indices]=cp.array(self.__sigma[indices])
                    if self.__conductivity_m:self.__sigma_m_cp[indices]=cp.array(self.__sigma_m[indices])

        
        if self.__instance in self.__start_frames:
            change=True
            for action in self.__video_starters[self.__instance]:
                mfs=[a[1]-a[0] for a in action[1]]
                indices=tuple([slice(k[0], k[1]) for k in action[1]])

                if self.__anisotropy:

                    self.__e[indices]*=np.logical_not(action[2])
                    self.__e[indices]+=np.full(mfs+[self.__dim, self.__dim],action[3][0])*action[2]
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    self.__mu[indices]+=np.full(mfs+[self.__dim, self.__dim],action[3][1])*action[2]
                    
                    if self.__conductivity:
                        self.__sigma[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,action[3][2])*action[2][:,:,:,0,0]
                        self.__sigma[indices]+=tg_a
                        
                    if self.__conductivity_m:
                        self.__sigma_m[indices]*=np.logical_not(action[2][:,:,:,0,0])
                        tg_a=np.full(mfs,action[3][3])*action[2][:,:,:,0,0]
                        self.__sigma_m[indices]+=tg_a

                else:
                    
                    self.__e[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,action[3][0])*action[2]
                    self.__e[indices]+=tg_a
                    
                    self.__mu[indices]*=np.logical_not(action[2])
                    tg_a=np.full(mfs,action[3][1])*action[2]
                    self.__mu[indices]+=tg_a
                    
                    if self.__conductivity:    
                        self.__sigma[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,action[3][2])*action[2]
                        self.__sigma[indices]+=tg_a
                        
                    if self.__conductivity_m:    
                        self.__sigma_m[indices]*=np.logical_not(action[2])
                        tg_a=np.full(mfs,action[3][3])*action[2]
                        self.__sigma_m[indices]+=tg_a
                        
                if self.__cupy_enabled:
                    self.__e_cp[indices]=cp.array(self.__e[indices])
                    self.__mu_cp[indices]=cp.array(self.__mu[indices])
                    if self.__conductivity:self.__sigma_cp[indices]=cp.array(self.__sigma[indices])
                    if self.__conductivity_m:self.__sigma_m_cp[indices]=cp.array(self.__sigma_m[indices])

        
                
        if change:
            if self.__conductivity:
                if self.__cupy_enabled:
                    self.__sigma_ex=self.__sigma_cp*self.__Jdt*self.__dt/e_0_2/self.__e
                else:
                    self.__sigma_ex=self.__sigma*self.__Jdt*self.__dt/e_0_2/self.__e
            if self.__conductivity_m:
                if self.__cupy_enabled:
                    self.__sigma_mux=self.__sigma_m_cp*self.__Jdt*self.__dt/mu_0_2/self.__mu
                else:
                    self.__sigma_mux=self.__sigma_m*self.__Jdt*self.__dt/mu_0_2/self.__mu
                
            
            if self.__anisotropy:
                if self.__cupy_enabled:
                    self.__e_inv=cp.linalg.inv(self.__e_cp)
                    self.__mu_inv=cp.linalg.inv(self.__mu_cp)
                else:
                    self.__e_inv=np.linalg.inv(self.__e)
                    self.__mu_inv=np.linalg.inv(self.__mu)
                    
        if self.__cupy_enabled:
            cp._default_memory_pool.free_all_blocks()

            
        

    def export_grid(self):
        return self.__e, self.__mu
    
    def export_field(self):
        return self.__E, self.__H

    def build(self,verbose=1,gpu_flag=False):
        if (not cupy_enabled and gpu_flag):
            raise NotImplementedError("GPU resources are not available. Set gpu_flag=False")
        
        self.__cupy_enabled=bool(gpu_flag)
        
        if gpu_flag==True:
            try:device=cp.cuda.Device(0);print(f"Building for GPU{device} Render stream.\n{int(device.mem_info[0]/1048576)}MiB({device.mem_info[0]/device.mem_info[1]*100:.1f}%) VRAM available");self.__built_for="cupy";
            except:pass
        else:mem=psutil.virtual_memory();print(f"Building for CPU Render stream.\n{int(mem.available/1048576)}MiB({100-mem.percent}%) RAM available");self.__built_for="numpy";
        if cupy_enabled and not gpu_flag:warnings.warn("GPU is available. You can use GPU for accelerating the computations significantly faster. Call build(gpu_flag=1) for utilizing GPU resources", UserWarning)
        
        if verbose:
            start=time.time()
        self.__bound=None
        self.__categorizer()
        self.__gravitonics()
        self.__emo_video_creator()
        self.__rendered=False
        self.__built=True
        self.__built_once=True
        self.__built_isotropic=self.__anisotropy
        self.__grid_generator_at_t_0()
        
        if self.__anisotropy and (self.__conductivity or self.__conductivity_m):
            raise NotImplementedError("Both conductive and anisotropic materials are not permitted.")
        self.__instance=0

        self.__E=np.zeros((3,)+self.__grid_size)
        self.__H=np.zeros((3,)+self.__grid_size)
        
        if gpu_flag==True:
            self.__E_cp=cp.zeros((3,)+self.__grid_size)
            self.__H_cp=cp.zeros((3,)+self.__grid_size)
        
        if verbose:
            rt=time.time()-start

            print(f"Built in {self.__convert_to_time(rt)}  {self.__prefix_quantifier(np.prod(self.__grid_size)/rt)}Points/s\n")
    
    @staticmethod
    def __prefix_quantifier(quantity):
        units = ['', 'K', 'M', 'G', 'T','P','E','Z','Y']
        unit_index = 0
        while quantity >= 1000 and unit_index < len(units) - 1:
            quantity /= 1000
            unit_index += 1
        return f'{quantity:.3f} {units[unit_index]}'
    
    @staticmethod
    def __convert_to_time(time_in_secs):
        hours = int(time_in_secs // 3600)
        minutes = int((time_in_secs % 3600) // 60)
        seconds = int(time_in_secs % 60)
        milliseconds = int((time_in_secs % 1) * 1000)
    
        time_components = ""
        if hours != 0:
            time_components += f"{hours:3d}h "
        if minutes != 0:
            time_components += f"{minutes:2d}m "
        if seconds != 0:
            time_components += f"{seconds:2d}s "
        if milliseconds != 0:
            time_components += f"{milliseconds:3d}ms"
    
        if time_components:
            return time_components
        else:
            return "0ms"
        
    @staticmethod
    def __create_progress_bar_with_ETA(current_time, current_step, total_steps):
        progress = int(((current_step+1) / total_steps) * 100)
        time_remaining = (time.time() - current_time) * (total_steps / (current_step + 1) - 1)
        filled_length = int(50 * progress / 100)
        if progress<10:
            bar = "=" * filled_length +":@"+"-" * (50 - filled_length)
        elif progress<35:
            bar = "=" * filled_length +":("+"-" * (50 - filled_length)
        elif progress<55:
            bar = "=" * filled_length +":)"+"-" * (50 - filled_length)    
        elif progress<85:
            bar = "=" * filled_length +":D"+"-" * (50 - filled_length)
        else:
            bar = "=" * filled_length +"B)"+"-" * (50 - filled_length)
        
        
        hours = int(time_remaining // 3600)
        minutes = int((time_remaining % 3600) // 60)
        seconds = int(time_remaining % 60)
        milliseconds = int(time_remaining * 1000) % 1000
        time_components = ""
        if hours != 0:
            time_components += f"{hours}h "
        if minutes != 0:
            time_components += f"{minutes}m "
        if seconds != 0:
            time_components += f"{seconds}s "
        if milliseconds != 0:
            time_components += f"{milliseconds}ms"
        if time_components:
            ETA= time_components
        else:
            ETA= "0ms"
            
        print(f"\r[{bar}] {progress}% - ETA:{ETA} - {current_step}/{total_steps}-------------",end="")
        sys.stdout.flush()

    def impose_grid(self, e, mu, sigma=False, sigma_m=False, anisotropy=(False,False)):
        if anisotropy[0]:
            if e.shape[:-1]!=self.__grid_size:
                raise ValueError(f"Grid size of the Continuum and imposed e-grid must be match:\nContinuum is {self.__grid_size}")
            elif e.shape[-1]!=3:
                raise ValueError("For anisotropic e-grid, select False in anisotropy flag")
            self.__e=e
        else:
            if e.shape!=self.__grid_size:
                raise ValueError(f"Grid size of the Continuum and imposed e-grid must be match:\nContinuum is {self.__grid_size}\nIf anisotropic e-grid imposed, then select True in anisotropy flag")
            self.__e=e
            
        if (sigma_m is not False or sigma is not False) and (anisotropy[0] or anisotropy[1]):
            raise NotImplementedError("Anisotropy and conductivity is not unified yet.")
        
        if sigma is not False:
            if sigma.shape!=self.__grid_size:
                    raise ValueError(f"Grid size of the Continuum and imposed sigma-grid must be match:\nContinuum is {self.__grid_size}")
            else:
                self.__sigma=sigma
                self.__conductivity=True
                
        if sigma_m is not False:
            if sigma_m.shape!=self.__grid_size:
                    raise ValueError(f"Grid size of the Continuum and imposed sigma_m-grid must be match:\nContinuum is {self.__grid_size}")
            else:
                self.__sigma_m=sigma_m
                self.__conductivity_m=True


        
        if anisotropy[1]:
            if mu.shape[:-1]!=self.__grid_size:
                raise ValueError(f"Grid size of the Continuum and imposed mu-grid must be match:\nContinuum is {self.__grid_size}")
            elif mu.shape[-1]!=3:
                raise ValueError("For isotropic mu-grid, select False in anisotropy flag")
            self.__mu=mu
        else:
            if mu.shape!=self.__grid_size:
                raise ValueError(f"Grid size of the Continuum and imposed mu-grid must be match:\nContinuum is {self.__grid_size}\nIf anisotropic mu-grid imposed, then select True in anisotropy flag")
            self.__mu=mu
            
        self.__built=True
           
        
    def view_metric(self, field="t",*args, colorbar=True):
        if not self.__built:
            warnings.warn("Recently added objects are not rendered. Call build() method before this")

        if field=="t":
            data=self.__Jdt
        else:
            raise ValueError(f"{field} is not a recognized dimension")

        plt.clf()
        plt.title(f"Metric Grid($\Delta${field})")
        

        if self.__dim==1:
            plt.plot(self.__Jdt)
                
        elif self.__dim==2:
            plt.imshow(data.T)
            plt.xlabel("x")
            plt.ylabel("y")
            if colorbar:
                plt.colorbar()
            
            
        elif self.__dim==3:
            axis={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
            if axis[args[0]]==0:
                plt.imshow(data[args[1]].T)
                plt.xlabel("y")
                plt.ylabel("z")
            elif axis[args[0]]==1:
                plt.imshow(data[:,args[1]].T)
                plt.xlabel("x")
                plt.ylabel("z")
            elif axis[args[0]]==2:
                plt.imshow(data[:,:,args[1]].T)
                plt.xlabel("x")
                plt.ylabel("y")
            else:
                raise ValueError("Invalid Dimension")
            if colorbar:
                plt.colorbar()
        plt.show()
        
        
    def view_structure(self, field="e", *args, colorbar=True):
        if not self.__built:
            warnings.warn("Recently added objects are not built. Call build() method before this")

        if field == "e":
            array = self.__e
            title="$\epsilon$"
        elif field == "mu":
            array = self.__mu
            title="$\mu$"
        elif field == "Z":
            array = self.__Z
            title="|Z|"
        elif field == "sigma":
            if not self.__conductivity:
                raise NotImplementedError("The Continuum doesn't contain any conductive object")
            else:
                array=self.__sigma
                title="$\sigma$"
                axlabels={0:"x", 1:"y", 2:"z"} 
                
                if self.__dim == 1:
                    plt.title(title)
                    plt.plot(array)
                    
                elif self.__dim == 2:
                    plt.title(title)
                    plt.imshow(array.T)
                    plt.xlabel("x")
                    plt.ylabel("y")
                    if colorbar:
                        plt.colorbar()
                
                elif self.__dim == 3:
                    ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                    plt.title(title+f" @{axlabels[ax[args[0]]]}={args[1]}")
                    axis=ax[args[0]]
                    if axis == 0:
                        plt.imshow(array[args[1]].T)
                        plt.xlabel("y")
                        plt.ylabel("z")
                    elif axis == 1:
                        plt.imshow(array[:,args[1]].T)
                        plt.xlabel("x")
                        plt.ylabel("z")
                    elif axis == 2:
                        plt.imshow(array[:,:,args[1]].T)
                        plt.xlabel("x")
                        plt.ylabel("y")
                    else:
                        raise ValueError("Invalid axis")
                        return
                    if colorbar:
                        plt.colorbar()
                else:
                    raise ValueError("Invalid dimension")
                    
        elif field == "sigma_m":
            if not self.__conductivity_m:
                raise NotImplementedError("The Continuum doesn't contain any magnetic conductive object")
            else:
                array=self.__sigma_m
                title="$\sigma_m$"
                axlabels={0:"x", 1:"y", 2:"z"} 
                
                if self.__dim == 1:
                    plt.title(title)
                    plt.plot(array)
                    
                elif self.__dim == 2:
                    plt.title(title)
                    plt.imshow(array.T)
                    plt.xlabel("x")
                    plt.ylabel("y")
                    if colorbar:
                        plt.colorbar()
                
                elif self.__dim == 3:
                    ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                    plt.title(title+f" @{axlabels[ax[args[0]]]}={args[1]}")
                    axis=ax[args[0]]
                    if axis == 0:
                        plt.imshow(array[args[1]].T)
                        plt.xlabel("y")
                        plt.ylabel("z")
                    elif axis == 1:
                        plt.imshow(array[:,args[1]].T)
                        plt.xlabel("x")
                        plt.ylabel("z")
                    elif axis == 2:
                        plt.imshow(array[:,:,args[1]].T)
                        plt.xlabel("x")
                        plt.ylabel("y")
                    else:
                        raise ValueError("Invalid axis")
                        return
                    if colorbar:
                        plt.colorbar()
                else:
                    raise ValueError("Invalid dimension")
        
        else:
            raise ValueError(f"{field} is not a recognized array. Only e, mu and Z are known")
        plt.clf()
         
        

        if not self.__anisotropy:
            axlabels={0:"x", 1:"y", 2:"z"} 
            
            if self.__dim == 1:
                plt.title(title)
                plt.plot(array)
                
            elif self.__dim == 2:
                plt.title(title)
                plt.imshow(array.T)
                plt.xlabel("x")
                plt.ylabel("y")
                if colorbar:
                    plt.colorbar()
            
            elif self.__dim == 3:
                ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                plt.title(title+f" @{axlabels[ax[args[0]]]}={args[1]}")
                axis=ax[args[0]]
                if axis == 0:
                    plt.imshow(array[args[1]].T)
                    plt.xlabel("y")
                    plt.ylabel("z")
                elif axis == 1:
                    plt.imshow(array[:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("z")
                elif axis == 2:
                    plt.imshow(array[:,:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("y")
                else:
                    raise ValueError("Invalid axis")
                    return
                if colorbar:
                    plt.colorbar()
            else:
                raise ValueError("Invalid dimension")
        
        
        
        else:
            if field=="sigma":
                ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                plt.title(title+f" @{axlabels[ax[args[0]]]}={args[1]}")
                axis=ax[args[0]]
                if axis == 0:
                    plt.imshow(array[args[1]].T)
                    plt.xlabel("y")
                    plt.ylabel("z")
                elif axis == 1:
                    plt.imshow(array[:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("z")
                elif axis == 2:
                    plt.imshow(array[:,:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("y")
                else:
                    raise ValueError("Invalid axis")
                    return
                if colorbar:
                    plt.colorbar()
                return
            
            elif field=="sigma_m":
                ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                plt.title(title+f" @{axlabels[ax[args[0]]]}={args[1]}")
                axis=ax[args[0]]
                if axis == 0:
                    plt.imshow(array[args[1]].T)
                    plt.xlabel("y")
                    plt.ylabel("z")
                elif axis == 1:
                    plt.imshow(array[:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("z")
                elif axis == 2:
                    plt.imshow(array[:,:,args[1]].T)
                    plt.xlabel("x")
                    plt.ylabel("y")
                else:
                    raise ValueError("Invalid axis")
                    return
                if colorbar:
                    plt.colorbar()
                return
                
            atitle=""
            xl=None;yl=None
            axlabels={0:"x", 1:"y", 2:"z"} 
            if self.__dim == 2:
                xl="x";yl="y"
            elif self.__dim == 3:
                ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
                axis=ax[args[0]]
                if axis == 0:
                    array=array[args[1]]
                    xl,yl="y","z"
                    
                elif axis == 1:
                    array=array[:,args[1]]
                    xl,yl="x","z"
                elif axis == 2:
                    array=array[:,:,args[1]]
                    xl,yl="x","y"

                else:
                    raise ValueError("Invalid axis")
                    return
                
                atitle+=f" @{axlabels[ax[args[0]]]}={args[1]}"
                    
            else:
                raise ValueError("Invalid dimension")
            
            fig,axarr=plt.subplots(self.__dim,self.__dim, figsize=(16,12))
            fig.set_tight_layout(True)
            fig.suptitle(title+atitle)
            for i in range(self.__dim):
                for j in range(self.__dim):
                    img=axarr[i,j].imshow(array[:,:,i,j].T)
                    axarr[i,j].title.set_text(f"{axlabels[i]}{axlabels[j]}")
                    axarr[i,j].set_xlabel(xl)
                    axarr[i,j].set_ylabel(yl)
                    if colorbar:
                        fig.colorbar(img,ax=axarr[i, j])
                    
        plt.show()

    def view_field(self, field="E", *args, colorbar=True):
        
        if type(colorbar)!=bool:
            raise TypeError("colorbar must be a boolean")
        
        if args and self.__dim!=3:
            raise ValueError("Plane selection is only available in 3D Continuum")
        
        if not self.__rendered:
            warnings.warn("Electromagnetic field is not rendered yet. You probably see graph of an empty field or previously rendered field")
        
        ax={"xy":2, "xz":1, "yz":0, "zy":0, "zx":1, "yx":2, "x":0, "y":1, "z":2, 0:0, 1:1, 2:2}
        axlabels={0:"x", 1:"y", 2:"z"}
        
        xl,yl="x","y"
        if field=="E":
            
            if self.__dim==2:
                data=self.__E
                title="E-Field"
            elif self.__dim==3:
                title=f"E-Field @{axlabels[ax[args[0]]]}={args[1]}"
                if ax[args[0]]==0:
                    data=self.__E[:,args[1]]
                    xl,yl="y","z"
                elif ax[args[0]]==1:
                    data=self.__E[:,:,args[1]]
                    xl,yl="x","z"
                elif ax[args[0]]==2:
                    data=self.__E[:,:,:,args[1]]
                
        elif field=="H":
            
            if self.__dim==2:
                title="H-Field"
                data=self.__H
            elif self.__dim==3:
                title=f"H-Field @{axlabels[ax[args[0]]]}={args[1]}"
                if ax[args[0]]==0:
                    data=self.__H[:,args[1]]
                    xl,yl="y","z"
                elif ax[args[0]]==1:
                    data=self.__H[:,:,args[1]]
                    xl,yl="x","z"
                elif ax[args[0]]==2:
                    data=self.__H[:,:,:,args[1]]
                    
        elif field=="J":
            
            if self.__dim==2:
                title="J-Field"
                data=self.__E*self.__sigma
            elif self.__dim==3:
                title=f"J-Field @{axlabels[ax[args[0]]]}={args[1]}"
                if ax[args[0]]==0:
                    data=self.__E[:,args[1]]*self.__sigma[args[1]]
                    xl,yl="y","z"
                elif ax[args[0]]==1:
                    data=self.__E[:,:,args[1]]*self.__sigma[:,args[1]]
                    xl,yl="x","z"
                elif ax[args[0]]==2:
                    data=self.__E[:,:,:,args[1]]*self.__sigma[:,:,args[1]]

        else:
            raise ValueError("Only E and H field can be displayed")
            
        plt.clf()
        
        
        
        if not self.__anisotropy and self.__dim==2:            
            if field=="E":
                plt.title("$E_z$")
                plt.imshow(data[2].T)
                plt.xlabel(xl)
                plt.ylabel(yl)
                if colorbar:
                    plt.colorbar()
                plt.show()
            elif field=="H":
                fig, axarr=plt.subplots(1,2,figsize=(9,4))
                fig.set_tight_layout("True")
                
                fig.suptitle(title)
                
                sub_heading={0:"x",1:"y",2:"z"}
                for i in range(2):
        
                    img=axarr[i].imshow(data[i].T)
                
                    axarr[i].title.set_text(f"${field}_{sub_heading[i]}$")
                    axarr[i].set_xlabel(xl)
                    axarr[i].set_ylabel(yl)
                    if colorbar:
                        fig.colorbar(img,ax=axarr[i])
                    
                plt.show()
                
            elif field=="J":
                fig, axarr=plt.subplots(1,3,figsize=(9,4))
                fig.set_tight_layout("True")
                
                fig.suptitle(title)
                
                sub_heading={0:"x",1:"y",2:"z"}
                for i in range(3):
        
                    img=axarr[i].imshow(data[i].T)
                
                    axarr[i].title.set_text(f"${field}_{sub_heading[i]}$")
                    axarr[i].set_xlabel(xl)
                    axarr[i].set_ylabel(yl)
                    if colorbar:
                        fig.colorbar(img,ax=axarr[i])
                    
                plt.show()
            
        else:                
            
            fig, axarr=plt.subplots(1,3,figsize=(12,4))
            fig.set_tight_layout("True")
            
            fig.suptitle(title)
            
            sub_heading={0:"x",1:"y",2:"z"}
            for i in range(3):
    
                img=axarr[i].imshow(data[i].T)
            
                axarr[i].title.set_text(f"${field}_{sub_heading[i]}$")
                axarr[i].set_xlabel(xl)
                axarr[i].set_ylabel(yl)
                if colorbar:
                    fig.colorbar(img,ax=axarr[i])
                
            plt.show()
            
        
            
    def __numpy_renderer(self, *args):
        if args[1]:
            obs=True
            n_obs=len(args[1])
            obs_array=np.empty((args[0],n_obs,3))
            
        else:
            obs=False
            
        if self.__dim==2:
            Z_c1=Z_0/2**.5*self.__Jdt
            Z_c2=1/Z_0/2**.5*self.__Jdt
            arr_shape=self.__E.shape


            def pre_E():
                ind = np.zeros(arr_shape)
            
                ind[0,:,:-1] += self.__E[2,:,1:] - self.__E[2,:,:-1]
                ind[1,:-1,:] -= self.__E[2,1:,:] - self.__E[2,:-1,:]
            
                return ind
            
            
            def pre_H():
                ind = np.zeros(arr_shape)
                
                ind[2,:,1:] += self.__H[0,:,1:] - self.__H[0,:,:-1]
                ind[2,1:,:] -= self.__H[1,1:,:] - self.__H[1,:-1,:]
                return ind
            
            start_time=time.time()
            
            
            for t in range(args[0]):
                
                
                if self.__conductivity_m:
                    
                    self.__H=self.__H *(1-self.__sigma_mux)/(1+self.__sigma_mux)+ pre_E()*Z_c2/self.__mu/(1+self.__sigma_mux)
                else:
                    self.__H+=pre_E()*Z_c2/self.__mu
                    
                    
                    
                if self.__conductivity:
                    self.__E=self.__E*(1-self.__sigma_ex)/(1+self.__sigma_ex)+pre_H()*Z_c1/self.__e/(1+self.__sigma_ex)
                    
                else:
                    self.__E+=pre_H()*Z_c1/self.__e


                
                
                for energizer in self.__energizers:
                    self.__E[:,energizer.location[0],energizer.location[1]]=energizer(t)
                
                self.__update_grid()

                
                if t%10==0:
                    self.__create_progress_bar_with_ETA(start_time,t,args[0])
                    
                if obs:
                    for i in range(n_obs):
                        for ind in range(3):
                            obs_array[t,i,ind]=self.__E[ind][args[1][i]]
                            
                if self.__bound_bool:
                    if self.__bound[2]==1:
                        self.__E[2,:,0]=-self.__E[2,:,1]
                        self.__H[0,:,0]=-self.__H[0,:,1]
                    
                    if self.__bound[3]==1:
                        self.__E[2,:,-1]=-self.__E[2,:,-2]
                        self.__H[0,:,-2]=-self.__H[0,:,-3]
                        
                    if self.__bound[1]==1:
                        self.__E[2,-1]=-self.__E[2,-2]
                        self.__H[1,-2]=-self.__H[1,-3]
                        
                    if self.__bound[0]==1:
                        self.__E[2,0]=-self.__E[2,1]
                        self.__H[1,0]=-self.__H[1,1]



        elif self.__dim==3:
            
            
            Z_c1=Z_0/3**.5
            Z_c2=1/Z_0/3**.5
            arr_shape=self.__E.shape
            
            def pre_E():
                ind = np.zeros(arr_shape)
            
                ind[0,:,:-1,:] += self.__E[2,:,1:,:] - self.__E[2,:,:-1,:]
                ind[0,:,:,:-1] -= self.__E[1,:,:,1:] - self.__E[1,:,:,:-1]
                ind[1,:,:,:-1] += self.__E[0,:,:,1:] - self.__E[0,:,:,:-1]
                ind[1,:-1,:,:] -= self.__E[2,1:,:,:] - self.__E[2,:-1,:,:]
                ind[2,:-1,:,:] += self.__E[1,1:,:,:] - self.__E[1,:-1,:,:]
                ind[2,:,:-1,:] -= self.__E[0,:,1:,:] - self.__E[0,:,:-1,:]
            
                return ind
            
            
            def pre_H():
                ind = np.zeros(arr_shape)
                
                ind[0,:,:,1:] += self.__H[1,:,:,1:] - self.__H[1,:,:,:-1]
                ind[0,:,1:,:] -= self.__H[2,:,1:,:] - self.__H[2,:,:-1,:]
                ind[1,1:,:,:] += self.__H[2,1:,:,:] - self.__H[2,:-1,:,:]
                ind[1,:,:,1:] -= self.__H[0,:,:,1:] - self.__H[0,:,:,:-1]
                ind[2,:,1:,:] += self.__H[0,:,1:,:] - self.__H[0,:,:-1,:]
                ind[2,1:,:,:] -= self.__H[1,1:,:,:] - self.__H[1,:-1,:,:]        
                return ind
            
            start_time=time.time()
            if self.__anisotropy:
                coord_E=self.__Jdt*Z_c1
                coord_H=self.__Jdt*Z_c2
                
            
            
            for t in range(args[0]):
                    
                if self.__anisotropy:
                    self.__H+=np.einsum("klmij,jklm->iklm",self.__mu_inv,pre_E())*coord_H
                    self.__E+=np.einsum("klmij,jklm->iklm",self.__e_inv,pre_H())*coord_E
                else:
                    if self.__conductivity_m:
                        self.__H=self.__H*(1-self.__sigma_mux)/(1+self.__sigma_mux)+pre_E()*self.__Jdt*Z_c2/self.__mu/(1+self.__sigma_mux)
                    else:
                        self.__H+=pre_E()*self.__Jdt*Z_c2/self.__mu
                        
                        
                    if self.__conductivity:
                        self.__E=self.__E*(1-self.__sigma_ex)/(1+self.__sigma_ex)+pre_H()*self.__Jdt*Z_c1/self.__e/(1+self.__sigma_ex)
                    else:
                        self.__E+=pre_H()*self.__Jdt*Z_c1/self.__e
                    
                
                
                for energizer in self.__energizers:
                    self.__E[:,energizer.location[0],energizer.location[1],energizer.location[2]]=energizer(t)
                
                self.__update_grid()
                
                self.__create_progress_bar_with_ETA(start_time,t,args[0])
                    
                if obs:
                    for i in range(n_obs):
                        for ind in range(3):
                            obs_array[t,i,ind]=self.__E[ind][args[1][i]]
                            
        
                if self.__bound_bool:
                    # Boundaries in the x-direction
                    if self.__bound[0] == 1:
                        self.__E[:, 0, :, :] = self.__E[:, 1, :, :]
                        self.__H[:, 0, :, :] = self.__H[:, 1, :, :]
                
                    if self.__bound[1] == 1:
                        self.__E[:, -2, :, :] = -self.__E[:, -3, :, :]
                        self.__H[:, -2, :, :] = -self.__H[:, -3, :, :]
                
                    # Boundaries in the y-direction
                    if self.__bound[2] == 1:
                        self.__E[:, :, 0, :] = self.__E[:, :, 1, :]
                        self.__H[:, :, 0, :] = self.__H[:, :, 1, :]
                
                    if self.__bound[3] == 1:
                        self.__E[:, :, -2, :] = -self.__E[:, :, -3, :]
                        self.__H[:, :, -2, :] = -self.__H[:, :, -3, :]
                
                    # Boundaries in the z-direction
                    if self.__bound[4] == 1:
                        self.__E[:, :, :, 0] = self.__E[:, :, :, 1]
                        self.__H[:, :, :, 0] = self.__H[:, :, :, 1]

                
                    if self.__bound[5] == 1:
                        self.__E[:, :, :, -2] = -self.__E[:, :, :, -3]
                        self.__H[:, :, :, -2] = -self.__H[:, :, :, -3]


                            
        if obs:
            return obs_array
        
    def __cupy_renderer(self, *args):
        if args[1]:
            obs=True
            n_obs=len(args[1])
            obs_array=np.empty((args[0],n_obs,3))
            
        else:
            obs=False
            
        if self.__dim==2:
            Z_c1=Z_0/2**.5*self.__Jdt_cp
            Z_c2=1/Z_0/2**.5*self.__Jdt_cp
            arr_shape=self.__E.shape


            def pre_E():
                ind = cp.zeros(arr_shape)
            
                ind[0,:,:-1] += self.__E_cp[2,:,1:] - self.__E_cp[2,:,:-1]
                ind[1,:-1,:] -= self.__E_cp[2,1:,:] - self.__E_cp[2,:-1,:]
            
                return ind
            
            
            def pre_H():
                ind = cp.zeros(arr_shape)
                
                ind[2,:,1:] += self.__H_cp[0,:,1:] - self.__H_cp[0,:,:-1]
                ind[2,1:,:] -= self.__H_cp[1,1:,:] - self.__H_cp[1,:-1,:]
                return ind
            
            start_time=time.time()
            
            
            for t in range(args[0]):
                
                
                if self.__conductivity_m:
                    
                    self.__H_cp=self.__H_cp *(1-self.__sigma_mux)/(1+self.__sigma_mux)+ pre_E()*Z_c2/self.__mu_cp/(1+self.__sigma_mux)
                else:
                    self.__H_cp+=pre_E()*Z_c2/self.__mu_cp
                                        
                    
                    
                if self.__conductivity:
                    self.__E_cp=self.__E_cp*(1-self.__sigma_ex)/(1+self.__sigma_ex)+pre_H()*Z_c1/self.__e_cp/(1+self.__sigma_ex)
                    
                else:
                    self.__E_cp+=pre_H()*Z_c1/self.__e_cp


                for energizer in self.__energizers:
                    self.__E_cp[:,energizer.location[0],energizer.location[1]]=cp.array(energizer(t))
                
                self.__update_grid()

                
                if t%10==0:
                    self.__create_progress_bar_with_ETA(start_time,t,args[0])
                    
                if obs:
                    for i in range(n_obs):
                        for ind in range(3):
                            obs_array[t,i,ind]=self.__E_cp[ind][args[1][i]]
                            
                if self.__bound_bool:
                    if self.__bound[2]==1:
                        self.__E_cp[2,:,0]=-self.__E_cp[2,:,1]
                        self.__H_cp[0,:,0]=-self.__H_cp[0,:,1]
                    
                    if self.__bound[3]==1:
                        self.__E_cp[2,:,-1]=-self.__E_cp[2,:,-2]
                        self.__H_cp[0,:,-2]=-self.__H_cp[0,:,-3]
                        
                    if self.__bound[1]==1:
                        self.__E_cp[2,-1]=-self.__E_cp[2,-2]
                        self.__H_cp[1,-2]=-self.__H_cp[1,-3]
                        
                    if self.__bound[0]==1:
                        self.__E_cp[2,0]=-self.__E_cp[2,1]
                        self.__H_cp[1,0]=-self.__H_cp[1,1]



        elif self.__dim==3:
            
            
            Z_c1=Z_0/3**.5
            Z_c2=1/Z_0/3**.5
            arr_shape=self.__E.shape
            
            def pre_E():
                ind = cp.zeros(arr_shape)
            
                ind[0,:,:-1,:] += self.__E_cp[2,:,1:,:] - self.__E_cp[2,:,:-1,:]
                ind[0,:,:,:-1] -= self.__E_cp[1,:,:,1:] - self.__E_cp[1,:,:,:-1]
                ind[1,:,:,:-1] += self.__E_cp[0,:,:,1:] - self.__E_cp[0,:,:,:-1]
                ind[1,:-1,:,:] -= self.__E_cp[2,1:,:,:] - self.__E_cp[2,:-1,:,:]
                ind[2,:-1,:,:] += self.__E_cp[1,1:,:,:] - self.__E_cp[1,:-1,:,:]
                ind[2,:,:-1,:] -= self.__E_cp[0,:,1:,:] - self.__E_cp[0,:,:-1,:]
            
                return ind
            
            
            def pre_H():
                ind = cp.zeros(arr_shape)
                
                ind[0,:,:,1:] += self.__H_cp[1,:,:,1:] - self.__H_cp[1,:,:,:-1]
                ind[0,:,1:,:] -= self.__H_cp[2,:,1:,:] - self.__H_cp[2,:,:-1,:]
                ind[1,1:,:,:] += self.__H_cp[2,1:,:,:] - self.__H_cp[2,:-1,:,:]
                ind[1,:,:,1:] -= self.__H_cp[0,:,:,1:] - self.__H_cp[0,:,:,:-1]
                ind[2,:,1:,:] += self.__H_cp[0,:,1:,:] - self.__H_cp[0,:,:-1,:]
                ind[2,1:,:,:] -= self.__H_cp[1,1:,:,:] - self.__H_cp[1,:-1,:,:]        
                return ind
            
            start_time=time.time()
            
            coord_E=self.__Jdt_cp*Z_c1
            coord_H=self.__Jdt_cp*Z_c2
                
            
            
            for t in range(args[0]):
                    
                if self.__anisotropy:
                    self.__H_cp+=cp.einsum("klmij,jklm->iklm",self.__mu_inv,pre_E())*coord_H
                    self.__E_cp+=cp.einsum("klmij,jklm->iklm",self.__e_inv,pre_H())*coord_E
                        
                else:
                    if self.__conductivity_m:
                        self.__H_cp=self.__H_cp*(1-self.__sigma_mux)/(1+self.__sigma_mux)+pre_E()*coord_H/self.__mu_cp/(1+self.__sigma_mux)

                    else:
                        self.__H_cp+=pre_E()*coord_H/self.__mu_cp
                        
                        
                    if self.__conductivity:
                        self.__E_cp=self.__E_cp*(1-self.__sigma_ex)/(1+self.__sigma_ex)+pre_H()*coord_E/self.__e_cp/(1+self.__sigma_ex)
                    else:
                        self.__E_cp+=pre_H()*coord_E/self.__e_cp
                
                
                for energizer in self.__energizers:
                    self.__E_cp[:,energizer.location[0],energizer.location[1],energizer.location[2]]=cp.array(energizer(t))
                
                self.__update_grid()
                
                self.__create_progress_bar_with_ETA(start_time,t,args[0])
                    
                if obs:
                    for i in range(n_obs):
                        for ind in range(3):
                            obs_array[t,i,ind]=self.__E_cp[ind][args[1][i]]
                            
        
                if self.__bound_bool:
                    # Boundaries in the x-direction
                    if self.__bound[0] == 1:
                        self.__E_cp[:, 0, :, :] = self.__E_cp[:, 1, :, :]
                        self.__H_cp[:, 0, :, :] = self.__H_cp[:, 1, :, :]
                
                    if self.__bound[1] == 1:
                        self.__E_cp[:, -2, :, :] = -self.__E_cp[:, -3, :, :]
                        self.__H_cp[:, -2, :, :] = -self.__H_cp[:, -3, :, :]
                
                    # Boundaries in the y-direction
                    if self.__bound[2] == 1:
                        self.__E_cp[:, :, 0, :] = self.__E_cp[:, :, 1, :]
                        self.__H_cp[:, :, 0, :] = self.__H_cp[:, :, 1, :]
                
                    if self.__bound[3] == 1:
                        self.__E_cp[:, :, -2, :] = -self.__E_cp[:, :, -3, :]
                        self.__H_cp[:, :, -2, :] = -self.__H_cp[:, :, -3, :]
                
                    # Boundaries in the z-direction
                    if self.__bound[4] == 1:
                        self.__E_cp[:, :, :, 0] = self.__E_cp[:, :, :, 1]
                        self.__H_cp[:, :, :, 0] = self.__H_cp[:, :, :, 1]

                
                    if self.__bound[5] == 1:
                        self.__E_cp[:, :, :, -2] = -self.__E_cp[:, :, :, -3]
                        self.__H_cp[:, :, :, -2] = -self.__H_cp[:, :, :, -3]


                            
        if obs:
            return obs_array
                

    def Render(self, time_steps, backend="numpy", observers=None):
        
        if type(time_steps)!=int:
            raise TypeError("time_steps must be an int")
        
        if not time_steps>=0:
            raise ValueError("time_steps must be a positive integer")
        
        if not isinstance(observers, (tuple, list)) and not observers==None:
            raise TypeError("observers must be a None or tuple/list")
        
        if observers:
            for point in observers:
                if not len(point)==self.__dim:
                    raise ValueError(f"Each point must be in {self.__dim}D:\n{point} in {observers}")
                
                for i in point:
                    if i<0:
                        raise ValueError(f"Any coordinate can't be negative:\n{point} in {observers}")
                    
                    if not type(i)==int:
                        raise ValueError(f"Each coordinates must be int:\n{point} in {observers}")
            
        
        if not self.__built:
            raise NotImplementedError("The Continuum should be built first. Call build() method first.")
        
        start_time=time.time()

        if backend.upper()=="NUMPY":
            if self.__cupy_enabled==True and (self.__conductivity or self.__conductivity_m or self.__anisotropy):
                raise NotImplementedError("Prebuilt anisotropic or conductive medium for GPU is not available for NUMPY renderer.\nBuild for non-GPU or use 'cupy' as backend")
            obs=self.__numpy_renderer(time_steps, observers)
            time_elapsed=time.time()-start_time
            print(f"\nRendered Succesfully\nElapsed Time : {self.__convert_to_time(time_elapsed)} , {time_elapsed/time_steps} s/step\nRender Stream Rate : {self.__prefix_quantifier(np.prod(self.__grid_size)/time_elapsed*time_steps)}Points/s")
            
        elif backend.upper()=="CUPY":
            if self.__built_for!="cupy":
                raise ValueError("set build(gpu_flag=1) for utilizing GPU resources")
            obs=self.__cupy_renderer(time_steps, observers)
            time_elapsed=time.time()-start_time
            print(f"\nRendered Succesfully\nElapsed Time : {self.__convert_to_time(time_elapsed)} , {time_elapsed/time_steps} s/step\nRender Stream Rate : {self.__prefix_quantifier(np.prod(self.__grid_size)/time_elapsed*time_steps)}Points/s")
            cp._default_memory_pool.free_all_blocks()

            print("Transfering from GPU to host memory...")
            start_t=time.time()
            self.__E=self.__E_cp.get()
            self.__H=self.__H_cp.get()
            end_t=time.time()
            print(f"Data transferred in {end_t-start_t} secs")
        
        elif backend.upper()=="C++":
            raise ValueError("C++ renderer will be added in future releases")#self.__cpp_renderer(time_steps, observers)
        
        elif backend.upper()=="CUDA":
            raise ValueError("CUDA based GPU enabled renderer will be added in future releases")#self.__nvcc_render(time_steps, observers)
        
        elif backend.upper()=="FPGA":
            raise ValueError("FPGA based hardware accelerator will be added in future releases")#self.__fpga_renderer(time_steps, observers)
        
        else:
            raise ValueError(f"'{backend}' is not a recognized backend. Check for any typo. Supported background is:\n'numpy'")#raise ValueError(f"{backend} is not a recognized backend. Check for any typo. Supported backgrounds are:\n'numpy','C++','CUDA', 'FPGA")

        

        self.__rendered=True
        return obs
    

    
    @property
    def isbuilt(self):
        return self.__built
    
    @property
    def isrendered(self):
        return self.__rendered
    
    @property
    def __Z(self):
        if not self.__anisotropy:
            omega=self.__energizers[0].inf[4]*2*np.pi
            if self.__conductivity and self.__conductivity_m:
                return np.abs(Z_0*np.sqrt(self.__mu*(1-1j*self.__sigma_m/omega/self.__mu/mu_0)/self.__e*(1-1j*self.__sigma/omega/e_0/self.__e)))
                
            elif self.__conductivity and not self.__conductivity_m:
                return np.abs(Z_0*np.sqrt(self.__mu/self.__e*(1-1j*self.__sigma/omega/e_0/self.__e)))
            elif not self.__conductivity and self.__conductivity_m:
                return np.abs(Z_0*np.sqrt(self.__mu*(1-1j*self.__sigma_m/omega/self.__mu/mu_0)/self.__e))
            else:
                return Z_0*np.sqrt(self.__mu/self.__e)
        else:
            return np.linalg.matrix_power(np.linalg.inv(self.__e) @ self.__mu,.5)
    
    @property
    def stellar(self):
        return self.__stellar
    
    
    @property
    def ds(self):
        return self.__ds
    

    @property
    def dimensionality(self):
        return self.__dim
    
    def spec(self):
        return np.sum(self.__E)+np.sum(self.__H)




class DotSource(object):
    def __init__(self, location, presence, amplitude, frequency, E=(0,0,1), phase=0):
        if not isinstance(location, (tuple, list, np.ndarray)):
            raise TypeError(f"location must be a tuple, list or ndarray:\n{location}")
        
        if not isinstance(presence, (tuple, list, np.ndarray)):
            raise TypeError(f"presence must be a tuple, list or ndarray:\n{presence}")
            
        if not isinstance(amplitude, (int, float)):
            raise TypeError(f"amplitude must be an int or float:\n{amplitude}")

        if not isinstance(frequency, (int, float)):
            raise TypeError(f"frequency must be an int or float:\n{frequency}")      
            
        if not isinstance(phase, (int, float)):
            raise TypeError(f"phase must be an int or float:\n{phase}")
            
        if not isinstance(E, (tuple, list, np.ndarray)):
            raise TypeError(f"E-field vector direction must be a tuple, list or ndarray:\n{location}")
            

        if len(presence)!=2:
            raise ValueError(f"presence must contain two elements, start and stop:\n{presence}")
        
        if len(E)!=3:
            raise ValueError("E-field vector direction must contain 3 elements")
        

        self.__location=tuple(location)
        self.__amplitude=amplitude
        self.__frequency=frequency
        self.__omega=PI_2*frequency
        
        self.__phase=phase%np.pi
        self.__presence=presence
        self.__dim=len(location)
        
        self.__E=np.array(E)

        
    def __repr__(self):
        __=""
        for i in self.__location:
            __+=str(i)+" "
        for i in self.__presence:
            __+=str(i)+" "
        __+=f"Dot Source Amplitude:{self.__amplitude} Frequency:{self.__frequency} Phase:{self.__phase}"
        return __
    
    def set_dt(self, dt):
        self.__dt=dt
        self.__omega_dt=self.__omega*self.__dt
        
    @property
    def inf(self):
        return [0, self.__location, self.__presence, self.__amplitude, self.__frequency, self.__phase]

    @property
    def dimensionality(self):
        return self.__dim
    
    @property
    def location(self):
        return self.__location
    
    
    def __call__(self, t):
        if self.__presence[0]<=t<=self.__presence[1]:
            return self.__E*np.sin(self.__omega_dt * t + self.__phase)
        else:
            return 0,0,0




class Boundaries(object):
    def __init__(self, subject_grid_dim, all_bound="ABC"):
        self.__op_dict={"PEC":0, "ABC":1, "PBC":2}
        if not subject_grid_dim in {2,3}:
            raise ValueError("# dimensions in the subject grid must be 2 or 3")

        
        if subject_grid_dim==3:
            self.__ultimate_functions=[None]*6#L,R,B,F,D,U
        
        else:
            self.__ultimate_functions=[None]*4#L,R,B,F
        self.__dim=subject_grid_dim
        
        
        
        if all_bound:
            
            if self.__validator(all_bound):
                self.__ultimate_functions[:4]=[self.__op_dict[all_bound]]*4
                if self.__dim==3:
                    self.__ultimate_functions[4:6]=[self.__op_dict[all_bound]]*2
         
            
    def __call__(self):
        if None in self.__ultimate_functions:
            raise NotImplementedError("Some boundaries are not defined. Make sure that all of them are defined")
        
        for i in range(self.__dim):
            if (self.__ultimate_functions[2*i]=="PBC" and self.__ultimate_functions[2*i+1]!="PBC") or (self.__ultimate_functions[2*i]!="PBC" and self.__ultimate_functions[2*i+1]=="PBC"):
                raise ValueError("Opposite boundary surfaces must be shared periodically")
        
        return tuple(self.__ultimate_functions)
        
    
    def L(self, boundary_type="ABC"):
        self.__validator(boundary_type)
        self.__ultimate_functions[0]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[1]=self.__op_dict[boundary_type]
                
    
    def R(self, boundary_type="ABC"):
        self.__validator(boundary_type)
        self.__ultimate_functions[1]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[0]=self.__op_dict[boundary_type]
    
    def B(self, boundary_type="ABC"):
        self.__validator(boundary_type)
        self.__ultimate_functions[2]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[3]=self.__op_dict[boundary_type]
    
    def F(self, boundary_type="ABC"):
        self.__validator(boundary_type)
        self.__ultimate_functions[3]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[2]=self.__op_dict[boundary_type]
    
    def D(self, boundary_type="ABC"):
        if self.__dim==2:
            raise NotImplementedError("Employing a 3D operation in 2D impossible")
        self.__validator(boundary_type)
        self.__ultimate_functions[4]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[5]=self.__op_dict[boundary_type]
    
    def U(self, boundary_type="ABC"):
        if self.__dim==2:
            raise NotImplementedError("Employing a 3D operation in 2D impossible")
        self.__validator(boundary_type)
        self.__ultimate_functions[5]=self.__op_dict[boundary_type]
        if boundary_type=="PBC":
            self.__ultimate_functions[4]=self.__op_dict[boundary_type]
    
    @staticmethod       
    def __validator(inn):
        if inn not in {"ABC","PEC"}:
            raise ValueError("boundary type must be ABC, PBC or PEC.\nBoundary Types:\nPEC(Perfect Electric Conductor): Reflects all waves perfectly\nABC(Absorbing Boundary Conditions): Absorbs all waves.\n")
        return True
    @property
    def dimensionality(self):
        return self.__dim
