class Rectangle(object):
    def __init__(self, A,B,layer,e=1, mu=1):
        
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
    def __init__(self, A, r,layer, e=1, mu=1):
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
