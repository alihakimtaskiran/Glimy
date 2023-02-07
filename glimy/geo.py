from scipy.spatial import Delaunay
from numpy import ndarray, array, zeros, pi, linalg, math


class SingularCelestial(object):
    def __init__(self, location, mass):
        if not isinstance(location, (tuple, list, ndarray)):
            raise TypeError('Location must be a tuple, list or ndarray')

        if not isinstance(mass, (int, float)):
            raise TypeError('mass must be an int or float')

        self.__export=len(location),array(location), mass
        
    @property
    def export(self):
        return self.__export #Dimensions, Location, Mass
    
    @property
    def dimensionality(self):
        return self.__export[0]
    
    def __repr__(self):
        return f"Singular Celestial body {self.export[2]} kg, on {self.export[1]}"

class MassiveCluster(object):
    def __init__(self, objects, volatile=False):
        if not isinstance(objects, (tuple, list, set, frozenset)):
            raise TypeError("objects must be a list, tuple or set of SingularCelestial")
        for element in objects:
            if not isinstance(element, SingularCelestial):
                raise TypeError("Each element in the objects must be a SingularCelestial")
        
        if not type(volatile)==bool:
            raise TypeError("volatile is a bool")
        
        self.__dimensionality=None
        self.__volatile=volatile
        if volatile:
            self.__objects=set()
            self.add(objects)
        else:
            for element in objects:
                if self.__dimensionality==None:
                    self.__dimensionality=element.dimensionality
                elif self.__dimensionality!=element.dimensionality:
                    raise ValueError(f"# of dimensions of each element in massive cluster should match:\nWhile massive cluster is {self.__dimensionality}D, element is {element.dimensionality}D:\n {element}")

            self.__objects=frozenset(objects)
            
    def add(self, arg):
        if not self.__volatile:
            raise NotImplementedError("Non-Volatile MassiveCluster can't handle addition")
        if isinstance(arg, (tuple, list, set, frozenset)):
            for element in arg:
                self.add(element)
        elif isinstance(arg, SingularCelestial):
            if self.__dimensionality==None:
                self.__dimensionality=arg.dimensionality
            
            elif self.__dimensionality!=arg.dimensionality:
                raise ValueError(f"# of dimensions of each element in massive cluster should match:\nWhile massive cluster is {self.__dimensionality}D, element is {arg.dimensionality}D:\n {arg}")
            self.__objects.add(arg)
            
        else:
            raise TypeError("arg must be a list/tuple/set of SingularCelestial objects")
    
    @property
    def content(self):
        return self.__objects
    
    @property
    def dimensionality(self):
        return self.__dimensionality
    def __repr__(self):
        return f"Massive Cluster with {len(self.__objects)} SingularCelestials"


class PointCloud(object):
    def __init__(self, points, layer=0, e=1, mu=1, time=None):
        
        if not isinstance(points, (list, tuple, ndarray)):
            raise TypeError("points must be a tuple, list or ndarray")
            
        if not isinstance(layer, int):
            raise TypeError("layer must be an int")
            
        if not isinstance(e, (float, int, tuple, list, ndarray)):
            raise TypeError("e(epsilon) must be a float, int, tuple, list or ndarray")

        if not isinstance(mu, (float, int, tuple, list, ndarray)):
            raise TypeError("mu(epsilon) must be a float, int, tuple, list or ndarray")
            
        if not isinstance(time, (list, tuple)) and not time is None:
            raise TypeError("time must be a list, tuple or None(for eternity)")
        
        
        if time is None:
            self.__eternity=True
        else:
            if time[0]>time[1]:
                raise ValueError(f"time flows past to future. Starting instance must be less than final instance:{time}")
            self.__eternity=False
            if len(time)!=2:
                raise ValueError(f"time must be time interval(both inclusive):{time}")
            if type(time[0])!=int:
                raise TypeError(f"Starting point must be an int: {time}")
        
        
        if isinstance(e, (int,float)) and isinstance(mu, (int,float)):
            self.__anisotropy=False
            self.__e=e
            self.__mu=mu
        else:
            
            self.__anisotropy=True
            if isinstance(e, (int,float)) and not isinstance(mu, (int,float)):
                self.__mu=array(mu)
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")
                self.__e=zeros(self.__mu.shape)
                for i in range(self.__mu.shape[0]):
                    self.__e[i,i]=e
            elif isinstance(mu, (int,float)) and not isinstance(e, (int,float)):
                self.__e=array(e)
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                self.__mu=zeros(self.__e.shape)
                for i in range(self.__e.shape[0]):
                    self.__mu[i,i]=mu
            else:
                self.__e=array(e)
                self.__mu=array(mu)
                if self.__e.shape!=self.__mu.shape:
                    raise ValueError(f"Anisotropic permittivity and permeability tensors must have same dimensions:\n{e}\n{mu}")
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")


        self.__time=time
        self.__delaunay=Delaunay(points)
        self.__num_points=len(points)
        self.__layer=layer
        self.__dim=len(points[0])
        self.__coverage=[]
        
        #2D anisotropy disclaimer
        if self.__dim==2 and self.__anisotropy:
            raise ValueError("Anisotropic materials are only compatible with 3D")
 
            
        
        
        for d in range(self.__dim):
            __=[None,None]
            __[0]=int(min(self.__delaunay.points[:,d]))
            __[1]=int(max(self.__delaunay.points[:,d]))
            self.__coverage.append(__)
        
    def isIn(self, point):
        return self.__delaunay.find_simplex(point)>=0
        
    def ExistInInstance(self, time_step):
        if self.__eternity:
            return True
        else:
            return self.__time[0]<=time_step<=self.__time[1]
       
    @property
    def dimensionality(self):
        return self.__dim
    
    @property
    def info(self):
        return self.__dim, self.__anisotropy, self.__layer, self.__delaunay, self.__e, self.__mu, self.__eternity, self.__time, self.__coverage

    @property
    def eternity(self):
        return self.__eternity
    
    @property
    def fielder(self):
        return self.__e, self.__mu
    
    @property
    def duration(self):
        return self.__time
    
    @property
    def coverage(self):
        return self.__coverage
    
    @property
    def anisotropy(self):
        return self.__anisotropy
    
    @property
    def layer(self):
        return self.__layer
    
    def __repr__(self):
        return f"PointCloud-{self.__dim}D with {self.__num_points} points"

        
class Rectangle(PointCloud):
    def __init__(self, A, B, layer=0, e=1, mu=1, time=None):
        
        if not isinstance(A, (tuple, list, ndarray)):
            raise TypeError("A must be a tuple or list")
        if not isinstance(B, (tuple, list, ndarray)):
            raise TypeError("B must be a tuple or list")
        
        if len(A)!=2:
            raise ValueError("A must be 2D")
            
        if len(B)!=2:
            raise ValueError("B must be 2D")
         
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        for i in B:
            if not i>=0:
                raise ValueError("Coordinates of B must be greater than 0")
                
        super().__init__((A, B,(A[0],B[1]),(B[0],A[1])),layer,e,mu,time)


class RectPrism(PointCloud):
   def __init__(self, A, B, layer=0, e=1, mu=1, time=None):
        if not isinstance(A, (tuple, list, ndarray)):
            raise TypeError("A must be a tuple, list or ndarray")
    
        if not isinstance(B, (tuple, list, ndarray)):
            raise TypeError("B must be a tuple, list or ndarray")
    
        if len(A)!=3:
            raise ValueError('A is defined in 3D')
    
        if len(B)!=3:
            raise ValueError('B is defined in 3D')
    
        for i in A:
            if i<0:
                raise ValueError("Each component of A must be >=0")
          
        for i in B:
            if i<0:
                raise ValueError("Each component of B must be >=0")
        
        hull=[]
        for i in A[0],B[0]:
            for j in A[1],B[1]:
                for k in A[2],B[2]:
                    hull.append((i,j,k))
         
        super().__init__(hull,layer,e,mu,time)


class Circle(object):
    def __init__(self, A, r,layer=0, e=1, mu=1, time=None):
        if not isinstance(A, (tuple, list)):
            raise TypeError("A(center) must be a tuple or list")
            
        if len(A)!=2:
            raise ValueError("A(center) must be 2D")
            
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        if not isinstance(r, (int, float)):
            raise TypeError("r(radius) must be an int")
        
        if not r>=0:
            raise ValueError("r(radius) must be more than 0")
            
            
        if not isinstance(layer, int):
            raise TypeError("layer must be an int")
            
        if not isinstance(e, (float, int, tuple, list, ndarray)):
            raise TypeError("e(epsilon) must be a float, int, tuple, list or ndarray")

        if not isinstance(mu, (float, int, tuple, list, ndarray)):
            raise TypeError("mu(epsilon) must be a float, int, tuple, list or ndarray")
            
        if not isinstance(time, (list, tuple)) and not time is None:
            raise TypeError("time must be a list, tuple or None(for eternity)")
        
        
        if time is None:
            self.__eternity=True
        else:
            if time[0]>time[1]:
                raise ValueError(f"time flows past to future. Starting instance must be less than final instance:{time}")
            self.__eternity=False
            if len(time)!=2:
                raise ValueError(f"time must be time interval(both inclusive):{time}")
            if type(time[0])!=int:
                raise TypeError(f"Starting point must be an int: {time}")
        
        
        if isinstance(e, (int,float)) and isinstance(mu, (int,float)):
            self.__anisotropy=False
            self.__e=e
            self.__mu=mu
        else:
            
            self.__anisotropy=True
            if isinstance(e, (int,float)) and not isinstance(mu, (int,float)):
                self.__mu=array(mu)
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")
                self.__e=zeros(self.__mu.shape)
                for i in range(self.__mu.shape[0]):
                    self.__e[i,i]=e
            elif isinstance(mu, (int,float)) and not isinstance(e, (int,float)):
                self.__e=array(e)
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                self.__mu=zeros(self.__e.shape)
                for i in range(self.__e.shape[0]):
                    self.__mu[i,i]=mu
            else:
                self.__e=array(e)
                self.__mu=array(mu)
                if self.__e.shape!=self.__mu.shape:
                    raise ValueError(f"Anisotropic permittivity and permeability tensors must have same dimensions:\n{e}\n{mu}")
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")
            
        self.__A=array(A)
        self.__r=r
        self.__layer=layer
        self.__time=time
        self.__coverage=[[self.__A[i]-r,self.__A[i]+r] for i in range(2)]
        self.__dim=2
        
        
        #2D anisotropy disclaimer
        if self.__dim==2 and self.__anisotropy:
            raise ValueError("Anisotropic materials are only compatible with 3D")
        
    def isIn(self, point):
        return linalg.norm(self.__A-point)<=self.__r
        
    def ExistInInstance(self, time_step):
        if self.__eternity:
            return True
        else:
            return self.__time[0]<=time_step<=self.__time[1]
       
    @property
    def dimensionality(self):
        return self.__dim
    
    @property
    def info(self):
        return self.__dim, self.__anisotropy, self.__layer, ("CIRCLE",self.__A, self.__r), self.__e, self.__mu, self.__eternity, self.__time, self.__coverage

    @property
    def eternity(self):
        return self.__eternity
    
    @property
    def fielder(self):
        return self.__e, self.__mu
    
    @property
    def duration(self):
        return self.__time
    
    @property
    def coverage(self):
        return self.__coverage
    
    @property
    def anisotropy(self):
        return self.__anisotropy
    
    @property
    def layer(self):
        return self.__layer
    
    def __repr__(self):
        return f"Circle with A={self.__A} , r={self.__r}"
    
    
class Sphere(object):
    def __init__(self, A, r,layer=0, e=1, mu=1, time=None):
        if not isinstance(A, (tuple, list)):
            raise TypeError("A(center) must be a tuple or list")
            
        if len(A)!=3:
            raise ValueError("A(center) must be 3D")
            
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        if not isinstance(r, (int, float)):
            raise TypeError("r(radius) must be an int")
        
        if not r>=0:
            raise ValueError("r(radius) must be more than 0")
            
            
        if not isinstance(layer, int):
            raise TypeError("layer must be an int")
            
        if not isinstance(e, (float, int, tuple, list, ndarray)):
            raise TypeError("e(epsilon) must be a float, int, tuple, list or ndarray")

        if not isinstance(mu, (float, int, tuple, list, ndarray)):
            raise TypeError("mu(epsilon) must be a float, int, tuple, list or ndarray")
            
        if not isinstance(time, (list, tuple)) and not time is None:
            raise TypeError("time must be a list, tuple or None(for eternity)")
        
        
        if time is None:
            self.__eternity=True
        else:
            if time[0]>time[1]:
                raise ValueError(f"time flows past to future. Starting instance must be less than final instance:{time}")
            self.__eternity=False
            if len(time)!=2:
                raise ValueError(f"time must be time interval(both inclusive):{time}")
            if type(time[0])!=int:
                raise TypeError(f"Starting point must be an int: {time}")
        
        
        if isinstance(e, (int,float)) and isinstance(mu, (int,float)):
            self.__anisotropy=False
            self.__e=e
            self.__mu=mu
        else: 
            

            self.__anisotropy=True
            if isinstance(e, (int,float)) and not isinstance(mu, (int,float)):
                self.__mu=array(mu)
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")
                self.__e=zeros(self.__mu.shape)
                for i in range(self.__mu.shape[0]):
                    self.__e[i,i]=e
            elif isinstance(mu, (int,float)) and not isinstance(e, (int,float)):
                self.__e=array(e)
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                self.__mu=zeros(self.__e.shape)
                for i in range(self.__e.shape[0]):
                    self.__mu[i,i]=mu
            else:
                self.__e=array(e)
                self.__mu=array(mu)
                if self.__e.shape!=self.__mu.shape:
                    raise ValueError(f"Anisotropic permittivity and permeability tensors must have same dimensions:\n{e}\n{mu}")
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")

        self.__A=array(A)
        self.__r=r
        self.__layer=layer
        self.__time=time
        self.__coverage=[[self.__A[i]-r,self.__A[i]+r] for i in range(3)]
        self.__dim=3

        
    def isIn(self, point):
        return linalg.norm(self.__A-point)<=self.__r
        
    def ExistInInstance(self, time_step):
        if self.__eternity:
            return True
        else:
            return self.__time[0]<=time_step<=self.__time[1]
       
    @property
    def dimensionality(self):
        return self.__dim
    
    @property
    def info(self):
        return self.__dim, self.__anisotropy, self.__layer, ("SPHERE",self.__A, self.__r), self.__e, self.__mu, self.__eternity, self.__time, self.__coverage
    @property
    def eternity(self):
        return self.__eternity
    
    @property
    def fielder(self):
        return self.__e, self.__mu
    
    @property
    def duration(self):
        return self.__time
    
    @property
    def coverage(self):
        return self.__coverage
    
    @property
    def anisotropy(self):
        return self.__anisotropy
    
    @property
    def layer(self):
        return self.__layer
    
    def __repr__(self):
        return f"Sphere with A={self.__A}, r={self.__r}"


class Cylinder(object):
    def __init__(self, A, r, h, layer=0, e=1, mu=1, time=None):
        if not isinstance(A, (tuple, list)):
            raise TypeError("A(center) must be a tuple or list")
            
        if len(A)!=3:
            raise ValueError("A(center) must be 3D")
            
        for i in A:
            if not i>=0:
                raise ValueError("Coordinates of A must be greater than 0") 
        
        if not isinstance(r, (int, float)):
            raise TypeError("r(radius) must be an int")
        
        if not r>=0:
            raise ValueError("r(radius) must be more than 0")
                
        if not isinstance(h, (int, float)):
            raise TypeError("h(height) must be an int")
        
        if not r>=0:
            raise ValueError("h(height) must be more than 0")

            
        if not isinstance(layer, int):
            raise TypeError("layer must be an int")
            
        if not isinstance(e, (float, int, tuple, list, ndarray)):
            raise TypeError("e(epsilon) must be a float, int, tuple, list or ndarray")

        if not isinstance(mu, (float, int, tuple, list, ndarray)):
            raise TypeError("mu(epsilon) must be a float, int, tuple, list or ndarray")
            
        if not isinstance(time, (list, tuple)) and not time is None:
            raise TypeError("time must be a list, tuple or None(for eternity)")
        
        
        if time is None:
            self.__eternity=True
        else:
            if time[0]>time[1]:
                raise ValueError(f"time flows past to future. Starting instance must be less than final instance:{time}")
            self.__eternity=False
            if len(time)!=2:
                raise ValueError(f"time must be time interval(both inclusive):{time}")
            if type(time[0])!=int:
                raise TypeError(f"Starting point must be an int: {time}")
        
        
        if isinstance(e, (int,float)) and isinstance(mu, (int,float)):
            self.__anisotropy=False
            self.__e=e
            self.__mu=mu
        else: 
            

            self.__anisotropy=True
            if isinstance(e, (int,float)) and not isinstance(mu, (int,float)):
                self.__mu=array(mu)
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")
                self.__e=zeros(self.__mu.shape)
                for i in range(self.__mu.shape[0]):
                    self.__e[i,i]=e
            elif isinstance(mu, (int,float)) and not isinstance(e, (int,float)):
                self.__e=array(e)
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                self.__mu=zeros(self.__e.shape)
                for i in range(self.__e.shape[0]):
                    self.__mu[i,i]=mu
            else:
                self.__e=array(e)
                self.__mu=array(mu)
                if self.__e.shape!=self.__mu.shape:
                    raise ValueError(f"Anisotropic permittivity and permeability tensors must have same dimensions:\n{e}\n{mu}")
                if self.__e.shape[0]!=self.__e.shape[1]:
                    raise ValueError(f"Anisotropic permittivity tensor must be a n × n :\n{e}")
                if self.__mu.shape[0]!=self.__mu.shape[1]:
                    raise ValueError(f"Anisotropic permeability tensor must be a n × n :\n{mu}")

        self.__A=A
        self.__r=r
        self.__r_2=r**2
        self.__h=h
        self.__layer=layer
        self.__time=time
        self.__coverage=[[self.__A[i]-r,self.__A[i]+r] for i in range(3)]
        self.__dim=3
        self.__coverage=[[A[0]-r,A[0]+r],[A[1]-r,A[1]+r],[A[2],A[2]+h]]
        
    def isIn(self, point):
        return (point[0]-self.__A[0])**2+(point[1]-self.__A[1])**2<=self.__r_2 and 0<=point[2]-self.__A[2]<=self.__h
        
    def ExistInInstance(self, time_step):
        if self.__eternity:
            return True
        else:
            return self.__time[0]<=time_step<=self.__time[1]
       
    @property
    def dimensionality(self):
        return self.__dim
    
    @property
    def info(self):
        return self.__dim, self.__anisotropy, self.__layer, ("CYLINDER",self.__A, self.__r, self.__h, self.__axis), self.__e, self.__mu, self.__eternity, self.__time, self.__coverage
    @property
    def eternity(self):
        return self.__eternity
    
    @property
    def fielder(self):
        return self.__e, self.__mu
    
    @property
    def duration(self):
        return self.__time
    
    @property
    def coverage(self):
        return self.__coverage
    
    @property
    def anisotropy(self):
        return self.__anisotropy
    
    @property
    def layer(self):
        return self.__layer
    
    def __repr__(self):
        return f"Cylinder with A={self.__A}, r={self.__r}, h={self.__h}"
                 