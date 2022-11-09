from scipy.spatial import Delaunay
from numpy import ndarray, array
class Rectangle(object):
    def __init__(self, A,B,layer=0,e=1, mu=1):
        
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
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")
        
        self.__A=tuple(A)
        self.__B=tuple(B)
        self.__layer=layer
        self.__e=e
        self.__mu=mu
        
    def __repr__(self):
        __="1 "
        for i in self.__A+self.__B:
            __+=str(i)+" "
        __+=f"{self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
        return __
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu

    def t(self):
        return 1
    
    def isIn(self, point):
        for i in range(2):
            if self.__A[i]<=point[i]<=self.__B[i] or self.__B[i]<=point[i]<=self.__A[i]:
                pass
            else:
                return False
        return True
    
    


class Circle(object):
    def __init__(self, A, r,layer=0, e=1, mu=1):
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
    
        if not layer<=1000:
            raise ValueError("Layer priority must be <=1000")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")
        
        self.__A=tuple(A)
        self.__r=r
        self.__r_2=r**2
        self.__layer=layer
        self.__e=e
        self.__mu=mu
        
    def __repr__(self):
        return f"2 {self.__A[0]} {self.__A[1]} {self.__r} {self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
        
    def t(self):
        return 2
    
    def isIn(self, point):
        __=0
        for i in range(2):
            __+=(point[i]-self.__A[i])**2
        if self.__r_2>=__:
            return True
        else:
            return False

class PointCloud(object):
    def __init__(self, points, layer=0, e=1, mu=1):
        
        if not isinstance(points, (tuple, list, ndarray)):
            raise TypeError("points must be a tuple, list or ndarray")

        if not isinstance(layer, int):
            raise TypeError("layer must be an int")
            
        if not isinstance(e, (tuple, list, int, float,ndarray)):
            raise TypeError("e must be an int, float, tuple, list or ndarray")
            
        if not isinstance(mu, (tuple, list, int, float, ndarray)):
            raise TypeError("mu must be an int, float, tuple, list or ndarray")
        
        if not len(points)>2:
            raise ValueError("At least 3 points required to build 2D PointCloud")
            
        for point in points:
            if len(point)!=2:
                raise ValueError("points must include 2D coordinates of points")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")
        
        self.__hull=Delaunay(points)
        self.__layer=layer
        self.__e=e
        self.__mu=mu

    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu
        
    def t(self):
        return 3
    
    def isIn(self, point):
        return self.__hull.find_simplex(point)>=0


class VRectangle(object):
    def __init__(self, A,B,time, layer=0,e=1, mu=1):
        
        if not isinstance(A, (tuple, list)):
            raise TypeError("A must be a tuple or list")
        if not isinstance(B, (tuple, list)):
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
                
        if not isinstance(time, int):
            raise TypeError("time must be an int")
        
        if not isinstance(layer, int):
            raise TypeError("Layer must be an int")
        
        if not isinstance(e, (int, float)):
            raise TypeError("e(permittivity) must be a float or int")
        
        if not isinstance(mu, (int, float)):
            raise TypeError("mu(permiablity) must be a float or int")
        
        self.__A=tuple(A)
        self.__B=tuple(B)
        self.__time=time
        self.__layer=layer
        self.__e=e
        self.__mu=mu
        
    def __repr__(self):
        __="1 "
        for i in self.__A+self.__B:
            __+=str(i)+" "
        __+=f"{self.__layer} {self.__e.real} {self.__e.imag} {self.__mu.real} {self.__mu.imag}"
        return __
    
    @property
    def inf(self):
        return self.__layer, self.__e, self.__mu

    def t(self):
        return 1
    
    def isIn(self, point):
        for i in range(2):
            if self.__A[i]<=point[i]<=self.__B[i] or self.__B[i]<=point[i]<=self.__A[i]:
                pass
            else:
                return False
        return True

    @property  
    def time(self):
        return self.__time
    
    def __ge__(self, other):
        return self.__layer>=other.__layer
    
    def __gt__(self, other):
        return self.__layer>other.__layer

    @property
    def loc(self):
        return self.__A, self.__B
